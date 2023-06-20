import requests
from bs4 import BeautifulSoup
import uuid




def chefkoch_scrape(URL):
    if "https://www.chefkoch.de/rezepte/" in URL:
        response = requests.get(URL)
        if response.status_code == 200:
            print(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find("h1").text.strip()
            ingredients = soup.find_all('table', class_='ingredients')
            products = []
            for ingredient in ingredients:
                data = [span.text.strip().replace(' ', '').replace(',', ' ') for span in ingredient.find_all('span') if span.text.strip()]
                for i in range(0, len(data), 2):
                    if i + 1 < len(data):
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
    else:
        return False

#url = "https://www.chefkoch.de/rezepte/820481186558221/Zitronenkuchen.html"
#print(chefkoch_scrape(url))

