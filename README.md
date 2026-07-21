# E-commerce OLTP Data Generator

This project uses **Python** and the **Faker** library to generate realistic synthetic data for an E-commerce OLTP (Online Transaction Processing) system and loads it into a **PostgreSQL** database.

## Features
- **Comprehensive Schema**: Generates data for 9 relational tables covering brands, categories, sellers, customers, products, orders, and promotions.
- **Data Integrity**: Ensures relational consistency (foreign keys), logical timestamps (e.g., `created_at >= order_date`), and unique constraints.
- **Localized Data**: Uses the `vi_VN` locale for realistic Vietnamese customer names and addresses.
- **Efficient Loading**: Leverages `Pandas` and `SQLAlchemy` for high-performance batch data insertion.
- **Idempotent Execution**: Automatically handles table creation and data truncation for repeatable runs.

## Database Schema
The system populates the following tables:
1. `brand`: Manufacturing brands.
2. `category`: Product categories with hierarchical support (Level 1 & 2).
3. `seller`: Official and Marketplace shops.
4. `customer`: User profiles with contact details.
5. `product`: Catalog items linked to brands, categories, and sellers.
6. `order`: Customer purchase records.
7. `order_item`: Line items within each order.
8. `promotion`: Marketing campaigns and discounts.
9. `promotion_product`: Many-to-many mapping between promotions and products.

## Prerequisites
- **Python 3.10+**
- **PostgreSQL** database instance.

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thuyhung8789/Project_03.git
   cd Project_03
   ```

2. **Install dependencies**:
   Using `pip`:
   ```bash
   pip install -r requirement.txt
   ```
   *Note: If you are using Poetry, run `poetry install` instead.*

3. **Configure environment variables**:
   Create a `.env` file in the project root with your PostgreSQL credentials:
   ```env
   DB_HOST=localhost
   DB_NAME=ecommerce_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

## Usage
Run the main script to initialize the database and generate data:
```bash
python main.py
```

The script performs the following actions:
1. Connects to PostgreSQL using the credentials in `.env`.
2. Creates all 9 tables if they do not already exist.
3. Truncates any existing data in those tables (CASCADE) to ensure a clean state.
4. Generates and inserts fresh synthetic data for all tables.

## Project Structure
- `main.py`: The primary script containing table definitions and data generation logic.
- `requirement.txt`: List of Python package dependencies.
- `.env`: Configuration for database connectivity (not tracked in Git).
- `pyproject.toml`: Project metadata and dependency management.
