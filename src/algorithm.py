from matplotlib import test
import requests
import re
from bs4 import BeautifulSoup

training_tags = []
training_text = []
training_labels = []

# def extractWorkingDataset(site_url):
#     web_response = requests.get(url=site_url, headers={'User-Agent':'Requests'})
#     parsed_html = BeautifulSoup(web_response.text, 'html.parser').find_all()

#     raw_text = re.findall(r'>[\w\s]{3,1000}<', str(parsed_html))
#     formatted_text = list(set([x[1:-1].strip() for x in raw_text]))
    
#     return formatted_text

def test_func(site_url):
    web_response = requests.get( url=site_url, headers={'User-Agent':'Requests'})
    soup = BeautifulSoup(web_response.text, 'html.parser')
    return scrape_tags(soup)

def scrape_tags(soup):
    temp = []
    temp1 = []
    temp2 = []
    temp3 = []

    for tag in soup.body.descendants:
        temp.append(re.findall(r'>[\w\s]{3,500}<', str(tag)))

    for list in temp:
        temp1 += list
    
    temp2 = set([x[1:-1].strip() for x in temp1])

    for string in temp2:
        temp3 += string.lower().split()

    return set(temp3) 


def naiveBayesClassifier(training_tags, training_text, training_labels, working_set):
    from sklearn.naive_bayes import GaussianNB
    from sklearn import preprocessing
    
    le = preprocessing.LabelEncoder()
    
    training_tags_encoded = le.fit_transform(training_tags)
    training_text_encoded = le.fit_transform(training_text)
    training_labels_encoded = le.fit_transform(training_labels)
    
    training_features = zip(training_tags_encoded, training_text_encoded)
    
    model = GaussianNB()
    model.fit(training_features,training_labels_encoded)
    
    result_array = model.predict(working_set)
    # prediction set >> [[0,3],[1,1],[1,5],[0,1]]

    #TODO: condense the predicted array into a single boolean value
    
    return result_array
    