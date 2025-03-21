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

def init_db_engines(app):
    """Initialize database engines with application config.
    
    Args:
        app: Flask application instance with configuration
        
    Returns:
        tuple: (ac_engine, gse_engine) database engines
    """
    global ac_engine, gse_engine
    
    # Update engine connections based on app config
    ac_db_uri = app.config.get('AC_DB_URI', AC_DB_CONNECTION_STRING)
    gse_db_uri = app.config.get('GSE_DB_URI', GSE_DB_CONNECTION_STRING)
    
    ac_engine = create_engine(ac_db_uri)
    gse_engine = create_engine(gse_db_uri)
    
    logger.info(f"Initialized AC database engine with: {ac_db_uri}")
    logger.info(f"Initialized GSE database engine with: {gse_db_uri}")
    
    return ac_engine, gse_engine

def load_csv(file_name):
    """
    Load a CSV file from the data directory.
    
    Args:
        file_name (str): Name of the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data as a Pandas DataFrame.
    """
    # Try to get data path from Flask app config if in app context
    try:
        from flask import current_app
        data_path = current_app.config.get('DATA_DIR', DATA_PATH)
    except RuntimeError:
        # Not in Flask app context, use the default
        data_path = DATA_PATH
    
    file_path = os.path.join(data_path, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    logger.info(f"Loading CSV file: {file_path}")
    return pd.read_csv(file_path)

def populate_database(csv_file, engine, table_name):
    """
    Populate an SQLite database table from a CSV file, overwriting existing data.
    
    Args:
        csv_file (str): Path to the CSV file.
        engine (Engine): SQLAlchemy engine for the database.
        table_name (str): Name of the table to create/populate.
    """
    try:
        logger.info(f"Using database engine for table: {table_name}")
        
        # Read the CSV file
        logger.info(f"Reading data from {csv_file}...")
        df = pd.read_csv(os.path.join(DATA_PATH, csv_file))
        logger.info(f"First few rows of data from {csv_file}:\n{df.head()}")

        # Clean data if needed
        if "Ground support Equipment" in df.columns:
            df["Ground support Equipment"] = df["Ground support Equipment"].str.strip()

        # Write data to the database, overwriting if it exists
        logger.info(f"Populating table '{table_name}'...")
        with engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"Table '{table_name}' populated successfully.")

    except Exception as e:
        logger.error(f"Error populating database: {str(e)}")
        raise

def ensure_database_exists(engine, table_name, csv_file):
    """
    Ensure database table exists and is populated.
    
    Args:
        engine (Engine): SQLAlchemy engine for the database.
        table_name (str): Name of the table to check/create.
        csv_file (str): Path to the CSV file to use if table needs to be created.
    """
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
                logger.info(f"Table '{table_name}' was empty and has been populated.")
    except Exception:
        # Table doesn't exist, create it
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            if "Ground support Equipment" in df.columns:
                df["Ground support Equipment"] = df["Ground support Equipment"].str.strip()
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            logger.info(f"Table '{table_name}' didn't exist and has been created.")
        else:
            raise FileNotFoundError(f"No data found for table {table_name}")

def load_data_from_db(table_name, filters=None, db="ac"):
    """
    Load data from a database table with optional filters.
    
    Args:
        table_name (str): The name of the database table.
        filters (dict): Optional filters to apply (e.g., {"COLUMN_NAME": value} or {"COLUMN_NAME": [value1, value2]}).
        db (str): The database to connect to ("ac" or "gse").
        
    Returns:
        pd.DataFrame: The resulting dataset as a Pandas DataFrame.
    """
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
                # Handle column names with spaces
                column_name = f'"{key}"'
                
                if isinstance(value, list):
                    placeholders = []
                    for i, val in enumerate(value):
                        param_name = f"{key.replace(' ', '_')}_{i}"
                        placeholders.append(f":{param_name}")
                        params[param_name] = val.strip() if isinstance(val, str) else val
                    where_clauses.append(f'{column_name} IN ({", ".join(placeholders)})')
                else:
                    param_name = key.replace(" ", "_")
                    where_clauses.append(f'{column_name} = :{param_name}')
                    params[param_name] = value.strip() if isinstance(value, str) else value

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        logger.debug(f"Query: {query}")
        logger.debug(f"Params: {params}")

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