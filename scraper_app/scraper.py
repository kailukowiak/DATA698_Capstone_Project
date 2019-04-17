import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
from progress.bar import Bar
import googlemaps
import pandas as pd
from passwords import google_api_key
import numpy as np


start_time = time.time()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
# For no Images loaded:
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {'profile.managed_default_content_settings.images': 2,
         "profile.managed_default_content_settings.images": 2,
         'disk-cache-size': 4096 }
chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=chrome_options)


def scraper(driver, city_name):
    # print("Scraping: " + city_name)
    driver.get('https://www.gasbuddy.com/home?search='+city_name+'&fuel=1')
    time.sleep(2) # Removed sleep may have broken
    selector = '.colors__bgTeal___38u08.button__fluid___2ez5a'
    try:
        selector = '.colors__bgTeal___38u08.button__fluid___2ez5a'
        element = driver.find_element_by_css_selector(selector)
        driver.execute_script("arguments[0].scrollIntoView(top);", element)
        # print('scrolled')
        while True:
            time.sleep(2)
            element.click()
            # print("Clicked")
            time.sleep(2)
    except (NoSuchElementException, WebDriverException):
        pass
        # print("Done")
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    return soup



def city_iterator(city_list, driver):
    master_df = pd.DataFrame(columns=['names', 'price', 'time_ago',
                                      'address', 'time_scraped', 'area_name'])
    bar = Bar('Processing', max=20)
    for i in city_list:
        soup = scraper(driver, i)
        df = soup_reader(soup, i)
        master_df = master_df.append(df)
        bar.next()
    bar.finish()
    return master_df


def soup_reader(soup, city_name):
    names = soup.select('.styles__stationNameHeader___24lb3')  # Names
    prices = soup.select('.styles__price___3DxO5')  # prices
    date_time = soup.select('.style__postedTime___3s9-z')  # Time
    address = soup.select('.styles__address___8IK98')
    user_name = soup.select('.style__memberLink___24Vl5')
    names = pandifier(names)
    prices = pandifier(prices)
    date_time = pandifier(date_time)
    address = pandifier(address)
    user_name = pandifier(user_name)
    
    df = pd.concat([names, prices, date_time, address, user_name], axis=1)
    df.columns = ['names', 'price', 'time_ago', 'address', 'user_name']
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



cities = pd.read_excel(r"K:\S&OPS\Network Operations and Real " 
                       R"Estate\Business Analyst\Analyst "
                       r"Files\Temporary Loc List Source\Region Lookup.xlsx")

cities['area_query'] = cities['Location City']\
        .str.replace(' ', '%20') + '%20'+ cities.Province + "%20Canada"

city_list = cities.area_query.tolist()

city_list = ['calgary', 'edmonton']
df = city_iterator(city_list, driver)


driver.close()

end_time = time.time()

print(end_time - start_time)



def address_cleaner(df, col_name):
    df[col_name] = df[col_name].str.replace(r'\b([A-Z]{1,2})([A-Z][a-z])',
                                             r'\1 \2')
    return df
df = address_cleaner(df, 'address')
#
#df = address_cleaner(df, 'address')
#loc_df = address_cleaner(loc_df, 'location_address')
#
#
#df.area_name = df.area_name.str.lower()
#df.area_name = df.area_name.str.replace('%20', ' ')  # adds space
#
#
## .str.replace(r'\s\s', r'\s')
#
#df.address = df.address.str.replace('(?!^)([A-Z][a-z]+)', r' \1')

df.price = pd.to_numeric(df.price.str.replace(r'\xa2', '').str.replace('---' , ''))



# db = create_engine(connection_string, encoding="latin-1")

# con = db.connect()

# price_df = pd.read_sql(sql="SELECT * FROM gddb", con=con)
price_df = df
# price_df['address'] = price_df['address'].str.replace(
#     r'\b([A-Z]{1,2})([A-Z][a-z])',
#     r' \1 \2')

gm = googlemaps.Client(key=google_api_key)

unique_address = price_df.address.unique()


def google_scraper(address):
    lat_lng = {}
    for name in address:
        print(name)
        try:
            location = gm.geocode(name)[0]
        except IndexError:
            print(name+" Error Here")
        lat_lng[name] = location
    return lat_lng


location_dict = google_scraper(unique_address)


def location_framer(location_dict):
    lat_list = []
    lng_list = []
    names_list = []
    for address in location_dict.keys():
        try:
            lat = location_dict[address]['geometry']['location']['lat']
            lng = location_dict[address]['geometry']['location']['lng']
        except KeyError:
            lat = np.NAN
            lng = np.NAN
        lat_list.append(lat)
        lng_list.append(lng)
        names_list.append(address)

    df = pd.DataFrame({'location_address': names_list,
                       'lat': lat_list,
                       'lng': lng_list})
    return df


loc_df = location_framer(location_dict)

# loc_df.to_pickle("location_df.pkl")
# price_df.to_pickle('prices.pkl')





df_p = pd.merge(df, loc_df, how='left', left_on = 'address', 
                right_on = 'location_address')

df_p['time_ago'].replace(regex=True, inplace=True, to_replace=r' ago', value=r'')
df_p['time_diff'] = df_p['time_ago'].apply(pd.Timedelta)

df_p['time'] = df_p.time_scraped - df_p.time_diff

df_p.to_csv("SpotfirePricing_320.csv")

# price_df.to_pickle('prices.pkl')
