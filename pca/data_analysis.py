from ctypes import sizeof
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from sklearn import decomposition
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt


def extract_data():
    data = pd.read_csv("all_jokes.csv")
    data = data['full joke']
    docs = []
    docs =data.to_string()
    return docs


def word_tokenizing():
    aux = extract_data()
    aux =word_tokenize(aux)
    return aux


def most_relevants_words():
    data = word_tokenize(extract_data())
    stop_words = nltk.corpus.stopwords.words('english')
    data = [token.lower() for token, pos in nltk.pos_tag(data)]
    data = [w for w in data if len(w) > 2]
  
    for token, pos in nltk.pos_tag(data):    
        if (pos == 'NN') | (pos == 'NNP'):
            data.append(token)
       # if (pos == 'GPE') | (pos == 'LOC'):
       #     data.append(token)
        if token in stop_words:
            data.remove(token)
        else:
            data.remove(token)
    return data

def most_relevants_plot(data):
    fdist = FreqDist(data).most_common(20)
    fdist = pd.Series(dict(fdist))
    fdist.plot.bar()
    plt.show()
   

def find_topics(data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    doc_term_matrix = X
    vocab = vectorizer.get_feature_names_out()
    num_topics = 100
    decomp = decomposition.NMF(n_components = num_topics,
         init = 'nndsvd')
    doctopic = decomp.fit_transform(doc_term_matrix)
    n_top_words = 3
    topic_words = []
    for topic in decomp.components_:
        idx = np.argsort(topic)[::-1][0:n_top_words]
        topic_words.append([vocab[i] for i in idx])

    final = [x for list in topic_words for x in list]
    print(topic_words)


    

