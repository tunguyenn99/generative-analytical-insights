SELECT
    order_item_id,
    order_id,
    food_id,
    quantity,
    item_price,
    subtotal
FROM {{ ref('stg_order_items') }}
