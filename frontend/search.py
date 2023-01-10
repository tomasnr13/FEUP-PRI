from urllib.request import urlopen
import urllib.parse
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import spacy
from spacy import displacy
nltk.download('vader_lexicon')

NER = spacy.load("en_core_web_sm")

def dialogchk(joke):
    if joke.count('-') > 1:
        return True
    return False

def ner(joke):
    text= NER(joke)
    if len(text) > 1:
        return True
    return False

def ispunch(joke):
    if len(sent_tokenize(joke)) == 2 & joke.find('?')!=-1 & joke.find('.')!=-1:
        return True
    return False

def ispos(joke):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(joke)["compound"] > 0

def querysolr(query,sa=False,sd=False,sla=False,sld=False,qop=False,nr=10,tam=False,anti=False,jokes=False,other=False,punch=False, dialog=False, ne=False, pos=False, neg=False):
    url = "http://localhost:8983/solr/jokes/select?defType=edismax&df=full_joke&fl=score%2C%20subreddit%2C%20full_joke&indent=true&qf=full_joke%5E2&"
    if qop:
        url+="q.op=AND&"
    else:
        url+="q.op=OR&"
    rows = "rows=" + str(nr) + "&"
    url += rows
    url += "q="+urllib.parse.quote(query)
    if sa:
        url += "&sort=score%20asc"
    if sd:
        url += "&sort=score%20desc"
    if tam:
        url += "&fq=subreddit%3A%203amjokes"
    if anti:
        url += "&fq=subreddit%3A%20antijokes"
    if jokes:
        url += "&fq=subreddit%3A%20otherjokes"
    if other:
        url += "&fq=subreddit%3A%20jokes"
    print(url)
    response = urlopen(url)
    data_json = json.loads(response.read()) 
    data = data_json['response']['docs']

    newdata = []
    strj = []
    for doc in data:
        fj = doc['full_joke']
        included = False
        
        if fj in strj:
            included = True

        if punch:
            if ispunch(fj):
                if not included:
                    newdata.append(doc)
                    strj.append(fj)
                    included = True
        if ne:
            if ner(fj):
                if not included:
                    newdata.append(doc)
                    strj.append(fj)
                    included = True
        if dialog:
            if dialogchk(fj):
                if not included:
                    newdata.append(doc)
                    strj.append(fj)
                    included = True
        if pos | neg:
            isp = ispos(fj)
            if pos:
                if isp:
                    if not included:
                        newdata.append(doc)
                        strj.append(fj)
                        included = True
            if neg:
                if not isp:
                    if not included:
                        newdata.append(doc)
                        strj.append(fj)
                        included = True
        if not (punch | ne | dialog | neg | pos | included):
            newdata.append(doc)
            strj.append(fj)
            included = True
    print(newdata)
    return newdata
    # return data_json

