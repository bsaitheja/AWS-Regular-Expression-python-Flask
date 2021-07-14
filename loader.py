import pickle
import re
import math
from nltk.stem import SnowballStemmer 

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

def words_text(text):
    tokens = tokenize(text)
    tokens = lower(tokens)
    return [token for token in tokens if token]

def term_frequency(term,doc):
        freq=data[doc].get(term,0)
        return freq
def document_frequency(token):
        return len(index.get(token, set()))
def inverse_document_frequency(token,docs):

        return math.log10(len(docs) / document_frequency(token))

f = open("output.txt","rb")
data = pickle.load(f)
f.close()

f2 = open("tokens.txt","rb")
index = pickle.load(f2)
f2.close()

example = "she did not "
tkns = analyze(example)
#print(tkns)
array1=[]
docs=[]

for tkn in tkns:
    array1.append(index.get(tkn,set()))
for doc in set.intersection(*array1):
    docs.append(doc)

results=[]
for doc in docs:
    score=0.0
    for tkn in tkns:
        tf=term_frequency(tkn,doc)
        idf = inverse_document_frequency(tkn,docs)
        score= tf*idf
    results.append((doc,score))

result = sorted(results, key=lambda doc: doc[1], reverse=True)
##print(result)

res = []
for r in result:
    if(r[1]>-1000):
        res.append(r)
# print(res)
d={}
d_auth={}
d_lang={}
final=[]
ws = words_text(example)
for r in res:
    array2=[]
    file = open(r[0], encoding="utf8")
    words=words_text(file.read())
    if(ws[0] in words):
        li = [i for i, e in enumerate(words) if e == ws[0]]
        for l in li:
            #print(l+len(ws)-1,len(ws)-1)
            if(l+len(ws)-1<len(words)-1 and words[l+len(ws)-1]) == ws[len(ws)-1]:
                str1 = " " 
                d[r]=str1.join(words[l-20:l+len(ws)-1+20])
                #print(d[r]+"\n")
                array2.append(str1.join(words[l-20:l+len(ws)-1+20]))
                if("author:" in words):
        #print(words[words.index("author:")+1])
                    d_auth[r]=words[words.index("author:")+1]
                else:
                    d_auth[r]="not given"
                array2.append(d_auth[r])
                if("language:" in words):
        #print(words[words.index("author:")+1])
                    d_lang[r]=words[words.index("language:")+1]
                else:
                    d_lang[r]="not given"
                array2.append(d_lang[r])
                final.append(array2)
    print(final)