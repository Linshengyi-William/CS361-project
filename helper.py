from flask import Flask, redirect, url_for, render_template, request
import validators
import requests
import sys
from bs4 import BeautifulSoup
import re
import os

# check if the parameter url is a valid wiki url, 
# then return default url or oreginal url

def checkValidURL(url):
    check_validurl = validators.url(url)
    if check_validurl != True:
        return False
    return True

def setURL(url):
    check_wiki = "wikipedia.org" in url
    if check_wiki == False or checkValidURL(url) == False:
        return "https://en.wikipedia.org/wiki/Web_scraping"
    return url

def checkValidWikiURL(url):
    text = ""
    check_wiki = "wikipedia.org" in url
    
    if check_wiki == False or checkValidURL(url) == False:
        text+="*< The URL can't be used as the targeted URL. The scraper will use the default URL as the targeted URL >*\n"
        text+="*< Reason:  >*\n"
        if check_validurl == False:
            text+="*< Invlid URL >*\n"
        if check_wiki == False:
            text+="*< not a wekipedia URL >*\n"
        text+="\n"

    return text

def grabText(soup,text):
    for paragraph in soup.find_all('p'):
        if paragraph.text != '\n' and len(paragraph.text) > 100:
            text += paragraph.text
            text += "\n"
            break
    text = re.sub(r'\[.*?\]+', '', text)
    return text

def grabPics(soup,imageBuffer):
    pics = soup.find_all('img', {'src':re.compile('.jpg')})
    for image in pics: 
        imageBuffer+= (image['src']+'\n')
    return imageBuffer


    

def writeToFile(content):
    desktop =  str(Path.home()) + "/Desktop"
    filename = "scraper"+str(randint(0,10000))+".txt"
    path = os.path.join(desktop, filename)
    f = open(path,"w+")
    f.writelines(content)
    f.close() 

def scrapeText(outputType,text):
    if outputType == "output-on-screen": return text
    if outputType == "output-save-file": return text
    if outputType == "output-both": 
        writeToFile(text)
        return text

def scrapePics(outputType,pics):
    if outputType == "output-on-screen": return pics
    if outputType == "output-save-file": return pics
    if outputType == "output-both": 
        writeToFile(pics)
        return pics

def scrapeBoth(outputType,textPics):

    if outputType == "output-on-screen": return textPics
    if outputType == "output-save-file": return textPics
    if outputType == "output-both": 
        writeToFile(textPics)
        return textPics

