from app.utils.data_loader import populate_database, ac_engine, gse_engine

def test_populate_databases():
    # Populate ac_data.db
    populate_database("ac_data.csv", ac_engine, "ac_data")

    # Populate gse_data.db
    populate_database("gse_data.csv", gse_engine, "gse_data")

    print("Databases populated successfully.")

if __name__ == "__main__":
    test_populate_databases()