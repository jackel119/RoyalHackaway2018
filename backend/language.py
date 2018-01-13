import nltk

text = "William is coming over tonight"

tokens = nltk.word_tokenize(text)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)
