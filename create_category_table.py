import os
import psycopg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_category_table():
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

                # SQL command to create the category table
                create_table_query = """
                CREATE TABLE IF NOT EXISTS category (
                    category_id SERIAL PRIMARY KEY,
                    category_name VARCHAR(100) UNIQUE,
                    parent_category_id INT REFERENCES category(category_id),
                    level SMALLINT CHECK (level IN (1, 2)),
                    create_at TIMESTAMP
                );
                """

                # Execute the create table command
                cur.execute(create_table_query)

                # Commit the changes
                conn.commit()
                print("Table 'category' created successfully.")

    except Exception as error:
        print(f"Error while creating table: {error}")

if __name__ == "__main__":
    create_category_table()
