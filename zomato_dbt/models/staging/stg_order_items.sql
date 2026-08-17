WITH source AS (
    SELECT * FROM ZOMATO_RAW.order_items
),

renamed AS (
    SELECT
        CAST(order_item_id AS INT) AS order_item_id,
        CAST(order_id AS INT) AS order_id,
        CAST(food_id AS INT) AS food_id,
        CAST(quantity AS INT) AS quantity,
        CAST(item_price AS DOUBLE) AS item_price,
        CAST(quantity * item_price AS DOUBLE) AS subtotal
    FROM source
)

SELECT * FROM renamed
