from flask import Flask, redirect, url_for, render_template, request
import validators
import requests
import sys
from bs4 import BeautifulSoup
import re
import os
from pathlib import Path
from random import randint

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
        if checkValidURL(url) == False:
            text+="*< Invlid URL >*\n"
        if check_wiki == False:
            text+="*< not a wekipedia URL >*\n"
        text+="\n"

    return text


def firstWord(text):
    strr = ""
    textList = text.split()
    strr +="*< The first word of the text is: "
    strr +=textList[0]
    strr +=" *>\n"
    return strr

def wordCount(text):
    strr = ""
    textList = text.split()
    strr +="*< Total word: "
    strr +=str(len(textList))
    strr +=" *>\n"
    return strr
    
def grabText(soup,text,services):
    buffer = ""
    for paragraph in soup.find_all('p'):
        if paragraph.text != '\n' and len(paragraph.text) > 100:
            buffer = paragraph.text
            buffer += "\n"
            break
    buffer = re.sub(r'\[.*?\]+', '', buffer)
    
    if services[0] == True: text += firstWord(buffer)
    if services[1] == True: text += wordCount(buffer)
    text += buffer
    
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
    if outputType == "output-save-file": return writeToFile(text)
    if outputType == "output-both": 
        writeToFile(text)
        return text

def scrapePics(outputType,pics):
    if outputType == "output-on-screen": return pics
    if outputType == "output-save-file": return writeToFile(pics)
    if outputType == "output-both": 
        writeToFile(pics)
        return pics

def scrapeBoth(outputType,textPics):

    if outputType == "output-on-screen": return textPics
    if outputType == "output-save-file": return writeToFile(textPics)
    if outputType == "output-both": 
        writeToFile(textPics)
        return textPics

