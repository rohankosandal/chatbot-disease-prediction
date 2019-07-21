from nltk.tokenize import word_tokenize
import string
from nltk.tree import Tree
import nltk
import json
from nltk.corpus import stopwords
import os
stopword= set(stopwords.words('english'))

def getPOS(text):
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopword]
    POS = nltk.pos_tag(tokens)
    nouns = list()
    verbs = list()
    adverbs = list()
    adjective = list()
    pronouns = list()

    for (token,tag) in POS:
        if (tag =='NN') or (tag =='NNP') or (tag =='NNS'):
            nouns.append(token)
        if tag=='PRP' or tag=='PRP$':
            pronouns.append(token)
        if tag=='VBZ' or tag=='VB' or tag=='VBP' or tag== 'VBG':
            verbs.append(token)
        if tag=='RB' or tag=='RBR':
            adverbs.append(token)
        if tag=='JJ' or tag=='JJR':
            adjective.append(token)
    return POS,nouns,verbs,adjective,adverbs,pronouns


def structure_ne(ne_chunked):
    ne = []
    for subtree in ne_chunked:
        if type(subtree) == Tree:
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string , ne_label))
    return ne 

def extractDate(text):
    import re
    tokens = nltk.word_tokenize(text)
    POS = nltk.pos_tag(tokens)
    date = []
    date.append((re.findall(r'\d+\s\w+[a-zA-Z]\w+\s\d+|\d+\S\d+\S\d+|\w+\s\d+\S\s\d+',text)))
    for token,pos in POS:
        if pos == "CD":
            date.append((token))
    return date


def generateCSVtoJsonFile():
    import csv

    d=[{}]
    with open("first.csv","rb") as f:
        reader = csv.reader(f,delimiter=' ')
        for line in reader:
            s="".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in line[1:]]).strip()
            d.append({
                'type':line[0],
                'question':s
            })
        with open("first.txt","a") as f:
            json.dump(d,f)





def isQuestion(Question):
    QuestionData = word_tokenize(Question)
    isques=False
    qWords = ['does','Does','Which','which','what','What','Where','When','where','wat','wht','?','why','Why','who','Who','do','Do','whom','Whom','which','Which','whether','Whether','whose','Whose']
    for word in QuestionData:
        if word in qWords:
            isques=True
    return isques

def chunk(rawdata):
    tokens = nltk.word_tokenize(rawdata)
    POS = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(POS)
    return chunked





def getQuestionType(question):

    def build_features(corpus):
            """
            Features are words appear in a corpus
            """

            all_words = []
            for doc, label in corpus:
                all_words.extend(doc)

            word_distribution = nltk.FreqDist(all_words)
            return word_distribution.keys()

    def extract_features(document):
            return {word.lower():True for word in document.split() if word not in stopword}

    def build(labeled_tuple):
            corpus=[ (extract_features(words),label) for words,label in labeled_tuple ]
            return corpus
    # import pickle
    # if os.path.isfile("classifier.pickle"):
    #     f=open("classifier.pickle","rb")
    #     classifier=pickle.load(f)
    #     f.close()
    # else:
    with open("interface/2.txt",'r') as f:
        data=json.load(f)
        tup=[]
        for d in data:
            tup.append((d['question'],d['type']))

    classifier = nltk.NaiveBayesClassifier.train(build(tup))
    # savedClassifier = open("classifier.pickle","wb")
    # savedClassifier.close()
    # pickle.dump(classifier,savedClassifier)


    return classifier.classify(extract_features(question))
