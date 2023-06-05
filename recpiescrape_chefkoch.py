import requests
from bs4 import BeautifulSoup

url = "https://www.chefkoch.de/rezepte/1229661228043441/Pizzateig.html"


def chefkoch_scrape(URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ingredients = soup.find_all('table', class_='ingredients')
    zutaten_dict = {}
    for ingredient in ingredients:
        data = [span.text.strip().replace(' ', '').replace(',', ' ') for span in ingredient.find_all('span') if span.text.strip()]
        for i in range(0, len(data), 2):
            menge = data[i]
            zutat = data[i + 1]

            # Trenne die Mengenangabe in Wert und Einheit
            menge_wert, menge_einheit = menge[:-1], menge[-1]  # Letztes Zeichen entfernen

            # Speichere die Zutatendaten im Dictionary
            zutaten_dict[zutat] = {
                'menge_wert': menge_wert,
                'menge_einheit': menge_einheit
            }
    return zutaten_dict

#chefkoch_scrape(url)
