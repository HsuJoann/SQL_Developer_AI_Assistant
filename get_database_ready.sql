-- Switch to the ecommerce database
--\c ecommerce;

-- Create the customer table
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the product table
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the order table
CREATE TABLE "order" (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customer(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL
);

-- Create the order_detail table
CREATE TABLE order_detail (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES "order"(order_id),
    product_id INT NOT NULL REFERENCES product(product_id),
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO customer (first_name, last_name, email, phone)
SELECT 
    'FirstName' || i, 
    'LastName' || i, 
    'customer' || i || '@example.com', 
    '123-456-789' || i % 10
FROM generate_series(1, 100) AS i;


INSERT INTO product (product_name, price, stock_quantity)
VALUES 
    ('Product A', 10.99, 100),
    ('Product B', 20.99, 200),
    ('Product C', 30.99, 300),
    ('Product D', 40.99, 400);


INSERT INTO "order" (customer_id, total_amount)
SELECT 
    (i % 100) + 1, 
    (RANDOM() * 100 + 50)::DECIMAL(10, 2)
FROM generate_series(1, 200) AS i;


INSERT INTO order_detail (order_id, product_id, quantity, price)
SELECT 
    (i % 200) + 1, 
    (i % 4) + 1, 
    (RANDOM() * 10 + 1)::INT, 
    (RANDOM() * 50 + 10)::DECIMAL(10, 2)
FROM generate_series(1, 900) AS i;


ALTER TABLE "order" RENAME TO order_head;



UPDATE order_detail
SET price = product.price
FROM product
WHERE order_detail.product_id = product.product_id;




UPDATE order_head
SET total_amount = subquery.total
FROM (
    SELECT order_id, SUM(price * quantity) AS total
    FROM order_detail
    GROUP BY order_id
) AS subquery
WHERE order_head.order_id = subquery.order_id;



UPDATE order_head
SET order_date = 
    TIMESTAMP '2025-01-01' + 
    (RANDOM() * INTERVAL '90 days');