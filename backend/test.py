import time
from fbchat import Client
from fbchat.models import *

def get_login(f):
    with open(f, 'r') as file:
        lines =file.readlines()
    return lines[0].replace('\n', ''), lines[1].replace('\n', '')

def get_messages():
    username, login = get_login('login')
    client = Client(username, login)
    users = client.fetchAllUsers()
    user = client.searchForGroups("Socialist")[0]
    return client.fetchThreadMessages(thread_id=user.uid, limit=1000)
