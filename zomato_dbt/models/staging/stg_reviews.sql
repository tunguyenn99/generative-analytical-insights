WITH source AS (
    SELECT * FROM ZOMATO_RAW.reviews
),

renamed AS (
    SELECT
        CAST(review_id AS INT) AS review_id,
        CAST(order_id AS INT) AS order_id,
        CAST(user_id AS INT) AS user_id,
        CAST(restaurant_id AS INT) AS restaurant_id,
        TRIM(review_text) AS review_text,
        CAST(star_rating AS INT) AS star_rating,
        CAST(review_date AS TIMESTAMP) AS review_date
    FROM source
)

SELECT * FROM renamed
