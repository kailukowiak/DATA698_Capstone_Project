import pandas as pd
import datetime as dt

# weather = pd.read_pickle('weather_data.pkl')
location = pd.read_pickle('location_df.pkl')
prices = pd.read_pickle('prices.pkl')
prices = prices.drop('index', axis=1)
prices.area_name = prices.area_name.str.lower()
prices.area_name = prices.area_name.str.replace('%20', ' ')  # adds space


df = pd.merge(prices, location, left_on='address', right_on='location_address')
df = df.drop(['location_address'], axis=1)
df['date'] = pd.to_datetime(df['time_scraped'].dt.date)


weather['city_name'] = weather['city_name'].str.lower()
weather['date'] = pd.to_datetime(weather['date'])
df = pd.merge(df, weather, left_on=['area_name', 'date'],
              right_on=['city_name', 'date'])

df = df.dropna()

df['time_ago'].replace(regex=True, inplace=True, to_replace=r' ago', value=r'')
df['time_diff'] = df['time_ago'].apply(pd.Timedelta)

df['time'] = df.time_scraped - df.time_diff

alberta_excise = 10 + 13 + 6.73
vancouver_excise = 10 + 8.5 + 7.78 + 17 + 8.5
bc_excise = 10 + 8.5 + 7.78 + 8.5
gst = 0.05
victoria_excise = 37.78
kelowna_excise = 32.28
df['margin'] = df.price/(1+gst)
## Test
ab_cities = ['calgary', 'edmonton', 'lethbridge', 'red deer']

df.margin.loc[df.city_name.isin(ab_cities)] = df.margin.loc[df.city_name.isin(ab_cities)] -alberta_excise
df.margin.loc[df.city_name.isin(['vancourver'])] = df.margin.loc[df.city_name.isin(['vancouver'])] - vancouver_excise
df.margin.loc[df.city_name.isin(['kelowna'])] = df.margin.loc[df.city_name.isin(['kelowna'])] - kelowna_excise
df.margin.loc[df.city_name.isin(['victoria'])] = df.margin.loc[df.city_name.isin(['victoria'])] - victoria_excise


margins = pd.read_excel('Margins2.xlsx')
margins = margins.melt(id_vars='date', value_name='rack', var_name='area_name')

# http://www2.nrcan.gc.ca/eneene/sources/pripri/wholesale_bycity_e.cfm?priceYear=2017&productID=9&locationID=8,10,6,9,2,3&frequency=D#priceGraph




df = pd.merge(df, margins, on=['date', 'area_name'])

df['margin'] = df.margin - df.rack
df.to_pickle('master_df.pkl')
