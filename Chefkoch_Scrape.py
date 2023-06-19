import requests
from bs4 import BeautifulSoup
import uuid




def chefkoch_scrape(URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find("h1").text.strip()
    ingredients = soup.find_all('table', class_='ingredients')
    products = []
    for ingredient in ingredients:
        data = [span.text.strip().replace(' ', '').replace(',', ' ') for span in ingredient.find_all('span') if span.text.strip()]
        for i in range(0, len(data), 2):
            menge = data[i]
            zutat = data[i + 1]

            # Trenne die Mengenangabe in Wert und Einheit
            menge_wert = ""
            menge_einheit = ""
            for char in menge:
                if char.isdigit():
                    menge_wert += char
                elif char.isalpha():
                    menge_einheit += char
                
            # Speichere die Zutatendaten im Dictionary
            product = [zutat, menge_wert, menge_einheit]
            products.append(product)
    return products

    
url = "https://www.chefkoch.de/rezepte/1722041281270634"

print(chefkoch_scrape(url))
