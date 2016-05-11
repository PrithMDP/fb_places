# Script to find all places a users friends have checked-in at on facebook
#
import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from sets import Set

import time
#import pwd from things.json
pwd = ""
with open('things.json') as json_data:
    d = json.load(json_data)
    pwd = d["password"]
#pwd set

# Set of friends
friend_urls = Set([])

# dictionary for places (Check-ins)
places = {}

driver = webdriver.PhantomJS()

driver.get("http://www.facebook.org")

# test user
elem = driver.find_element_by_id("email")
elem.send_keys("pythontestforme@gmail.com")
elem = driver.find_element_by_id("pass")
# set pwd here
elem.send_keys(pwd)

#go to profile page for user
driver.get("http://www.facebook.com/profile.php")


#go to friends
friend_path = driver.current_url+"?sk=friends&source_ref=pb_friends_tl" # works for now but need something concrete
driver.get(friend_path)

 # run for 12 seconds to get to bottom of window and load all friends, need to make this concrete
t_end = time.time() + 60 * .2
while time.time() < t_end:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# make beautiful soup from page source
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

# find all friends
for link in soup.find_all('li', {'class':"_698"}):
    f_url =  str(link)
    
    start = f_url.find("https://www.facebook.com/")
    end = f_url.find("?fref=pb&amp;hc_location=friends_tab")
    
    print f_url[start:end]
    friend_urls.add(f_url[start:end]+"/map") # adding /map endpoint to url and then adding to set

print "Printing friend list"
print friend_urls

# obtain check-ins for all friends
for url in friend_urls:
    driver.get(url)
    
    t_end = time.time() + 60 * .1 # run for 6 seconds to load all/most check ins
    while time.time() < t_end:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    for link1 in soup.find('div', {'class':"_3i9"}):
        for link2 in link1.find('ul', {'class':"uiList _620 _14b9 _509- _4ki"}):
            for div_link in link2.findAll('div', {'class':"_3owb"}):
                #print div_link.find('a')['href']
                place_url = div_link.find('a')['href']
                print place_url
                if place_url in places:
                    places[place_url] +=1
                else:
                    places[place_url]= 1





print places


############################################################################################################
