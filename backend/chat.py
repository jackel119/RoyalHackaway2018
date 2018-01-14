from fbchat.models import *
from query import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

fuzzRatio = 80
baseRatio = 0.7 #percentage of message.clause words needed to match with the text of an answer

class Chat(object):

    def __init__(self, name, chat_id, messages, thread, owner_id, owner_name, lookup_table):
        self.name = name
        self.chat_id = chat_id
        self.messages = messages
        self.message_length = len(messages)
        self.thread = [value for key, value in thread.items()][0]
        self.participants = {}
        if isinstance(self.thread, User):
            self.isGroup = False
            self.participants[self.thread.uid] = lookup_table[self.thread.uid]
        else:
            for part_id in self.thread.participants:
                self.participants[part_id] = lookup_table[part_id]
            self.isGroup = True
        self.participants[owner_id] =  owner_name
        self.queries = []
        self.answers = []
        print("Participants in this conversation are:")
        for key, value in self.participants.items():
           print("    ", value) 
        self.generate()
        self.show_queries()
        self.show_answers()

    def get_messages(self):
        output = []
        for message in self.messages:
            output.append({'author' : self.participants[message.author], 'body' : message.text})
        return output

    def generate(self):
        for message in self.messages:
            if message.text:
                message.sanitized = sanitize(message.text)
                # Generate Query
                q = self.isQuery(message)
                if q:
                    self.queries.append(q)
                else:
                    # Check if it answers another query
                    for query in self.queries:
                        answer = self.isAnswer(query, message)
                        if answer:
                            self.answers.append(answer)

    def show_queries(self):
        print("------- SHOWING REMAINING QUERIES -------")
        for q in self.queries:
            q.show()

    def show_answers(self):
        print("------- SHOWING ACHIEVED ANSWERS -------")
        for answer in self.answers:
            answer.show()

    def isQuery(self, message):
        query = Query(text=message.text)
        tokens = nltk.word_tokenize(message.sanitized)
        for word in tokens:
            qtype = isQuestion(word)
            if qtype:
                query.qtype = qtype
                break
        if query.qtype:
            query.time = message.timestamp
            query.addressee = self.findSubject(message)

            tagged = nltk.pos_tag(tokens)

            #Checking the clause of the question
            query.clause = list(filter(lambda x : notIrrelevant(x[1]), tagged))
            # print(datetime.fromtimestamp(int(message.timestamp) // 1000).strftime('%Y-%m-%d %H:%M:%S'))
            # print(message.text)
            # print(message.sanitized)
            # print(query.qtype)
            # print("Clause:", query.clause)
            # print("Addressee: ", query.addressee)
            # print()
            return query
        return 
    
    def construct_answer(self, query, message):
        return Answer(query.text, query.qtype, query.addressee, query.clause, message.text)

    def isAnswer(self, query, message):
        # print("Checking if message is an answer:", message.sanitized)
        # print("Type of query: ",query.qtype)
        if query.qtype == QType.WHERE:
            # print("Query Type: ", query.qtype)
            if abs(int(query.time) - int(message.timestamp)) > 3*24*60*60:
                #If the message is more than 3 days away from the question, it's not relevant
                return False
            subjectName = self.findSubject(message)
            if query.addressee and subjectName:
                if subjectName != query.addressee:
                    return False
            tokens = nltk.word_tokenize(message.sanitized)
            keywords = [ word for word, tag in query.clause]
            matchRatio = 0
            tagged = nltk.pos_tag(tokens)
            print("Tagged: ", tagged) 
            chunks = nltk.ne_chunk(tagged)
            for chunk in chunks:
                # print(chunk)
                if isinstance(chunk, nltk.tree.Tree):
                    # print("Label:", chunk.label())
                    if chunk.label() in ['GPE', 'GEO']:
                        self.queries.remove(query)
                        return self.construct_answer(query, message)
            for word, tag in tagged:
                if tag == 'NN':
                    self.queries.remove(query)
                    return self.construct_answer(query, message)
            # print("Keywords: ", keywords)
            for word in keywords:
                if checkWord(tokens, word):
                    matchRatio += 1 / len(keywords)
                    # print("MatchRatio: ", matchRatio)
                    # print("BaseRatio: ", baseRatio)
                    if matchRatio > baseRatio:
                        self.queries.remove(query)
                        return self.construct_answer(query, message)
            # print("NOT AN ANSWER")
            return False

        if query.qtype == QType.WHEN:
            subjectName = self.findSubject(message)
            if query.addressee and subjectName:
                if subjectName != query.addressee:
                    #If the message isn't talking about the same person, it's not relevant
                    return False
            tagged = nltk.pos_tag(nltk.word_tokenize(message.sanitized))
            for chunk in nltk.ne_chunk(tagged):
                print("Chunk:", chunk)
                if type(chunk) == nltk.tree.Tree:
                    print(chunk.label())
                    if chunk.label() == 'CD':
                        self.queries.remove(query)
                        return self.construct_answer(query, message)
            return False

        if query.qtype == QType.WHY:
            return

        if query.qtype == QType.HOW:
            return

        if query.qtype == QType.WHICH:
            return

        if query.qtype == QType.WHAT:
            return

        if query.qtype == QType.WHO:
            return

        if query.qtype == QType.BOOL:
            for word in message.sanitized.split():
                if word.lower() in ['yes', 'no', 'yeah', 'yea', 'ya', 'nah']:
                    self.queries.remove(query)
                    return self.construct_answer(query, message)
            return

    def findSubject(self, message):
        tokens = []
        for token in nltk.word_tokenize(message.sanitized):
            if token == "i":
                tokens.append("I")
            else:
                tokens.append(token)
        tagged = nltk.pos_tag(tokens)
        if message.mentions:
             # the person is @'d
             return self.participants[message.mentions[0].thread_id]
        else:
             # checks to see if the person is mentioned in the message
             names = [value for key, value in self.participants.items()]
             posName =  findName([word for word, tag in tagged], names)
             if posName:
                 return posName
         
        # if there's no name mentioned, checks pronouns
        pronouns = [word for word, tag in list(filter(lambda x : x[1] == "PRP", tagged))]
        if pronouns:
            pronoun = ""
            if "you" in pronouns:
                pronoun = "you"
            else:
                pronoun = pronouns[0]
            if pronoun == "I" or pronoun == "me" or pronoun == "myself":
                return self.participants[message.author]
            if pronoun == "you":
                currentMessage = message
                index = 0
                while currentMessage.author == message.author:
                    index = self.messages.index(currentMessage) - 1
                    if index < 0:
                        break
                    currentMessage = self.messages[index]
                if index >=0:
                    return self.participants[currentMessage.author]
            if pronoun == "we" or pronoun == "us":
                return " ".join([value for key, value in self.participants.items()])
        return


def checkWord(stringList, word):
    word = word.lower()
    for string in stringList:
        string = string.lower()
        if fuzz.ratio(word, string) > fuzzRatio:
            return True
    return False


def findName(stringList, nameList):
    for word in stringList:
         for name in nameList:
              word = word.lower()
              lowerName = name.lower()
              if fuzz.ratio(word, lowerName) > fuzzRatio:
                   return name 
              splitName = lowerName.split(" ")
              for subName in splitName:
                   if fuzz.ratio(word, subName) > fuzzRatio:
                        return name



replacements = {
  'y': 'why',
  'l8': 'late',
  'u': 'you',
  'ur': 'your',
  'youre' : 'you\'re',
  'wru' : 'where are you',
  'wot' : 'what',
  'wat' : 'what',
  'wanna' : 'want to',
  'gonna' : 'going to',
  'hes' : 'he\'s',
  'shes' :'she\'s',
  }


def sanitize(text):
    sanitized = text[0].lower() + text[1:]
    sanitized = sanitized.replace('?', ' ? ').replace('.', ' . ')
    sanitized = ' '.join([replacements.get(w, w) for w in sanitized.split()])
    return sanitized

#print("Do you wanna go on a Wednesday night then?".split())
