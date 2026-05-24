with weather_forecast as (
        select * from {{ ref('base_raw_data_pull_output') }}
  ),
  weather_codes as (
        select * from {{ ref('weather_codes') }}
  ),
  final as(
        select
            f.date_updated_utc,
            f.date_updated_pt,
            f.forecast_date,
            f.city,
            f.weather_code,
            coalesce(c.Description,'Missing Description') AS weather_code_def,
            f.uv_index_max,
            f.temperature_2m_max_c,
            f.temperature_2m_max_f,
            f.temperature_2m_min_c,
            f.temperature_2m_min_f,
            f.temperature_2m_mean_c,
            f.temperature_2m_mean_f,
            f.sunrise_utc,
            f.sunrise_pt,
            f.sunset_utc,
            f.sunset_pt,
            f.daylight_duration_sec,
            f.daylight_duration_hr,
            f.wind_gusts_10m_max_kph,
            f.wind_gusts_10m_max_mph,
            f.rain_sum_mm,
            f.rain_sum_in
        from weather_forecast f
        left join weather_codes c ON c.Code = f.weather_code
  )
  select * from final
