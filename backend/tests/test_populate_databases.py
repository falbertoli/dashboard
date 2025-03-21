import pytest
import os
from sqlalchemy import text
from app.utils.data_loader import populate_database, ac_engine, gse_engine

def test_populate_databases():
    # Populate ac_data.db
    populate_database("ac_data.csv", ac_engine, "ac_data")

    # Populate gse_data.db
    populate_database("gse_data.csv", gse_engine, "gse_data")

    # Verify the data was populated
    with gse_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM gse_data")).scalar()
        assert result == 14  # Number of rows in your CSV
        
        # Test specific equipment exists
        result = conn.execute(
            text('SELECT * FROM gse_data WHERE "Ground support Equipment" = :equip'),
            {"equip": "F250"}
        ).fetchone()
        assert result is not None
        assert result[1] == "Diesel"  # Verify fuel type

    print("Databases populated successfully.")

if __name__ == "__main__":
    test_populate_databases()