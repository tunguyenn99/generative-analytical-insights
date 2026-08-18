import os
import sys
import random
import pandas as pd
from datetime import datetime, timedelta

# Ensure project root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DATA_DIR = "data/raw"


def generate_daily_incremental_data(num_new_orders=30, num_new_users=3):
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.now()

    # Load existing CSVs or generate full dataset if missing
    orders_file = os.path.join(DATA_DIR, "orders.csv")
    order_items_file = os.path.join(DATA_DIR, "order_items.csv")
    reviews_file = os.path.join(DATA_DIR, "reviews.csv")
    users_file = os.path.join(DATA_DIR, "users.csv")
    restaurants_file = os.path.join(DATA_DIR, "restaurants.csv")
    menu_file = os.path.join(DATA_DIR, "menu.csv")

    if not os.path.exists(orders_file):
        from generate_sample_data import generate_zomato_dataset

        generate_zomato_dataset(DATA_DIR)

    df_orders = pd.read_csv(orders_file)
    df_order_items = pd.read_csv(order_items_file)
    df_reviews = pd.read_csv(reviews_file)
    df_users = pd.read_csv(users_file)
    df_restaurants = pd.read_csv(restaurants_file)
    df_menu = pd.read_csv(menu_file)

    max_order_id = int(df_orders["order_id"].max()) if not df_orders.empty else 0
    max_order_item_id = (
        int(df_order_items["order_item_id"].max()) if not df_order_items.empty else 0
    )
    max_review_id = int(df_reviews["review_id"].max()) if not df_reviews.empty else 0
    max_user_id = int(df_users["user_id"].max()) if not df_users.empty else 0

    print(f"📅 Generating incremental daily batch data for {today.strftime('%Y-%m-%d')}...")

    # 1. Generate New Daily Users
    first_names = ["Aarav", "Ananya", "Rohan", "Priya", "Rahul", "Neha", "Vikram", "Sneha"]
    last_names = ["Sharma", "Verma", "Patel", "Reddy", "Gupta", "Nair", "Singh", "Kumar"]
    cities = list(df_restaurants["city"].unique())

    new_users = []
    for i in range(1, num_new_users + 1):
        uid = max_user_id + i
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        new_users.append(
            {
                "user_id": uid,
                "name": f"{fn} {ln}",
                "email": f"{fn.lower()}.{ln.lower()}{uid}@example.com",
                "age": random.randint(20, 55),
                "gender": random.choice(["Male", "Female", "Other"]),
                "city": random.choice(cities),
                "signup_date": today.strftime("%Y-%m-%d"),
            }
        )
    df_new_users = pd.DataFrame(new_users)
    df_users_updated = pd.concat([df_users, df_new_users], ignore_index=True)
    df_users_updated.to_csv(users_file, index=False)
    print(f"  ├─ Appended {len(new_users)} new users.")

    # 2. Generate New Daily Orders & Items
    all_users = list(df_users_updated["user_id"].unique())
    all_restaurants = df_restaurants.to_dict(orient="records")
    statuses = ["DELIVERED", "DELIVERED", "DELIVERED", "DELIVERED", "CANCELLED"]

    new_orders = []
    new_order_items = []
    curr_item_id = max_order_item_id + 1

    for i in range(1, num_new_orders + 1):
        order_id = max_order_id + i
        user_id = random.choice(all_users)
        restaurant = random.choice(all_restaurants)
        r_id = restaurant["restaurant_id"]

        r_menu = df_menu[df_menu["restaurant_id"] == r_id]
        if r_menu.empty:
            continue

        order_dt = today.replace(
            hour=random.randint(11, 22), minute=random.randint(0, 59), second=random.randint(0, 59)
        )
        status = random.choice(statuses)

        if status == "DELIVERED":
            delivery_dt = order_dt + timedelta(minutes=random.randint(18, 55))
            delivery_str = delivery_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            delivery_str = None

        chosen_items = r_menu.sample(n=min(random.randint(1, 3), len(r_menu)))
        total_amount = 0.0

        for _, m_row in chosen_items.iterrows():
            qty = random.randint(1, 3)
            price = float(m_row["price"])
            total_amount += qty * price

            new_order_items.append(
                {
                    "order_item_id": curr_item_id,
                    "order_id": order_id,
                    "food_id": m_row["food_id"],
                    "quantity": qty,
                    "item_price": price,
                }
            )
            curr_item_id += 1

        new_orders.append(
            {
                "order_id": order_id,
                "user_id": user_id,
                "restaurant_id": r_id,
                "order_timestamp": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "delivery_timestamp": delivery_str,
                "order_status": status,
                "total_amount": round(total_amount, 2),
            }
        )

    df_new_orders = pd.DataFrame(new_orders)
    df_orders_updated = pd.concat([df_orders, df_new_orders], ignore_index=True)
    df_orders_updated.to_csv(orders_file, index=False)

    df_new_items = pd.DataFrame(new_order_items)
    df_order_items_updated = pd.concat([df_order_items, df_new_items], ignore_index=True)
    df_order_items_updated.to_csv(order_items_file, index=False)

    print(f"  ├─ Appended {len(new_orders)} new orders & {len(new_order_items)} order items.")

    # 3. Generate New Daily Customer Reviews
    positive_reviews = [
        "Super fast delivery! Food was still sizzling hot.",
        "Delicious meal as always. Highly satisfied!",
        "Great portion size and clean packaging.",
    ]
    negative_reviews = [
        "Delivery took over an hour, food was cold.",
        "Missing an item from my order. Disappointed.",
    ]

    delivered_new_orders = df_new_orders[df_new_orders["order_status"] == "DELIVERED"]
    new_reviews = []
    curr_review_id = max_review_id + 1

    for _, ord_row in delivered_new_orders.iterrows():
        if random.random() < 0.6:  # 60% chance to leave review
            is_pos = random.random() > 0.3
            text = random.choice(positive_reviews if is_pos else negative_reviews)
            rating = random.randint(4, 5) if is_pos else random.randint(1, 2)

            new_reviews.append(
                {
                    "review_id": curr_review_id,
                    "order_id": ord_row["order_id"],
                    "user_id": ord_row["user_id"],
                    "restaurant_id": ord_row["restaurant_id"],
                    "review_text": text,
                    "star_rating": rating,
                    "review_date": ord_row["order_timestamp"],
                }
            )
            curr_review_id += 1

    df_new_reviews = pd.DataFrame(new_reviews)
    df_reviews_updated = pd.concat([df_reviews, df_new_reviews], ignore_index=True)
    df_reviews_updated.to_csv(reviews_file, index=False)
    print(f"  └─ Appended {len(new_reviews)} new customer reviews.")

    print(
        f"✅ Incremental daily dataset updated! Total orders: {len(df_orders_updated)}, Total reviews: {len(df_reviews_updated)}"
    )


if __name__ == "__main__":
    generate_daily_incremental_data()
