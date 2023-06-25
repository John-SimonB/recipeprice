from fuzzywuzzy import fuzz
import pandas as pd
from search_optimierung import search_words

def fuzzy_search(data, search_term, kategorie="", threshold=80):
    if kategorie.lower() == "tk":
        kategorie = "tiefkuehl"
    elif kategorie.lower() == "nudeln":
        kategorie = "nudeln-reis-getreide"


    results = []
    partial = []
    token = []
    best_match = None
    best_distance = float('inf')
    for item in data:
        name = item['name']
        similarity = fuzz.partial_token_set_ratio(name.lower(), search_term.lower())
        if(similarity > 70): 
            partial.append(name)
        similarity = fuzz.token_set_ratio(name.lower(), search_term.lower())
        if(similarity > 70): 
            token.append(name)
        if similarity >= threshold:
            if item["kategorie"] == kategorie.lower() or kategorie.lower() == "":
                new_product = {"name": name, "price" : item["price"], "menge" : item["menge"], "einheit" : item["einheit"], "icon" : item["icon"]} 
                results.append(new_product)
    if len(results) >= 1:
        return results
    else:
        # Führe eine zweite Suche mit threshold=60 durch
        #for item in data:
        #    name = item['name']
        #    similarity = fuzz.token_set_ratio(name.lower(), search_term.lower())
        #    if similarity >= 60:
        #        if item["kategorie"] == kategorie.lower() or kategorie.lower() == "":
        #            results.append((name, similarity))
#
        #if len(results) >= 1:
        #    results.sort(key=lambda x: x[1], reverse=True)
        #    return results
        #else:
            return False

# Daten
def exceltodict():
  df = pd.read_excel('Data.xlsx')
  data = []
  for index, row in df.iterrows():
    item = {
      "name" : row["name"],
      "price" : row['price'],
      "menge" : row['menge'],
      "einheit" : row['einheit'],
      "icon" : row['icon'],
      "kategorie" : row["kategorie"]
      }
    data.append(item)
  return data

data = exceltodict()

# Suchbegrif
#print(data)
# Durchführung der Fuzzy-Suche
#suche = fuzzy_search(data, 'Balsamico', "")

