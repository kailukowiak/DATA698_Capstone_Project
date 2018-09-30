import pandas as pd

from sqlalchemy import create_engine
from passwords import connection_string


db = create_engine(connection_string, encoding="latin-1")

con = db.connect()

df = pd.read_sql("SELECT * FROM gddb", con=con)

df.ta
