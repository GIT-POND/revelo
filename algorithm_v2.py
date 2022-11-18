import requests
from bs4 import BeautifulSoup
import csv

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

def scrape_words(soup, tag_name):
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

def create_dataset(file_name, site_url):
    #?-------------------------------------------
    '''
        create a csv file containing a training
        dataset for the Naive Bays classifier
    '''
    #?-------------------------------------------
    

    web_response = requests.get( url=site_url, headers={'User-Agent':'Requests'})
    soup = BeautifulSoup(web_response.text, 'html.parser')

    # Scrape words
    div_words = scrape_words(soup, 'div')
    span_words = scrape_words(soup, 'span')
    a_words = scrape_words(soup, 'a')

    # Setup csv writer
    file_obj = open(file_name, 'w', encoding='UTF8', newline='')
    writer = csv.writer(file_obj)

    # Write to csv file
    writer.writerow(f'----- {len(div_words)+len(span_words)+len(a_words)} -----')
    for word in div_words:
        writer.writerow(word)
    for word in span_words:
        writer.writerow(word)
    for word in a_words:
        writer.writerow(word)
        
def csv_to_list(file):
    temp = list()
    for line in file:
        temp.append(line[0])
    return temp
    
    
def validate_dataset():
    scarcity_instances = 0
    countDown_instances= 0
    socialProof_instances = 0
    
    dataset = csv.reader(open('dataset(training).csv'))
    scarcity_file = csv.reader(open('_scarcity.csv'))
    countDown_file = csv.reader(open('_countDown.csv'))
    socialProof_file = csv.reader(open('_socialProof.csv'))
    
    scarcity_words = csv_to_list(scarcity_file)
    countDown_words = csv_to_list(countDown_file)
    socialProof_words = csv_to_list(socialProof_file)
    dataset_words = csv_to_list(dataset)
    
    for word in dataset_words:
        if word in scarcity_words:
            scarcity_instances += 1
        if word in countDown_words:
            countDown_instances += 1
        if word in socialProof_words:
            socialProof_instances += 1
        
    return [scarcity_instances, countDown_instances, socialProof_instances]