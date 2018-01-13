import time
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

username, login = get_login('login')
client = Client(username, login)
print("Input the user you want to message:")
to_search = input()
users = client.searchForUsers(to_search) + client.searchForGroups(to_search)
users = users
for i in range(0,len(users)):
    print(i, ":", users[i].name)
user = users[int(input("Please specify which chat you'd like to participate in:"))]
for message in client.fetchThreadMessages(thread_id=user.uid, limit=1000)[::-1]:
    print(message.author, message.text)

# 100002663745605
