WITH source AS (
    SELECT * FROM zomato_raw.reviews
),

renamed AS (
    SELECT
        CAST(review_id AS INT) AS review_id,
        CAST(order_id AS INT) AS order_id,
        CAST(user_id AS INT) AS user_id,
        CAST(restaurant_id AS INT) AS restaurant_id,
        CAST(star_rating AS INT) AS star_rating,
        CAST(review_date AS TIMESTAMP) AS review_date,
        TRIM(review_text) AS review_text
    FROM source
)

SELECT * FROM renamed
