import pandas as pd

df = pd.read_excel('Unleaded_Wholesale_DAILY_2018.xlsx', skiprows=[0, 1])

df = df.rename({"Unnamed: 0": 'date'}, axis=1)
df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.drop('canada_ave(v)', axis=1)
df = pd.melt(df, id_vars=['date'],
             var_name='city_name',
             value_name='rack_price')
print(df.head())
