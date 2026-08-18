WITH source AS (
    SELECT * FROM zomato_raw.orders
),

renamed AS (
    SELECT
        CAST(source.order_id AS INT) AS order_id,
        CAST(source.user_id AS INT) AS user_id,
        CAST(source.restaurant_id AS INT) AS restaurant_id,
        CAST(source.order_timestamp AS TIMESTAMP) AS order_timestamp,
        CAST(source.delivery_timestamp AS TIMESTAMP) AS delivery_timestamp,
        CAST(source.total_amount AS DOUBLE) AS total_amount,
        UPPER(TRIM(source.order_status)) AS order_status,
        COALESCE(UPPER(TRIM(source.order_status)) = 'DELIVERED', FALSE) AS is_delivered,
        -- Calculate delivery duration in minutes for completed orders
        CASE
            WHEN source.delivery_timestamp IS NOT NULL AND source.order_timestamp IS NOT NULL
                THEN
                    DATE_DIFF(
                        'minute',
                        CAST(source.order_timestamp AS TIMESTAMP),
                        CAST(source.delivery_timestamp AS TIMESTAMP)
                    )
        END AS delivery_duration_mins
    FROM source
)

SELECT * FROM renamed
