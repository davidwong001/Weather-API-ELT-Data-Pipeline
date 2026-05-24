#%%
from utils.motherdb_connection import get_motherdb_connection

def load_data(df):

    db_name = 'weather_api'
    conn = get_motherdb_connection(db_name)

    try:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS raw.data_pull_output (
            date_updated TIMESTAMPTZ,
            time VARCHAR,
            city VARCHAR,
            weather_code INTEGER,
            uv_index_max FLOAT,
            temperature_2m_max FLOAT,
            temperature_2m_min FLOAT,
            temperature_2m_mean FLOAT,
            sunrise VARCHAR,
            sunset VARCHAR,
            daylight_duration FLOAT,
            wind_gusts_10m_max FLOAT,
            rain_sum FLOAT
        )
        """)

        conn.execute("INSERT INTO raw.data_pull_output SELECT * FROM df")
        print('\nData Inserted to DB')

    except Exception as e:
        print(f'Failed to run query: {e}')
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    from datetime import date, timedelta
    from extract_data import get_output
    from motherdb_connection import get_motherdb_connection

    start_date = date.today()
    end_date = date.today() + timedelta(days=7)

    testdf, failed_locations = get_output(start_date,end_date)

    load_data(testdf)

