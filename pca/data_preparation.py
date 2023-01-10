import pandas as pd

def select_columns(data):
    data.iloc[:,(1,4,9)]

def select_columns_other(data):
    data.iloc[:,(2,3,0)]

def extract_data():
    files = []

    file1 = pd.read_csv("data/3amjokes.csv", usecols = [1,4,9])
    file2 = pd.read_csv("data/Jokes.csv", usecols = [1,4,9])
    file3 = pd.read_csv("data/AntiJokes.csv", usecols = [1,4,9])
    file4 = pd.read_csv("data/OtherJokes.csv",sep=';', nrows=20000)
    file4 = file4[['score', 'title', 'selftext']]

    data_trimmed1 = remove_low_rated(file1, 25)
    data_trimmed1['Subreddit'] = '3amjokes'
    data_trimmed2 = remove_low_rated(file2, 100)
    data_trimmed2['Subreddit'] = 'Jokes'
    data_trimmed3 = remove_low_rated(file3, 25)
    data_trimmed3['Subreddit'] = 'AntiJokes'
    data_trimmed4 = remove_low_rated(file4, 10)
    data_trimmed4['Subreddit'] = 'OtherJokes'
    print(data_trimmed4.head())

    files.append(data_trimmed1)
    files.append(data_trimmed2)
    files.append(data_trimmed3)
    files.append(data_trimmed4)
    	
    data = pd.concat(files, axis=0, ignore_index=True)

    data_filtered = sort_by_column(data, 'score')

    data_filtered.loc[:,'full joke'] = ""
    data_filtered['full joke'] = data_filtered['title'].astype(str) + " " + data_filtered['selftext'].astype(str)

    data_filtered.drop('title', inplace=True, axis=1)
    data_filtered.drop('selftext', inplace=True, axis=1)

    return data_filtered


def sort_by_column(data, column_name):
    
    sorted_data = data.sort_values(by=[column_name], ascending=False)

    return sorted_data

def remove_low_rated(data, threshold):
    filtered_data = data[(data.loc[:, ('score')]) >= threshold]

    return filtered_data

def writeDataToCsv(data, filename):
    data.to_csv(filename + '.csv', index=False)