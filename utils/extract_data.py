#%%
import requests
import time
import pandas as pd
from datetime import datetime, timezone
from utils.motherdb_connection import get_motherdb_connection

def get_data(city, lat, lon,start_date,end_date):
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": lat,
		"longitude": lon,
		"daily": ["weather_code", "uv_index_max", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", 
				"sunrise", "sunset", "daylight_duration", "wind_gusts_10m_max", "rain_sum"],
		"start_date": start_date,
		"end_date": end_date,
	}

	for attempt in range(3): 
		try:
			response = requests.get(url, params=params, timeout=10)
			response.raise_for_status() #This does nothing on successful connections. 
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Attempt {attempt + 1} failed for {city}: {e}")
			if attempt < 2:
				time.sleep(5)
	print(f"All retries failed for {city}")
	return None

def get_locations():
	db_name = 'weather_api'
	conn = get_motherdb_connection(db_name)

	try:
		locations = conn.execute(
		"""
		SELECT *
		FROM weather_api.raw.locations
		"""
		).df().to_dict('records')

		return locations
	except Exception as e:
		raise
	finally:
		conn.close()
	

def get_output(start_date,end_date):
	all_data = [] 
	failed_locations= []

	locations = get_locations()

	for location in locations:
		data = get_data(location["city"],location["lat"],location["lon"],start_date,end_date)
		#print(data)

		if data is None:
			failed_locations.append(location["city"])
			continue

		df = pd.DataFrame(data["daily"])
		df["city"] = location["city"]

		all_data.append(df)

	if not all_data:
		raise Exception("All locations failed to extract")

	df_output = pd.concat(all_data, ignore_index=True)

	now = datetime.now(timezone.utc) #.replace(microsecond=0) # add tzinfo=None to remove timezone data
	df_output["date_updated"] = now

	cols = ["date_updated","time","city"] + [col for col in df_output.columns if col not in ["date_updated","time","city"]]
	df_output = df_output[cols]

	return df_output, failed_locations
     
if __name__ == "__main__":
	from datetime import date, timedelta
	
	start_date = date.today()
	end_date = date.today() + timedelta(days=7)

	testdf, failed_locations = get_output(start_date,end_date)
	print(testdf)
	print(f"Failed locations: {failed_locations}")