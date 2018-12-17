import re
import pandas as pd
from sqlalchemy import create_engine
from passwords import connection_string

loc_df = pd.read_pickle('location_df.pkl')

# db = create_engine(connection_string, encoding="latin-1")

# con = db.connect()

price_df = pd.read_pickle('prices.pkl')
# pd.read_sql(sql="SELECT * FROM gddb", con=con)

price_df['address'] = price_df['address'].str.replace(
    r'\b([A-Z]{1,2})([A-Z][a-z])',
    r'\1 \2').str.replace(r'\s\s', r'\s')

price_df.address = price_df.address.str.replace('(?!^)([A-Z][a-z]+)', r' \1')


price_df.to_pickle('prices.pkl')
