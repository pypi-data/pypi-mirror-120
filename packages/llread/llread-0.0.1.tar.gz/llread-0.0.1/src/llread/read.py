import json

def read():
        with open('config.json', 'r') as f:
                config_data=f.read()
        config = json.loads(config_data)
        print(config)