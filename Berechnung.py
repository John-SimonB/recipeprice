from recpiescrape_chefkoch import chefkoch_scrape
from scraper import get_all_item

def calculate_recipe_cost(zutaten, preise):
    total_cost = 0
    
    for zutat in zutaten:
        for zutat_name, zutat_info in zutat.items():
            menge = float(zutat_info['menge_wert'])
            einheit = zutat_info['menge_einheit']
            
            for produkt in preise:
                if produkt['title'] == zutat_name:
                    preis = float(produkt['normal_price'].replace(',', '.'))
                    package_size = float(produkt['package'].split()[0])
                    
                    if einheit == 'g':
                        total_cost += (preis / package_size) * menge
                    elif einheit == 'ml':
                        total_cost += (preis / package_size) * menge
                    elif einheit == 'kg':
                        total_cost += (preis / package_size) * menge
                    break
    
    return total_cost

zutaten = [{'Mehl': {'menge_wert': '500', 'menge_einheit': 'g'}, 'Hefe frische': {'menge_wert': '4', 'menge_einheit': 'g'}}]


recipe_cost = calculate_recipe_cost(zutaten, get_all_item())
print("Gesamtpreis des Rezepts: " + str(recipe_cost) + "€")