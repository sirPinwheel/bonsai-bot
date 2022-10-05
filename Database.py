import os
import sys
import json
from typing import Dict

class Database():
    def __init__(self, db_file: str) -> None:
        self.filename: str = db_file
        self.load()

    def sync(self) -> None:
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.json_data, f, indent=4)
        except IOError as e:
            print(f'I/O error({e.errno}): {e.strerror}')
        except:
            print('Unexpected error while writing to file')


    def load(self) -> None:
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.json_data = json.load(f)
            else:
                self.json_data = dict()
        except json.JSONDecodeError:
            sys.exit('Incorrect json format in data file, exitting...')
        except IOError as e:
            sys.exit(f'I/O error({e.errno}): {e.strerror}')
        except:
            sys.exit('Unexpected error while reading from file')
        self.sync()

    def get(self) -> Dict[str, str]:
        return self.json_data

    def set(self, emote: str, role: str) -> bool:
        if emote not in self.json_data:
            self.json_data[emote] = role
            self.sync()
            return True
        else:
            return False

    def remove(self, emote: str) -> bool:
        if emote in self.json_data:
            del self.json_data[emote]
            self.sync()
            return True
        else:
            return False