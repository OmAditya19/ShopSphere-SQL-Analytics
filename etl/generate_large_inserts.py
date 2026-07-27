from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from pathlib import Path

# --------------------------------------------------
# CONFIG
# Start smaller for testing, then scale up.
# --------------------------------------------------
SEED = 42
CUSTOMER_COUNT = 200
CATEGORY_COUNT = 5
SUPPLIER_COUNT = 10
PRODUCT_COUNT = 100
ORDER_COUNT = 500
TARGET_RETURN_COUNT = 30
TARGET_REVIEW_COUNT = 150
BATCH_SIZE = 50

ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "sql" / "02_insert_data.sql"


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def sql(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, date) and not isinstance(v, datetime):
        return f"'{v.isoformat()}'"
    if isinstance(v, datetime):
        return f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'"
    return "'" + str(v).replace("'", "''") + "'"


def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


class BatchWriter:
    def __init__(self, fp, table: str, columns: list[str], batch_size: int = 1000):
        self.fp = fp
        self.table = table
        self.columns = columns
        self.batch_size = batch_size
        self.rows: list[tuple[str, ...]] = []

    def add(self, *values: str) -> None:
        self.rows.append(values)
        if len(self.rows) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        if not self.rows:
            return
        cols = ", ".join(self.columns)
        values = ",\n".join("(" + ", ".join(row) + ")" for row in self.rows)
        self.fp.write(f"INSERT INTO {self.table} ({cols}) VALUES\n{values};\n\n")
        self.rows.clear()


def write_simple_insert(fp, table: str, columns: list[str], rows: list[tuple]) -> None:
    values = ",\n".join("(" + ", ".join(sql(v) for v in row) + ")" for row in rows)
    cols = ", ".join(columns)
    fp.write(f"INSERT INTO {table} ({cols}) VALUES\n{values};\n\n")


# --------------------------------------------------
# DATA POOLS
# --------------------------------------------------
random.seed(SEED)

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
# GENERATE DIMENSIONS
# --------------------------------------------------
categories = [(i, category_names[i - 1]) for i in range(1, CATEGORY_COUNT + 1)]

suppliers = []
for i in range(1, SUPPLIER_COUNT + 1):
    supplier_name = f"{random.choice(supplier_adjectives)} {random.choice(supplier_nouns)} {i:03d}"
    country = random.choice(countries)
    suppliers.append((i, supplier_name, country))

customers = []
for i in range(1, CUSTOMER_COUNT + 1):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    full_name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
    gender = random.choice(["Male", "Female"])
    city, state = random.choice(cities_states)
    country = "USA"
    signup_dt = date(2024, 1, 1) + timedelta(days=random.randint(0, 730))
    customers.append((i, full_name, email, gender, city, state, country, signup_dt))

products = []
product_price_by_id: dict[int, float] = {}
for i in range(1, PRODUCT_COUNT + 1):
    category_id = random.randint(1, CATEGORY_COUNT)
    supplier_id = random.randint(1, SUPPLIER_COUNT)
    product_name = f"{random.choice(product_adjectives)} {random.choice(product_nouns)}"
    brand = f"Brand{random.randint(1, 120)}"
    cost_price = round(random.uniform(5, 120), 2)
    selling_price = round(cost_price * random.uniform(1.2, 2.5), 2)
    stock = random.randint(0, 500)
    is_active = random.random() > 0.02
    products.append(
        (i, category_id, supplier_id, product_name, brand, cost_price, selling_price, stock, is_active)
    )
    product_price_by_id[i] = selling_price


# --------------------------------------------------
# WRITE SQL
# --------------------------------------------------
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUT_FILE.open("w", encoding="utf-8") as fp:
    fp.write("BEGIN;\n\n")

    # Reference tables
    write_simple_insert(fp, "categories", ["category_id", "category_name"], categories)
    write_simple_insert(fp, "suppliers", ["supplier_id", "supplier_name", "country"], suppliers)
    write_simple_insert(
        fp,
        "customers",
        ["customer_id", "full_name", "email", "gender", "city", "state", "country", "signup_date"],
        customers,
    )
    write_simple_insert(
        fp,
        "products",
        ["product_id", "category_id", "supplier_id", "product_name", "brand", "cost_price", "selling_price", "stock", "is_active"],
        products,
    )

    # Fact tables streamed in batches
    orders_writer = BatchWriter(
        fp,
        "orders",
        ["order_id", "customer_id", "order_date", "status", "shipping_cost", "discount", "total_amount"],
        BATCH_SIZE,
    )
    order_items_writer = BatchWriter(
        fp,
        "order_items",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        BATCH_SIZE,
    )
    payments_writer = BatchWriter(
        fp,
        "payments",
        ["payment_id", "order_id", "payment_method", "payment_status", "payment_date", "amount"],
        BATCH_SIZE,
    )
    returns_writer = BatchWriter(
        fp,
        "returns",
        ["return_id", "order_id", "reason", "refund_amount", "return_date"],
        BATCH_SIZE,
    )

    order_totals: dict[int, float] = {}
    delivered_orders: list[int] = []
    review_candidates: set[tuple[int, int]] = set()

    order_start = datetime(2025, 1, 1, 8, 0, 0)
    order_end = datetime(2025, 12, 31, 20, 0, 0)

    return_id = 1
    order_item_id = 1
    payment_id = 1

    for order_id in range(1, ORDER_COUNT + 1):
        customer_id = random.randint(1, CUSTOMER_COUNT)
        order_date = random_datetime(order_start, order_end)
        status = random.choices(order_statuses, weights=[70, 20, 10], k=1)[0]

        # 2–4 unique products per order gives you ~300k order_items at 100k orders
        item_count = random.randint(2, 4)
        chosen_products = random.sample(products, item_count)

        subtotal = 0.0
        for product in chosen_products:
            product_id = product[0]
            unit_price = float(product[6])  # selling_price
            quantity = random.randint(1, 3)
            subtotal += quantity * unit_price

            order_items_writer.add(
                sql(order_item_id),
                sql(order_id),
                sql(product_id),
                sql(quantity),
                sql(unit_price),
            )
            order_item_id += 1

            if status == "delivered":
                review_candidates.add((customer_id, product_id))

        shipping_cost = round(random.uniform(3.99, 9.99), 2)
        discount_rate = random.choices([0.00, 0.05, 0.10, 0.15], weights=[45, 30, 15, 10], k=1)[0]
        discount = round(min(subtotal * discount_rate, 20.00), 2)
        total_amount = round(subtotal + shipping_cost - discount, 2)

        orders_writer.add(
            sql(order_id),
            sql(customer_id),
            sql(order_date),
            sql(status),
            sql(shipping_cost),
            sql(discount),
            sql(total_amount),
        )

        order_totals[order_id] = total_amount

        payment_status = "paid" if status in ("delivered", "shipped") else "pending"
        payment_method = random.choice(payment_methods)

        payments_writer.add(
            sql(payment_id),
            sql(order_id),
            sql(payment_method),
            sql(payment_status),
            sql(order_date + timedelta(minutes=random.randint(3, 60))),
            sql(total_amount),
        )
        payment_id += 1

        if status == "delivered":
            delivered_orders.append(order_id)

        # ~8% return rate on delivered orders
        if status == "delivered" and random.random() < 0.08:
            refund_amount = round(total_amount * random.uniform(0.5, 1.0), 2)
            return_date = order_date + timedelta(days=random.randint(2, 21))
            returns_writer.add(
                sql(return_id),
                sql(order_id),
                sql(random.choice(return_reasons)),
                sql(refund_amount),
                sql(return_date),
            )
            return_id += 1

        if order_id % 10_000 == 0:
            print(f"Generated {order_id:,} orders...")

    # Flush remaining fact rows
    orders_writer.flush()
    order_items_writer.flush()
    payments_writer.flush()
    returns_writer.flush()

    # Reviews
    review_writer = BatchWriter(
        fp,
        "reviews",
        ["review_id", "customer_id", "product_id", "rating", "review_text", "review_date"],
        BATCH_SIZE,
    )

    review_pairs = list(review_candidates)
    random.shuffle(review_pairs)
    review_count = min(TARGET_REVIEW_COUNT, len(review_pairs))

    review_start = datetime(2025, 2, 1, 9, 0, 0)
    review_end = datetime(2025, 12, 31, 18, 0, 0)

    for review_id, (customer_id, product_id) in enumerate(review_pairs[:review_count], start=1):
        review_writer.add(
            sql(review_id),
            sql(customer_id),
            sql(product_id),
            sql(random.randint(1, 5)),
            sql(random.choice(review_texts)),
            sql(random_datetime(review_start, review_end)),
        )

    review_writer.flush()

    fp.write("COMMIT;\n")

print(f"Done. SQL written to: {OUT_FILE}")
