with source as (
        select * from {{ source('raw_weather_output', 'data_pull_output') }}
  ),
  renamed as (
      select
          TIMEZONE('UTC', date_updated) AS date_updated_utc,
          TIMEZONE('America/Los_Angeles', date_updated) AS date_updated_pt,
          CAST("time" as date) as forecast_date,
          city,
          weather_code,
          CAST(uv_index_max AS DECIMAL(10,2)) AS uv_index_max, 
          CAST(temperature_2m_max AS DECIMAL(10,2)) AS temperature_2m_max_c,
          CAST((temperature_2m_max * 9/5)+32 AS DECIMAL(10,2)) AS temperature_2m_max_f,
          CAST(temperature_2m_min AS DECIMAL(10,2)) AS temperature_2m_min_c,
          CAST((temperature_2m_min * 9/5)+32 AS DECIMAL(10,2)) AS temperature_2m_min_f,
          CAST(temperature_2m_mean AS DECIMAL(10,2)) AS temperature_2m_mean_c,
          CAST((temperature_2m_mean * 9/5)+32 AS DECIMAL(10,2)) AS temperature_2m_mean_f,
          CAST(sunrise AS datetime) AS sunrise_utc,
          TIMEZONE('America/Los_Angeles',TIMEZONE('UTC', CAST(sunrise AS datetime))) AS sunrise_pt,
          CAST(sunset AS datetime) AS sunset_utc,
          TIMEZONE('America/Los_Angeles',TIMEZONE('UTC', CAST(sunset AS datetime))) AS sunset_pt,
          CAST(daylight_duration AS DECIMAL(10,2)) AS daylight_duration_sec,
          CAST(daylight_duration / 3600 AS DECIMAL(10,2)) AS daylight_duration_hr,
          CAST(wind_gusts_10m_max AS DECIMAL(10,2)) AS wind_gusts_10m_max_kph,
          CAST(wind_gusts_10m_max / 1.609 AS DECIMAL(10,2)) AS wind_gusts_10m_max_mph,
          CAST(rain_sum AS DECIMAL(10,2)) AS rain_sum_mm,
          CAST(rain_sum / 25.4 AS DECIMAL(10,2)) AS rain_sum_in,
          ROW_NUMBER() OVER (PARTITION BY city, forecast_date ORDER BY date_updated_utc DESC) AS row_num
      from source
  )
  select * from renamed
  where row_num = 1