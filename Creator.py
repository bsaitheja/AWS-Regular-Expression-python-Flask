import os
from nltk.stem import SnowballStemmer 
import re
import string
from collections import Counter
import pickle



path="corpus"

files=os.listdir(path)
paths=[]
for file in files:
    paths.append(os.path.join(path,file))

documents={}
index={}

stop = open('stopwords.txt','r')
stopwords=stop.read().split()


#PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def tokenize(text):
    lines = text.split("\n")
    words=[]
    for line in lines:
        spli = line.split(" ")
        for word in spli:
            words.append(word)
    return words

def lower(tokens):
    tokn=[]
    for token in tokens:
        tokn.append(token.lower())
    #return [token.lower() for token in tokens]
    return tokn

def steming_en(tokens):
    stemng = SnowballStemmer('english',)
    return [stemng.stem(token) for token in tokens]

def punctuation_filter(tokens):
    return [re.sub('[^\w\s]', '', token) for token in tokens]

def stopword_filter(tokens):
    tkn=[]
    for token in tokens:
         if token in stopwords:
             pass
         else:
             tkn.append(token)
    return tkn


def analyze(text):
    tokens = tokenize(text)
    tokens = lower(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = steming_en(tokens)
    return [token for token in tokens if token]

for path in paths:
    file = open(path, encoding="utf8")
    tokens = analyze(file.read())
    #print(documents.keys()    )
    if( path not in documents.keys()):
        documents[path]=Counter(tokens)
        #documents['termFreq']=
    #print(tokens)
    for token in tokens:
        if token not in index:
            index[token]=set()
        index[token].add(path)
        #print(analyze('title'))
        #if(analyze('title')[0]== token):
           # print("pass")
#print(documents)

out = open("output.txt","wb+")
out.write(pickle.dumps(documents))
out.close()

out2 = open("tokens.txt","wb+")
out2.write(pickle.dumps(index))
out2.close()