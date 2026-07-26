import logging
import random
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

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

def generate_seller_data(engine, fake, num_sellers):
    logger.info("Generating Seller data...")
    sellers = []
    for _ in range(num_sellers):
        sellers.append({
            'seller_name': f"{fake.company()} Shop",
            'join_date': fake.date_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31)),
            'seller_type': random.choice(['Official', 'Marketplace']),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'country': 'Vietnam'
        })
    df_seller = pd.DataFrame(sellers)
    df_seller.to_sql('seller', engine, if_exists='append', index=False)

    seller_ids = pd.read_sql("SELECT seller_id FROM seller", engine)['seller_id'].tolist()
    return seller_ids
