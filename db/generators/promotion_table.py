CREATE_PROMOTION_TABLE = """
CREATE TABLE IF NOT EXISTS promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100),
    promotion_type VARCHAR(50),
    discount_type VARCHAR(20) CHECK (discount_type IN ('percentage', 'fixed_amount')),
    discount_value NUMERIC(10,2) CHECK (discount_value > 0 AND (discount_type = 'fixed_amount' OR discount_value <= 100)),
    start_date DATE CHECK (start_date >= DATE(created_at)),
    end_date DATE CHECK (end_date >= start_date),
    created_at TIMESTAMP
);
"""
