import os
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_zomato_dataset(output_dir="data/raw", force=False):
    os.makedirs(output_dir, exist_ok=True)
    orders_file = os.path.join(output_dir, "orders.csv")

    # Check if data already exists and force flag is not set
    if os.path.exists(orders_file) and not force:
        print(
            f"ℹ️ Base dataset already exists in '{output_dir}'. Skipping baseline dataset generation."
        )
        print(
            "   (Tip: Use force=True or run scripts/generate_daily_incremental_data.py for incremental batching)"
        )
        return

    random.seed(42)

    # 1. Restaurants
    cities = [
        "Mumbai",
        "Delhi",
        "Bengaluru",
        "Hyderabad",
        "Pune",
        "Chennai",
        "Kolkata",
    ]
    cuisines = [
        "North Indian",
        "South Indian",
        "Chinese",
        "Fast Food",
        "Italian",
        "Biryani",
        "Desserts",
        "Street Food",
    ]
    restaurant_names = [
        "Spice Garden",
        "Royal Biryani House",
        "Dragon Wok",
        "Pizza Paradiso",
        "Tandoori Nights",
        "Sagar Ratna",
        "The Great Indian Thali",
        "Burger Bistro",
        "Urban Cafe",
        "Flavors of Punjab",
        "Subway Express",
        "Baskin Robbins",
        "Dosa Plaza",
        "Mainland China",
        "Kabab Corner",
        "Green Bowl Salads",
        "Momo Station",
        "Chai Point",
        "Curry Leaf",
        "Pasta Fresca",
    ]

    restaurants = []
    for i, name in enumerate(restaurant_names, start=1):
        city = random.choice(cities)
        rating = round(random.uniform(3.2, 4.9), 1)
        votes = random.randint(50, 4500)
        # Intentionally messy cost formatting to mimic real raw Zomato data ("₹ 400" or "--" or "350")
        raw_cost = f"₹ {random.randint(2, 12) * 100}" if random.random() > 0.1 else "--"
        cuisine = random.choice(cuisines)
        restaurants.append(
            {
                "restaurant_id": i,
                "name": f"{name} ({city})",
                "city": city,
                "rating": rating,
                "votes": votes,
                "cost_for_two": raw_cost,
                "cuisine": cuisine,
            }
        )
    df_restaurants = pd.DataFrame(restaurants)
    df_restaurants.to_csv(os.path.join(output_dir, "restaurants.csv"), index=False)

    # 2. Users
    first_names = [
        "Aarav",
        "Ananya",
        "Rohan",
        "Priya",
        "Rahul",
        "Neha",
        "Vikram",
        "Sneha",
        "Amit",
        "Kavya",
        "Arjun",
        "Diya",
        "Karan",
        "Pooja",
        "Siddharth",
        "Meera",
        "Varun",
        "Riya",
        "Aditya",
        "Ishita",
    ]
    last_names = [
        "Sharma",
        "Verma",
        "Patel",
        "Reddy",
        "Gupta",
        "Nair",
        "Singh",
        "Rao",
        "Joshi",
        "Kumar",
    ]

    users = []
    for i in range(1, 101):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        # Raw emails with mixed cases and whitespace
        email = f" {fn.lower()}.{ln.lower()}{random.randint(10,99)}@Example.Com "
        age = random.randint(18, 65)
        gender = random.choice(["Male", "Female", "Other"])
        city = random.choice(cities)
        signup_date = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime(
            "%Y-%m-%d"
        )
        users.append(
            {
                "user_id": i,
                "name": f"{fn} {ln}",
                "email": email,
                "age": age,
                "gender": gender,
                "city": city,
                "signup_date": signup_date,
            }
        )
    df_users = pd.DataFrame(users)
    df_users.to_csv(os.path.join(output_dir, "users.csv"), index=False)

    # 3. Food Items
    food_items = [
        ("Butter Chicken", "Main Course", 0),
        ("Paneer Butter Masala", "Main Course", 1),
        ("Hyderabadi Chicken Biryani", "Biryani", 0),
        ("Veg Dum Biryani", "Biryani", 1),
        ("Margherita Pizza", "Pizza", 1),
        ("Pepperoni Pizza", "Pizza", 0),
        ("Hakkaa Noodles", "Chinese", 1),
        ("Chicken Steamed Momos", "Starters", 0),
        ("Masala Dosa", "South Indian", 1),
        ("Gulab Jamun (2 pcs)", "Dessert", 1),
        ("Chocolate Lava Cake", "Dessert", 1),
        ("Cold Coffee", "Beverages", 1),
        ("Garlic Naan", "Breads", 1),
        ("Tandoori Chicken (Half)", "Starters", 0),
        ("Crispy Corn", "Starters", 1),
    ]
    food_list = []
    for i, (item, cat, is_veg) in enumerate(food_items, start=1):
        food_list.append({"food_id": i, "item_name": item, "category": cat, "is_veg": is_veg})
    df_food = pd.DataFrame(food_list)
    df_food.to_csv(os.path.join(output_dir, "food.csv"), index=False)

    # 4. Menu (Mapping restaurants to food items with custom prices)
    menu_list = []
    menu_id = 1
    for r in restaurants:
        r_id = r["restaurant_id"]
        # Sample 5 to 10 food items for each restaurant
        available_food = random.sample(food_list, random.randint(5, 10))
        for f in available_food:
            base_price = random.randint(120, 480)
            menu_list.append(
                {
                    "menu_id": menu_id,
                    "restaurant_id": r_id,
                    "food_id": f["food_id"],
                    "price": base_price,
                }
            )
            menu_id += 1
    df_menu = pd.DataFrame(menu_list)
    df_menu.to_csv(os.path.join(output_dir, "menu.csv"), index=False)

    # 5 & 6. Orders and Order Items
    statuses = ["DELIVERED", "DELIVERED", "DELIVERED", "DELIVERED", "CANCELLED"]
    orders = []
    order_items = []
    order_item_id = 1

    start_date = datetime(2024, 1, 1)
    end_date = datetime.now()
    total_days = max(1, (end_date - start_date).days)

    for order_id in range(1, 1501):
        user = random.choice(users)
        restaurant = random.choice(restaurants)
        r_id = restaurant["restaurant_id"]

        # Restaurant menu items
        r_menu = df_menu[df_menu["restaurant_id"] == r_id]
        if r_menu.empty:
            continue

        order_dt = start_date + timedelta(
            days=random.randint(0, total_days),
            hours=random.randint(10, 22),
            minutes=random.randint(0, 59),
        )
        if order_dt > end_date:
            order_dt = end_date - timedelta(minutes=random.randint(5, 120))

        status = random.choice(statuses)

        if status == "DELIVERED":
            delivery_dt = order_dt + timedelta(minutes=random.randint(20, 65))
            delivery_str = delivery_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            delivery_str = None

        # Sample order items
        num_items = random.randint(1, 4)
        chosen_items = r_menu.sample(n=min(num_items, len(r_menu)))

        total_amount = 0.0
        for _, m_row in chosen_items.iterrows():
            qty = random.randint(1, 3)
            price = float(m_row["price"])
            total_amount += qty * price
            order_items.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "food_id": m_row["food_id"],
                    "quantity": qty,
                    "item_price": price,
                }
            )
            order_item_id += 1

        orders.append(
            {
                "order_id": order_id,
                "user_id": user["user_id"],
                "restaurant_id": r_id,
                "order_timestamp": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "delivery_timestamp": delivery_str,
                "order_status": status,
                "total_amount": round(total_amount, 2),
            }
        )

    df_orders = pd.DataFrame(orders)
    df_orders.to_csv(os.path.join(output_dir, "orders.csv"), index=False)

    df_order_items = pd.DataFrame(order_items)
    df_order_items.to_csv(os.path.join(output_dir, "order_items.csv"), index=False)

    # 7. Reviews (Free-text feedback for AI LLM enrichment & RAG)
    positive_reviews = [
        "Food was piping hot and super fresh! Excellent delivery speed.",
        ("The Biryani flavor was authentic and delicious. Packaging was" " clean and leak-proof."),
        "Amazing taste and great portion sizes! Will definitely order again.",
        "Best butter chicken in town! Delivered 10 minutes early.",
        "Very crisp crust pizza, fresh toppings. Highly recommended!",
    ]
    neutral_reviews = [
        "Food taste was average, nothing special. Delivery took around 45 minutes.",
        "Portion size could be bigger for the price charged. Okay overall.",
        "Decent taste, but gravy was slightly spilled inside the box.",
        "Food was warm but Naan became a bit chewy during transit.",
    ]
    negative_reviews = [
        "Horrible experience! Food was cold and delivery took over an hour.",
        "Very oily curry and completely missing garlic naan from my order!",
        "Extremely disappointing packaging. Everything was spilled everywhere.",
        "Food tasted stale and smelled bad. Never ordering from here again.",
        ("Rude delivery agent and delayed by 40 minutes with no tracking" " updates."),
    ]

    reviews = []
    delivered_orders = df_orders[df_orders["order_status"] == "DELIVERED"]
    sampled_orders = delivered_orders.sample(n=min(500, len(delivered_orders)))

    for rev_id, (_, ord_row) in enumerate(sampled_orders.iterrows(), start=1):
        rand_val = random.random()
        if rand_val < 0.55:
            text = random.choice(positive_reviews)
            rating = random.randint(4, 5)
        elif rand_val < 0.80:
            text = random.choice(neutral_reviews)
            rating = 3
        else:
            text = random.choice(negative_reviews)
            rating = random.randint(1, 2)

        reviews.append(
            {
                "review_id": rev_id,
                "order_id": ord_row["order_id"],
                "user_id": ord_row["user_id"],
                "restaurant_id": ord_row["restaurant_id"],
                "review_text": text,
                "star_rating": rating,
                "review_date": ord_row["order_timestamp"],
            }
        )

    df_reviews = pd.DataFrame(reviews)
    df_reviews.to_csv(os.path.join(output_dir, "reviews.csv"), index=False)

    print(f"✅ Successfully generated Zomato dataset in '{output_dir}':")
    print(f"   - restaurants.csv: {len(df_restaurants)} rows")
    print(f"   - users.csv: {len(df_users)} rows")
    print(f"   - food.csv: {len(df_food)} rows")
    print(f"   - menu.csv: {len(df_menu)} rows")
    print(f"   - orders.csv: {len(df_orders)} rows")
    print(f"   - order_items.csv: {len(df_order_items)} rows")
    print(f"   - reviews.csv: {len(df_reviews)} rows")


if __name__ == "__main__":
    generate_zomato_dataset()
