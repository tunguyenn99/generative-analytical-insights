WITH reviews AS (
    SELECT
        rev.review_id,
        rev.restaurant_id,
        r.name AS restaurant_name,
        r.city,
        rev.star_rating,
        rev.review_text
    FROM {{ ref('stg_reviews') }} AS rev
    INNER JOIN {{ ref('stg_restaurants') }} AS r ON rev.restaurant_id = r.restaurant_id
)

SELECT
    restaurant_id,
    restaurant_name,
    city,
    COUNT(review_id) AS total_reviews,
    ROUND(AVG(star_rating), 2) AS avg_star_rating,
    SUM(CASE WHEN star_rating >= 4 THEN 1 ELSE 0 END) AS positive_reviews_count,
    SUM(CASE WHEN star_rating = 3 THEN 1 ELSE 0 END) AS neutral_reviews_count,
    SUM(CASE WHEN star_rating <= 2 THEN 1 ELSE 0 END) AS negative_reviews_count
FROM reviews
GROUP BY restaurant_id, restaurant_name, city
ORDER BY avg_star_rating DESC, total_reviews DESC
