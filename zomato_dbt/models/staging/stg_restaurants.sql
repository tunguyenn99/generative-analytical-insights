WITH source AS (
    SELECT * FROM zomato_raw.restaurants
),

renamed AS (
    SELECT
        CAST(restaurant_id AS INT) AS restaurant_id,
        CAST(rating AS DOUBLE) AS rating,
        CAST(votes AS INT) AS votes,
        TRIM(name) AS name,
        TRIM(city) AS city,
        -- Clean currency formatting (e.g. '₹ 400' -> 400, '--' -> NULL)
        TRY_CAST(REGEXP_REPLACE(cost_for_two, '[^0-9]', '', 'g') AS INT) AS cost_for_two,
        TRIM(cuisine) AS cuisine
    FROM source
)

SELECT * FROM renamed
