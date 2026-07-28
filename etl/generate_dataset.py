from pathlib import Path
import csv
import random
from datetime import date, timedelta, datetime

# ----------------------------
# Configuration
# ----------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

CUSTOMER_COUNT = 200
SUPPLIER_COUNT = 10
CATEGORY_COUNT = 20
PRODUCT_COUNT = 100
ORDER_COUNT = 500
MIN_ITEMS_PER_ORDER = 2
MAX_ITEMS_PER_ORDER = 4

random.seed(42)

# --------------------------------------------------
# DATA POOLS
# --------------------------------------------------

random.seed(42)

first_names = [
    "Ava", "Liam", "Sophia", "Noah", "Mia", "Ethan", "Olivia", "James",
    "Emma", "Lucas", "Isabella", "Benjamin", "Amelia", "Mason", "Harper",
    "Elijah", "Charlotte", "Logan", "Evelyn", "Henry", "Harley", "Leo"
]

last_names = [
    "Thompson", "Carter", "Reed", "Brooks", "Patel", "Gray", "Stone",
    "Hall", "Walker", "Green", "Adams", "Ward", "Baker", "Turner",
    "Phillips", "Evans", "Cooper", "Murphy", "Rivera", "Bennett"
]

cities_states = [
    ("Austin", "Texas"), ("Dallas", "Texas"), ("Miami", "Florida"),
    ("Seattle", "Washington"), ("Chicago", "Illinois"), ("Denver", "Colorado"),
    ("Boston", "Massachusetts"), ("Phoenix", "Arizona"), ("Atlanta", "Georgia"),
    ("San Diego", "California"), ("Portland", "Oregon"), ("Houston", "Texas")
]

countries = ["USA", "Canada", "UK", "Germany", "France", "Australia"]

category_names = [
    "Electronics", "Home & Kitchen", "Fashion", "Beauty", "Sports",
    "Books", "Toys", "Grocery", "Automotive", "Health",
    "Office Supplies", "Garden", "Baby", "Pets", "Tools",
    "Furniture", "Jewelry", "Music", "Gaming", "Accessories"
]

supplier_adjectives = [
    "Nova", "Urban", "Prime", "Blue", "Global", "Metro", "Pioneer", "Peak",
    "Core", "Summit", "Vertex", "Orbit", "Apex", "Nimbus", "Bright"
]

supplier_nouns = [
    "Supply", "Goods", "Trade", "Source", "Market", "Works", "Imports",
    "Holdings", "Distribution", "Partners", "Logistics", "Wholesale"
]

product_adjectives = [
    "Wireless", "Portable", "Smart", "Compact", "Premium", "Deluxe",
    "Advanced", "Eco", "Multi", "Ultra", "Pro", "Essential"
]

product_nouns = [
    "Headphones", "Speaker", "Lamp", "Blender", "Backpack", "Shoes",
    "Serum", "Mat", "Mug", "Chair", "Watch", "Keyboard", "Mouse",
    "Bottle", "Jacket", "Camera", "Vacuum", "Brush", "Desk", "Set"
]

payment_methods = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]
payment_statuses = ["paid", "pending", "failed"]
order_statuses = ["delivered", "shipped", "processing"]
review_texts = [
    "Great quality and fast shipping.",
    "Exactly what I needed.",
    "Good value for the price.",
    "Works well and feels durable.",
    "Would buy again.",
    "The product matched the description.",
    "Solid performance overall.",
    "Packaging could be better, but the item is good."
]

return_reasons = [
    "Wrong item received",
    "Damaged on arrival",
    "Does not match description",
    "Changed mind",
    "Defective product"
]


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def random_signup_date():
    start = date(2023, 1, 1)
    end = date(2025, 12, 31)

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))

def random_order_datetime():
    start = datetime(2025, 1, 1, 8, 0, 0)
    end = datetime(2025, 12, 31, 20, 0, 0)

    delta = end - start

    seconds = random.randint(0, int(delta.total_seconds()))

    return start + timedelta(seconds=seconds)

def payment_datetime(order_datetime):
    return order_datetime + timedelta(
        minutes=random.randint(1, 30)
    )

# --------------------------------------------------------------
# Categories
# --------------------------------------------------------------
with open(DATA_DIR / "categories.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "category_id",
        "category_name"
    ])

    for category_id, category_name in enumerate(category_names, start=1):
        writer.writerow([
            category_id,
            category_name
        ])

print("✔ categories.csv created")

# -------------------------------------------------------------
# Suppliers
# -------------------------------------------------------------


with open(DATA_DIR / "suppliers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "supplier_id",
        "supplier_name",
        "country"
    ])

    for supplier_id in range(1, 201):

        supplier_name = (
            f"{random.choice(supplier_adjectives)} "
            f"{random.choice(supplier_nouns)} "
            f"{supplier_id:03d}"
        )

        writer.writerow([
            supplier_id,
            supplier_name,
            random.choice(countries)
        ])

print("✔ suppliers.csv created")

# --------------------------------------------------
# Customers
# --------------------------------------------------

with open(DATA_DIR / "customers.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "customer_id",
        "full_name",
        "email",
        "gender",
        "city",
        "state",
        "country",
        "signup_date"
    ])

    for customer_id in range(1, CUSTOMER_COUNT + 1):

        first = random.choice(first_names)
        last = random.choice(last_names)

        full_name = f"{first} {last}"

        email = f"{first.lower()}.{last.lower()}{customer_id}@example.com"

        city, state = random.choice(cities_states)

        gender = random.choice(["Male", "Female"])

        writer.writerow([
            customer_id,
            full_name,
            email,
            gender,
            city,
            state,
            "USA",
            random_signup_date()
        ])

print("✔ customers.csv created")

# --------------------------------------------------
# Products
# --------------------------------------------------

with open(DATA_DIR / "products.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "product_id",
        "category_id",
        "supplier_id",
        "product_name",
        "brand",
        "cost_price",
        "selling_price",
        "stock",
        "is_active"
    ])

    product_prices = {}

    for product_id in range(1, PRODUCT_COUNT + 1):

        category_id = random.randint(1, CATEGORY_COUNT)
        supplier_id = random.randint(1, SUPPLIER_COUNT)

        product_name = (
            f"{random.choice(product_adjectives)} "
            f"{random.choice(product_nouns)}"
        )

        brand = f"Brand {random.randint(1,50)}"

        cost_price = round(random.uniform(5, 150), 2)

        selling_price = round(cost_price * random.uniform(1.20, 2.50), 2)

        product_prices[product_id] = selling_price

        stock = random.randint(0, 500)

        is_active = random.choice([True, True, True, True, False])

        writer.writerow([
            product_id,
            category_id,
            supplier_id,
            product_name,
            brand,
            cost_price,
            selling_price,
            stock,
            is_active
        ])

print("✔ products.csv created")

# -------------------------------------------------------------------------
# Orders
# -------------------------------------------------------------------------

orders = []
order_items = []
order_item_id = 1

for order_id in range(1, ORDER_COUNT + 1):

    customer_id = random.randint(1, CUSTOMER_COUNT)

    order_date = random_order_datetime()

    status = random.choices(
        ["delivered", "shipped", "processing"],
        weights=[70,20,10]
    )[0]

    shipping_cost = round(random.uniform(4.99,12.99),2)

    discount = round(random.uniform(0,25),2)

    subtotal = 0

    number_of_items = random.randint(
        MIN_ITEMS_PER_ORDER,
        MAX_ITEMS_PER_ORDER
    )

    selected_products = random.sample(
        range(1, PRODUCT_COUNT + 1),
        number_of_items
    )

    for product_id in selected_products:

        quantity = random.randint(1,3)

        unit_price = product_prices[product_id]

        subtotal += quantity * unit_price

        order_items.append([
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ])

        order_item_id += 1

    total_amount = round(
        subtotal + shipping_cost - discount,
        2
    )

    orders.append([
        order_id,
        customer_id,
        order_date,
        status,
        shipping_cost,
        discount,
        total_amount
    ])

with open(DATA_DIR / "orders.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "order_id",
        "customer_id",
        "order_date",
        "status",
        "shipping_cost",
        "discount",
        "total_amount"
    ])

    writer.writerows(orders)

print("✔ orders.csv created")

with open(DATA_DIR / "order_items.csv",
          "w",
          newline="",
          encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price"
    ])

    writer.writerows(order_items)

print("✔ order_items.csv created")

# --------------------------------------------------
# Payments
# --------------------------------------------------

payments = []

payment_id = 1

for order in orders:

    (
        order_id,
        customer_id,
        order_date,
        status,
        shipping_cost,
        discount,
        total_amount
    ) = order

    if status == "delivered":
        payment_status = "paid"

    elif status == "shipped":
        payment_status = random.choice(["paid", "paid", "pending"])

    else:
        payment_status = random.choice(["pending", "failed"])

    payments.append([
        payment_id,
        order_id,
        random.choice(payment_methods),
        payment_status,
        payment_datetime(order_date),
        total_amount
    ])

    payment_id += 1

with open(DATA_DIR / "payments.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "payment_id",
        "order_id",
        "payment_method",
        "payment_status",
        "payment_date",
        "amount"
    ])

    writer.writerows(payments)

print("✔ payments.csv created")

# --------------------------------------------------
# Returns
# --------------------------------------------------

returns = []

return_id = 1

for order in orders:

    (
        order_id,
        customer_id,
        order_date,
        status,
        shipping_cost,
        discount,
        total_amount
    ) = order

    if status == "delivered":

        if random.random() < 0.08:

            returns.append([
                return_id,
                order_id,
                random.choice(return_reasons),
                round(total_amount * random.uniform(0.5, 1.0), 2),
                order_date + timedelta(days=random.randint(3, 21))
            ])

            return_id += 1

with open(DATA_DIR / "returns.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "return_id",
        "order_id",
        "reason",
        "refund_amount",
        "return_date"
    ])

    writer.writerows(returns)

print("✔ returns.csv created")

order_lookup = {
    order[0]: order
    for order in orders
}

# --------------------------------------------------
# Reviews
# --------------------------------------------------

reviews = []

review_id = 1

for item in order_items:

    (
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price
    ) = item

    order = order_lookup[order_id]

    customer_id = order[1]

    status = order[3]

    order_date = order[2]

    if status == "delivered":

        if random.random() < 0.35:

            reviews.append([
                review_id,
                customer_id,
                product_id,
                random.randint(3, 5),
                random.choice(review_texts),
                order_date + timedelta(days=random.randint(5, 40))
            ])

            review_id += 1
            
with open(DATA_DIR / "reviews.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "review_id",
        "customer_id",
        "product_id",
        "rating",
        "review_text",
        "review_date"
    ])

    writer.writerows(reviews)

print("✔ reviews.csv created")