import logging
from sqlalchemy import text
from db.connection import get_engine
from db.generators.brand_table import CREATE_BRAND_TABLE
from db.generators.category_table import CREATE_CATEGORY_TABLE
from db.generators.seller_table import CREATE_SELLER_TABLE
from db.generators.customer_table import CREATE_CUSTOMER_TABLE
from db.generators.product_table import CREATE_PRODUCT_TABLE
from db.generators.order_table import CREATE_ORDER_TABLE
from db.generators.order_item_table import CREATE_ORDER_ITEM_TABLE
from db.generators.promotion_table import CREATE_PROMOTION_TABLE
from db.generators.promotion_product_table import CREATE_PROMOTION_PRODUCT_TABLE

logger = logging.getLogger(__name__)

def create_tables():
    tables = [
        CREATE_BRAND_TABLE,
        CREATE_CATEGORY_TABLE,
        CREATE_SELLER_TABLE,
        CREATE_CUSTOMER_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_ORDER_TABLE,
        CREATE_ORDER_ITEM_TABLE,
        CREATE_PROMOTION_TABLE,
        CREATE_PROMOTION_PRODUCT_TABLE
    ]

    engine = get_engine()
    try:
        with engine.connect() as conn:
            with conn.begin():
                for table_sql in tables:
                    conn.execute(text(table_sql))
            logger.info("Tables created successfully.")
    except Exception as error:
        logger.error(f"Error while creating tables: {error}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    create_tables()
