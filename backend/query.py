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

def isQuestion(word):
    word = word.lower()
    if "where" in word:
        return QType.WHERE
    if "when" in word:
        return QType.WHAT
    if "why" in word:
        return QType.WHY
    if "how" in word:
        return QType.HOW
    if "which" in word:
        return QType.WHICH
    if "what" in word:
        return QType.WHAT
    if "who" in word:
        return QType.WHO
    if "?" in word:
        return QType.BOOL
 
class Query:
    def __init__(self, qtype, addressee, clause):
        self.qtype = qtype
        self.addressee = addressee
        self.clause = clause

def isQuery(message):
    tagged = nltk.pos_tag(nltk.word_tokenize(message.text.lower()))
    for word, tag in tagged:
        word = isQuestion(word)
        if word:
            self.qtype = word
    if self.qtype:
       # query = Query(self.qtype, )
       pass
