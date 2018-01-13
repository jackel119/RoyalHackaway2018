from datetime import datetime
from query import *
from chat import Chat
import time
import json
from fbchat import Client
from fbchat.models import *

def get_login(f):
    with open(f, 'r') as file:
        lines = file.readlines()
    return lines[0].replace('\n', ''), lines[1].replace('\n', '')

def get_messages():
    username, login = get_login('login')
    client = Client(username, login)
    users = client.fetchAllUsers()
    user = client.searchForGroups("Socialist")[0]
    return client.fetchThreadMessages(thread_id=user.uid, limit=1000)

class Messenger(object):

    def __init__(self):
        username, login = get_login('login')
        self.client = Client(username, login)
        self.user_map = {}
        self.chats = {}
        self._initialize_contacts()
        self.messages = []

    def _initialize_contacts(self):
        self.user_map[self.client.uid] = self.client.fetchUserInfo(self.client.uid)[self.client.uid].name
        for user in self.client.fetchAllUsers():
            self.user_map[user.uid] = user.name

    def run_loop(self):
        print("Input the user you want to message:")
        to_search = input()
        users = self.client.searchForUsers(to_search) + self.client.searchForGroups(to_search)
        users = users
        for i in range(0,len(users)):
            print(i, ":", users[i].name)
        user = users[int(input("Please specify which chat you'd like to participate in:"))]
        messages = self.client.fetchThreadMessages(thread_id=user.uid, limit=1000)[::-1]
        chat = Chat(user.name, user.uid, messages)
        # for message in self.messages:
        #     if message.text:
        #         q = isQuery(message)
        #         if q:
        #             print(datetime.fromtimestamp(int(message.timestamp) // 1000).strftime('%Y-%m-%d %H:%M:%S'), self.user_map[message.author], message.text)
        #             print("Question Type: ", q.qtype)
        #         else:
        #             print()
        chat.show_queries()

    def test(self):
        print(self.client.fetchAllUsers())
        print(type(self.client.fetchAllUsers()[0]))



if __name__ == '__main__':
    m = Messenger()
    #print(json.dumps(m.user_map, indent=4, sort_keys=True))
    m.run_loop()
