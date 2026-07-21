# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os
import psycopg
import random
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine, text, Integer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_tables():
    try:
        # Connect to the database
        with psycopg.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        ) as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:

                # SQL command to create the brand table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS brand (
                    brand_id SERIAL PRIMARY KEY,
                    brand_name VARCHAR(100) UNIQUE,
                    country VARCHAR(50),
                    create_at TIMESTAMP
                );
                """)
                # SQL command to create the category table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    category_id SERIAL PRIMARY KEY,
                    category_name VARCHAR(100) UNIQUE,
                    parent_category_id INT REFERENCES category(category_id),
                    level SMALLINT CHECK (level IN (1, 2)),
                    create_at TIMESTAMP
                );
                """)

                # SQL command to create the seller table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS seller (
                    seller_id SERIAL PRIMARY KEY,
                    seller_name VARCHAR(150),
                    join_date DATE,
                    seller_type VARCHAR(50) CHECK (seller_type IN ('Official', 'Marketplace')),
                    rating DECIMAL(2,1),
                    country VARCHAR(50)
                );
                """)

                # SQL command to create the customer table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS customer (
                    customer_id SERIAL PRIMARY KEY,
                    customer_name VARCHAR(150),
                    email VARCHAR(150) UNIQUE,
                    phone VARCHAR(20) UNIQUE,
                    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
                    address VARCHAR(255),
                    city VARCHAR(100),
                    created_at TIMESTAMP
                );
                """)

                # SQL command to create the product table
                cur.execute("""
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
                """)

                # SQL command to create the order table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS "order" (
                    order_id SERIAL PRIMARY KEY,
                    customer_id INT REFERENCES customer(customer_id),
                    order_date TIMESTAMP,
                    status VARCHAR(20) CHECK (status IN ('PLACED','PAID','SHIPPED','DELIVERED','CANCELLED','RETURNED')),
                    total_amount DECIMAL(12,2) CHECK (total_amount >= 0),
                    created_at TIMESTAMP CHECK (created_at >= order_date)
                );
                """)

                # SQL command to create the order_item table
                cur.execute("""
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
                """)

                # SQL command to create the promotion table
                cur.execute("""
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
                """)

                # SQL command to create the promotion_product table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS promotion_product (
                    promo_product_id SERIAL PRIMARY KEY,
                    promotion_id INT REFERENCES promotion(promotion_id),
                    product_id INT REFERENCES product(product_id),
                    created_at TIMESTAMP
                );
                """)

                # Commit the changes
                conn.commit()
                print("Tables 'brand', 'category', 'seller', 'customer', 'product', 'order', 'order_item', 'promotion' and 'promotion_product' checked/created successfully.")

    except Exception as error:
        print(f"Error while creating tables: {error}")

def insert_fake_data():
    # 1. Khởi tạo Faker (Hỗ trợ tiếng Việt cho Customer/Address nếu muốn, ở đây dùng chuẩn en_US/vi_VN)
    fake = Faker('vi_VN')
    Faker.seed(42)
    random.seed(42)

    # Cấu hình chuỗi kết nối Database (Lấy từ environment variables)
    password = urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))
    DB_URL = f"postgresql+psycopg://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(DB_URL)

    # Clear existing data to avoid UniqueViolation during debug
    print("Clearing existing data...")
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("TRUNCATE TABLE promotion_product, promotion, order_item, \"order\", product, customer, seller, category, brand CASCADE;"))

    # Số lượng bản ghi muốn sinh (Tuỳ chỉnh theo nhu cầu)
    NUM_BRANDS = 20
    NUM_SELLERS = 50
    NUM_CUSTOMERS = 200
    NUM_PRODUCTS = 500
    NUM_ORDERS = 1000
    NUM_PROMOTIONS = 30

    # ==========================================
    # 3.1 BRAND
    # ==========================================
    print("Generating Brand data...")
    brands = []
    brand_names = set()
    while len(brand_names) < NUM_BRANDS:
        brand_names.add(fake.company())

    for b_name in brand_names:
        brands.append({
            'brand_name': b_name,
            'country': fake.country(),
            'create_at': fake.date_time_between(start_date='-2y', end_date='-1y')
        })
    df_brand = pd.DataFrame(brands)
    df_brand.to_sql('brand', engine, if_exists='append', index=False)

    # Lấy brand_ids vừa insert
    brand_ids = pd.read_sql("SELECT brand_id FROM brand", engine)['brand_id'].tolist()

    # ==========================================
    # 3.2 CATEGORY
    # ==========================================
    print("Generating Category data...")
    # Danh mục cấp 1 (Main categories)
    main_categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty & Personal Care", "Sports"]
    categories = []

    for main in main_categories:
        categories.append({
            'category_name': main,
            'parent_category_id': None,
            'level': 1,
            'create_at': fake.date_time_between(start_date='-2y', end_date='-18m')
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
        ("Cookware", "Home & Kitchen"), ("Skincare", "Beauty & Personal Care")
    ]

    sub_cat_data = []
    for sub, parent in sub_categories:
        sub_cat_data.append({
            'category_name': sub,
            'parent_category_id': main_cat_map[parent],
            'level': 2,
            'create_at': fake.date_time_between(start_date='-18m', end_date='-1y')
        })

    df_sub_cat = pd.DataFrame(sub_cat_data)
    df_sub_cat.to_sql('category', engine, if_exists='append', index=False, dtype={'parent_category_id': Integer})

    category_ids = pd.read_sql("SELECT category_id FROM category", engine)['category_id'].tolist()

    # ==========================================
    # 3.3 SELLER
    # ==========================================
    print("Generating Seller data...")
    sellers = []
    for _ in range(NUM_SELLERS):
        sellers.append({
            'seller_name': f"{fake.company()} Shop",
            'join_date': fake.date_between(start_date='-2y', end_date='now'),
            'seller_type': random.choice(['Official', 'Marketplace']),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'country': 'Vietnam'
        })
    df_seller = pd.DataFrame(sellers)
    df_seller.to_sql('seller', engine, if_exists='append', index=False)

    seller_ids = pd.read_sql("SELECT seller_id FROM seller", engine)['seller_id'].tolist()

    # ==========================================
    # 3.4 CUSTOMER
    # ==========================================
    print("Generating Customer data...")
    customers = []

    while len(customers) < NUM_CUSTOMERS:
        email = fake.unique.email()
        phone = fake.unique.phone_number()[:20]
        
        customers.append({
            'customer_name': fake.name(),
            'email': email,
            'phone': phone,
            'gender': random.choice(['Male', 'Female']),
            'address': fake.street_address(),
            'city': fake.city(),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now')
        })

    df_customer = pd.DataFrame(customers)
    df_customer.to_sql('customer', engine, if_exists='append', index=False)

    customer_ids = pd.read_sql("SELECT customer_id FROM customer", engine)['customer_id'].tolist()

    # ==========================================
    # 3.5 PRODUCT
    # ==========================================
    print("Generating Product data...")
    products = []
    for _ in range(NUM_PRODUCTS):
        products.append({
            'product_name': fake.catch_phrase(),
            'category_id': random.choice(category_ids),
            'brand_id': random.choice(brand_ids),
            'seller_id': random.choice(seller_ids),
            'price': round(random.uniform(100000, 50000000), -3), # Giá làm tròn hàng nghìn
            'stock_qty': random.randint(0, 500),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
            'is_active': random.choice([True, True, True, False]) # 75% active
        })

    df_product = pd.DataFrame(products)
    df_product.to_sql('product', engine, if_exists='append', index=False)

    # Lưu lại sản phẩm và giá để dùng tính Order / Order Item
    product_df_db = pd.read_sql("SELECT product_id, price FROM product", engine)
    product_dict = dict(zip(product_df_db['product_id'], product_df_db['price']))
    product_ids = list(product_dict.keys())

    # ==========================================
    # 3.6 & 3.7 ORDER & ORDER_ITEM
    # ==========================================
    print("Generating Orders & Order Items data...")
    orders = []
    order_items = []

    for _ in range(NUM_ORDERS):
        order_date = fake.date_time_between(start_date='-6m', end_date='now')
        created_at = order_date + timedelta(seconds=random.randint(0, 3600))
        customer_id = random.choice(customer_ids)
        status = random.choice(['PLACED', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED'])
        
        # Tạo ngẫu nhiên 1 - 4 item cho mỗi đơn hàng
        num_items = random.randint(1, 4)
        selected_products = random.sample(product_ids, num_items)
        
        order_total = 0
        temp_items = []
        
        for prod_id in selected_products:
            qty = random.randint(1, 3)
            unit_price = float(product_dict[prod_id])
            subtotal = qty * unit_price
            order_total += subtotal
            
            temp_items.append({
                'product_id': prod_id,
                'order_date': order_date,
                'quantity': qty,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'created_at': created_at
            })
        
        # Lưu thông tin đơn hàng
        orders.append({
            'customer_id': customer_id,
            'order_date': order_date,
            'status': status,
            'total_amount': order_total,
            'created_at': created_at,
            'items': temp_items
        })

    # Insert Orders từng cái để lấy `order_id` map sang Order Items
    for o in orders:
        items = o.pop('items')
        # Insert order
        df_single_order = pd.DataFrame([o])
        df_single_order.to_sql('order', engine, if_exists='append', index=False)
        
        # Lấy order_id vừa tạo
        curr_order_id = pd.read_sql("SELECT MAX(order_id) as id FROM \"order\"", engine)['id'].values[0]
        
        # Gán order_id vào items và lưu
        for it in items:
            it['order_id'] = curr_order_id
            order_items.append(it)

    df_order_items = pd.DataFrame(order_items)
    df_order_items.to_sql('order_item', engine, if_exists='append', index=False)

    # ==========================================
    # 3.8 PROMOTION
    # ==========================================
    print("Generating Promotion data...")
    promotions = []
    for _ in range(NUM_PROMOTIONS):
        created_at = fake.date_time_between(start_date='-6m', end_date='-1m')
        start_date = created_at.date() + timedelta(days=random.randint(0, 10))
        end_date = start_date + timedelta(days=random.randint(7, 30))
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

    # ==========================================
    # 3.9 PROMOTION_PRODUCT
    # ==========================================
    print("Generating Promotion_Product mapping...")
    promo_products = []
    unique_pairs = set()

    # Tạo liên kết giữa KM và SP (đảm bảo Constraint UNIQUE(promotion_id, product_id))
    while len(promo_products) < (NUM_PROMOTIONS * 5): # Mỗi CTKM áp dụng khoảng 5 sản phẩm
        p_id = random.choice(promo_ids)
        prod_id = random.choice(product_ids)
        
        if (p_id, prod_id) not in unique_pairs:
            unique_pairs.add((p_id, prod_id))
            promo_products.append({
                'promotion_id': p_id,
                'product_id': prod_id,
                'created_at': fake.date_time_between(start_date='-1m', end_date='now')
            })

    df_promo_prod = pd.DataFrame(promo_products)
    df_promo_prod.to_sql('promotion_product', engine, if_exists='append', index=False)

    print("SUCCESS: Data successfully generated and inserted into the database!")


if __name__ == "__main__":
    create_tables()
    insert_fake_data()
