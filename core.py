#Takes Company name as input and returns it's Last Traded Price

import sys
import requests
from bs4 import BeautifulSoup as bs

def price(company_name):
  
    if company_name == '':
        err = 'Enter Company Name!!!'
        return err
    company_name = company_name[:-1]
    ticker = company_name[:1]
    url = 'https://www.tickertape.in/stocks?filter=' + ticker
    first_part = 'https://www.tickertape.in'

    r = requests.get(url)
    content = r.text
    soup = bs(content,'html.parser')

    secondpart = ''
    for link in soup.find_all('a'):
            if link.text == company_name:
                secondpart=link['href']
                break

    if secondpart == '':
            err = 'Check Company Name'
            return err

    url = first_part + secondpart

    #finding price from Stock URL

    r = requests.get(url)
    content = r.content

    soup = bs(content,"html.parser")
    element = soup.find("span",{"class":"jsx-2945882850 current-price text-dark text-24"})

    if(element):
        res = element.text
        return '₹ ' + res
    else:
        err = 'Check Company Name'
        return err

#print(price('Asian Paints Ltd.'))