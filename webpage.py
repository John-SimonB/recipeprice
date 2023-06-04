from flask import Flask, redirect, url_for, render_template, request
import harperdb


def createApp(secretKey):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secretKey
    return app

app = createApp('REZEPTE')


title= ("Name", "role", "sss")
data = (
    ("rolf", "212", "zaisd"),
    ("asda", "sadua", "2929292")
)

db = harperdb.HarperDB(
    url = "https://db-recipeprice.harperdbcloud.com",
    username= "admin",
    password = "1305!"
)

@app.route("/", methods=["POST", "GET"])  # Pfade der Webpage
def home():
    data2 = db.sql(f"select * from products.items")

    #data2 = ("asdasda","asdda")

    # Daten an das Template übergeben
    return render_template('home.html', data=data, data2=data2)

if __name__ == '__main__':
    app.run(debug=True) 