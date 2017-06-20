#
#

import json
import sys

from hostdb import HostDB

def load(fp):
    jsn = {}
    if isinstance(fp, basestring):
        with open(fp) as f:
            jsn = json.load(f)
    elif isinstance(fp, file):
        jsn = json.load(fp)
    else:
        raise TypeError("parameter should be file or string containing path to file")
    return jsn

def conv2csv(db, fields, outp):
    pass

def rec2str(rec):
    return ', '.join([rec.get('owner', ''), rec.get('fqdn', ''), rec.get('ip', ''), rec.get('cpu', ''), rec.get('ram', ''), rec.get('hcas', '')])

def main():
    config = { 'input': sys.stdin, 'output': sys.stdin }
    
    db = load(config['input'])
    for k in db:
        rec = db[k]
        print ', '.join([k, rec2str(rec)]) 


if __name__ == '__main__':
    main()
