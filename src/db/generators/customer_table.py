import logging
import random
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

CREATE_CUSTOMER_TABLE = """
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
"""

def generate_customer_data(engine, fake, num_customers):
    logger.info("Generating Customer data...")
    customers = []
    seen_emails = set()
    seen_phones = set()
    
    for i in range(num_customers):
        # Generate unique email
        email = fake.email()
        if email in seen_emails:
            name_part, domain = email.split('@')
            email = f"{name_part}_{i}@{domain}"
        seen_emails.add(email)
        
        # Generate unique phone
        phone = fake.phone_number()[:20]
        attempts = 0
        while phone in seen_phones and attempts < 10:
            phone = fake.phone_number()[:20]
            attempts += 1
        if phone in seen_phones:
            phone = f"{phone[:10]}{i}"[:20]
        seen_phones.add(phone)

        customers.append({
            'customer_name': fake.name(),
            'email': email,
            'phone': phone,
            'gender': random.choice(['Male', 'Female']),
            'address': fake.street_address()[:255],
            'city': fake.city()[:100],
            'created_at': fake.date_time_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31))
        })

    df_customer = pd.DataFrame(customers)
    df_customer.to_sql('customer', engine, if_exists='append', index=False)

    customer_ids = pd.read_sql("SELECT customer_id FROM customer", engine)['customer_id'].tolist()
    return customer_ids
