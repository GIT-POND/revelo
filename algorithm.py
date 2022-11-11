from msilib.schema import Error
import requests
from bs4 import BeautifulSoup
import csv

def create_dataset_from_url(file_name, site_url):
    #?-------------------------------------------
    '''
        create a csv file containing a training
        dataset for the Naive Bays classifier
    '''
    #?-------------------------------------------
    

    web_response = requests.get( url=site_url, headers={'User-Agent':'Requests'})
    soup = BeautifulSoup(web_response.text, 'html.parser')

    # Scrape words
    div_words = scrape_tag_words(soup, 'div')
    span_words = scrape_tag_words(soup, 'span')
    a_words = scrape_tag_words(soup, 'a')

    # Setup csv writer
    file_obj = open(file_name, 'w', encoding='UTF8', newline='')
    writer = csv.writer(file_obj)

    # Write to csv file
    for word in remove_numbers(div_words):
        writer.writerow(['div', word])
    for word in remove_numbers(span_words):
        writer.writerow(['span', word])
    for word in remove_numbers(a_words):
        writer.writerow(['a', word])
    
    return 'training set created'

def label_dataset():
    #?-------------------------------------------
    '''
        add labels to training set using a 
        word bank
    '''
    #?-------------------------------------------
    input_file = open('dataset(unprocessed).csv')
    reference_file = open('dataset(reference).csv')
    output_file = open('dataset(training).csv', 'w', encoding='UTF8',newline='')

    table = csv.reader(input_file)
    word_bank_unformatted = csv.reader(reference_file)
    writer = csv.writer(output_file)

    word_bank = []

    for list in word_bank_unformatted:
        word_bank.append(list[0])

    for row in table:
        if str(row[1]) in word_bank:
            row.append(1)
            writer.writerow(row)
        else:
            row.append(0)
            writer.writerow(row)


def scrape_tag_words(soup, tag_name):
    #?-------------------------------------------
    ''' 
        scrape words within specified html tags
    '''
    #?-------------------------------------------
    temp = []

    for tag in soup.body.find_all(tag_name, recursive=True):
        worded_tag = remove_nonalpha(tag.getText()).split()
        for word in worded_tag:
            if len(word) < 30:
                temp.append(word.lower())

    return list(set(temp))


def remove_nonalpha(word):
    #?-------------------------------------------
    '''
        remove non-alphanumric characters within
        words found in html tags
    '''
    #?-------------------------------------------
    nonAlpha = [
        '(',')','[',']',':','#','@',
        '/','*','\\','|','%','$','&',
        '.',',','?','!','\'','\"',
        '}','{',':',';','>','<',
        ]
    new_word = ''
    
    for i in range(0,len(word)):
        if word[i] not in nonAlpha:
            new_word += word[i]
            
    return new_word


def remove_numbers(word_list):
    for word in word_list:
        if word.isdigit():
            word_list.remove(word)
        if type(word) == type(1):
            word_list.remove(word)

    return word_list


def trainModel():
    #?-------------------------------------------
    '''
        binary text classifier algorithm
    '''
    #?-------------------------------------------
    training_file = open('dataset(training).csv')
    training_dataset = csv.reader(training_file)
    
    tags = []
    text = []
    labels = []

    try:
        for line in training_dataset:
            tags.append(line[0])
            text.append(line[1])
            labels.append(line[2])

        from sklearn import preprocessing

        le = preprocessing.LabelEncoder()
        tags_encoded = le.fit_transform(tags)
        text_encoded = le.fit_transform(text)
        
        # features = zip(tags_encoded, text_encoded)
        # print(features)
        
        # from sklearn.naive_bayes import GaussianNB
        # model = GaussianNB()
        #model.fit(features,labels)
        #-----------------------------------------------------
        #result = model.predict([[0,2],[0,12]])

        
        return tags_encoded
        
    except Exception as e:
        print(e)


