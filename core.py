#Takes Company name as input and returns it's Last Traded Price

import sys
import requests
from bs4 import BeautifulSoup as bs

def price(company_name):
    #taking input
    # company_name = input('Enter Company Name: ')
    if company_name == '':
        err = 'Enter Company Name!!!'
        return err
    
    ticker = company_name[:1]
    #Base URL to Stock URL
    url='https://economictimes.indiatimes.com/markets/stocks/stock-quotes?ticker=' + ticker
    r = requests.get(url)
    content = r.content
    soup = bs(content, "html.parser")

    secondpart = ''
    for link in soup.find_all('a'):
        if link.text==company_name:
            secondpart=link['href']
            break

    if secondpart == '':
        err = 'Check Company Name'
        return err

    firstpart="http://economictimes.indiatimes.com"
    url = firstpart+secondpart
    #print(url)

    #finding price from Stock URL
    r = requests.get(url)
    content = r.content
    soup = bs(content,"html.parser")
    element = soup.find("div",{"class":"value","id":"nseTradeprice"})

    if(element):
        res = element.text
        return '₹ ' + res
    else:
        err = 'Check Company Name'
        return err

#print(price('IOL Chemicals and Pharmaceuticals Ltd.'))