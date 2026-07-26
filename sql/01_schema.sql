CREATE TABLE Categories (
  category_id int PRIMARY KEY,
  category_name varchar(100) UNIQUE NOT NULL
);

CREATE TABLE Suppliers (
  supplier_id int PRIMARY KEY,
  supplier_name varchar(100) UNIQUE NOT NULL,
  country varchar(80)
);

CREATE TABLE Customers (
  customer_id int PRIMARY KEY,
  full_name varchar(150) NOT NULL,
  email varchar(150) UNIQUE NOT NULL,
  gender varchar(20),
  city varchar(80),
  state varchar(80),
  country varchar(80),
  signup_date date NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Products (
  product_id int PRIMARY KEY,
  category_id int NOT NULL REFERENCES Categories(category_id),
  supplier_id int NOT NULL REFERENCES Suppliers(supplier_id),
  product_name varchar(150) NOT NULL,
  brand varchar(100),
  cost_price decimal(10,2) NOT NULL,
  selling_price decimal(10,2) NOT NULL,
  stock int NOT NULL DEFAULT 0,
  is_active boolean NOT NULL DEFAULT true,
  CONSTRAINT chk_product_prices CHECK (cost_price >= 0 AND selling_price >= 0),
  CONSTRAINT chk_product_stock CHECK (stock >= 0)
);

CREATE TABLE Orders (
  order_id int PRIMARY KEY,
  customer_id int NOT NULL REFERENCES Customers(customer_id),
  order_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status varchar(30) NOT NULL,
  shipping_cost decimal(10,2) NOT NULL DEFAULT 0,
  discount decimal(10,2) NOT NULL DEFAULT 0,
  total_amount decimal(12,2) NOT NULL,
  CONSTRAINT chk_order_amounts CHECK (shipping_cost >= 0 AND discount >= 0 AND total_amount >= 0)
);

CREATE TABLE Order_items (
  order_item_id int PRIMARY KEY,
  order_id int UNIQUE NOT NULL REFERENCES Orders(order_id),
  product_id int UNIQUE NOT NULL REFERENCES Products(product_id),
  quantity int NOT NULL,
  unit_price decimal(10,2) NOT NULL,
  CONSTRAINT chk_order_items_quantity CHECK (quantity > 0),
  CONSTRAINT chk_order_items_price CHECK (unit_price >= 0)
);

CREATE TABLE Payments (
  payment_id int PRIMARY KEY,
  order_id int UNIQUE NOT NULL REFERENCES Orders(order_id),
  payment_method varchar(40) NOT NULL,
  payment_status varchar(30) NOT NULL,
  payment_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  amount decimal(12,2) NOT NULL,
  CONSTRAINT chk_payment_amount CHECK (amount >= 0)
);

CREATE TABLE Returns (
  return_id int PRIMARY KEY,
  order_id int UNIQUE NOT NULL REFERENCES Orders(order_id),
  reason varchar(255) NOT NULL,
  refund_amount decimal(12,2) NOT NULL,
  return_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_refund_amount CHECK (refund_amount >= 0)
);

CREATE TABLE Reviews (
  review_id int PRIMARY KEY,
  customer_id int NOT NULL REFERENCES Customers(customer_id),
  product_id int NOT NULL REFERENCES Products(product_id),
  rating int NOT NULL,
  review_text text,
  review_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5),
  CONSTRAINT uq_customer_product_review UNIQUE (customer_id, product_id)
);
