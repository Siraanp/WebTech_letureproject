from flask import Flask,render_template,request,redirect
from urllib.parse import quote
from urllib.request import urlopen
import json
import requests
import urllib.parse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db,info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Dev_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Game_URL ="https://www.cheapshark.com/api/1.0/deals"

NEWS_URL ="http://newsapi.org/v2/everything?q=videogame&from={YMD}}&sortBy=publishedAt&apiKey=3f9a09e2092a46febac3ba21fef17969"
YMD = datetime.today().strftime('%Y-%m-%d')

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/")
def home():
    game=Game()
    return render_template("home.html",game=game)

def Game():
    
    url ="https://www.cheapshark.com/api/1.0/deals"
    store_url ="https://www.cheapshark.com/api/1.0/stores"
    response2 = requests.request("GET", store_url)
    R = response2.json()
    response = requests.request("GET", url)
    r = response.json()
    show = []
    for x in range(len(R)) :
        name = r[x]['title']
        normalPrice = r[x]['normalPrice']
        salePrice = r[x]['salePrice']
        savings = round(float(r[x]['savings']),2)
        thumb = r[x]['thumb']
        storeID = r[x]['storeID']
        dealID = r[x]['dealID']

        show.append({"title":name,"normalPrice":normalPrice,"salePrice":salePrice,"savings":savings,"thumb":thumb,"storeID":storeID,"dealID":dealID})
    
    return show 

@app.route("/search")
def search():
    findGame = find_game()
    return render_template('search.html',findGame=findGame)

def find_game():
    find_url = "https://www.cheapshark.com/api/1.0/games?title={0}&limit=60&exact=0"
    word = request.args.get('word')
    url = find_url.format(word)
    data = urlopen(url).read()
    r = json.loads(data)
    show = []
    for x in range(len(r)) :
        name = r[x]['external']
        thumb = r[x]['thumb']
        steamAppID = r[x]['steamAppID']
        cheapest = r[x]['cheapest']
        cheapestDealID = r[x]['cheapestDealID']
        show.append({"external":name,"thumb":thumb,"steamAppID":steamAppID,"cheapest":cheapest,"cheapestDealID":cheapestDealID})
    return show

NEWS_URL = "http://newsapi.org/v2/everything?q={0}&from=2021-3-11&sortBy=publishedAt&apiKey={1}"

NEWS_KEY = "125abe47c9fb4dccb9241c39c7f1abeb" 

@app.route('/news')
def news():
    word = request.args.get('word')
    if not word:
        word = 'game+steam'
   
    news = get_news(word, NEWS_KEY)
    return render_template('news.html',news=news)

def get_news(word,NEWS_KEY):
    word = convert_to_unicode(word)
    url = NEWS_URL.format(word, NEWS_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = []
    
    for i in range(len(parsed['articles'])):
        title = parsed['articles'][i]['title']
        description = parsed['articles'][i]['description']
        img = parsed['articles'][i]['urlToImage']
        link = parsed['articles'][i]['url']
        news.append({"title":title,"description":description,"link":link,"img":img})
    
    return news

def convert_to_unicode(txt):
    encode = urllib.parse.quote(txt)
    return encode

@app.route('/about')
def about():
    return render_template('aboutUS.html',Dev_info = info.query.all())

@app.route("/stored")
def stored_page():
    stored=Stored()
    return render_template("stored.html",stored=stored)

def Stored():
    store_url ="https://www.cheapshark.com/api/1.0/stores"
    response = requests.request("GET", store_url)
    r = response.json()
    show = []
    for x in range(len(r)) :
        storeID = r[x]['storeID']
        storeName = r[x]['storeName']
        
        show.append({"storeID":storeID,"storeName":storeName})
    
    return show

app.run(debug=True,use_reloader=True)