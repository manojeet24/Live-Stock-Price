#Takes Company name as input and returns it's Last Traded Price

import sys,json
import requests
from bs4 import BeautifulSoup as bs

def price(company_name):
  
    if len(company_name) == 0:
        return 'Enter Company Name!!!'

    ticker = company_name[:1]
    
    #Removing last character(.) from "Ltd."
    company_name = company_name[:-1]
    url = 'https://www.tickertape.in/stocks?filter=' + ticker

    #parsing the HTML to find the SYMBOL of company
    r = requests.get(url)
    content = r.text
    soup = bs(content,'html.parser')

    secondpart = ''
    for link in soup.find_all('a'):
            if link.text.lower() == company_name.lower():
                secondpart=link['href']
                break

    if secondpart == '':
            return 'Check Company Name'

    #TICKER = SYMBOL of Stock 
    TICKER = ""

    for i in range( len(secondpart) - 1, -1, -1) :
        if secondpart[i] != '-':
            TICKER=secondpart[i]+TICKER
        else:
            break
    
    if len(TICKER)<=1:
        return 'Check Company Name'
    else:
        url = "https://api.tickertape.in/stocks/charts/intra/"
        url = url + TICKER
        r = requests.get(url)
        content = r.text
        obj = json.loads(content)
        data = obj['data']
        data = data[0]['points']
        data = data[-1]
        price = data['lp'] 
        return ('₹ ' + str(price))

#print(price('Reliance Industries Ltd.'))