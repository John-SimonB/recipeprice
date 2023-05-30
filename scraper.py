#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:16:45 2023

@author: john-simonbachhuber
DataScraper für Angebote von Flink, folgende Daten werden ermittelt:
Produktname, Angebotspreis, Normalpreis, Menge(Verpackung), Produktlink
"""

import requests
from bs4 import BeautifulSoup
#Test

url = "https://www.bringmeister.de/angebote?isAvailable"


def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print("\nWebsite not found: " + response.status_code)
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        print("\nloading data from = \n" + url)
    return soup

def parse_soup(soup):
    productlist = []
    items = soup.find_all('div', class_="container svelte-98e10g")
    for item in items:
        product_name = item.find('a', class_='product-name').text.strip()
        prices = item.find('div', class_='price-container').text.strip()
        link = item.find('a', class_='product-name')['href']
        package = item.find('span', class_='svelte-98e10g').text.strip()
        
        
        price_splited = prices.split("\n")
        special_price = price_splited[0]
        if len(price_splited) >= 2:
            normal_price = price_splited[1]
        else:
            normal_price = 0


        product = {
            "productname", product_name,
            "price_special", special_price,
            "normal_price", normal_price,
            "package", package,
            "link", "www.bringmeister.de" + link
        }
        productlist.append(product)
    print(productlist[1])


parse_soup(get_page(url))

