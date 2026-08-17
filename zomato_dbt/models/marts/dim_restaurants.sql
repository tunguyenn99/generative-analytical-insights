WITH stg_r AS (
    SELECT * FROM {{ ref('stg_restaurants') }}
),

ord_stats AS (
    SELECT
        restaurant_id,
        COUNT(order_id) AS total_orders,
        SUM(CASE WHEN is_delivered THEN total_amount ELSE 0 END) AS total_gmv
    FROM {{ ref('stg_orders') }}
    GROUP BY restaurant_id
)

SELECT
    r.restaurant_id,
    r.name,
    r.city,
    r.rating,
    r.votes,
    r.cost_for_two,
    r.cuisine,
    COALESCE(o.total_orders, 0) AS total_orders,
    COALESCE(o.total_gmv, 0.0) AS total_gmv
FROM stg_r AS r
LEFT JOIN ord_stats AS o ON r.restaurant_id = o.restaurant_id
