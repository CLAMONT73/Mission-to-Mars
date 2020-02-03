from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Setup Flask.
app = Flask(__name__)

# Tell Python to connect to Mongo using PyMongo.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Setup app routes: 1. Define route for HTML page.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Setup app routes: 2. Set up scraping route.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scrape_mars.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Tell Flask to run the code.
if __name__ == "__main__":
    app.run()