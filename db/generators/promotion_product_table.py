CREATE_PROMOTION_PRODUCT_TABLE = """
CREATE TABLE IF NOT EXISTS promotion_product (
    promo_product_id SERIAL PRIMARY KEY,
    promotion_id INT REFERENCES promotion(promotion_id),
    product_id INT REFERENCES product(product_id),
    created_at TIMESTAMP
);
"""
