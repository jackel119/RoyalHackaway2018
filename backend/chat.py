from datetime import datetime
from fbchat.models import *
from query import *

class Chat(object):

    def __init__(self, name, chat_id, messages):
        self.name = name
        self.chat_id = chat_id
        self.messages = messages
        self.queries = []
        self.generate()

    def generate(self):
        for message in self.messages:
            if message.text:
                # Generate Query
                q = isQuery(message)
                if q:
                    self.queries.append(q)
                else:
                    # Check if it answers another query
                    pass

    def show_queries(self):
        print(self.queries)
