import json
def load_config(path: str) -> dict:
    """
    Load configuration settings from a JSON file.
    Args:
        path (str): The file path for the JSON file you want to load.
    Returns:
        config (dict): The JSON as a dictionary.

    """
    with open(path, 'r') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    config = load_config('Config.json')
    print(config)
    print(type(config))
    categories = config.keys()
    print(categories)
    values = config.values()
    print(values)

