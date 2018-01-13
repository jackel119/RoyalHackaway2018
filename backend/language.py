import nltk

text = "Greetings, earthlings. I have come from the space beyond your known galaxy."

tokens = nltk.word_tokenize(text)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)
