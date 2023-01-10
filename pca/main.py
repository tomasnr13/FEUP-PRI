import data_preparation as prep
import data_characterization
import data_analysis as ana 
import pandas as pd
from textblob import TextBlob

data = prep.extract_data()
print(data.head())
print(data.describe())
data.to_json(path_or_buf='all_jokes.json', orient='records')

print('data characterization:')
print(data)
print(data.describe())

print('words vs score characterization:')
data_characterization.words_score(data)

tokens_list = data_characterization.text_cleaning_tokenize(data)
#print(tokens_list)

# concat_list = [token for nested_list in tokens_list for token in nested_list]
# names = data_characterization.extract_names(concat_list)
# data_characterization.frequency_analysis(concat_list)
# data_characterization.frequency_analysis(names)

data_characterization.get_topics(tokens_list)


#data_a = ana.extract_data()


ana.word_tokenizing()
data_a = ana.most_relevants_words() 
ana.most_relevants_plot(data_a)
ana.find_topics(data_a)




