import os
import sys
import json

class Database():
    def __init__(self, db_file: str) -> None:
        self.filename: str = db_file
        self.load()

    def sync(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.json_data, f, indent=4)

    def load(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.json_data = json.load(f)
            except json.JSONDecodeError:
                sys.exit('Incorrect json format in data file, exitting...')
        else:
            self.json_data = dict()
            self.sync()

    def get(self) -> dict[str]:
        return self.json_data

    def add_association(self, emote: str, role: str) -> None:
        self.json_data[emote] = role
        self.sync()

    def remove_association(self, emote: str) -> None:
        del self.json_data[emote]
        self.sync()