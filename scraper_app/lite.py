import pandas as pd
## Data
location = pd.read_pickle('location_df.pkl')

rack = pd.read_excel('RackPricesNov10.xlsx')
rack = rack.melt(id_vars='Date', var_name='City', value_name='Rack')
rack.City = rack.City.str.lower()
rack.columns = rack.columns.str.lower()

## Prices
prices = pd.read_pickle('prices.pkl')
prices = prices.drop('index', axis=1)
prices.area_name = prices.area_name.str.lower()
prices.area_name = prices.area_name.str.replace('%20', ' ')  # adds space

prices['rack_area_name'] = prices.area_name
prices.rack_area_name[prices['rack_area_name'] == 'lethbridge'] = 'calgary'
prices.rack_area_name[prices['rack_area_name'] == 'kamloops'] = 'kelowna'


prices['time_ago'].replace(regex=True,
                           inplace=True,
                           to_replace=r' ago',
                           value=r'')
prices['time_diff'] = prices['time_ago'].apply(pd.Timedelta)

prices['time'] = prices.time_scraped - prices.time_diff
prices['date'] = prices.time.dt.date.astype('datetime64[ns]')

# prices['rack_area_name']

# prices.index = prices['Date']

## Merging
# df = pd.merge(prices,location, left_on='address',right_on='location_address')
# df = df.drop(['location_address'], axis=1)
# df['date'] = pd.to_datetime(df['time_scraped'].dt.date)

alberta_excise = 10 + 13 + 6.73
vancouver_excise = 10 + 8.5 + 7.78 + 17 + 8.5
bc_excise = 10 + 8.5 + 7.78 + 8.5
gst = 0.05
victoria_excise = 37.78
kelowna_excise = 32.28
prices['tax_less'] = prices.price/(1+gst)
## Test
ab_cities = ['calgary', 'edmonton', 'lethbridge', 'red deer']

prices.tax_less.loc[prices.area_name.isin(ab_cities)] = \
    prices.tax_less.loc[prices.area_name.isin(ab_cities)] - alberta_excise

prices.tax_less.loc[prices.area_name.isin(['vancouver'])] = \
    prices.tax_less.loc[prices.area_name.isin(['vancouver'])] - vancouver_excise

prices.tax_less.loc[prices.area_name.isin(['kelowna'])] = \
    prices.tax_less.loc[prices.area_name.isin(['kelowna'])] - kelowna_excise

prices.tax_less.loc[prices.area_name.isin(['victoria'])] = \
    prices.tax_less.loc[prices.area_name.isin(['victoria'])] - victoria_excise


## Joining
df = pd.merge(prices,
              rack,
              left_on=['date',
                       'area_name'],
              right_on=['date', 'city'])

df['margin'] = df.tax_less - df.rack

# This is a bit fuzzy here. There could be weird things but honestly if I
# reindex to hours it should be fine.

df.drop_duplicates(subset=['price', 'address', 'date'], inplace=True)

df.to_csv('noDups.csv')
