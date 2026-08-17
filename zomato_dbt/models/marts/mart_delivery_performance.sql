WITH delivery_data AS (
    SELECT
        o.order_id,
        r.city,
        o.order_hour,
        o.delivery_duration_mins
    FROM {{ ref('fct_orders') }} AS o
    INNER JOIN {{ ref('dim_restaurants') }} AS r ON o.restaurant_id = r.restaurant_id
    WHERE o.is_delivered AND o.delivery_duration_mins IS NOT NULL
)

SELECT
    city,
    order_hour,
    COUNT(order_id) AS total_deliveries,
    ROUND(AVG(delivery_duration_mins), 1) AS avg_delivery_mins,
    ROUND(QUANTILE_CONT(delivery_duration_mins, 0.50), 1) AS p50_delivery_mins,
    ROUND(QUANTILE_CONT(delivery_duration_mins, 0.90), 1) AS p90_delivery_mins
FROM delivery_data
GROUP BY city, order_hour
ORDER BY city, order_hour
