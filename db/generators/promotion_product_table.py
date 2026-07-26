import logging
import random
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

CREATE_PROMOTION_PRODUCT_TABLE = """
CREATE TABLE IF NOT EXISTS promotion_product (
    promo_product_id SERIAL PRIMARY KEY,
    promotion_id INT REFERENCES promotion(promotion_id),
    product_id INT REFERENCES product(product_id),
    created_at TIMESTAMP
);
"""

def generate_promotion_product_data(engine, fake, number_product_promotions, promo_ids, product_ids):
    logger.info("Generating Promotion_Product mapping...")
    promo_products = []
    unique_pairs = set()

    # Tạo liên kết giữa KM và SP (đảm bảo Constraint UNIQUE(promotion_id, product_id))
    while len(promo_products) < number_product_promotions:
        p_id = random.choice(promo_ids)
        prod_id = random.choice(product_ids)
        
        if (p_id, prod_id) not in unique_pairs:
            unique_pairs.add((p_id, prod_id))
            promo_products.append({
                'promotion_id': p_id,
                'product_id': prod_id,
                'created_at': fake.date_time_between(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 4, 30))
            })

    df_promo_prod = pd.DataFrame(promo_products)
    df_promo_prod.to_sql('promotion_product', engine, if_exists='append', index=False)
