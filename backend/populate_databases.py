import pandas as pd
from sqlalchemy import create_engine
import os

# Paths to files and databases
DATA_PATH = "./data"
AC_CSV_FILE = os.path.join(DATA_PATH, "ac_data.csv")
GSE_CSV_FILE = os.path.join(DATA_PATH, "gse_data.csv")
AC_DB_FILE = os.path.join(DATA_PATH, "ac_data.db")
GSE_DB_FILE = os.path.join(DATA_PATH, "gse_data.db")

# Table names
AC_TABLE_NAME = "ac_data"
GSE_TABLE_NAME = "gse_data"

def populate_database(csv_file, db_file, table_name):
    """
    Populate an SQLite database with a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to create/populate.
    """
    # Read the CSV file
    print(f"Reading data from {csv_file}...")
    df = pd.read_csv(csv_file)

    # Create SQLite engine
    print(f"Connecting to database {db_file}...")
    engine = create_engine(f"sqlite:///{db_file}")

    # Write data into the database
    print(f"Populating table '{table_name}' in {db_file}...")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Successfully populated {db_file} with data from {csv_file}.")

def main():
    # Populate the ac_data.db from ac_data.csv
    populate_database(AC_CSV_FILE, AC_DB_FILE, "ac_data")

    # Populate the gse_data.db from gse_data.csv
    populate_database(GSE_CSV_FILE, GSE_DB_FILE, "gse_data")

if __name__ == "__main__":
    main()