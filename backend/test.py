import time
from fbchat import Client
from fbchat.models import *

def get_login(f):
    with open(f, 'r') as file:
        lines =file.readlines()
    return lines[0].replace('\n', ''), lines[1].replace('\n', '')

username, login = get_login('login')
client = Client(username, login)
users = client.fetchAllUsers()
user = client.searchForUsers("Emma Tye")[0]
print(user.uid)
# while True:
#     client.send(Message(text="Heeeyyyyyy Emmma 8====D"), int(user.uid))
#     time.sleep(10) 
#for message in client.fetchThreadMessages(thread_id=user.uid, limit=1000):
#    print(message.timestamp, message.text)

all_threads = client.fetchThreadList()
print(all_threads)
