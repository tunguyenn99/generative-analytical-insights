-- MetricFlow Time Spine model required for dbt Semantic Layer time-based metrics
{{
    config(
        materialized='table'
    )
}}

WITH days AS (
    SELECT CAST('2024-01-01' AS DATE) + INTERVAL (i) DAY AS date_day
    FROM range(0, 730) AS t(i)
)

SELECT date_day
FROM days
