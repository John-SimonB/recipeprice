from flask import Flask, redirect, url_for, render_template, request
from test import exceltodict,fuzzy_search
from search_optimierung import search_words
from fuzzywuzzy import fuzz
from collections import defaultdict
from Chefkoch_Scrape import chefkoch_scrape


def createApp(secretKey):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secretKey
    return app

app = createApp('REZEPTE')


products = exceltodict()
selected_products = []  # Liste für ausgewählte Produkte


@app.route("/", methods=["POST", "GET"])  # Pfade der Webpage
def home():
    global selected_products

    if request.method == 'POST':
        query = request.form.get('query')
        category = request.form.get('category')
        action = request.form.get('action')  # Neu: Aktion (hinzufügen/entfernen)
        product_name = request.form.get('product_name')  # Neu: Name des ausgewählten Produkts
        link = request.form.get('console_link')  # Neu: Link aus dem Formular erhalten
    else:
        query = request.args.get('query')
        category = request.args.get('category')
        action = request.args.get('action')
        product_name = request.args.get('product_name')
        link = request.form.get('console_link')  # Neu: Link aus dem Formular erhalten

    if link:
        print(link)
        print("")
        recipelist = chefkoch_scrape(link)
        print(recipelist)

    if query:
        for original, replacement in search_words:
            query = query.lower().replace(original.lower(), replacement.lower())
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

    if action == 'add':  # Neu: Produkt zur ausgewählten Liste hinzufügen
        selected_product = next((product for product in products if product['name'] == product_name), None)
        if selected_product:
            selected_products.append(selected_product)
    elif action == 'remove':  # Neu: Produkt aus der ausgewählten Liste entfernen
        selected_products = [product for product in selected_products if product['name'] != product_name]

    total_price = sum(product['price'] for product in selected_products)  # Gesamtpreis berechnen

    return render_template('home.html', products=results, selected_products=selected_products, total_price=total_price, message=message)





if __name__ == '__main__':
    app.run(debug=True) 