SELECT
    order_id,
    user_id,
    restaurant_id,
    order_timestamp,
    delivery_timestamp,
    CAST(order_timestamp AS DATE) AS order_date,
    EXTRACT(HOUR FROM order_timestamp) AS order_hour,
    order_status,
    is_delivered,
    total_amount,
    delivery_duration_mins
FROM {{ ref('stg_orders') }}
