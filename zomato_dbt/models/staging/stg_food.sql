WITH source AS (
    SELECT * FROM zomato_raw.food
),

renamed AS (
    SELECT
        CAST(food_id AS INT) AS food_id,
        CAST(is_veg AS BOOLEAN) AS is_veg,
        TRIM(item_name) AS item_name,
        TRIM(category) AS category
    FROM source
)

SELECT * FROM renamed
