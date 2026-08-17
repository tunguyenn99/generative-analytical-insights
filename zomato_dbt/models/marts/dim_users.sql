WITH stg_u AS (
    SELECT * FROM {{ ref('stg_users') }}
),

user_orders AS (
    SELECT
        user_id,
        COUNT(order_id) AS total_orders_placed,
        SUM(CASE WHEN is_delivered THEN total_amount ELSE 0 END) AS total_spent
    FROM {{ ref('stg_orders') }}
    GROUP BY user_id
)

SELECT
    u.user_id,
    u.name,
    u.email,
    u.age,
    u.age_group,
    u.gender,
    u.city,
    u.signup_date,
    COALESCE(o.total_orders_placed, 0) AS total_orders_placed,
    COALESCE(o.total_spent, 0.0) AS total_spent
FROM stg_u AS u
LEFT JOIN user_orders AS o ON u.user_id = o.user_id
