import time
from fbchat import Client
from fbchat.models import *

def get_login(f):
    with open(f, 'r') as file:
        lines = file.readlines()
    return lines[0].replace('\n', ''), lines[1].replace('\n', '')

username, login = get_login('login')
client = Client(username, login)
users = client.fetchAllUsers()
print("Input the user you want to message:")
user = client.searchForUsers(input())[0]
print(user.uid + " is id of " + user.name)
while True:
    client.send(Message(text="Heeeyyyyyy" + user.name + "8====D"), int(user.uid))
    time.sleep(10)
    print("Sent")
#for message in client.fetchThreadMessages(thread_id=user.uid, limit=1000):
#    print(message.timestamp, message.text)

