import logging
import random
import pandas as pd
from datetime import datetime, timedelta
from db.connection import get_connection

logger = logging.getLogger(__name__)

CREATE_ORDER_TABLE = """
CREATE TABLE IF NOT EXISTS "order" (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customer(customer_id),
    order_date TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('PLACED','PAID','SHIPPED','DELIVERED','CANCELLED','RETURNED')),
    total_amount DECIMAL(12,2) CHECK (total_amount >= 0),
    created_at TIMESTAMP CHECK (created_at >= order_date)
);
"""

def generate_order_data(engine, fake, num_orders, customer_ids, product_ids, product_dict):
    logger.info("Generating Orders & Order Items data...")
    orders = []
    order_items = []

    for _ in range(num_orders):
        order_date = fake.date_time_between(start_date=datetime(2026, 1, 1), end_date=datetime(2026, 5, 31))
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
    logger.info("Inserting Orders and retrieving IDs using RETURNING...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            for o in orders:
                items = o.pop('items')
                # Insert order with RETURNING order_id
                insert_query = """
                    INSERT INTO "order" (customer_id, order_date, status, total_amount, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING order_id
                """
                cur.execute(insert_query, (
                    o['customer_id'],
                    o['order_date'],
                    o['status'],
                    o['total_amount'],
                    o['created_at']
                ))
                curr_order_id = cur.fetchone()[0]
                
                # Gán order_id vào items và lưu
                for it in items:
                    it['order_id'] = curr_order_id
                    order_items.append(it)
            conn.commit()

    df_order_items = pd.DataFrame(order_items)
    df_order_items.to_sql('order_item', engine, if_exists='append', index=False)
