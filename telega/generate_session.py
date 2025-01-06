# telega/generate_session.py
import json
from pyrogram import Client

with open("telega/session_keys.json", "r") as f:
    keys = json.load(f)

api_id = int(keys["api_id"])
api_hash = keys["api_hash"]

app = Client("user_session", api_id=api_id, api_hash=api_hash)

with app:
    print("Session string generated successfully!")
    session_string = app.export_session_string()
    print("\nYour session string:\n")
    print(session_string)

    with open("telega/session_keys.json", "w") as f:
        keys["session_string"] = session_string
        json.dump(keys, f, indent=4)

    print("\nSession string has been saved to 'telega/session_keys.json'")
