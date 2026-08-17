WITH source AS (
    SELECT * FROM ZOMATO_RAW.food
),

renamed AS (
    SELECT
        CAST(food_id AS INT) AS food_id,
        TRIM(item_name) AS item_name,
        TRIM(category) AS category,
        CAST(is_veg AS BOOLEAN) AS is_veg
    FROM source
)

SELECT * FROM renamed
