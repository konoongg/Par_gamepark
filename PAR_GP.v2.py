import requests
from bs4 import BeautifulSoup
import csv
import re
import time

start_time=time.time()
URL = "https://www.gamepark.ru/switch/games/?count=-1"
HEADERS = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
HOST = 'https://www.gamepark.ru/'
path = 'ns.csv'
ninSv = []
links = []
platform = ''
title = ''
price = ''
img = ''
age = ''
des = ''

def xl(items,path):
    with open (path,'w',newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Название','Платформа','Цена','фото','Описание','возраст'])
        for item in items:
            writer.writerow([item[0],item[1],item[2],item[3],item[4],item[5]])
            

r = requests.get(URL,headers=HEADERS)
soup = BeautifulSoup(r.text,'html.parser')

items = soup.findAll('li',class_='catalog-item')
for a_link in items:
    link = { 'link':HOST+a_link.find('a',class_='catalog-item-h')['href'],
            'title':a_link.find('a',class_='catalog-item-h').get_text(strip=True),
            'price':a_link.find('div',class_='catalog-item-body-right').a['data-price'],
            'platform':a_link.find('div',class_='catalog-item-legend').get_text(strip=True),
            'img':HOST + a_link.find('div',class_='catalog-item-img-wrap').img['src'],
            'des':a_link.find('div',class_='catalog-item-properties').get_text(strip=True)}
    
    links.append(link)


        
    

for i in links:
    platform = i['platform']
    img= i['img']
    title= i['title']
    des_np = soup.find('div',class_='catalog-item-properties-left').get_text(strip=True)
    price = i['price']
    age = ''
    des_ful=i['des']
    
    r = requests.get(i['link'],headers=HEADERS)
    soup = BeautifulSoup(r.text,'html.parser')
    playDes=''
    a = True
    product = []
    des_a= soup.findAll('div', class_="catalog-item-property")
    for letter in range (0,len(des_a)):
        param = des_a[letter].find('span',class_="cip-name-in").get_text(strip=True)
        if param == 'Возраст':
            age=des_a[letter].get_text(strip=True)[len(param):]
        
            


    
            
                    
           
            
            
    if age == '':
        age = 'без ограничений'
        
    
    
    
    
    play ={'title': title,
            'platform':platform,
            'price':price,
            'img':img,
            'des':des_ful,
            'age':age}

    
        
        
            

    product.append(play['title'])
    product.append(play['platform'])
    product.append(play['price'])
    product.append(play['img'])
    p_des = re.findall(r'[А-Я]?[^А-Я]*',play['des'] )
    for p in p_des:
        playDes+=p
        if a==True:
            playDes+=':'
            a=False
        elif a==False:
            playDes+=';'
            a=True
       
            
            
        playDes+=' '

    product.append(playDes[:-2])
    product.append(play['age'])
    
                                
    
    ninSv.append(product)
    xl(ninSv,path)

finish_time=time.time()
print(finish_time-start_time)
