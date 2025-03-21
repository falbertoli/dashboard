# File: backend/app/utils/data_loader.py

import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set default data path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data")

# Database connection strings
AC_DB_CONNECTION_STRING = os.getenv("AC_DB_CONNECTION_STRING", f"sqlite:///{DATA_PATH}/ac_data.db")
GSE_DB_CONNECTION_STRING = os.getenv("GSE_DB_CONNECTION_STRING", f"sqlite:///{DATA_PATH}/gse_data.db")

# Initialize database engines
ac_engine = create_engine(AC_DB_CONNECTION_STRING)
gse_engine = create_engine(GSE_DB_CONNECTION_STRING)

def load_csv(file_name):
    """
    Load a CSV file from the data directory.
    """
    file_path = os.path.join(DATA_PATH, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def populate_database(csv_file, engine, table_name):
    """
    Populate an SQLite database table from a CSV file, overwriting existing data.
    """
    try:
        logger.info(f"Using database file: {AC_DB_CONNECTION_STRING}")
        logger.info(f"Using database file: {GSE_DB_CONNECTION_STRING}")
        # Read the CSV file
        logger.info(f"Reading data from {csv_file}...")
        df = pd.read_csv(os.path.join(DATA_PATH, csv_file))
        logger.info(f"First few rows of data from {csv_file}:\n{df.head()}")

        # Write data to the database, overwriting if it exists
        logger.info(f"Populating table '{table_name}'...")
        with engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"Table '{table_name}' populated successfully.")

    except Exception as e:
        logger.error(f"Error populating database: {str(e)}")
        raise

def ensure_database_exists(engine, table_name, csv_file):
    """Ensure database table exists and is populated"""
    try:
        with engine.connect() as conn:
            # Check if table exists and has data
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            if result == 0:
                # Table exists but is empty
                df = pd.read_csv(csv_file)
                if "Ground support Equipment" in df.columns:
                    df["Ground support Equipment"] = df["Ground support Equipment"].str.strip()
                df.to_sql(table_name, engine, if_exists="replace", index=False)
    except Exception:
        # Table doesn't exist, create it
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            if "Ground support Equipment" in df.columns:
                df["Ground support Equipment"] = df["Ground support Equipment"].str.strip()
            df.to_sql(table_name, engine, if_exists="replace", index=False)
        else:
            raise FileNotFoundError(f"No data found for table {table_name}")

def load_data_from_db(table_name, filters=None, db="ac"):
    """Load data from a database table with optional filters."""
    try:
        # Select the appropriate engine and CSV file
        engine = ac_engine if db == "ac" else gse_engine
        csv_file = os.path.join(DATA_PATH, f"{table_name}.csv")
        
        # Ensure database exists and is populated
        ensure_database_exists(engine, table_name, csv_file)
        
        # Build query
        query = f"SELECT * FROM {table_name}"
        params = {}

        if filters:
            where_clauses = []
            for key, value in filters.items():
                if isinstance(value, list):
                    placeholders = []
                    for i, val in enumerate(value):
                        param_name = f"{key.replace(' ', '_')}_{i}"
                        placeholders.append(f":{param_name}")
                        params[param_name] = val.strip() if isinstance(val, str) else val
                    where_clauses.append(f'"{key}" IN ({", ".join(placeholders)})')
                else:
                    param_name = key.replace(" ", "_")
                    where_clauses.append(f'"{key}" = :{param_name}')
                    params[param_name] = value.strip() if isinstance(value, str) else value

            query += " WHERE " + " AND ".join(where_clauses)

        print("Query:", query)
        print("Params:", params)

        return pd.read_sql(text(query), engine, params=params)

    except Exception as e:
        logger.error(f"Error executing database query: {str(e)}")
        raise

# Specific loaders for each dataset
def load_ac_data():
    return load_csv("ac_data.csv")

def load_gse_data():
    return load_csv("gse_data.csv")

def load_income_data():
    return load_csv("t_f41schedule_p12.csv")

def load_operational_hours():
    return load_csv("t_schedule_t1.csv")

def load_carrier_operations():
    return load_csv("t_t100d_segment_us_carrier_only.csv")