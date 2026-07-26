CREATE_SELLER_TABLE = """
CREATE TABLE IF NOT EXISTS seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150),
    join_date DATE,
    seller_type VARCHAR(50) CHECK (seller_type IN ('Official', 'Marketplace')),
    rating DECIMAL(2,1),
    country VARCHAR(50)
);
"""
