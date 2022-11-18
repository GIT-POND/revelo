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
        create training set by replacing all words
        with "scarcity", "countDown", "socialProof",
        or "None". As well as adding a "True" or 
        "False" to each line stating if a DP is found.
    '''
    #?-------------------------------------------
    input_file = open('dataset(unprocessed).csv')
    scarcity_file = open('_scarcity.csv')
    countDown_file = open('_countDown.csv')
    socialProof_file = open('_socialProof.csv')   
    output_file = open('dataset(training).csv', 'w', encoding='UTF8',newline='')

    table = csv.reader(input_file)
    file1 = csv.reader(scarcity_file)
    file2 = csv.reader(countDown_file)
    file3 = csv.reader(socialProof_file)
    writer = csv.writer(output_file)

    wb1 = []
    wb2 = []
    wb3 = []

    for line in file1:
        wb1.append(line[0])
    for line in file2:
        wb2.append(line[0])
    for line in file3:
        wb3.append(line[0])

    for row in table:
        if str(row[1]) in wb1:
            row[1] = 'scarcity'
            row.append(True)
            writer.writerow(row)
        elif str(row[1]) in wb2:
            row[1] = 'countDown'
            row.append(True)
            writer.writerow(row)
        elif str(row[1]) in wb3:
            row[1] = 'socialProof'
            row.append(True)
            writer.writerow(row)
        else:
            row[1] = 'None'
            row.append(False)
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


