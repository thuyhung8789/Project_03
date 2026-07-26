import logging
import random
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

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

def generate_promotion_data(engine, fake, num_promotions):
    logger.info("Generating Promotion data...")
    promotions = []
    for _ in range(num_promotions):
        created_at = fake.date_time_between(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 1, 31))
        start_date = created_at + timedelta(days=random.randint(0, 60))
        end_date = start_date + timedelta(days=random.randint(30, 50))
        discount_type = random.choice(['percentage', 'fixed_amount'])
        
        if discount_type == 'percentage':
            discount_value = float(random.choice([5, 10, 15, 20, 50]))
        else:
            discount_value = float(random.choice([20000, 50000, 100000, 200000]))
            
        promotions.append({
            'promotion_name': f"{fake.word().upper()} Sale Campaign",
            'promotion_type': random.choice(['product', 'category', 'seller', 'flash_sale']),
            'discount_type': discount_type,
            'discount_value': discount_value,
            'start_date': start_date,
            'end_date': end_date,
            'created_at': created_at
        })

    df_promo = pd.DataFrame(promotions)
    df_promo.to_sql('promotion', engine, if_exists='append', index=False)

    promo_ids = pd.read_sql("SELECT promotion_id FROM promotion", engine)['promotion_id'].tolist()
    return promo_ids
