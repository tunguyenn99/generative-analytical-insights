WITH source AS (
    SELECT * FROM zomato_raw.users
),

renamed AS (
    SELECT
        CAST(user_id AS INT) AS user_id,
        CAST(age AS INT) AS age,
        CAST(signup_date AS DATE) AS signup_date,
        TRIM(name) AS name,
        LOWER(TRIM(email)) AS email,
        CASE
            WHEN age < 25 THEN '18-24'
            WHEN age BETWEEN 25 AND 40 THEN '25-40'
            ELSE '41+'
        END AS age_group,
        TRIM(gender) AS gender,
        TRIM(city) AS city
    FROM source
)

SELECT * FROM renamed
