WITH orders AS (
    SELECT
        o.order_id,
        o.order_date,
        r.city,
        o.order_status,
        o.is_delivered,
        o.total_amount
    FROM {{ ref('fct_orders') }} AS o
    INNER JOIN {{ ref('dim_restaurants') }} AS r ON o.restaurant_id = r.restaurant_id
)

SELECT
    order_date,
    city,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN is_delivered THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN is_delivered THEN total_amount ELSE 0 END), 2)
        AS gross_merchandise_value_gmv,
    ROUND(AVG(CASE WHEN is_delivered THEN total_amount END), 2)
        AS average_order_value_aov,
    ROUND(
        SUM(CASE WHEN order_status = 'CANCELLED' THEN 1.0 ELSE 0.0 END) / COUNT(order_id) * 100, 2
    ) AS cancellation_rate_pct
FROM orders
GROUP BY order_date, city
ORDER BY order_date DESC, city ASC
