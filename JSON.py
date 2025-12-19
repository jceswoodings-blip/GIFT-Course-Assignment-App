import json
def load_config(path: str) -> dict:
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

