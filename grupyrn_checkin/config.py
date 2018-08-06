import json
import pkg_resources

path = 'config.json'  # always use slash
filepath = pkg_resources.resource_filename(__name__, path)

with open(filepath, 'r') as f:
    config = json.load(f)


def get(key):
    return config.get(key)
