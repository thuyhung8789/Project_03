import logging
import random
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

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

def generate_product_data(engine, fake, num_products, category_ids, brand_ids, seller_ids):
    logger.info("Generating Product data...")
    products = []
    for _ in range(num_products):
        products.append({
            'product_name': fake.catch_phrase(),
            'category_id': random.choice(category_ids),
            'brand_id': random.choice(brand_ids),
            'seller_id': random.choice(seller_ids),
            'price': round(random.uniform(100000, 50000000), -3),
            'stock_qty': random.randint(0, 500),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'created_at': fake.date_time_between(start_date=datetime(2025, 6, 1), end_date=datetime(2025, 12, 31)),
            'is_active': random.choice([True, True, True, False])
        })

    df_product = pd.DataFrame(products)
    df_product.to_sql('product', engine, if_exists='append', index=False)

    # Lưu lại sản phẩm và giá để dùng tính Order / Order Item
    product_df_db = pd.read_sql("SELECT product_id, price FROM product", engine)
    product_dict = dict(zip(product_df_db['product_id'], product_df_db['price']))
    product_ids = list(product_dict.keys())
    return product_ids, product_dict
