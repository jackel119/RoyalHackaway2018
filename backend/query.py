import nltk
from enum import Enum

class QType(Enum):
    WHERE = 1
    WHEN = 2
    WHY = 3
    HOW = 4
    WHICH = 5
    WHAT = 6
    WHO = 7
    BOOL = 8

def isWQuestion(word):
    word = word.lower()
    if "where" == word:
        return QType.WHERE
    if "when" == word:
        return QType.WHEN
    if "why" == word:
        return QType.WHY
    if "how" == word:
        return QType.HOW
    if "which" == word:
        return QType.WHICH
    if "what" == word:
        return QType.WHAT
    if "who" == word:
        return QType.WHO
 
class Query:
    def __init__(self):
        self.qtype = None
        #self.addressee = addressee
        #self.clause = clause
        pass

def notIrrelevant(tag):
    goodTags = ["NN", "NNS", "NNP", "NNPS", "VB", "VBG", "JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
    if tag in goodTags:
        return True
    return False

def isQuery(message):
    query = Query()
    tagged = nltk.pos_tag(nltk.word_tokenize(message.text))
    firstTag = tagged[0][1]
    if firstTag == "CC" or firstTag == "RB":
        tagged = tagged[1:]
        if not tagged:
            return
    wqWord = isWQuestion(tagged[0][0])
    if wqWord:
        query.qtype = wqWord
    else:
        for word, tag in tagged:
            if word == "?":
                query.qtype = QType.BOOL
                break
    if query.qtype:
        #Checking the addressee of the question
        if message.mentions:
            query.addressee = message.mentions[0]
        #else if:
            #see if there are group users' names in the message i.e. jack, dima, natalia ... for The New Socialist State
            #if there are pronouns AND names in the message, check if the name is a user in the chat
            #if the name is NOT a user, then the addressee will be the PRONOUN
        #else:
            #pronouns: replace I/me/etc with author, replace you with last person, replace he/she/them with relevant people if possible (maybe the last name mentioned in the chat?)

        #Checking the clause of the question
        #query.clause = set(filter(lambda word, tag : notIrrelevant(tag), message.text))
        return query
    return 
        