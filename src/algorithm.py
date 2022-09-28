import requests
import re
from bs4 import BeautifulSoup

headers = {
    'www.amazon.com': {
        'accept': 'text/html,*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'device-memory': '8',
        'dnt': '1',
        'downlink': '10',
        'dpr': '1.5',
        'ect': '4g',
        'origin': 'https://www.amazon.com',
        'referer': 'https://www.amazon.com/s?k=iphone',
        'rtt': '50',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.5',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-ch-viewport-width': '669',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50',
        'viewport-width': '1920'
        },
    'www.ebay.com': {

    },
    'www.walmart.com': {

    },
    'www.etsy.com': {

    },
    'www.wish.com': {

    },
    'www.bestbuy.com': {

    },
    'www.wish.com': {

    },
    'www.target.com': {

    },
    'www.homedepot.com': {

    },
    'www.sears.com': {

    },
    'www.kohls.com': {

    },
    'www.google.com': {

    },
    'www2.hm.com': {
        'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'referer': 'https://www2.hm.com/',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50},',
    },
}

def getHeaders(site_url):
    base_url = re.findall(r'[\w]{3,4}[\.]{1}[\w]+[\.]{1}[\w]{3}', site_url)[0]
    return headers[base_url]

def extractText(site_url):
    site_html = requests.get(url=site_url, headers=getHeaders(site_url))
    parsed_html = BeautifulSoup(site_html.text, 'html.parser').find_all()

    raw_text = re.findall(r'>[\w\s]{3,500}<', str(parsed_html))
    formatted_text = list(set([x[1:-1].strip() for x in raw_text]))
    
    return formatted_text

def findDarkPatterns(text):
    print()