import os
import sys
import json

class Database():
    def __init__(self, db_file):
        self.filename = db_file
        self.load()

    def sync(self):
        with open(self.filename, 'w') as f:
            json.dump(self.json_data, f, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.json_data = json.load(f)
            except json.JSONDecodeError:
                sys.exit('Incorrect json format in data file, exitting...')
        else:
            self.json_data = dict()
            self.sync()

    def get(self):
        return self.json_data

    def add_association(self, emote, role):
        self.json_data[emote] = role
        self.sync()

    def remove_association(self, emote):
        del self.json_data[emote]
        self.sync()