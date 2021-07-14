from flask import Flask,render_template,request

import os

import datetime
import pickle
import re
import math
from collections import Counter
from nltk.stem import SnowballStemmer 

app = Flask(__name__)






# client = MongoClient("mongodb+srv://Lumia540:Lumia540@cluster0.9vjsq.mongodb.net/mongodb1?retryWrites=true&w=majority")
# collec = client.mongodb1.collection6331

stop = open('stopwords.txt','r')
stopwords=stop.read().split()

stop_spanish =open('SpanishStopWords.csv','r',encoding="latin-1")
stopwords_spanish=stop_spanish.read().split()

#print(stopwords_spanish)
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

def stopword_filter_spanish(tokens):
    tkn=[]
    for token in tokens:
         if token in stopwords_spanish:
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

@app.route("/",methods=['GET', 'POST'])
def hello():
    return render_template('home.html')
@app.route('/s2')
def s2():
   return render_template('s2.html')
@app.route('/s3')
def s3():
   return render_template('s3.html')

@app.route('/s4')
def s():
   return render_template('s4.html')

@app.route('/se')
def s4():
   return render_template('search.html')

@app.route("/save",methods=['GET', 'POST'])
def save():
    #file = open('Alamo.txt', encoding="utf8")
    #a= file.read()
    name = str(request.form['f'])
    text = str(request.form['c'])
    if(name!="" and text!=""):
        name="files/"+name
        fl =open(name,"w+")
        fl.write(text)
        fl.close()
        words = words_text(text)
        l =len(words)
    return render_template("0.html",nam = name,leng=l)

@app.route("/show",methods=['GET', 'POST'])
def show():
    file = open('Alamo.txt', encoding="utf8")
    a= file.read()
    words = tokenize(a)
    words=lower(words)
    words = punctuation_filter(words)
    counter = Counter(words)
    #print(counter.most_common())
    word_count={}
    for word in words:
        if word in stopwords_spanish:
            if(word not in word_count):
                word_count[word]=1
            else:
                word_count[word]+=1
    print(word_count)
    return render_template("opt.html",rows=word_count)

@app.route("/show1",methods=['GET', 'POST'])
def show1():
    file = open('Alamo.txt', encoding="utf8")
    a= file.read()
    words = tokenize(a)
    words=lower(words)
    words = punctuation_filter(words)
    counter = Counter(words)
    #print(counter.most_common())
    rows=[]
    str1 = " " 
    for i in range(len(words)):
        if words[i] in stopwords_spanish:
            row=[]
            
            if(i>1):
                row.append(words[i-1])
                row.append(words[i])
                row.append(words[i+1])
                #print(row)
            rows.append(row)
    words= stopword_filter_spanish(words)
    text=str1.join(words)

    return render_template("list3.html",rows=rows,text=text)


@app.route("/q1_b",methods=['GET', 'POST'])
def q1_b():
    #file = open('Alamo.txt', encoding="utf8")
    #a= file.read()
    
    text = str(request.form['recent1'])

    root = 'files'
    files=os.listdir(root)
    paths=[]

    for fil in files:
        paths.append(os.path.join(root,fil))

    for path in paths:
        name=path
        c=0
        if(name!="" and text!=""):
            
            fl =open(name,"r+")
            lines=fl.read()
            fl.close()
            words = words_text(lines)
            ex = words_text(text)
            count=0
            for word in words:
                print(word,ex)
                if(word == ex[0]):
                    c=c+1
                 
    return render_template("1.html",nam = name,text=text,c=c)

@app.route("/q6",methods=['GET', 'POST'])
def q6():
    root = 'files'
    files=os.listdir(root)
    paths=[]

    for fil in files:
        paths.append(os.path.join(root,fil))

    for path in paths:
        name=path
        c=0
        file = open(name, encoding="utf8")
        a= file.read()
        str1 = a.split(" ")
        str2 = []
        for i in str1:             
            if i not in str2:
                str2.append(i) 
        opt=[]     
        for i in range(0, len(str2)):
            opt.append("Frequency of "+ str2[i]+ " is :"+ str(str1.count(str2[i])))   
    return render_template("2.html",opt = opt)

@app.route("/q7",methods=['GET', 'POST'])
def q7():
    root = 'files'
    files=os.listdir(root)
    paths=[]
    text = str(request.form['recent1'])
    words =text.split(" ")
    for fil in files:
        paths.append(os.path.join(root,fil))
    opt=[] 

    for path in paths:
        name=path
        c=0
        file = open(name, encoding="utf8")
        a= file.read()
        str1 = a.split(" ")
        str2 = []
        for i in str1:             
            if i not in str2:
                str2.append(i)
        count=str1.count(text) 
        
        for w in words: 
            for i in range(0, len(str2)):
                if str2[i]==w:
                    opt.append(str2[i]+ " is removed: "+ str(str1.count(str2[i]))+" many times")
        for w in words:  
            str1.remove(w)
    return render_template("3.html",opt = opt,str=str1)

@app.route("/q8",methods=['GET', 'POST'])
def q8():
    root = 'files'
    files=os.listdir(root)
    paths=[]
    text = str(request.form['recent1'])
    
    for fil in files:
        paths.append(os.path.join(root,fil))
    opt=[] 
      
    for path in paths:
        name=path
        c=0
        file = open(name, encoding="utf8")
        a= file.read()
        str1 = a.split(".")
        opt=[]
        count=0
        for s in str1:
            if(re.search(text,s)):
                opt.append(s)
                count=count+1
    return render_template("4.html",opt = opt,c=count)

@app.route("/show2",methods=['GET', 'POST'])
def show2():
    ex = int(request.form['recent1'])
    file = open('Alamo.txt', encoding="utf8")
    a= file.read()
    words = tokenize(a)
    words=lower(words)
    words = punctuation_filter(words)
    counter = Counter(words)
    #print(counter.most_common())
    word_count={}
    for word in words:
        if word in stopwords_spanish:
            if(word not in word_count):
                word_count[word]=1
            else:
                word_count[word]+=1
    wc=dict(sorted(word_count.items(), key=lambda item: item[1]))
    w=list(wc.items())[:ex]
    return render_template("list4.html",rows=w)

@app.route("/show3",methods=['GET', 'POST'])
def show3():
    ex = str(request.form['recent1'])
    docs=['Alamo.txt','AliceCleaner.txt','AliceInWonderland.txt','Shakespeare.txt']
    for doc in docs:
        file = open(doc, encoding="utf8")
        a= file.read()
        sentences = a.split(".")
        sen=[]
        for s in sentences:
        #     if(all(map(lambda v:v in s,ex))):
        #         sen.append()
        # print(sen)
            if(re.search(ex,s)):
                #print(s+"\n")
                sen.append(s)
    return render_template("list5.html",rows=sen,word=ex)

@app.route("/show5",methods=['GET', 'POST'])
def show5():
    ex = str(request.form['recent1'])
    file = open('Alamo.txt', encoding="utf8")
    a= file.read()
    sentences = a.split("\n")
    sen=[]
    for s in sentences:
    #     if(all(map(lambda v:v in s,ex))):
    #         sen.append()
    # print(sen)
          if(re.search(ex,s)):
              #print(s+"\n")
              sen.append(s)
    return render_template("list5.html",rows=sen,word=ex)

@app.route("/show4",methods=['GET', 'POST'])
def show4   ():
    ex = str(request.form['recent1'])
    file = open('Alamo.txt', encoding="utf8")
    a= file.read()
    sentences = a.split(".")
    sen=[]
    for s in sentences:
    #     if(all(map(lambda v:v in s,ex))):
    #         sen.append()
    # print(sen)
          if(re.search(ex,s)):
              #print(s+"\n")
              sen.append(s)
    return render_template("list5.html",rows=sen,word=ex)

@app.route("/search",methods=['GET', 'POST'])
def search():
    ex = str(request.form['recent1'])
    if(ex!=""):
        tkns = analyze(ex)
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
        print("results")
        print(result)

        res = []
        for r in result:
            if(r[1]>-1000):
                res.append(r)
            # print(res)
        d={}
        d_auth={}
        d_lang={}
        final=[]
        ws = words_text(ex)
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
                        array2.append(r)
            final.append(array2)
        print(final)
        return render_template("list1.html",rows=final)




if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)