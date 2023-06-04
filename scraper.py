#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:16:45 2023

@author: john-simonbachhuber
"""

import uuid
import requests
from bs4 import BeautifulSoup
from harperDB import insert_item, delete_all_items, get_all_item, delete_item

url = "https://www.bringmeister.de/k/obst-und-gemuese"
def scrape_data(URL):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_="container svelte-igvw6e")

    data = {}

    #delete_all_items()
    for item in items:
        product_name = item.find('a', class_='product-name').text.strip()
        prices = item.find('div', class_='price-container').text.strip()
        link = item.find('a', class_='product-name')['href']
        #package = item.find('span', class_='svelte-98e10g').text.strip()
            
        price_splited = prices.split("\n")
        
        if len(price_splited) >= 2:
            normal_price = price_splited[1]
            special_price = price_splited[0]
        else:
            normal_price = price_splited[0]
            special_price = 0
        id = uuid.uuid4()

        data[id] = {
            "id": str(id),
            "title": product_name,
            "special_price": special_price,
            "normal_price": normal_price,
            "link": "www.bringmeister.de" + str(link),
            "package": "10 KG"
        }
        #insert_item(data[id])
    return data
        


#scrape_data(url)
#delete_all_items()
#insert_item(data)
#insert_item(product)
#productlist.append(product)




