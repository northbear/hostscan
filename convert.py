#
#

import json
import sys
import string

from hostdb import HostDB

forder = ['host', 'owner', 'fqdn', 'ip', 'cpu', 'ram', 'hcas', 'user_activity']

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

def killcomma(sdata):
    if isinstance(sdata, str) or isinstance(sdata, unicode):
        return string.replace(sdata, ',', '')
    else:
        return sdata
       
def header():
    return ', '.join(forder)

def rec2str(rec):
    data = []
    for fl in forder:
        data.append(killcomma(rec.get(fl, '')))
    return ', '.join(data)

def main():
    config = { 'input': sys.stdin, 'output': sys.stdout }
    
    db = load(config['input'])
    print header()
    for k in db:
        rec = db[k]
        print rec2str(rec)


if __name__ == '__main__':
    main()
