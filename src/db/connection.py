import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_url():
    return URL.create(
        drivername="postgresql",
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )

def get_engine():
    return create_engine(get_url())

def get_connection():
    # Returning a raw connection for compatibility with existing code
    return get_engine().raw_connection()
