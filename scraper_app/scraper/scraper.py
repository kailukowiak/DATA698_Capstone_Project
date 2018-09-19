

## Importing
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
print("Loading images")
# driver = webdriver.Firefox(executable_path='/Users/kailukowiak/DATA698_Capstone_Project/geckodriver')
driver = webdriver.Chrome('/Users/kailukowiak/DATA698_Capstone_Project/scraper_app/scraper/chromedriver')
## Script
# commit 
def ad_closer():
    try:
        xpath = ("//body/div[2]/span//img[@src='https://c.gumgum.com/ads/com/"+
                 "gumgum/close/new/close_dark_3x.png']")
        # driver.find_element_by_css_selector(css).click()
        driver.find_element_by_xpath(xpath).click()
        print('ad closed')
    except NoSuchElementException:
        print('no add')

def scraper(driver, city_name):
    print(city_name)
    driver.get('https://www.gasbuddy.com/home?search='+city_name+'&fuel=1')
    time.sleep(5)
    ad_closer()
    try:
        while True:
            time.sleep(3)
            print("Start Scrape...")
            selector = '.colors__bgTeal___pV1j5.style__fluid___2-Qjz'
            driver.find_element_by_css_selector(selector).click()
            print("Clicked")
            time.sleep(2)
    except (NoSuchElementException, WebDriverException):
        print("Done")
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def city_iterator(city_list, driver):
    master_df = pd.DataFrame(columns=['names', 'price', 'time_ago',
                                      'address', 'time_scraped', 'area_name'])
    for i in city_list:
        soup = scraper(driver, i)
        df = soup_reader(soup, i)
        master_df = master_df.append(df)

    return master_df


def soup_reader(soup, city_name):
    names = soup.select('.styles__stationNameHeader___24lb3')  # Names
    prices = soup.select('.styles__price___3DxO5')  # prices
    date_time = soup.select('.style__postedTime___3s9-z')  # Time
    address = soup.select('.styles__address___8IK98')
    names = pandifier(names)
    prices = pandifier(prices)
    date_time = pandifier(date_time)
    address = pandifier(address)
    df = pd.concat([names, prices, date_time, address], axis=1)
    df.columns = ['names', 'price', 'time_ago', 'address']
    df['time_scraped'] = pd.to_datetime('now')
    df['area_name'] = city_name
    return df


def pandifier(_list):
    pandas_series = []
    for i in _list:
        val = i.get_text()
        pandas_series.append(val)
    pandas_series = pd.Series(pandas_series)
    return pandas_series


city_list = ['calgary', 'edmonton']
test = city_iterator(city_list, driver)


# soup = scraper(driver, 'calgary')
# driver.close()
## Driver close
driver.close()
