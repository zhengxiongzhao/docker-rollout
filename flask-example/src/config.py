import yaml

# Load configuration from YAML file
with open('application.yaml', 'r') as f:
    config = yaml.safe_load(f)