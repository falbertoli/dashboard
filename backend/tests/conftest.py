# File: tests/conftest.py

import pytest
import pandas as pd
from sqlalchemy import create_engine, text
import os
import shutil
from app import create_app

@pytest.fixture(scope="session", autouse=True)
def setup_test_databases():
    """Fixture to set up test databases with sample data"""
    try:
        # Get the absolute path to the data directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Set up GSE database
        gse_csv_path = os.path.join(data_dir, "gse_data.csv")
        gse_db_path = os.path.join(data_dir, "gse_data.db")
        
        # Remove existing database if it exists
        if os.path.exists(gse_db_path):
            os.remove(gse_db_path)
        
        # Create new database
        gse_engine = create_engine(f"sqlite:///{gse_db_path}")
        
        # Read and populate GSE data
        gse_data = pd.read_csv(gse_csv_path)
        gse_data["Ground support Equipment"] = gse_data["Ground support Equipment"].str.strip()
        gse_data.to_sql("gse_data", gse_engine, if_exists="replace", index=False)
        
        # Verify GSE data
        with gse_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM gse_data")).scalar()
            print(f"Populated GSE database with {result} rows")
            
            # Verify specific records
            result = conn.execute(
                text('SELECT "Ground support Equipment" FROM gse_data WHERE "Ground support Equipment" = :equip'),
                {"equip": "F250"}
            ).fetchone()
            assert result is not None, "Test data not properly loaded"
        
        # Similar setup for AC database
        ac_csv_path = os.path.join(data_dir, "ac_data.csv")
        ac_db_path = os.path.join(data_dir, "ac_data.db")
        
        if os.path.exists(ac_db_path):
            os.remove(ac_db_path)
            
        ac_engine = create_engine(f"sqlite:///{ac_db_path}")
        
        if os.path.exists(ac_csv_path):
            ac_data = pd.read_csv(ac_csv_path)
            ac_data.to_sql("ac_data", ac_engine, if_exists="replace", index=False)
            
            with ac_engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM ac_data")).scalar()
                print(f"Populated AC database with {result} rows")
        
        yield
        
    except Exception as e:
        print(f"Error setting up test databases: {str(e)}")
        raise

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app("testing")
    
    # Create a test context
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()