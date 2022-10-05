import requests
import re
from bs4 import BeautifulSoup

div_tags = []
div_text = []

span_tags = []
span_text = []

h2_tags = []
h2_text = []


all_tags = []
all_text = []
all_labels =[]

# def extractWorkingDataset(site_url):
#     web_response = requests.get(url=site_url, headers={'User-Agent':'Requests'})
#     parsed_html = BeautifulSoup(web_response.text, 'html.parser').find_all()

#     raw_text = re.findall(r'>[\w\s]{3,1000}<', str(parsed_html))
#     formatted_text = list(set([x[1:-1].strip() for x in raw_text]))
    
#     return formatted_text



def scrapePage(site_url, tags = all_tags, text = all_text):
    ''' --------------------------------------------------
    #*              create training dataset
    -------------------------------------------------- '''
    web_response = requests.get( url=site_url, headers={'User-Agent':'Requests'})
    soup = BeautifulSoup(web_response.text, 'html.parser')
    
    temp = scrape_divs(soup)
    tags += temp[0]
    text += temp[1]
    
    temp = scrape_spans(soup)
    tags += temp[0]
    text += temp[1]
    
    temp = scrape_h2s(soup)
    tags += temp[0]
    text += temp[1]
    
    return [tags,text]

def scrape_divs(soup):
    ''' --------------------------------------------------
    #*              scrape div tags
    -------------------------------------------------- '''
    temp = []

    for tag in soup.body.find_all('div', recursive=True):
        worded_tag = remove_nonalpha(tag.getText()).split()
        for word in worded_tag:
            if len(word) < 30:
                temp.append(word.lower())
            
    div_text = list(set(temp))
    div_tags = ['div' for x in div_text ]

    return [div_tags, div_text]

def scrape_spans(soup):
    ''' --------------------------------------------------
    #*              scrape span tags
    -------------------------------------------------- '''
    temp = []

    for tag in soup.body.find_all('span', recursive=True):
        worded_tag = remove_nonalpha(tag.getText()).split()
        for word in worded_tag:
            if len(word) < 30:
                temp.append(word.lower())
            
    span_text = list(set(temp))
    span_tags = ['span' for x in span_text ]

    return [span_tags, span_text]

def scrape_h2s(soup):
    ''' --------------------------------------------------
    #*              scrape h2s tags
    -------------------------------------------------- '''
    temp = []

    for tag in soup.body.find_all('h2', recursive=True):
        worded_tag = remove_nonalpha(tag.getText()).split()
        for word in worded_tag:
            if len(word) < 30:
                temp.append(word.lower())
            
    h2_text = list(set(temp))
    h2_tags = ['h2' for x in h2_text ]

    return [h2_tags, h2_text]

def remove_nonalpha(word):
    ''' --------------------------------------------------
    #*           remove non-alphanumric values
    -------------------------------------------------- '''
    nonAlpha = [
        '(',')','[',']',':','#','@',
        '/','*','\\','|','%','$','&',
        '.',',','?','!','\'','\"',
        '-'
        ]
    new_word = ''
    
    for i in range(0,len(word)):
        if word[i] not in nonAlpha:
            new_word += word[i]
            
    return new_word


def naiveBayesClassifier(div_tags, div_text, div_labels, working_set):
    ''' --------------------------------------------------
    #*              text classifier algorithm
    -------------------------------------------------- '''
    from sklearn.naive_bayes import GaussianNB
    from sklearn import preprocessing
    
    le = preprocessing.LabelEncoder()
    
    training_tags_encoded = le.fit_transform(div_tags)
    training_text_encoded = le.fit_transform(div_text)
    training_labels_encoded = le.fit_transform(div_labels)
    
    training_features = zip(training_tags_encoded, training_text_encoded)
    
    model = GaussianNB()
    model.fit(training_features,training_labels_encoded)
    
    result_array = model.predict(working_set)
    # prediction set >> [[0,3],[1,1],[1,5],[0,1]]

    #TODO: condense the predicted array into a single boolean value
    
    return result_array
    