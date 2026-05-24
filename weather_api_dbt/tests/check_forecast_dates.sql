with date_city as (
SELECT cdate, city
FROM {{ source('dim_date','dim_date') }}
CROSS JOIN(
  SELECT distinct city
  FROM {{ ref('weather_forecast') }}
) cities
WHERE datediff('day', cdate, current_date) between -7 and 7
),
data as (
SELECT *
FROM {{ ref('weather_forecast') }}
WHERE datediff('day', forecast_date, current_date) between -7 and 7
)
SELECT dc.cdate,
       dc.city,
       d.forecast_date,
       count(forecast_date)
FROM date_city dc
LEFT JOIN data d ON dc.cdate = d.forecast_date and dc.city = d.city
WHERE forecast_date is NULL
GROUP BY 1,2,3
