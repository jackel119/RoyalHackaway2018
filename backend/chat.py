from datetime import datetime
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
            print("Instance of a User")
            self.isGroup = False
            self.participants[self.thread.uid] = lookup_table[self.thread.uid]
        else:
            print("Instance of a group")
            print(self.thread.participants)
            for part_id in self.thread.participants:
                self.participants[part_id] = lookup_table[part_id]
            self.isGroup = True
        self.participants[owner_id] =  owner_name
        self.queries = []
        #self.generate()

    def generate(self):
        for message in self.messages:
            if message.text:
                message.sanitized = sanitize(message.text)
                # Generate Query
                q = isQuery(message)
                if q:
                    self.queries.append(q)
                else:
                    # Check if it answers another query
                    pass

    def show_queries(self):
        print(self.queries)

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
