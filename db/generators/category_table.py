CREATE_CATEGORY_TABLE = """
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE,
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT CHECK (level IN (1, 2)),
    create_at TIMESTAMP
);
"""
