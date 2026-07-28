-- ==========================================
-- ShopSphere Data Cleaning Script
-- ==========================================

UPDATE customers
SET full_name = INITCAP(TRIM(full_name));

UPDATE customers
SET email = LOWER(TRIM(email));

DELETE FROM reviews r1
USING reviews r2
WHERE r1.review_id > r2.review_id
  AND r1.customer_id = r2.customer_id
  AND r1.product_id = r2.product_id;

DELETE
FROM payments
WHERE amount < 0;

UPDATE products
SET brand = INITCAP(TRIM(brand));