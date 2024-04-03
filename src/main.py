import yaml
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():

    with open("onion_links/collection.yaml", "r") as f:
        data = yaml.safe_load(f)
    print(data)