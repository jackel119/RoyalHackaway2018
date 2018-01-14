from fbchat.models import *
from query import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

fuzzRatio = 80 

class Chat(object):

    def __init__(self, name, chat_id, messages, thread, owner_id, owner_name, lookup_table):
        self.name = name
        self.chat_id = chat_id
        self.messages = messages
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
        print("Participants in this conversation are:")
        for key, value in self.participants.items():
           print("    ", value) 
        self.generate()

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
                    pass

    def show_queries(self):
        print(self.queries)

    def isQuery(self, message):
        query = Query()
        tagged = nltk.pos_tag(nltk.word_tokenize(message.sanitized))
        for word, tag in tagged:
            qtype = isQuestion(word)
            if qtype:
                query.qtype = qtype
                break
        if query.qtype:
            #Checking the addressee of the question
            if message.mentions:
                # the person is @'d
                query.addressee = self.participants[message.mentions[0].thread_id]
            else:
                # checks to see if the person is mentioned in the message
                names = [value for key, value in self.participants.items()]
                for word, tag in tagged:
                    for name in names:
                        word = word.lower()
                        uName = name.lower()
                        if fuzz.ratio(word, uName) > fuzzRatio:
                            query.addressee = name
                            break
                        splitName = uName.split(" ")
                        for subName in splitName:
                            if fuzz.ratio(word, subName) > fuzzRatio:
                                query.addressee = name
                                break
            if not query.addressee:
                # if there's no name mentioned, checks pronouns
                pronouns = list(filter(lambda x : x[1] == "PRP", tagged))
                if pronouns:
                    if "you" in pronouns:
                        pronoun = "you"
                    else:
                        pronoun = pronouns[0]
                    if pronoun == "I" or pronoun == "me" or pronoun == "myself":
                        query.addressee = self.participants[message.author]
                    if pronoun == "you":
                        currentMessage = message
                        index = 0
                        while currentMessage.author == message.author:
                            index = self.messages.index(currentMessage) - 1
                            if index < 0:
                                break
                            currentMessage = self.messages[index]
                        if index >=0:
                            query.addressee = self.participants[currentMessage.author]
                else:
                    return
                    


                

            #Checking the clause of the question
            query.clause = list(filter(lambda x : notIrrelevant(x[1]), tagged))
            print(datetime.fromtimestamp(int(message.timestamp) // 1000).strftime('%Y-%m-%d %H:%M:%S'))
            print(message.text)
            print(message.sanitized)
            print(query.qtype)
            print("Clause:", query.clause)
            print("Addressee: ", query.addressee)
            print()
            return query
        return 
   
def isName(posName, names):
    if posName in names:
        return posName
    for name in names:
        sepName = name.split(" ")
        if posName in sepName:
            return name
    return

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
