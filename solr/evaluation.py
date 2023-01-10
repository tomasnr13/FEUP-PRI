# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

QRELS_FILE_TERM = "qrels/arnold_schwarzenegger_qrels.txt"
QUERY_URL_TERM1 = "http://localhost:8983/solr/jokes/select?defType=edismax&indent=true&q.op=AND&q=full_joke%3A%22Arnold%20Schwarzenegger%22&rows=30"
QUERY_URL_TERM2 = "http://localhost:8983/solr/jokes/select?defType=edismax&indent=true&mm=50%25&pf2=full_joke%5E10&ps2=0&q.op=OR&q=full_joke%3AArnold%20Schwarzenegger&rows=30&sort=score%20desc"

QRELS_FILE_LONG = "qrels/long_qrels.txt"
QUERY_URL_LONG1 = "http://localhost:8983/solr/jokes/select?defType=edismax&fq=full_joke%3A%2F.%7B20%7D.*%2F&indent=true&q.op=OR&q=*%3A*&rows=30"
QUERY_URL_LONG2 = "http://localhost:8983/solr/jokes/select?bq=subreddit%3A3amjokes&defType=edismax&fq=full_joke%3A%2F.%7B20%7D.*%2F&indent=true&q.op=OR&q=full_joke%3AWhat&rows=30&sort=score%20desc"

QRELS_FILE_PUNCH = "qrels/punchline_qrels.txt"
QUERY_URL_PUNCH1 = "http://localhost:8983/solr/jokes/select?indent=true&q.op=OR&q=full_joke%3A%20what%20why&rows=30&sort=score%20desc"
QUERY_URL_PUNCH2 = "http://localhost:8983/solr/jokes/select?fq=subreddit%3A%203amjokes&indent=true&q.op=OR&q=full_joke%3A%20what%20OR%20why%20OR%20how%20OR%20when&rows=30&sort=score%20desc"

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE_PUNCH).readlines()))

# Get query results from Solr instance
results = requests.get(QUERY_URL_PUNCH1).json()['response']['docs']
results_b = requests.get(QUERY_URL_PUNCH2).json()['response']['docs']


# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['id'] in relevant])/n

@metric
def r(results, relevant):
    return len([doc for doc in results if doc['id'] in relevant])/len(relevant)

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)


# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)',
    'r': 'Recall'
}


# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric','Value']] +
    [
        [evaluation_metrics[m], calculate_metric(m, results, relevant)]
        for m in evaluation_metrics
    ]
)

with open('results.tex','w') as tf:
    tf.write(df.to_latex())


def pr_curve(results):
    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp.plot()
    plt.show()
    plt.ylim(0,1.1)
    plt.savefig('precision_recall.pdf')

def pr_curve_b(results, results_b):
    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

    precision_values_b = [
        len([
            doc 
            for doc in results_b[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx, _ in enumerate(results_b, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values_b = [
        len([
            doc for doc in results_b[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results_b, start=1)
    ]

    precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}
    precision_recall_match_b = {k: v for k,v in zip(recall_values_b, precision_values_b)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))
    recall_values_b.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values_b])
    recall_values_b = sorted(set(recall_values_b))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]
    for idx, step in enumerate(recall_values_b):
        if step not in precision_recall_match_b:
            if recall_values_b[idx-1] in precision_recall_match_b:
                precision_recall_match_b[step] = precision_recall_match_b[recall_values_b[idx-1]]
            else:
                precision_recall_match_b[step] = precision_recall_match_b[recall_values_b[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp_b = PrecisionRecallDisplay([precision_recall_match_b.get(r) for r in recall_values_b], recall_values_b)

    _, ax = plt.subplots()

    disp.plot(ax=ax, name="Initial")
    disp_b.plot(ax=ax, name="Optimized")
    # PrecisionRecallDisplay.from_predictions([precision_recall_match.get(r) for r in recall_values], recall_values, ax=ax)
    # PrecisionRecallDisplay.from_predictions([precision_recall_match_b.get(r) for r in recall_values_b], recall_values_b, ax=ax)
    # plt.ylim(0,1.1)
    plt.savefig('precision_recall_b.pdf')

# only the results are evaluated singularly
#for plot with single curve
pr_curve(results)
#for plot with 2 curves
# pr_curve_b(results,results_b)