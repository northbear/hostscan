#
#

import json
import sys

class DbTotals:
    def __init__(self, db):
        self.__db = db
        self.__totals = { 'total': len(db) }

    def calc(self, value, cond): 
        pass
        

    def string(self):
       return str(self.__totals)


def load(fp):
    jsn = {}
    if isinstance(fp, basestring):
        with open(fp) as f:
            jsn = json.load(f)
    elif isinstance(fp, File):
        jsn = json.load(fp)
    else:
        raise TypeError("parameter should be file or string containing path to file")
    return jsn

def conv2csv(db, fields, outp):
    pass

def rec2str(rec):
    return ', '.join([rec.get('owner', ''), rec.get('fqdn', ''), rec.get('ip', ''), rec.get('cpu', ''), rec.get('ram', '')])

def main():
    config = { 'input': sys.stdin, 'output': sys.stdin }
    
    config['input'] = "results/hostinfo170618.json"
    db = load(config['input'])
    for k in db:
        rec = db[k]
        print ', '.join([k, rec2str(rec)]) 
    stat = DbTotals(db) 
    print "stat:", stat.string()
    flist = []
    conv2csv(db, flist, config['output'])


if __name__ == '__main__':
    main()
