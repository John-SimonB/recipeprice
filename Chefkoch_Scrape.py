import requests
from bs4 import BeautifulSoup
import uuid
import re



def chefkoch_scrape(URL):
    if "https://www.chefkoch.de/rezepte/" in URL:
        response = requests.get(URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find("h1").text.strip()
            ingredients = soup.find_all('table', class_='ingredients')
            products = []
            products.append(name)
            td_left_elements = soup.find_all("td", class_="td-left")
            td_right_elements = soup.find_all("td", class_="td-right")

            td_left_contents = [td_left.text.strip() for td_left in td_left_elements]
            td_right_contents = [td_right.text.strip() for td_right in td_right_elements]

            td_left_contents = [content.strip().replace(" ", "") if content.strip() != "" else "0g" for content in td_left_contents]

            data = []

            for i in range(min(len(td_left_contents), len(td_right_contents))):
                left_content = td_left_contents[i]
                right_content = td_right_contents[i]

                if left_content != "0g":
                    amount = "".join(filter(str.isdigit, left_content))
                    unit = "".join(filter(str.isalpha, left_content))
                else:
                    amount, unit = "0", "g"

                product = [right_content, amount, unit]
                products.append(product)
            
            return products
    else:
        return False

url = "https://www.chefkoch.de/rezepte/1151011221381450/Der-beste-Pizzateig.html"
print(chefkoch_scrape(url))

