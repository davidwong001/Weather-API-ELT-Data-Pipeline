#%%
import os
from dotenv import load_dotenv
import duckdb

def get_motherdb_connection(db_name=None):
    load_dotenv()
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")

    return duckdb.connect(f"md:{db_name}?motherduck_token={motherduck_token}")
