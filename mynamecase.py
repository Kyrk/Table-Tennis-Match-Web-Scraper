#!/usr/bin/env python3
'''
Python script that scrapes all Liga Pro table tennis match results of a
specified day from a website that aggregates table tennis matches.

External libraries to install:
    requests (pip install requests)
    BeautifulSoup (pip install beautifulsoup4)
    selenium (pip install selenium)

Running program:
    python mynamecase.py
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import selenium
import pandas as pd

#TODO: Write function for clicking ad and collapse buttons
def clickButtons(driver, xpath, xpath2):
    '''Function that clicks button to show all Liga Pro matches as well as
    close buttons on ads that would otherwise block/intercept the click
    request.'''
    #TODO: Get buttons to work I guess lol
    poppath = '/html/body/div[2]/div[5]/div/div[2]/div/div/button'
    pop_close = driver.find_element_by_xpath(poppath)
    pop_close.click()

    adpath = '/html/body/div[2]/div[2]/div[6]/button'
    ad_close = driver.find_element_by_xpath(adpath)

#TODO: Write function to process data
def getData(data):
    '''Function that processes scraped data and stores values into different
    lists.'''
    # Lists to store values of collected data
    p1 = []         # First players of each match
    p2 = []         # Second players of each match
    result1 = []    # Game results of player 1
    result2 = []    # Game results of player 2
    score1 = []     # Combined score of player 1
    score2 = []     # Combined score of player 2
    point_diff = [] # Difference between player's scores

    for a in data.findAll():
        print('hi')

# Initialize WebDriver
#chrome_options = Options()
#chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
#        options=chrome_options)
#driver = webdriver.Chrome()
#driver.create_options()

URL = "https://scores24.live/en/table-tennis/2021-07-16"
page = requests.get(URL)    # Get response from target page
driver.implicitly_wait(5)  # Wait 10 seconds to do stuff so page maybe loads
driver.get(URL)             # Direct WebDriver to URL

# Lists to store values of collected data
p1 = []         # First players of each match
p2 = []         # Second players of each match
result1 = []    # Game results of player 1
result2 = []    # Game results of player 2
score1 = []     # Combined score of player 1
score2 = []     # Combined score of player 2
point_diff = [] # Difference between player's scores

# Create BeautifulSoup object by parsing HTML of page source
html = BeautifulSoup(page.content, 'html.parser')

# Get all instances of leagueWrappers in HTML
leagueWrappers = html.find_all('div', {'data-test':'leagueWrapper'})

# Determine xpath by finding leagueWrapper containing Liga Pro matches
print('Obtaining xpath for show button...')
for div, leagueWrapper in enumerate(leagueWrappers):
    if 'Liga Pro' in str(leagueWrapper):
        xpath = '''/html/body/div[2]/div[2]/div[4]/div[2]/div/div[2]/
        div[5]/div[{}]/div[1]/button'''.format(div + 1)
        xpath2 = '''/html/body/div[2]/div[2]/div[4]/div[2]/div/div[2]/
        div[5]/div[{}]/div[1]/button'''.format(div + 2)

# Click away popups that prevent show button from being interacted with
# Ad covering page
adpath = '/html/body/div[2]/div[5]/div/div[2]/div/div/button'
ad_close = driver.find_element_by_xpath(adpath)
ad_close.click()
# Move browser to activate second ad
driver.execute_script('window.scrollTo(0, 100)')
# Ad block at bottom
adpath2 = '/html/body/div[2]/div[2]/div[6]/button'
ad_close = driver.find_element_by_xpath(adpath2)
ad_close.click()

# Locate correct collapse button using xpath
try:
    print('Searching for show button...')
    show_button = driver.find_element_by_xpath(xpath)
except selenium.common.exceptions.NoSuchElementException:
    # Try variation of xpath if original doesn't work
    print('Xpath for show button not accessible. Using alternative xpath...')
    show_button = driver.find_element_by_xpath(xpath2)

# Click button
print('Clicking show button for Liga Pro matches...')
show_button.click()

# Parse HTML of driver-modified page source
print('Parsing HTML of modified page...')
newhtml = BeautifulSoup(driver.page_source, 'html.parser')

# Get new instances of leagueWrappers
leagueWrappers = newhtml.find_all('div', {'data-test':'leagueWrapper'})

# Get code block of leagueWrapper with Liga Pro matches
print('Fetching Liga Pro matches...')
for leagueWrapper in leagueWrappers:
    if 'Liga Pro' in str(leagueWrapper):
        #print(result.prettify())
        ligaPro = BeautifulSoup(str(leagueWrapper), 'html.parser')
        matches = ligaPro.find_all(class_='sc-10gv6xe-0 cdEgTT __CommonRowTennis')
        matchCount = len(matches)
        for match in matches:
            players = match.findAll('div',attrs={'class':'_3OUew'})
            results = match.findAll('div',attrs={'class':'_27LPx _3e8K6 _1wSdM'})
            #print(result2.prettify())
            #print('===============================')
            # Get players
            #print('Players...')
            for i, player in enumerate(players):
                if i == 0:
                    p1.append(player.text)
                elif i == 1:
                    p2.append(player.text)
            # Get game results
            #print('Results...')
            if len(results) > 0:
                for i, result in enumerate(
                match.findAll('div',attrs={'class':'_27LPx _3e8K6 _1wSdM'})):
                    #print('match')
                    if i == 0:
                        result1.append(int(result.text))
                    elif i == 1:
                        result2.append(int(result.text))
            else:
                result1.append(0)
                result2.append(0)
            # Get scores
            #for i, score in enumerate(match.findAll('div',attrs={

#print(p1)
#print(p2)
#print(result1)
#print(result2)

# Organize extracted data as data frame
print('Extracting data...')
#df = pd.DataFrame({'PLAYER 1':p1,'PLAYER 2':p2})
df = pd.DataFrame({'PLAYER 1':p1,'PLAYER 2':p2,'RESULT1':result1,'RESULT2':result2})
print(df)
# Store data frame in Excel format
print('Converting data to Excel file...')
df.to_excel('output.xlsx', sheet_name='Matches', index=False)
