from src.config.setup import load_config, validate_config

# Load configuration
config = load_config("config/data.yaml")
print("Loaded Configuration:", config)

# Validate configuration
is_valid = validate_config(config)
print("Configuration Validity:", is_valid)
