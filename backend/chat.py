from fbchat.models import *
from query import *

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
        firstTag = tagged[0][1]
        if firstTag == "CC" or firstTag == "RB":
            tagged = tagged[1:]
            if not tagged:
                return
        wqWord = isWQuestion(tagged[0][0])
        if wqWord:
            query.qtype = wqWord
        else:
            for word, tag in tagged:
                if word == "?":
                    query.qtype = QType.BOOL
                    break
        if query.qtype:
            #Checking the addressee of the question
            if message.mentions:
                query.addressee = self.participants[message.mentions[0].thread_id]
                #see if there are group users' names in the message i.e. jack, dima, natalia ... for The New Socialist State
                #if there are pronouns AND names in the message, check if the name is a user in the chat
                #if the name is NOT a user, then the addressee will be the PRONOUN
                #pronouns: replace I/me/etc with author, replace you with last person, replace he/she/them with relevant people if possible (maybe the last name mentioned in the chat?)
            else:
                names = list(filter(lambda x : x[0] in [value for key,value in self.participants.items()], tagged))
                if names:
                    query.addressee = names[0]

            #Checking the clause of the question
            query.clause = list(filter(lambda x : notIrrelevant(x[1]), tagged))
            if query.addressee:
              print(datetime.fromtimestamp(int(message.timestamp) // 1000).strftime('%Y-%m-%d %H:%M:%S'))
              print(message.text)
              print(message.sanitized)
              print(query.qtype)
              print("Clause:", query.clause)
              print("Addressee: ", query.addressee)
              print()
            return query
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
