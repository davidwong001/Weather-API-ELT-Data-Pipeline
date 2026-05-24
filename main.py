#%%
from utils.extract_data import get_output
from utils.load_data import load_data
from utils.run_history_log import insert_log
import sys
import subprocess
import os
import time
from datetime import date, timedelta, datetime, timezone

main_path = os.getenv('Main_Directory')
dbt_path = os.path.join(main_path, 'Weather API Data Pipeline','weather_api_dbt')

def run_dbt():
    result = subprocess.run(
        ["dbt", "build"],
        cwd= dbt_path,
        capture_output = True,
        text = True
    )
    
    if result.returncode != 0:
        raise Exception(f"dbt build failed: {result.stderr}")
    
    print(result.stdout)

def main():
    process_start_time = time.time()
    df = None
    failed_locations = []
    run_status = "Success"
    run_message = None

    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--manual":
            print('Running in Manual Mode\n')
            run_mode = 'Manual'
            print('Please enter the date range to backfill in this format YYYY-MM-DD:')
            start_date = input('Start Date: ')
            end_date = input('End Date: ')
            print('\nStarting backfill...\n')
        else:
            print('Running in Auto Mode\n')
            run_mode = 'Auto'
            start_date = date.today()
            end_date = date.today() + timedelta(days=7)

        df, failed_locations = get_output(start_date,end_date)

        if failed_locations:
            run_status = "Warning"
            run_message = f"Partial success. Failed cities: {', '.join(failed_locations)}"
            print(f"Warning: {run_message}")
            
        load_data(df)
        run_dbt()
        print('Done')

    except Exception as e:
        print(f'An error has occurred: {e}')
        run_status = "Error"
        run_message = str(e)
    
    finally:
        run_time = round(time.time() - process_start_time, 2)

        log_data = {
            "pipeline_name": "Weather API Load",
            "date_updated_utc": datetime.now(timezone.utc),
            "date_updated_pt": None,
            "run_mode": run_mode,
            "run_duration": run_time,
            "min_date_ran": start_date,
            "max_date_ran": end_date,
            "row_count": len(df) if df is not None else 0,
            "run_status": run_status,
            "run_message": run_message
            }

        insert_log(log_data)

if __name__ == "__main__":
    main()

