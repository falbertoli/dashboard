from app.utils.data_loader import load_data_from_db

def test_load_ac_data():
    # Test loading data from ac_data table
    df = load_data_from_db("ac_data", filters={"MONTH": 7, "DATA_SOURCE": "DU"}, db="ac")
    assert not df.empty, "ac_data table should not be empty."
    print(df.head())

def test_load_gse_data():
    # Test loading data from gse_data table
    df = load_data_from_db("gse_data", filters={"Ground support Equipment": ["F250", "FMC Commander 15"]}, db="gse")
    assert not df.empty, "gse_data table should not be empty."
    print(df.head())

if __name__ == "__main__":
    test_load_ac_data()
    test_load_gse_data()