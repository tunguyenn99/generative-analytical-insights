{% docs dim_restaurants_doc %}
Dimension table for Zomato partner restaurants containing normalized profiles, geographic locations, rating metrics, price ranges, and aggregated gross merchandise value (GMV).
{% enddocs %}

{% docs dim_users_doc %}
Dimension table containing registered Zomato customer accounts, demographics (age, gender, city), signup timestamps, and order history aggregates.
{% enddocs %}

{% docs dim_date_doc %}
Calendar date dimension table providing granular temporal attributes (year, month, day of month, day of week, month name) for time-series analytics.
{% enddocs %}

{% docs dim_food_doc %}
Dimension table containing food catalog items, categories, and vegetarian flags.
{% enddocs %}

{% docs fct_orders_doc %}
Core transaction fact table detailing order timestamps, delivery duration, delivery status, and financial order totals.
{% enddocs %}

{% docs fct_order_items_doc %}
Granular transaction fact table linking individual menu item sales to parent orders.
{% enddocs %}

{% docs mart_daily_revenue_doc %}
Executive Gold Mart detailing daily revenue performance, Gross Merchandise Value (GMV), Average Order Value (AOV), and cancellation rates aggregated by city and order date.
{% enddocs %}

{% docs mart_delivery_performance_doc %}
Operations Gold Mart analyzing delivery speed SLAs, average duration, P50 (median), and P90 delivery metrics broken down by city and peak order hour.
{% enddocs %}

{% docs mart_review_insights_doc %}
Customer Experience Gold Mart consolidating customer ratings, sentiment analysis counts (positive, neutral, negative), and review volume per restaurant.
{% enddocs %}
