import pandas, sklearn, nltk, re, string
import matplotlib.pyplot as plt
from textblob import TextBlob
import gensim
from gensim.models.ldamulticore import LdaMulticore
from gensim import corpora, models 
nltk.download('maxent_ne_chunker')
nltk.download('words')

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

from nltk import FreqDist

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist

def text_cleaning_tokenize(data):
    tokens_list=[]
    lemma = WordNetLemmatizer()
    for i in range(0,data.shape[0]):
        text = data.iloc[i,3] #full joke
        joke = re.sub('[^a-zA-Z]', ' ', text)
        tokens = []

        for word in joke.lower().split():
            if word not in stopwords.words('english'):
                tokens.append(lemma.lemmatize(word))
        tokens_list.append(tokens)
        tokens=[]
    return tokens_list

def extract_names(tokens_list):
    nouns_list = [token[0] for token in nltk.pos_tag(tokens_list) if token[1]=="NN"]
    return nouns_list

def frequency_analysis(concat_list):
    freq_dist = FreqDist(concat_list)
    print(freq_dist.most_common)
    freq_dist.plot(20, cumulative=True)

def get_topics(tokens_list):
    dictionary = corpora.Dictionary(tokens_list)
    dictionary.filter_extremes(no_below=3)
    corpus = [dictionary.doc2bow(tokens) for tokens in tokens_list]

    num_topics=20
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=7, alpha=[0.01]*num_topics, eta=[0.01]*len(dictionary.keys()))
    for topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=5):
        print(topic)
    vis = gensimvis.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary)
    pyLDAvis.save_html(vis, 'LDA_Visualization.html')

def words_score(data):
    lendf = data[['full joke', 'score']]
    for i in range(0,lendf.shape[0]):
        joke = str(lendf.iat[i,0])
        lendf.iat[i,0] = len(joke.split())

    print(lendf.describe())
    lendf.plot(x='score', y='full joke', kind='scatter')
    plt.show()








