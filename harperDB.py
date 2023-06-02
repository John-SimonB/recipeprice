import harperdb
import uuid

url = "https://db-recipeprice.harperdbcloud.com"
username = "admin"
passwort = "1305!"

db = harperdb.HarperDB(
    url = url,
    username= username,
    password = passwort
)

SCHEMA = "products"
TABLE = "items"

def insert_item(item):
    print(str(item) + " wurde hinzugefügt") 
    return db.insert(SCHEMA, TABLE, [item])

def delete_item(item_id):
    print(item_id + " wurde gelöscht")
    return db.delete(SCHEMA, TABLE, [item_id])

def get_all_item():
    print("Alle Daten geladen")
    return db.sql(f"select * from {SCHEMA}.{TABLE}")
    

def delete_all_items():
    items = get_all_item()
    for item in items:
        value = item["id"]
        delete_item(value)
    print("Alle Daten gelöscht")    
    return True


data = {
    "id": str(uuid.uuid4()),
    "title": "sdfasf32323232",
    "special_price": "123",
    "normal_price": "2222",
    "link": "https/ss",
    "package": "10 KG"
}

#insert_item(data)
#get_all_item()
#delete_item("d8fd9b71-c9bc-4425-9eb5-7f488bb636df")
#delete_all_items()