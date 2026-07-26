CREATE_ORDER_TABLE = """
CREATE TABLE IF NOT EXISTS "order" (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customer(customer_id),
    order_date TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('PLACED','PAID','SHIPPED','DELIVERED','CANCELLED','RETURNED')),
    total_amount DECIMAL(12,2) CHECK (total_amount >= 0),
    created_at TIMESTAMP CHECK (created_at >= order_date)
);
"""
