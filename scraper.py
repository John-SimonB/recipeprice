#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:16:45 2023

@author: john-simonbachhuber
"""

import uuid
import re
import requests
from bs4 import BeautifulSoup
from harperDB import insert_item, delete_all_items, get_all_item, delete_item

url = "https://www.bringmeister.de/k/kuehlregal"
def scrape_data(URL):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_="container svelte-igvw6e")

    data = {}

    #delete_all_items()
    for item in items:
        product_name = item.find('a', class_='product-name').text.strip().replace("Ã¶", "ö").replace("Ã¼", "ü").replace("Ã¤","ä")
        prices = item.find('div', class_='price-container').text.strip()
        link = item.find('a', class_='product-name')['href']
        packung = item.find('div', class_='small-info')
        pack = packung.find('span').text.strip()
        
        #Menge und Mengenangabe für das Produkt ermitteln und entsprechened Formatieren
        menge_wert = ""
        menge_einheit = ""
        for char in pack:
            if char.isdigit():
                menge_wert += char
            elif char.isalpha():
                menge_einheit += char

        if(menge_einheit == "gPackung"):
            menge_einheit = "g"
        elif(menge_einheit == "kgPackung"):
            menge_einheit = "kg"
        elif(menge_einheit == "mlFlasche"):
            menge_einheit = "ml"
        elif(menge_einheit == "erTÃte"):
            menge_einheit = "Tüte"
        elif(menge_einheit == "gGlas"):
            menge_einheit = "g"
        elif(menge_einheit == "gStÃck"):
            menge_einheit = "g"
        elif(menge_einheit == "gFlasche"):
            menge_einheit = "g"
        elif(menge_einheit == "kgStÃck"):
            menge_einheit = "kg"
        
            
        price_splited = prices.split("\n")
        
        #Preis für das Produkt ermitteln und entsprechend formatieren
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
            "menge_wert": menge_wert,
            "menge_einheit": menge_einheit
        }
        print(product_name)
        #insert_item(data[id])
        print(len(data))
    return data


#scrape_data(url)
#delete_all_items()
#insert_item(data)
#insert_item(product)
#productlist.append(product)
#print(get_all_item())

#idee keine angebote scrapen sondern immer nur die normalen preise
#so könnte ich mit einer tabelle arbeiten und müsste nicht alte preise erstezen (produkt ist nicht mehr im angebot)
#außerdem würde so nur einmal im monat scrapen reichen (programm läuft schneller)
