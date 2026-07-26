BEGIN;

-- 1) Reference tables
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Home & Kitchen'),
(3, 'Fashion'),
(4, 'Beauty'),
(5, 'Sports');

INSERT INTO suppliers (supplier_id, supplier_name, country) VALUES
(1, 'NovaTech Supplies', 'USA'),
(2, 'Urban Home Co', 'Canada'),
(3, 'StyleWorks Ltd', 'UK'),
(4, 'GlowLab Brands', 'France'),
(5, 'ActiveLife Goods', 'Germany');

-- 2) Customers
INSERT INTO customers (customer_id, full_name, email, gender, city, state, country, signup_date) VALUES
(1, 'Ava Thompson', 'ava.thompson@example.com', 'Female', 'Austin', 'Texas', 'USA', '2025-01-10'),
(2, 'Liam Carter', 'liam.carter@example.com', 'Male', 'Dallas', 'Texas', 'USA', '2025-01-12'),
(3, 'Sophia Reed', 'sophia.reed@example.com', 'Female', 'Miami', 'Florida', 'USA', '2025-01-15'),
(4, 'Noah Brooks', 'noah.brooks@example.com', 'Male', 'Seattle', 'Washington', 'USA', '2025-01-18'),
(5, 'Mia Patel', 'mia.patel@example.com', 'Female', 'Chicago', 'Illinois', 'USA', '2025-01-20'),
(6, 'Ethan Gray', 'ethan.gray@example.com', 'Male', 'Denver', 'Colorado', 'USA', '2025-01-22'),
(7, 'Olivia Stone', 'olivia.stone@example.com', 'Female', 'Boston', 'Massachusetts', 'USA', '2025-01-25'),
(8, 'James Hall', 'james.hall@example.com', 'Male', 'Phoenix', 'Arizona', 'USA', '2025-01-28');

-- 3) Products
INSERT INTO products (product_id, category_id, supplier_id, product_name, brand, cost_price, selling_price, stock, is_active) VALUES
(1, 1, 1, 'Wireless Headphones', 'NovaSound', 40.00, 79.99, 120, true),
(2, 1, 1, 'Bluetooth Speaker', 'NovaSound', 25.00, 49.99, 150, true),
(3, 2, 2, 'Air Fryer', 'UrbanChef', 55.00, 99.99, 80, true),
(4, 2, 2, 'Coffee Maker', 'UrbanChef', 35.00, 69.99, 70, true),
(5, 3, 3, 'Running Shoes', 'StylePro', 45.00, 89.99, 200, true),
(6, 3, 3, 'Denim Jacket', 'StylePro', 30.00, 64.99, 90, true),
(7, 4, 4, 'Face Serum', 'GlowLab', 12.00, 29.99, 300, true),
(8, 4, 4, 'Moisturizer', 'GlowLab', 10.00, 24.99, 250, true),
(9, 5, 5, 'Yoga Mat', 'ActiveLife', 15.00, 34.99, 180, true),
(10, 5, 5, 'Dumbbell Set', 'ActiveLife', 60.00, 119.99, 60, true);

-- 4) Orders
INSERT INTO orders (order_id, customer_id, order_date, status, shipping_cost, discount, total_amount) VALUES
(1, 1, '2025-02-01 09:15:00', 'delivered', 5.99, 10.00, 109.97),
(2, 2, '2025-02-02 11:30:00', 'delivered', 4.99, 0.00, 54.98),
(3, 3, '2025-02-03 14:05:00', 'delivered', 6.99, 5.00, 121.97),
(4, 4, '2025-02-04 10:20:00', 'shipped', 7.99, 0.00, 77.98),
(5, 5, '2025-02-05 16:45:00', 'delivered', 5.49, 8.00, 111.47),
(6, 6, '2025-02-06 13:10:00', 'cancelled', 0.00, 0.00, 0.00),
(7, 7, '2025-02-07 08:50:00', 'delivered', 6.49, 12.00, 88.97),
(8, 8, '2025-02-08 12:25:00', 'processing', 5.99, 0.00, 124.98);

-- 5) Order items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 79.99),
(2, 1, 7, 1, 29.99),
(3, 2, 2, 1, 49.99),
(4, 3, 3, 1, 99.99),
(5, 3, 8, 1, 24.99),
(6, 4, 5, 1, 89.99),
(7, 5, 6, 1, 64.99),
(8, 7, 9, 1, 34.99),
(9, 8, 10, 1, 119.99);

-- 6) Payments
INSERT INTO payments (payment_id, order_id, payment_method, payment_status, payment_date, amount) VALUES
(1, 1, 'Credit Card', 'paid', '2025-02-01 09:20:00', 109.97),
(2, 2, 'PayPal', 'paid', '2025-02-02 11:35:00', 54.98),
(3, 3, 'Credit Card', 'paid', '2025-02-03 14:10:00', 121.97),
(4, 4, 'Debit Card', 'pending', '2025-02-04 10:25:00', 77.98),
(5, 5, 'Credit Card', 'paid', '2025-02-05 16:50:00', 111.47),
(6, 7, 'Apple Pay', 'paid', '2025-02-07 08:55:00', 88.97),
(7, 8, 'Credit Card', 'pending', '2025-02-08 12:30:00', 124.98);

-- 7) Returns
INSERT INTO returns (return_id, order_id, reason, refund_amount, return_date) VALUES
(1, 2, 'Wrong item received', 49.99, '2025-02-10 10:00:00');

-- 8) Reviews
INSERT INTO reviews (review_id, customer_id, product_id, rating, review_text, review_date) VALUES
(1, 1, 1, 5, 'Excellent sound quality and battery life.', '2025-02-12 09:00:00'),
(2, 1, 7, 4, 'Good serum, lightweight texture.', '2025-02-12 09:10:00'),
(3, 2, 2, 4, 'Portable and loud for its size.', '2025-02-13 11:00:00'),
(4, 3, 3, 5, 'Heats up fast and cooks evenly.', '2025-02-14 15:30:00'),
(5, 5, 6, 4, 'Nice fit and good material.', '2025-02-15 12:20:00'),
(6, 7, 9, 5, 'Great quality yoga mat.', '2025-02-16 08:45:00');

COMMIT;
