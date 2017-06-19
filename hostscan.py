##
##

from __future__ import print_function
from fabric import tasks
from fabric.api import env

import sys
import json
import fabtask
import catchinfo
import odcim

def gatherStats(stats, dbhost):
    pass

class HostDB:
    def __init__(self, lst=[]):
        self.db = {}
        for item in lst:
            self.db[item] = {}
    
    def remove(self, items):
        for it in items:
            self.db.pop(it, 0)

    def update(self, dct):
        for it in dct:
            if it in self.db:
                self.db[it].update(dct[it])
                

def json_print(jsn):
    return json.dumps(jsn, indent = 2, sort_keys=True)

def usage_msg():
    print("Usage: %s [all|test] [<file>]" % sys.argv[0])
        
def normalize_devinfo(devi):
    for dev in devi:
        dev['Owner'] = str(dev['Owner'])

def makedept(di):
    dept = {}
    for it in di:
        dept.update({ it['DeptID']: it['Name'] })
    return dept

def getowner(devinfo, dept):
    devdb = {}
    for it in devinfo:
        if 'Owner' in it:
            oid = str(it['Owner'])
            if oid in dept:
                devdb[it['Label'].lower()] = { 'owner': dept[oid] } 
    return devdb

def main():

    if len(sys.argv) == 1:
        usage_msg()
        exit()

    hosts_set = 'test'
    outp_file = 'myfile.json'

    if sys.argv[1] == 'all':
        hosts_set = 'all'

    if len(sys.argv) >= 3:
        outp_file = sys.argv[2]


    dcim = odcim.DcimApi()
    filter = odcim.FilterInfo()

    devinfo = dcim.devices()
    deptinfo = dcim.departments()

    dept = makedept(deptinfo)
    ownerinfo = getowner(devinfo, dept)


    exclude_hosts = ['dev-r-vrt-100', 'r-ufm89', 'r-ufm88', 'rsws09']

    # print(json_print(dbhost.db))
    # return

    env.commands = False
    env.user = 'root'
    test_hosts = ['hpchead', 'hpc-master', 'r-softiron-01', 'r-ufm189']

    if hosts_set == 'all':
        dbhost = HostDB(filter.getServedServers(devinfo))
    else:
        dbhost = HostDB(test_hosts)
        
    dbhost.remove(exclude_hosts)
    dbhost.update(ownerinfo)

    host_list = dbhost.db.keys()

    for hst in host_list:
        try:
            tasks.execute(fabtask.statistic, catchinfo.stats, dbhost.db, hosts=hst)
            print("Scanning complete. Writing info to file %s" % outp_file)
        except:
            print("Scanning failed. Trying to write results to file %s" % outp_file)
        finally:
            result = json_print(dbhost.db)

            try:
                with open(outp_file, 'w') as outp:
                    print(result, file=outp)
            except IOError as err:
                print("Error: cannot write info to file %s" % outp_file)
    
    print("Complete...")

if __name__ == '__main__':
    main()

