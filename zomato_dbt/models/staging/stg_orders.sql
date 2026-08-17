WITH source AS (
    SELECT * FROM zomato_raw.orders
),

renamed AS (
    SELECT
        CAST(order_id AS INT) AS order_id,
        CAST(user_id AS INT) AS user_id,
        CAST(restaurant_id AS INT) AS restaurant_id,
        CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
        CAST(delivery_timestamp AS TIMESTAMP) AS delivery_timestamp,
        CAST(total_amount AS DOUBLE) AS total_amount,
        UPPER(TRIM(order_status)) AS order_status,
        COALESCE(UPPER(TRIM(order_status)) = 'DELIVERED', FALSE) AS is_delivered,
        -- Calculate delivery duration in minutes for completed orders
        CASE
            WHEN delivery_timestamp IS NOT NULL AND order_timestamp IS NOT NULL
                THEN
                    DATE_DIFF(
                        'minute',
                        CAST(order_timestamp AS TIMESTAMP),
                        CAST(delivery_timestamp AS TIMESTAMP)
                    )
        END AS delivery_duration_mins
    FROM source
)

SELECT * FROM renamed
