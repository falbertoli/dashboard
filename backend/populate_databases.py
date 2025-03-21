# File: backend/populate_databases.py

import pandas as pd
from sqlalchemy import create_engine
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the absolute path to the data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

# Define file paths
AC_CSV_FILE = os.path.join(DATA_PATH, "ac_data.csv")
GSE_CSV_FILE = os.path.join(DATA_PATH, "gse_data.csv")
AC_DB_FILE = os.path.join(DATA_PATH, "ac_data.db")
GSE_DB_FILE = os.path.join(DATA_PATH, "gse_data.db")

# Table names
AC_TABLE_NAME = "ac_data"
GSE_TABLE_NAME = "gse_data"

def ensure_data_directory():
    """
    Ensure the data directory exists.
    """
    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        logger.info(f"Data directory confirmed at: {DATA_PATH}")
    except Exception as e:
        logger.error(f"Failed to create data directory: {str(e)}")
        raise

def check_csv_files():
    """
    Check if required CSV files exist.
    """
    missing_files = []
    for file_path in [AC_CSV_FILE, GSE_CSV_FILE]:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        raise FileNotFoundError(
            f"Required CSV files are missing: {', '.join(missing_files)}"
        )

def populate_database(csv_file, db_file, table_name):
    """
    Populate an SQLite database with data from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to create/populate.
    """
    try:
        # Read the CSV file
        logger.info(f"Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)
        logger.info(f"Successfully read {len(df)} rows from {csv_file}")

        # Create SQLite engine with absolute path
        db_uri = f"sqlite:///{os.path.abspath(db_file)}"
        logger.info(f"Creating database connection to {db_uri}...")
        engine = create_engine(db_uri)

        # Write data into the database
        logger.info(f"Populating table '{table_name}' in {db_file}...")
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        
        # Verify the data was written
        verification_df = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", engine)
        row_count = verification_df.iloc[0]['count']
        logger.info(f"Successfully populated {row_count} rows in {table_name} table")

    except pd.errors.EmptyDataError:
        logger.error(f"The CSV file {csv_file} is empty")
        raise
    except Exception as e:
        logger.error(f"Error while populating database: {str(e)}")
        raise

def main():
    """
    Main function to populate all databases.
    """
    try:
        # Ensure data directory exists
        ensure_data_directory()

        # Check if required CSV files exist
        check_csv_files()

        # Populate the ac_data database
        logger.info("Starting population of ac_data database...")
        populate_database(AC_CSV_FILE, AC_DB_FILE, AC_TABLE_NAME)
        logger.info("Completed population of ac_data database")

        # Populate the gse_data database
        logger.info("Starting population of gse_data database...")
        populate_database(GSE_CSV_FILE, GSE_DB_FILE, GSE_TABLE_NAME)
        logger.info("Completed population of gse_data database")

        logger.info("Database population completed successfully")

    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error during database population: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise