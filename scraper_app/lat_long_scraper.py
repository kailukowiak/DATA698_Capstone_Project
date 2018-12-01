import googlemaps
import pandas as pd
from passwords import google_api_key, connection_string
from sqlalchemy import create_engine
import numpy as np


# db = create_engine(connection_string, encoding="latin-1")

# con = db.connect()

# price_df = pd.read_sql(sql="SELECT * FROM gddb", con=con)
price_df = pd.read_pickle('prices.pkl')

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

loc_df.to_pickle("location_df.pkl")
# price_df.to_pickle('prices.pkl')
con.close()
