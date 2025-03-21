# File backend/app/utils/validation.py
def validate_required_params(data, required_params):
    for param in required_params:
        if param not in data or data[param] is None:
            raise ValueError(f"Missing required parameter: {param}")
