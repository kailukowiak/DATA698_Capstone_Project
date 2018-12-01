import requests
import pandas as pd
from datetime import timedelta
from passwords import weather_api

df = pd.read_pickle('prices.pkl')


def date_finder(df):
    dates = df.time_scraped.dt.date.unique()
    return dates


def city_weather(df):
    cities = df.area_name.unique()
    start_date = date_finder(df)
    end_date = start_date + timedelta(days=1)
    return cities, start_date, end_date


cities, start_dates, end_dates = city_weather(df)


def weather_scraper(cities, start_dates, end_dates):
    url_list = []
    for i in range(len(cities)):
        city = cities[i]
        for i in range(len(start_dates)):
            start_date = start_dates[i]
            end_date = end_dates[i]
            url = (f'https://api.weatherbit.io/v2.0/history/daily?' +
                   f'city={city},Canada&start_date={start_date}&end_date=' +
                   f'{end_date}&key={weather_api}')
            url_list.append(url)
    return url_list


urls = weather_scraper(cities, start_dates, end_dates)


def scraper(urls):
    json_list = []
    for i in urls:
        info = requests.get(i)
        json_list.append(info)
    return json_list


data = scraper(urls)


def df_builder(data):
    city_name = []
    date = []
    precip = []
    min_temp = []
    max_temp = []
    clouds = []
    max_wind_spd = []
    snow = []
    for i in data:
        info = i.json()
        try:
            date.append(info['data'][0]['datetime'])
            city_name.append(info['city_name'])
            precip.append(info['data'][0]['precip'])
            min_temp.append(info['data'][0]['min_temp'])
            max_temp.append(info['data'][0]['max_temp'])
            clouds.append(info['data'][0]['clouds'])
            max_wind_spd.append(info['data'][0]['max_wind_spd'])
            snow.append(info['data'][0]['snow'])
        except KeyError:
            pass

    df = pd.DataFrame({'city_name': city_name,
                       "date": date,
                       "precip": precip,
                       "min_temp": min_temp,
                       "max_temp": max_temp,
                       'clouds': clouds,
                       'max_wind_spd': max_wind_spd,
                       'snow': snow})
    return df


df = df_builder(data)

df.to_pickle('weather_data.pkl')
