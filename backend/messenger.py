from backend.query import *
from backend.chat import Chat
from fbchat import Client

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

    def run_loop(self, limit=1000):
        print("Input the user you want to message:")
        to_search = input()
        users = self.client.searchForUsers(to_search) + self.client.searchForGroups(to_search)
        users = users
        for i in range(0,len(users)):
            print(i, ":", users[i].name)
        user = users[int(input("Please specify which chat you'd like to participate in: "))]
        messages = self.client.fetchThreadMessages(thread_id=user.uid, limit=limit)[::-1]
        thread = self.client.fetchThreadInfo(user.uid)
        chat = Chat(user.name, user.uid, messages, thread, self.client.uid, self.user_map[self.client.uid], self.user_map)
        print(chat.participants)

    def test(self):
        print(self.client.fetchAllUsers())
        print(type(self.client.fetchAllUsers()[0]))



if __name__ == '__main__':
    m = Messenger()
    m.run_loop()
