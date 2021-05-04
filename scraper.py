# partial code was inspired here: 
# https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b

import validators
import requests
import sys
from bs4 import BeautifulSoup
import re
#from selenium import webdriver
#from BeautifulSoup import BeautifulSoup
#import pandas as pd

sys.tracebacklimit=0

default_url = "https://en.wikipedia.org/wiki/Web_scraping"
inp_url = raw_input("URL: ")
check_wiki = "wikipedia.org" in inp_url
#print("check_wiki is: ",check_wiki)
check_validurl = validators.url(inp_url)
if check_validurl != True:
    check_validurl = False
#print("check_validurl is: ", check_validurl)
print("The url you entered: ")
print(inp_url)
if check_wiki == False or check_validurl == False:
    print("is not a valid wikipedia URL.")
    print("Possible reason: ")
    if check_validurl == False:
        print("invalid URL")
    if check_wiki == False:
        print("not a wekipedia URL")
    right_url = default_url
else: 
    print("is a valid wikipedia URL.")
    right_url = inp_url
   
response = requests.get(url=right_url)
print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')

text = ""
for paragraph in soup.find_all('p'):
    #for i in range(0,10):
    #    print("->",paragraph.text[i],"<-")
    if paragraph.text != '\n' and len(paragraph.text) > 20:
        text += paragraph.text
        text += "\n"
        break
text = re.sub(r'\[.*?\]+', '', text)
#text = text.replace('\n', '')

images = soup.find_all('img', {'src':re.compile('.jpg')})
for image in images: 
    print(image['src']+'\n')


inp_output=input("how do you want to output the text?\n 1. Display on the screen \n 2. Output to a csv file \n 3. Both")
if inp_output == 2 or inp_output == 3:
    if inp_output == 3:
        print(text)
    inp_filename = str(raw_input("What's going to be the file name?(Please don't enter '.csv' at the end): "))
    print("inp_filename is: ",inp_filename)
    print("inp_filename type is: ",type(inp_filename))
    filename = inp_filename +".csv"
    print("filename is: ",filename)
    f = open(inp_filename,"w+")
    f.write(text) #Give your csv text here.
    ## Python will convert \n to os.linesep
    f.close()
else:
    print(text)
#content = soup.find('div',id="bodyContent").p
#data = str(content)
#print(data)

#data = re.sub("\(.*?\)","<>",data)
#data.replace("<b>",'')
#data.replace("</b>",'')

#print(data)
#firstParagragh = soup.find(id="bodyContent").findall("p")
#print(firstParagragh)

