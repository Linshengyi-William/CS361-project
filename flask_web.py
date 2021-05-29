# partial code was inspired here: 
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b
from flask import Flask, redirect, url_for, render_template, request

import os
import helper
from pathlib import Path
from random import randint
import validators
import requests
import sys
from bs4 import BeautifulSoup
import re



app = Flask(__name__)
@app.route("/", methods=["POST", "GET"])
def home():
    #displayScreenValue = None
    if request.method == "POST":
        url = request.form["inp_url"]
        scrapeType = request.form["scrape_type"]
        outputType = request.form["outputType"]
        screenValue = scraper(url, scrapeType, outputType)
        #print(screenValue)
        #response
        return render_template("index.html", displayScreenValue=screenValue)
    else:
        return render_template("index.html", displayScreenValue="")

    

@app.route("/<name>")
def user(name):
    return render_template("index.html",content = name)

    #return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))


def scraper(input_url,scrapeType,outputType):
    
    text = ""  
    pics = "" 
    right_url = helper.setURL(input_url)

    text += helper.checkValidWikiURL(input_url)

    response = requests.get(url=right_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    text = helper.grabText(soup, text)
    pics = helper.grabPics(soup, pics)
    textPics = text + pics

    if scrapeType == "scrape-text": return helper.scrapeText(outputType, text)
    if scrapeType == "scrape-picture": return helper.scrapePics(outputType, pics)
    if scrapeType == "scrape-both": return helper.scrapeText(outputType, textPics)

        
def writeToFile(pathname,content):
    filename = "scraper"+str(randint(0,10000))+".txt"
    path = os.path.join(pathname, filename)
    f = open(path,"w+")
    f.writelines(content)
    f.close() 

if __name__ == "__main__":
    app.run(debug = True)
    #app.run()