#%%
import os
from dotenv import load_dotenv
import duckdb

def insert_log(log_data):

    load_dotenv()
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    db_name = "my_db"

    conn = duckdb.connect(f"md:{db_name}?motherduck_token={motherduck_token}")    
    
    line = list(log_data.values())

    try:
        conn.execute("INSERT INTO main.run_history_log (pipeline_name, date_updated_utc, date_updated_pt, run_mode, run_duration, min_date_ran, max_date_ran, row_count, run_status, run_message) VALUES (?,?,?,?,?,?,?,?,?,?)",line)
        print('\nLog Inserted to DB')
    except Exception as e:
        print(f'Failed to run query: {e}')
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    from datetime import date, timedelta, datetime, timezone
    import time
    
    process_start_time = time.time()
    print(process_start_time)
    print(type(process_start_time))

    run_mode = 'Auto'
    start_date = date.today()
    end_date = date.today() + timedelta(days=7)
    run_status = 'Success'
    e = None

    run_time = round(time.time() - process_start_time, 2)
    print(run_time)
    print(type(run_time))

    log_data = {
        "pipeline_name": "TESTING",
        "date_updated_utc": datetime.now(timezone.utc),
        "date_updated_pt": None,
        "run_mode": run_mode,
        "run_duration": run_time,
        "min_date_ran": start_date,
        "max_date_ran": end_date,
        "row_count": 2,
        "run_status": run_status,
        "run_message": e
        }

    insert_log(log_data)


