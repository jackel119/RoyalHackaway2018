import nltk
from test import get_messages

def isQuestion(tagged_tokens):
    for word, tag in tagged_tokens:
        if word in ['what', 'who', 'where', 'how', 'when', 'which', 'why', '?']:
            return True
    return False


if __name__ == '__main__':
    messages = get_messages()[::-1]

    for message in messages:
        if message.text == "":
            continue
        tagged = nltk.pos_tag(nltk.word_tokenize(message.text.lower()))
        print(message.text)
        if isQuestion(tagged):
            print("is a question")
        else:
            print("is not a question")
        print()
