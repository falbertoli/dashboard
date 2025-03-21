# File: backend/tests/test_config.py
import os
from app.config import config, DevelopmentConfig, TestingConfig, ProductionConfig

# def test_config_paths():
#     """Test that configuration paths are correct."""
#     # Test development config
#     dev_config = config['development']
#     print(f"Development DATA_DIR exists: {os.path.exists(dev_config.DATA_DIR)}")
#     print(f"Development AC_DB_URI: {dev_config.AC_DB_URI}")
#     print(f"Development GSE_DB_URI: {dev_config.GSE_DB_URI}")
    
#     # Test production config
#     prod_config = config['production']
#     print(f"Production DATA_DIR exists: {os.path.exists(prod_config.DATA_DIR)}")
#     print(f"Production AC_DB_URI: {prod_config.AC_DB_URI}")
#     print(f"Production GSE_DB_URI: {prod_config.GSE_DB_URI}")
    
#     # Test that config paths are absolute
#     print(f"DATA_DIR is absolute: {os.path.isabs(DevelopmentConfig.DATA_DIR)}")

def test_development_config(app):
    """Test development configuration."""
    app.config.from_object('app.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['AC_DB_URI'].endswith('ac_data.db')
    assert app.config['GSE_DB_URI'].endswith('gse_data.db')

def test_testing_config():
    """Test testing configuration."""
    from app import create_app
    app = create_app('testing')
    assert app.config['TESTING']
    assert app.config['AC_DB_URI'] == 'sqlite:///:memory:'
    assert app.config['GSE_DB_URI'] == 'sqlite:///:memory:'

def test_production_config():
    """Test production configuration."""
    from app import create_app
    app = create_app('production')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['AC_DB_URI'].endswith('ac_data.db')
    assert app.config['GSE_DB_URI'].endswith('gse_data.db')

# if __name__ == "__main__":
#     test_config_paths()