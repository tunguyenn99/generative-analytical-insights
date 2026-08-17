WITH source AS (
    SELECT * FROM ZOMATO_RAW.menu
),

renamed AS (
    SELECT
        CAST(menu_id AS INT) AS menu_id,
        CAST(restaurant_id AS INT) AS restaurant_id,
        CAST(food_id AS INT) AS food_id,
        CAST(price AS DOUBLE) AS price
    FROM source
)

SELECT * FROM renamed
