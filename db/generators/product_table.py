CREATE_PRODUCT_TABLE = """
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200),
    category_id INT REFERENCES category(category_id),
    brand_id INT REFERENCES brand(brand_id),
    seller_id INT REFERENCES seller(seller_id),
    price DECIMAL(12,2) CHECK (price > 0),
    stock_qty INT CHECK (stock_qty >= 0),
    rating DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
"""
