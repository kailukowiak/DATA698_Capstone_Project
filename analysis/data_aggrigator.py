# %%
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

prices = pd.read_pickle("scraper_app/prices.pkl")

location = pd.read_pickle("scraper_app/location_df.pkl")

prices = prices.drop('index', axis=1)
prices.area_name = prices.area_name.str.lower()
prices.area_name = prices.area_name.str.replace('%20', ' ')  # adds space


df = pd.merge(prices, location, left_on='address', right_on='location_address')
df = df.drop(['location_address'], axis=1)
df['date'] = pd.to_datetime(df['time_scraped'].dt.date)


df['time_ago'].replace(regex=True, inplace=True, to_replace=r' ago', value=r'')
df.time_ago[df.time_ago.isnull()] = "0 hours"
df['time_diff'] = df['time_ago'].apply(pd.Timedelta)
df['time'] = df.time_scraped - df.time_diff


alberta_excise = 10 + 13 + 6.73
vancouver_excise = 10 + 8.5 + 7.78 + 17 + 8.5
bc_excise = 10 + 8.5 + 7.78 + 8.5
gst = 0.05
victoria_excise = 37.78
kelowna_excise = 32.28
df['margin'] = df.price/(1+gst)

ab_cities = ['calgary', 'edmonton', 'lethbridge', 'red deer']

df.margin.loc[df.area_name.isin(ab_cities)] = \
    df.margin.loc[df.area_name.isin(ab_cities)] - alberta_excise
df.margin.loc[df.area_name.isin(['vancouver'])] = \
    df.margin.loc[df.area_name.isin(['vancouver'])] - vancouver_excise
df.margin.loc[df.area_name.isin(['kelowna'])] = \
    df.margin.loc[df.area_name.isin(['kelowna'])] - kelowna_excise
df.margin.loc[df.area_name.isin(['victoria'])] = \
    df.margin.loc[df.area_name.isin(['victoria'])] - victoria_excise


margins = pd.read_csv("scraper_app/city_margins.csv")
margins = margins.melt(id_vars='date',
                       value_name='rack',
                       var_name='area_name')

margins.area_name = margins.area_name.str.lower()
margins.date = pd.to_datetime(margins.date)
# http://www2.nrcan.gc.ca/eneene/sources/pripri/
# wholesale_bycity_e.cfm?priceYear=2017&productID=9&locationID=8,10,6,9,2,3&
# frequency=D#priceGraph

df = pd.merge(df, margins, on=['date', 'area_name'])
df['margin'] = df.margin - df.rack
# Test

df = df[['names', 'price', 'address', 'area_name',
         'lat', 'lng', 'time', 'margin']]


df.time = df.time.dt.round("H")
df.drop_duplicates(subset=['time', 'address'], inplace=True)


df_p = df.reset_index().pivot('time', 'address', 'margin')

df_p = df_p.fillna(method='ffill', limit=72)
df_p = df_p.fillna(method='bfill', limit=72)
tmp = df_p.dropna(axis=1)

cor_mat = tmp.corr()

#
cor_mat.dropna(inplace=True)

# Z=linkage(cor_mat, 'single', 'correlation')

# dendrogram(Z, color_threshold=0);

missing = df_p.isna().sum().sort_values()

calg = df.loc[df['area_name'] == "calgary"]
calg.set_index('time', inplace=True)
calg = calg.sort_index()
# %%
calg['rolling_mean'] = calg.margin.rolling("1d", min_periods=1).mean()
calg.margin = calg.margin - calg.rolling_mean


# %%


calg = calg.pivot(None, 'address', 'margin')
calg = calg.fillna(method='ffill', limit=72)
calg = calg.fillna(method='bfill', limit=72)
calg_missing = calg.isna().sum().sort_values()
calg_missing = calg_missing.loc[calg_missing > 1]

calg.drop((calg_missing.index), axis=1, inplace=True)

# calg.roll

calg_cor = calg.corr()
calg_cor.isna().sum()

dissimilarity = 1 - np.abs(calg_cor)
hierarchy = linkage(squareform(dissimilarity), method='average')
labels = fcluster(hierarchy, 0.8, criterion='distance')
labels
Z = linkage(dissimilarity, 'single', 'correlation')

dendrogram(Z, color_threshold=0.15)

calg_clusters = pd.DataFrame({'cluster': labels}, index=calg_cor.index)
calg = df.loc[df['area_name'] == "calgary"]
calg = calg.set_index(keys=['address', 'time'])

calg = calg.join(calg_clusters, how='inner')
# calg.cluster = str(calg.cluster)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']  # , 'e', 'f', 'g', 'h'
calg.cluster = calg.cluster.replace([1, 2, 3, 4, 5, 6, 7], letters)
# calg['cluster_cat'] = calg.cluster
sns.scatterplot('lat', 'lng', hue='cluster', data=calg)
