import json

def json_print(jsn):
    return json.dumps(jsn, indent = 2)

class HostDB:
    def __init__(self, param=[]):
        if isinstance(param, file):
            self.db = json.load(param)
        elif isinstance(param, str):
            with open(param) as f:
                self.db = json.load(f)
        elif isinstance(param, list):
            self.db = {}
            for item in param:
                self.db[item] = {}
    
    def remove(self, keys):
        for k in keys:
            self.db.pop(k, 0)

    def update(self, dct):
        for it in dct:
            if it in self.db:
                self.db[it].update(dct[it])

    def store(self, f):
        if isinstance(f, file):
            f.write(json.dumps(self.db, indent=2))
                
    def load(self, f):
        if isinstance(f, file):
            self.db = json.load(f)

    def select(self, query):
        result = { key: value for (key, value) in self.db.items() if dict_in(query, value) }
        return result
        

def dict_in(d1, d2):
    if not (isinstance(d1, dict) and isinstance(d2, dict)):
        return False
    for (key, value) in d1.items():
        try:
            if d2[key] != value:
                return False
        except KeyError:
            return False
    return True
