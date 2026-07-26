CREATE_BRAND_TABLE = """
CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE,
    country VARCHAR(50),
    create_at TIMESTAMP
);
"""
