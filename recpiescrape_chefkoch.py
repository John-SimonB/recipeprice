import requests
from bs4 import BeautifulSoup

url = "https://www.chefkoch.de/rezepte/2352371374010722/Cremiger-Nudelauflauf-mit-Tomaten-und-Mozzarella.html"


def chefkoch_scrape(URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ingredients = soup.find_all('table', class_='ingredients')
    for ingredient in ingredients:
        zutaten = [span.text.strip().replace(' ', '').replace(',', ' ') for span in ingredient.find_all('span') if span.text.strip()]
        #product_name = zutaten[1::2]
        #package = zutaten[::2]
    return zutaten

#chefkoch_scrape(url)