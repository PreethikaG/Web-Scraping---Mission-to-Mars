from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars 

app = Flask(__name__)

# Establish Mongo db connection with db(mars_db) and collection(mars_collection)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_collection

#Index route 
@app.route("/")
def index():
    mars = collection.find_one()
    return render_template("index.html", mars = mars)

#Scrape route that calls the master function scrape_data from the Python file scrape_mars
@app.route("/scrape")
def scrape():
    
    mars_data_scrape = scrape_mars.scrape_data()
    collection.update({}, mars_data_scrape, upsert=True)
    return redirect("/")

#Route to clear data on webpage and to delete data in db
@app.route('/clear')
def clear():
    collection.remove()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
