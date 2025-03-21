# File: backend/app/utils/data_loader.py

import os
import pandas as pd
from sqlalchemy import create_engine, text

# Set default data path
DATA_PATH = os.getenv("DATA_PATH", "./data")

# Database connection strings
AC_DB_CONNECTION_STRING = os.getenv("AC_DB_CONNECTION_STRING", f"sqlite:///{DATA_PATH}/ac_data.db")
GSE_DB_CONNECTION_STRING = os.getenv("GSE_DB_CONNECTION_STRING", f"sqlite:///{DATA_PATH}/gse_data.db")

# Initialize database engines
ac_engine = create_engine(AC_DB_CONNECTION_STRING)
gse_engine = create_engine(GSE_DB_CONNECTION_STRING)

def load_csv(file_name):
    """
    Load a CSV file from the data directory.

    Args:
        file_name (str): Name of the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a Pandas DataFrame.
    """
    file_path = os.path.join(DATA_PATH, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def populate_database(csv_file, engine, table_name):
    """
    Populate an SQLite database table from a CSV file if it is empty.

    Args:
        csv_file (str): Path to the CSV file.
        engine (Engine): SQLAlchemy engine for the database.
        table_name (str): Name of the table to create/populate.
    """
    # Check if the table exists and contains data
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()

    if count > 0:
        print(f"Table '{table_name}' is already populated. Skipping.")
        return

    # Read the CSV file
    print(f"Reading data from {csv_file}...")
    df = pd.read_csv(os.path.join(DATA_PATH, csv_file))

    # Write data to the database
    print(f"Populating table '{table_name}'...")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Table '{table_name}' populated successfully.")

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
    # Select the appropriate engine
    engine = ac_engine if db == "ac" else gse_engine

    # Start with the base query
    query = f"SELECT * FROM {table_name}"
    params = {}

    # Add optional filtering
    if filters:
        where_clauses = []
        for key, value in filters.items():
            if isinstance(value, list):
                # Dynamically generate bind parameters for the IN clause
                placeholders = ", ".join([f":{key}_{i}" for i in range(len(value))])
                where_clauses.append(f'"{key}" IN ({placeholders})')
                # Add each value in the list to the params dictionary with a unique key
                for i, v in enumerate(value):
                    params[f"{key}_{i}"] = v
            else:
                where_clauses.append(f'"{key}" = :{key}')
                params[key] = value
        query += f" WHERE {' AND '.join(where_clauses)}"

    # Debugging: Print the query and parameters
    print("Query:", query)
    print("Params:", params)

    # Execute the query and return the results as a DataFrame
    return pd.read_sql(text(query), engine, params=params)

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