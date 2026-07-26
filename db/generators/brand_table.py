import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

CREATE_BRAND_TABLE = """
CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) UNIQUE,
    country VARCHAR(50),
    created_at TIMESTAMP
);
"""

def generate_brand_data(engine, fake, num_brands):
    logger.info("Generating Brand data...")
    brands = []
    brand_names = set()
    while len(brand_names) < num_brands:
        brand_names.add(fake.company())

    for b_name in brand_names:
        brands.append({
            'brand_name': b_name,
            'country': fake.country(),
            'created_at': fake.date_time_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31))
        })
    df_brand = pd.DataFrame(brands)
    df_brand.to_sql('brand', engine, if_exists='append', index=False)

    # Lấy brand_ids vừa insert
    brand_ids = pd.read_sql("SELECT brand_id FROM brand", engine)['brand_id'].tolist()
    return brand_ids
