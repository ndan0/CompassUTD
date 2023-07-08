import json
import os

secrets = None
google_key_path = None

try: # For local development, Deployment must load these variables from environment variables
    with open(os.path.join(os.path.dirname(__file__), "search_secrets.json"), "r") as f:
        secrets = json.load(f)
    # Get the file location of google_key.json from everywhere
    google_key_path = os.path.join(os.path.dirname(__file__), "google_key.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_key_path
except:
    print("Not in local development mode, skipping loading secrets.json and google_key.json")
    pass


