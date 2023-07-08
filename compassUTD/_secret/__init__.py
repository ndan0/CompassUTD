import json
import os

with open(os.path.join(os.path.dirname(__file__), "secrets.json"), "r") as f:
    secrets = json.load(f)

# Get the file location of google_key.json from everywhere
google_key_path = os.path.join(os.path.dirname(__file__), "google_key.json")
