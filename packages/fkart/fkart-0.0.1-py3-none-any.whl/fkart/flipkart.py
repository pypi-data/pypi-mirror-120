import requests
from bs4 import BeautifulSoup

# search query


query = input('Enter Search Item:')

url = 'https://www.flipkart.com/search?q='+query+''

def fkart(url):
    res = requests.get(url).content

    soup = BeautifulSoup(res,'html.parser') 

    block = soup.find_all('div',class_='_1xHGtK _373qXS')

    if len(block)>0:
        c =1
        for i in block:
            brand  = i.find('div',class_='_2WkVRV')
            title = i.find('a',class_='IRpwTa')
            price = i.find('div',class_='_30jeq3')

            print(c,10*'---')
            print(brand.text)
            print(title.text)
            print(price.text)
            c+=1
            print()

    else:
        block  = soup.find_all('div',class_='_13oc-S')
        c = 1

        for i in block:    
            title = i.find('div',class_='_4rR01T')
            price = i.find('div',class_='_30jeq3 _1_WHN1')
            rating = i.find('div',class_='_3LWZlK')

            print(c,10*'------')   
            print(title.text)
            print(price.text)
            print(rating.text)
            c+=1

    if c == 0:
        print('Sorry, unable to find the results')

    
