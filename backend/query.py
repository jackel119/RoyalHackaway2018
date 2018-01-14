import nltk
from enum import Enum
from datetime import datetime

class QType(Enum):
    WHERE = 1
    WHEN = 2
    WHY = 3
    HOW = 4
    WHICH = 5
    WHAT = 6
    WHO = 7
    BOOL = 8

def isQuestion(word):
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
    if "?" == word:
        return QType.BOOL
 
class Query(object):
    def __init__(self, text=None, message_number=0):
        self.text = text
        self.qtype = None
        self.addressee = None
        self.clause = None
        self.time = None
        self.message_number = message_number

    def show(self):
        print()
        print(self.text)
        print(self.qtype)
        print(self.addressee)
        print(self.clause)

    def __str__(self):
        return str(self.qtype)

    def __repr__(self):
        return self.__str__()

def notIrrelevant(tag):
    goodTags = ["NN", "NNS", "NNP", "NNPS", "VB", "VBG", "JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
    if tag in goodTags:
        return True
    return False

class Answer(object):
    def __init__(self, qtext, qtype, addressee, clauses, text):
        self.qtext= qtext
        self.qtype = qtype
        self.addressee = addressee
        self.clauses = clauses
        self.text = text

    def show(self):
        print()
        print(self.qtext)
        print(self.qtype)
        print(self.addressee)
        print(self.clauses)
        print(self.text)
