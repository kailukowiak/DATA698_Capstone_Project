## Importing
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests


import re
import os
import time


## Selinium
driver = webdriver.Chrome('chromedriver')

## Test scrape
page = requests.get('https://www.gasbuddy.com/home?search=calgary&fuel=1')



## Soup
soup = BeautifulSoup(page.content, 'html.parser')



## Selinium


## css selections
names = soup.select('.styles__stationNameHeader___24lb3') # Names
prices = soup.select('.styles__price___3DxO5') # prices
time = soup.select('.style__postedTime___3s9-z') # Time

# .colors__bgTeal___pV1j5.style__fluid___2-Qjz
