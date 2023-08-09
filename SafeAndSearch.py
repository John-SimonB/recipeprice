import requests
from thefuzz import fuzz
import re
import pandas as pd

#####################               #####################
#####################  LEVENSHTEIN  #####################
#####################               #####################

def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

#####################                  #####################
#####################  GetAllProducts  #####################
#####################  SaveDatatoExcel #####################
#####################                  #####################

def AllProductsAPI(urls):
  responses = []    
  for url in urls:
    payload={}
    headers = {
        'hub-slug': 'de_all_skus',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=10).json()
    print(response)
    responses.append(response)

  return responses

# Menge und Einheit extrahieren zum anschließenden speichern
def extract_data(angabe):
    muster = r'(\d+\.?\d*)\s*(\w+)'
    treffer = re.search(muster, angabe)
    if treffer:
        menge = treffer.group(1)
        einheit = treffer.group(2)
        return menge, einheit
    return None

def SafeProducts(ResponseLIST):
  items = []
  for Response in ResponseLIST:
    categories = Response["categories"]
    categorie = Response["slug"]
    for category in categories:
      products = category["products"]["products"]
      for product in products:
        product_name = product["name"]
        price = product["price"]["amount"]
        amount = extract_data(product_name)
        if "thumbnail" in product:
          icon = product["thumbnail"]
        else: 
          icon = ""
        if amount:
          amount = extract_data(product_name)
        else:
          amount = [0,0]
          item = {
            "name" : product_name,
            "price" : price,
            "menge" : amount[0],
            "einheit" : amount[1],
            "icon" : icon,
            "kategorie" : categorie
          }
        items.append(item)

  print(items)
  df = pd.DataFrame(items)
  df.to_excel('Data.xlsx', index=False)
  print ("Daten gespeichert")
  return True

#####################                  #####################
#####################  LoadDatatoDict  #####################
#####################                  #####################

def exceltodict():
  df = pd.read_excel('Data.xlsx')
  data = []
  for index, row in df.iterrows():
    item = {
      "name" : row["name"],
      "price" : row['price'],
      "menge" : row['menge'],
      "einheit" : row['einheit'],
      "icon" : row['icon']
      }
    data.append(item)
  return data

#####################                #####################
#####################  Produktsuche  #####################
#####################                #####################

def Searchitem(search_string):
  data = []
  df = pd.read_excel('Data.xlsx')

  schwellenwert = 80 

  for index, row in df.iterrows():
    text = row['name']
    ähnlichkeit = fuzz.ratio(search_string, text)
    if ähnlichkeit >= schwellenwert:
      item = {
        "name" : text,
        "price" : row['price'],
        "menge" : row['menge'],
        "einheit" : row['einheit'],
        "icon" : row['icon']
      }
      data.append(item)
  for item in data:
    distance = levenshtein_distance(search_string, ["name"])  
    print(distance)
    












#####################               #####################
#####################  Testbereich  #####################
#####################               #####################
links = [
  "https://consumer-api.goflink.com/v2/categories/obst",
  "https://consumer-api.goflink.com/v2/categories/feinkost",
  "https://consumer-api.goflink.com/v2/categories/gemuese",
  "https://consumer-api.goflink.com/v2/categories/nudeln-reis-getreide",
  "https://consumer-api.goflink.com/v2/categories/hotfood-by-circus",
  "https://consumer-api.goflink.com/v2/categories/frisch-fertig",
  "https://consumer-api.goflink.com/v2/categories/vegan-vegetarisch",
  "https://consumer-api.goflink.com/v2/categories/fleisch-fisch",
  "https://consumer-api.goflink.com/v2/categories/grillen",
  "https://consumer-api.goflink.com/v2/categories/backwaren",
  "https://consumer-api.goflink.com/v2/categories/eier-milch",
  "https://consumer-api.goflink.com/v2/categories/joghurt-desserts",
  "https://consumer-api.goflink.com/v2/categories/kaese",
  "https://consumer-api.goflink.com/v2/categories/wurst-aufschnitt",
  "https://consumer-api.goflink.com/v2/categories/alkoholfreie-getraenke",
  "https://consumer-api.goflink.com/v2/categories/bier",
  "https://consumer-api.goflink.com/v2/categories/wein-sekt",
  "https://consumer-api.goflink.com/v2/categories/spirituosen-mehr",
  "https://consumer-api.goflink.com/v2/categories/suesse-snacks",
  "https://consumer-api.goflink.com/v2/categories/salzige-snacks",
  "https://consumer-api.goflink.com/v2/categories/tiefkuehl",
  "https://consumer-api.goflink.com/v2/categories/eis",
  "https://consumer-api.goflink.com/v2/categories/dauerguenstig",
  "https://consumer-api.goflink.com/v2/categories/konserven-fertiggerichte",
  "https://consumer-api.goflink.com/v2/categories/aufstriche-cerealien",
  "https://consumer-api.goflink.com/v2/categories/saucen-oele-gewuerze",
  "https://consumer-api.goflink.com/v2/categories/kaffee-tee-kakao",
  "https://consumer-api.goflink.com/v2/categories/backen-dessert",
  "https://consumer-api.goflink.com/v2/categories/internationale-kueche",
  "https://consumer-api.goflink.com/v2/categories/drogerie-hygiene",
  "https://consumer-api.goflink.com/v2/categories/kosmetik",
  "https://consumer-api.goflink.com/v2/categories/haushalt-technik",
  "https://consumer-api.goflink.com/v2/categories/baby-titel",
  "https://consumer-api.goflink.com/v2/categories/katze-hund",
  "https://consumer-api.goflink.com/v2/categories/fitness",
]      


#Alle Produkte laden
#Datalist = AllProductsAPI(links)
#Produkte in eine Excel speichern
#SafeProducts(Datalist)
#Nach einem Produkt Suchen
#datas = exceltodict()
#Searchitem("Balsamico")

