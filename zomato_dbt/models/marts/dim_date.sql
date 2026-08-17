WITH date_spine AS (
    SELECT CAST('2024-01-01' AS DATE) + INTERVAL (i) DAY AS date_day
    FROM range(0, 365) AS t(i)
)

SELECT
    date_day,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    DAY(date_day) AS day_of_month,
    DAYOFWEEK(date_day) AS day_of_week,
    STRFTIME(date_day, '%B') AS month_name,
    STRFTIME(date_day, '%A') AS day_name
FROM date_spine
