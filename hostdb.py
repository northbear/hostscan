import json

def json_print(jsn):
    return json.dumps(jsn, indent = 2)

class HostDB(dict):
    def __init__(self, param=[]):
        if isinstance(param, file):
            jsn = json.load(param)
            self.update(jsn)
        elif isinstance(param, str):
            with open(param) as f:
                self.update(json.load(f))
        elif isinstance(param, list):
            for item in param:
                self[item] = {}
        elif isinstance(param, dict):
            self.update(param)
        
    def remove(self, keys):
        for k in keys:
            self.pop(k, 0)

    def store(self, f):
        if isinstance(f, file):
            f.write(json.dumps(self, indent=2))
                
    def load(self, f):
        if isinstance(f, file):
            self = json.load(f)

    def select(self, query):
        result = { key: value for (key, value) in self.items() if dict_in(query, value) }
        return HostDB(result)
        

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
