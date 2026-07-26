import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import Integer

logger = logging.getLogger(__name__)

CREATE_CATEGORY_TABLE = """
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE,
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT CHECK (level IN (1, 2)),
    created_at TIMESTAMP
);
"""

def generate_category_data(engine, fake):
    logger.info("Generating Category data...")
    # Danh mục cấp 1 (Main categories)
    main_categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty & Personal Care", "Sports"]
    categories = []

    for main in main_categories:
        categories.append({
            'category_name': main,
            'parent_category_id': None,
            'level': 1,
            'created_at': fake.date_time_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31))
        })

    df_main_cat = pd.DataFrame(categories)
    df_main_cat.to_sql('category', engine, if_exists='append', index=False, dtype={'parent_category_id': Integer})

    # Lấy ID của các category cấp 1
    main_cat_df = pd.read_sql("SELECT category_id, category_name FROM category WHERE level = 1", engine)
    main_cat_map = dict(zip(main_cat_df['category_name'], main_cat_df['category_id']))

    # Danh mục cấp 2 (Sub categories)
    sub_categories = [
        ("Mobile Phones", "Electronics"), ("Laptops", "Electronics"),
        ("Men Clothing", "Fashion"), ("Women Clothing", "Fashion"),
        ("Cookware", "Home & Kitchen"), ("Skincare", "Beauty & Personal Care"),
        ("Furniture", "Home & Kitchen"),
        ("Bedding", "Home & Kitchen"), ("Storage", "Home & Kitchen"),
        ("Makeup", "Beauty & Personal Care"),
        ("Fitness Equipment", "Sports"), ("Outdoor Gear", "Sports")
    ]

    sub_cat_data = []
    for sub, parent in sub_categories:
        sub_cat_data.append({
            'category_name': sub,
            'parent_category_id': main_cat_map[parent],
            'level': 2,
            'created_at': fake.date_time_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31))
        })

    df_sub_cat = pd.DataFrame(sub_cat_data)
    df_sub_cat.to_sql('category', engine, if_exists='append', index=False, dtype={'parent_category_id': Integer})

    category_ids = pd.read_sql("SELECT category_id FROM category", engine)['category_id'].tolist()
    return category_ids
