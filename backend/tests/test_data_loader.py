import pytest
from sqlalchemy import text
from app.utils.data_loader import load_data_from_db, gse_engine, ac_engine

def test_load_gse_data():
    """Test loading data from gse_data table"""
    # First verify the database is populated
    engine = gse_engine
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM gse_data")).scalar()
        assert result > 0, "GSE database should be populated"
    
    # Test the query
    df = load_data_from_db(
        "gse_data",
        filters={"Ground support Equipment": ["F250", "FMC Commander 15"]},
        db="gse"
    )
    
    # Print debug information
    print("\nReturned DataFrame:")
    print(df)
    print("\nUnique equipment in result:", df["Ground support Equipment"].unique())
    
    assert not df.empty, "gse_data table should not be empty"
    assert len(df) == 2, f"Should return exactly 2 rows, got {len(df)} rows"
    assert set(df["Ground support Equipment"].unique()) == {"F250", "FMC Commander 15"}, \
        f"Should return exactly F250 and FMC Commander 15, got {df['Ground support Equipment'].unique()}"

def test_load_ac_data():
    """Test loading data from ac_data table"""
    # Test loading with multiple filters
    df = load_data_from_db(
        "ac_data", 
        filters={
            "MONTH": 7,
            "DATA_SOURCE": "DU"
        }, 
        db="ac"
    )
    assert not df.empty, "ac_data table should not be empty."
    
    # Also test without filters to verify data exists
    df_all = load_data_from_db("ac_data", db="ac")
    assert not df_all.empty, "ac_data table should not be empty."

if __name__ == "__main__":
    test_load_ac_data()
    test_load_gse_data()