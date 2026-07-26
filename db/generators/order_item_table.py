CREATE_ORDER_ITEM_TABLE = """
CREATE TABLE IF NOT EXISTS order_item (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id INT REFERENCES "order"(order_id),
    product_id INT REFERENCES product(product_id),
    order_date TIMESTAMP,
    quantity INT CHECK (quantity > 0),
    unit_price DECIMAL(12,2) CHECK (unit_price > 0),
    subtotal DECIMAL(12,2) CHECK (subtotal = quantity * unit_price),
    created_at TIMESTAMP CHECK (created_at >= order_date)
);
"""
