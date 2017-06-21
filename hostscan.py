##
##

from __future__ import print_function

import locale 

from fabric import tasks
from fabric.api import env
from fabric.exceptions import NetworkError

from hostdb import HostDB

import sys
import json
import fabtask
import catchinfo
import odcim

def gatherStats(stats, dbhost):
    pass

def json_print(jsn):
    return json.dumps(jsn, indent = 2)

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


    # dcim = odcim.DcimApi()
    # filter = odcim.FilterInfo()

    # devinfo = dcim.devices()
    # deptinfo = dcim.departments()

    # dept = makedept(deptinfo)
    # ownerinfo = getowner(devinfo, dept)


    exclude_hosts = ['dev-r-vrt-010', 'dev-r-vrt-011', 'dev-r-vrt-012', 'dev-r-vrt-013', 'dev-r-vrt-100', 'r-ufm89', 'r-aa-fatty10', 'hpc-arm-03', 'r-ufm116', 'r-ole17', 'r-ufm118', 'r-ufm88', 'rsws09']

    # print(json_print(dbhost.db))
    # return

    ## Configure fabric
    ## env.eagerly_disconnect = True
    ## env.parallel = True
    env.commands = False
    env.user = 'root'

    test_hosts = ['hpchead', 'hpc-master', 'r-softiron-01', 'r-ufm189']

    if hosts_set == 'all':
        # dbhost = HostDB(filter.getServedServers(devinfo))
        dbhost = HostDB('results/host170620bis.json')
    else:
        dbhost = HostDB(test_hosts)
        
    dbhost.remove(exclude_hosts)
    # dbhost.update(ownerinfo)

    # dbhost.store(sys.stdout)
    # exit()

    host_list = dbhost.db.keys()

    try:
        count = 1
        for hst in host_list:
            try:
                print("count: %s" % count)
                tasks.execute(fabtask.statistic, catchinfo.stats, dbhost.db, hosts=hst)
                count += 1
            except NetworkError as nerr:
                print("Scanning %s failed. Go for scanning next host" % hst)
            except EOFError:
                pass
    finally:
        try:
            with open(outp_file, 'w') as outp:
                dbhost.store(outp)
        except IOError as err:
            print("Error: cannot write results to file")
    
    print("Complete!")

if __name__ == '__main__':
    main()

