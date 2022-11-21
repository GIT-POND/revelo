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
        '}','{',':',';','>','<','»',
        '©'
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
        create a txt file containing dataset
    '''
    #?-------------------------------------------
    web_response = requests.get( url=site_url, headers={'User-Agent':'Requests'})
    soup = BeautifulSoup(web_response.text, 'html.parser')

    # Scrape words
    dataset = []
    dataset.append(scrape_words(soup, 'div'))
    dataset.append(scrape_words(soup, 'span'))
    dataset.append(scrape_words(soup, 'a'))

    #write dataset
    file_obj = open(file_name, 'w', encoding='UTF8')
    
    for list in dataset:
        for word in list:
            file_obj.write(word+'\n')

def csv_to_list(file):
    #?-------------------------------------------
    '''
        turn text file into list
    '''
    #?-------------------------------------------
    temp = list()
    for line in file.readlines():
        temp.append(line)
    return temp
    
    
def validate_dataset(file_name):
    #?-------------------------------------------
    '''
        check the dataset for dp words
    '''
    #?-------------------------------------------
    scarcity_instances = 0
    countDown_instances= 0
    socialProof_instances = 0  

    scarcity_file = open('_scarcity.txt','r')
    countDown_file = open('_countDown.txt','r')
    socialProof_file = open('_socialProof.txt','r')
    dataset_file = open(file_name,'r')
    
    scarcity_words = csv_to_list(scarcity_file)
    countDown_words = csv_to_list(countDown_file)
    socialProof_words = csv_to_list(socialProof_file)
    dataset_words = csv_to_list(dataset_file)
    
    for word in dataset_words:
        if word in scarcity_words:
            scarcity_instances += 1
        if word in countDown_words:
            countDown_instances += 1
        if word in socialProof_words:
            socialProof_instances += 1
        
    return [scarcity_instances, countDown_instances, socialProof_instances]