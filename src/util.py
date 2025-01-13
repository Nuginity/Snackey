import yaml

def readyaml(path):
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error Loading YAML Files, exiting: {e}")
            return None
        
def load_config(file_path="config.yaml"):
    """
    Memuat konfigurasi dari file YAML yang diberikan.
    """
    return readyaml(file_path)

config = load_config()