import requests
import json

api_url = "https://graph.facebook.com/v2.6/me/messages?access_token="
class Messenger(object):
    def  __init__(self, access_token):
        self.access_token = access_token
        self.initialize_chats()

class Chat(object):

    def __init__(self):
        pass

if __name__ == '__main__':
    key = "EAACjIzhxmh0BAEQJChOD9fnYEiIkJNkF4LEtUWud1Xi4kgwImRuolLZC0ZAAEIINad3qltu3RucBEbSsTS9kCm7PCEPSDqGUbLZAtgKZBsKfNy1fGteTZBn8sKejZCA6VgjIoZB0IBpm3jUSGHJBX81C0yWbD7jJYx41YyZCPKjUPQZDZD"
    url = api_url + key
    print(requests.post(url).json())

