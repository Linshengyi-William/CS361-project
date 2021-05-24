# partial code was inspired here: 
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b
from flask import Flask, redirect, url_for, render_template, request

import os
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
    
    homename =  str(Path.home())
    desktop = homename + "/Desktop"
    print(desktop)

    default_url = "https://en.wikipedia.org/wiki/Web_scraping"
    check_wiki = "wikipedia.org" in input_url
    check_validurl = validators.url(input_url)
    if check_validurl != True:
        check_validurl = False
    print("The url you entered: ")
    print(input_url)

    text = ""
    allImages =""
    if check_wiki == False or check_validurl == False:
        text+="*< The URL can't be used as the targeted URL. The scraper will use the default URL as the targeted URL >*\n"
        text+="*< Reason:  >*\n"
        if check_validurl == False:
            text+="*< Invlid URL >*\n"
            print("invalid URL")
        if check_wiki == False:
            text+="*< not a wekipedia URL >*\n"
            print("not a wekipedia URL")
            right_url = default_url
        text+="\n"
    else: 
        print("is a valid wikipedia URL.")
        right_url = input_url


    response = requests.get(url=right_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for paragraph in soup.find_all('p'):
        if paragraph.text != '\n' and len(paragraph.text) > 100:
            text += paragraph.text
            text += "\n"
            break
    text = re.sub(r'\[.*?\]+', '', text)
    images = soup.find_all('img', {'src':re.compile('.jpg')})
    textImages = text
    for image in images: 
        textImages += image['src']+ '\n'
        allImages+= (image['src']+'\n')
    if(scrapeType == "scrape-text" or scrapeType == "scrape-both"):  
        if outputType == "output-on-screen" or outputType == "output-both":
            if outputType == "output-both":
                if scrapeType == "scrape-text":
                    writeToFile(desktop, text)
                    return text
                writeToFile(desktop, textImages)
                return textImages
                
            if scrapeType == "scrape-text":
                return text
            return textImages
        else:
            if scrapeType == "scrape-text":
                writeToFile(desktop, text)
            else:
                writeToFile(desktop, textImages)


    else:
        if outputType == "output-on-screen" or outputType == "output-both":
            if outputType == "output-both":
                writeToFile(desktop, allImages)
            return allImages
        else:
                writeToFile(desktop, allImages)

        
def writeToFile(pathname,content):
    filename = "scraper"+str(randint(0,10000))+".txt"
    path = os.path.join(pathname, filename)
    f = open(path,"w+")
    f.writelines(content)
    f.close() 

if __name__ == "__main__":
    app.run(debug = True)
    #app.run()