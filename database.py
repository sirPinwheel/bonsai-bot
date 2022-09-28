import os
import json

class Database():
    def __init__(self):
        self.filename = 'data.json'
        self.json_data = None
        
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.json_data = json.load(f)

        if self.json_data is None:
            with open(self.filename, 'w') as f:
                f.write('{}')
