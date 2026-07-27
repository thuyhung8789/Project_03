# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import logging
import random
from faker import Faker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from db.schema import create_tables
from db.connection import get_url
from db.generators.brand_table import generate_brand_data
from db.generators.category_table import generate_category_data
from db.generators.seller_table import generate_seller_data
from db.generators.customer_table import generate_customer_data
from db.generators.product_table import generate_product_data
from db.generators.order_table import generate_order_data
from db.generators.promotion_table import generate_promotion_data
from db.generators.promotion_product_table import generate_promotion_product_data

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def insert_fake_data():
    # 1. Khởi tạo Faker (Hỗ trợ tiếng Việt cho Customer/Address nếu muốn, ở đây dùng chuẩn en_US/vi_VN)
    fake = Faker('vi_VN')
    Faker.seed(42)
    random.seed(42)

    # Cấu hình chuỗi kết nối Database (Lấy từ environment variables)
    DB_URL = get_url()
    engine = create_engine(DB_URL)

    try:
        # Clear existing data to avoid UniqueViolation during debug
        logger.info("Clearing existing data...")
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("TRUNCATE TABLE promotion_product, promotion, order_item, \"order\", product, customer, seller, category, brand CASCADE;"))

        # Số lượng bản ghi muốn sinh (Tuỳ chỉnh theo nhu cầu)
        NUM_BRANDS = 20
        NUM_SELLERS = 50
        NUM_CUSTOMERS = 30000
        NUM_PRODUCTS = 3000
        NUM_ORDERS = 1000
        NUM_PROMOTIONS = 30
        number_product_promotions = 500

        # 3.1 BRAND
        brand_ids = generate_brand_data(engine, fake, NUM_BRANDS)

        # 3.2 CATEGORY
        category_ids = generate_category_data(engine, fake)

        # 3.3 SELLER
        seller_ids = generate_seller_data(engine, fake, NUM_SELLERS)

        # 3.4 CUSTOMER
        customer_ids = generate_customer_data(engine, fake, NUM_CUSTOMERS)

        # 3.5 PRODUCT
        product_ids, product_dict = generate_product_data(engine, fake, NUM_PRODUCTS, category_ids, brand_ids, seller_ids)

        # 3.6 & 3.7 ORDER & ORDER_ITEM
        generate_order_data(engine, fake, NUM_ORDERS, customer_ids, product_ids, product_dict)

        # 3.8 PROMOTION
        promo_ids = generate_promotion_data(engine, fake, NUM_PROMOTIONS)

        # 3.9 PROMOTION_PRODUCT
        generate_promotion_product_data(engine, fake, number_product_promotions, promo_ids, product_ids)

        logger.info("SUCCESS: Data successfully generated and inserted into the database!")
    finally:
        engine.dispose()


if __name__ == "__main__":
    create_tables()
    insert_fake_data()
