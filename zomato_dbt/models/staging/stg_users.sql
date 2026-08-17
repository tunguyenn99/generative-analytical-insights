WITH source AS (
    SELECT * FROM ZOMATO_RAW.users
),

renamed AS (
    SELECT
        CAST(user_id AS INT) AS user_id,
        TRIM(name) AS name,
        LOWER(TRIM(email)) AS email,
        CAST(age AS INT) AS age,
        CASE 
            WHEN age < 25 THEN '18-24'
            WHEN age BETWEEN 25 AND 40 THEN '25-40'
            ELSE '41+'
        END AS age_group,
        TRIM(gender) AS gender,
        TRIM(city) AS city,
        CAST(signup_date AS DATE) AS signup_date
    FROM source
)

SELECT * FROM renamed
