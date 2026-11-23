
USE smart_spaza_shop;

-- 1. Insert a sample user
INSERT INTO users (
    first_name,
    surname,
    email,
    phone_number,
    username,
    password_hash
)
VALUES (
    'Nwayitelo',
    'Sethole',
    'lightsethole@gmail.com',
    '0792487487',
    'NwayiSR_services',
    'SEED_ONLY_NOT_A_LOGIN_PASSWORD'
);

-- Store the new user's ID
SET @demo_user_id = LAST_INSERT_ID();

-- 2. Insert sample products
INSERT INTO products (
    user_id,
    name,
    quantity,
    expiry_date,
    annual_demand,
    ordering_cost,
    holding_cost,
    avg_daily_demand,
    lead_time,
    demand_std_dev,
    category
)
VALUES
(@demo_user_id, 'Milk', 30, '2026-12-10', 1200, 45.00, 5.00, 4.00, 2, 1.20, 'A'),
(@demo_user_id, 'Bread', 20, '2026-11-26', 900, 30.00, 3.00, 3.00, 1, 0.80, 'A'),
(@demo_user_id, 'Flour', 50, '2027-03-15', 600, 35.00, 4.00, 2.00, 3, 0.50, 'B');

-- 3. Insert sample stock movements
INSERT INTO stock_movements (
    product_id,
    movement_type,
    quantity_changed,
    reason
)
SELECT product_id, 'IN', 30, 'Initial stock received'
FROM products
WHERE user_id = @demo_user_id AND name = 'Milk';

INSERT INTO stock_movements (
    product_id,
    movement_type,
    quantity_changed,
    reason
)
SELECT product_id, 'IN', 20, 'Initial stock received'
FROM products
WHERE user_id = @demo_user_id AND name = 'Bread';

INSERT INTO stock_movements (
    product_id,
    movement_type,
    quantity_changed,
    reason
)
SELECT product_id, 'IN', 50, 'Initial stock received'
FROM products
WHERE user_id = @demo_user_id AND name = 'Flour';
