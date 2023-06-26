from flask import Flask, redirect, url_for, render_template, request
from LoadData import exceltodict,fuzzy_search
from search_optimierung import search_words, skip_words
from fuzzywuzzy import fuzz
from collections import defaultdict
from Chefkoch_Scrape import chefkoch_scrape
from Berechnung import calculate_price, convert_quantity

def createApp(secretKey):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secretKey
    return app

app = createApp('REZEPTE')


products = exceltodict()
selected_products = []  # Liste für ausgewählte Produkte
current_recipe_index = 0  # Index für das aktuelle Rezept
recipelist = []

@app.route("/", methods=["POST", "GET"])  # Pfade der Webpage
def home():
    
    global selected_products
    global current_recipe_index
    default_query = ""
    info = None
    if request.method == 'POST':
        query = request.form.get('query')
        category = request.form.get('category')
        action = request.form.get('action')  # Neu: Aktion (hinzufügen/entfernen)
        product_name = request.form.get('product_name')  # Neu: Name des ausgewählten Produkts
        link = request.form.get('console_link') 
        if action == 'weiter':  # Neu: Überprüfen, ob der Benutzer auf den Button "weiter" geklickt hat
            current_recipe_index += 1  # Index für das nächste Rezept erhöhen
    else:
        query = request.args.get('query')
        category = request.args.get('category')
        action = request.args.get('action')
        product_name = request.args.get('product_name')
        link = request.args.get('console_link')  # Neu: Link aus dem Formular erhalten

    if link:
        recipelist.clear()
        selected_products.clear()
        current_recipe_index = 0
        recipelist.append(chefkoch_scrape(link))
        if(recipelist is not None):
            for original, replacement in search_words:
                query = recipelist[0][1][0]
            fuzzy_results = []
            for product in products:
                product_name = product['name'].lower()
                ratio = fuzz.ratio(query, product_name)
                if ratio >= 70:
                    fuzzy_results.append(product)
            normal_results = [product for product in products if query in product['name'].lower()]

            if category:  # Neue Bedingung: Nur nach Kategorie filtern, wenn eine Kategorie angegeben ist
                fuzzy_results = [product for product in fuzzy_results if product['kategorie'] == category]
                normal_results = [product for product in normal_results if product['kategorie'] == category]

            results = fuzzy_results + normal_results
            unique_results = defaultdict(list)
            for product in results:
                unique_results[(product['name'], product['kategorie'])].append(product)
            results = [product for sublist in unique_results.values() for product in sublist]
            results = results[:20]

            if len(results) == 0:
                message = 'Produkt nicht gefunden'
            else:
                message = None
        else:
            if category:  # Neue Bedingung: Nur Produkte der angegebenen Kategorie anzeigen
                results = [product for product in products if product['kategorie'] == category]
            else:
                results = products[:50]
            message = None
    if action == "clear":
        recipelist.clear()
        selected_products.clear()

    if action == "weiter":
        if(recipelist is not None):
            for original, replacement in search_words:
                if current_recipe_index < len(recipelist[0]):
                    query = recipelist[0][current_recipe_index][0]
                else:
                    query = ""
            fuzzy_results = []
            for product in products:
                product_name = product['name'].lower()
                ratio = fuzz.ratio(query, product_name)
                if ratio >= 70:
                    fuzzy_results.append(product)
            normal_results = [product for product in products if query in product['name'].lower()]

            if category:  # Neue Bedingung: Nur nach Kategorie filtern, wenn eine Kategorie angegeben ist
                fuzzy_results = [product for product in fuzzy_results if product['kategorie'] == category]
                normal_results = [product for product in normal_results if product['kategorie'] == category]

            results = fuzzy_results + normal_results
            unique_results = defaultdict(list)
            for product in results:
                unique_results[(product['name'], product['kategorie'])].append(product)
            results = [product for sublist in unique_results.values() for product in sublist]
            results = results[:20]

            if len(results) == 0:
                message = 'Produkt nicht gefunden'
            else:
                message = None
        else:
            if category:  # Neue Bedingung: Nur Produkte der angegebenen Kategorie anzeigen
                results = [product for product in products if product['kategorie'] == category]
            else:
                results = products[:50]
            message = None 
       
        
    if query:
        if ' ' in query:
            query_words = query.split()  # Teile die Query in einzelne Wörter auf
            results = []  # Ergebnisliste initialisieren
            default_query = query
            for word in query_words:
                replaced_word = word.lower()  # Standardmäßig das Wort in Kleinbuchstaben
                
                if word.isdigit():
                    continue

                if replaced_word in skip_words:
                    continue

                for original, replacement in search_words:
                    if word.lower() == original.lower():  # Überprüfe, ob das Wort ersetzt werden muss
                        replaced_word = replacement.lower()
                        break
                
                fuzzy_results = []
                for product in products:
                    product_name = product['name'].lower()
                    ratio = fuzz.ratio(replaced_word, product_name)
                    if ratio >= 60:
                        fuzzy_results.append(product)
                
                normal_results = [product for product in products if replaced_word in product['name'].lower()]

                if category:
                    fuzzy_results = [product for product in fuzzy_results if product['kategorie'] == category]
                    normal_results = [product for product in normal_results if product['kategorie'] == category]

                results.extend(fuzzy_results + normal_results)
            
            # Entferne Duplikate aus den Ergebnissen
            unique_results = defaultdict(list)
            for product in results:
                unique_results[(product['name'], product['kategorie'])].append(product)
            results = [product for sublist in unique_results.values() for product in sublist]
            results = results[:600]

            if len(results) == 0:
                message = 'Produkt nicht gefunden'
            else:
                message = None
        else:
            for original, replacement in search_words:
                query = query.lower().replace(original.lower(), replacement.lower())
                default_query = query
            fuzzy_results = []
            for product in products:
                product_name = product['name'].lower()
                ratio = fuzz.ratio(query, product_name)
                if ratio >= 80:
                    fuzzy_results.append(product)
            normal_results = [product for product in products if query in product['name'].lower()]

            if category:  # Neue Bedingung: Nur nach Kategorie filtern, wenn eine Kategorie angegeben ist
                fuzzy_results = [product for product in fuzzy_results if product['kategorie'] == category]
                normal_results = [product for product in normal_results if product['kategorie'] == category]

            results = fuzzy_results + normal_results
            unique_results = defaultdict(list)
            for product in results:
                unique_results[(product['name'], product['kategorie'])].append(product)
            results = [product for sublist in unique_results.values() for product in sublist]
            results = results[:50]

            if len(results) == 0:
                message = 'Produkt nicht gefunden'
            else:
                message = None
    else:
        if category:  # Neue Bedingung: Nur Produkte der angegebenen Kategorie anzeigen
            results = [product for product in products if product['kategorie'] == category]
        else:
            results = products[:500]
        message = None

    # button zum löschen des rezeptes einfügen
    if action == 'add':  # Neu: Produkt zur ausgewählten Liste hinzufügen
        selected_product = next((product for product in products if product['name'] == product_name), None) 
        if(recipelist):             
            if(recipelist[0][current_recipe_index][2] == "X"):
                info = "Das eingetragen Rezept enthält Zutaten mit ungenauen Mengenangaben. Der Preis kann nicht genau berechnet werden"

            total_price = calculate_price(recipelist[0][current_recipe_index], selected_product)
            data = {
                "name": selected_product["name"],
                "price": round(total_price[0],2),
                "menge": recipelist[0][current_recipe_index][1],
                "einheit": recipelist[0][current_recipe_index][2],
                "icon": selected_product["icon"],
                 "kategorie": selected_product["kategorie"]
            }
            selected_products.append(data)
        else: 
            if selected_product:
                info = None
                print(selected_product)
                selected_products.append(selected_product)
    elif action == 'remove':  # Neu: Produkt aus der ausgewählten Liste entfernen
        selected_products = [product for product in selected_products if product['name'] != product_name]

    total_price = round(sum(product['price'] for product in selected_products),2) # Gesamtpreis berechnen

    # Aktuelles Rezept abrufen
    if current_recipe_index < len(recipelist):
        current_recipe = recipelist[current_recipe_index]
    else:
        current_recipe = None
    return render_template('home.html', info=info, query=query, products=results, default_query=default_query, selected_products=selected_products, total_price=total_price, message=message, recipelist=recipelist, current_recipe=current_recipe)




if __name__ == '__main__':
    app.run(debug=False) 