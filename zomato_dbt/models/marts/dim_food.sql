SELECT
    food_id,
    item_name,
    category,
    is_veg
FROM {{ ref('stg_food') }}
