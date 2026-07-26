CREATE_CUSTOMER_TABLE = """
CREATE TABLE IF NOT EXISTS customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    address VARCHAR(255),
    city VARCHAR(100),
    created_at TIMESTAMP
);
"""
