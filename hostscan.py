##
##

## from __future__ import print_function

import locale 

from fabric import tasks
from fabric.api import env
from fabric.network import ssh
from fabric.exceptions import NetworkError

from hostdb import HostDB

import sys
import json
import fabtask
import catchinfo
import odcim
import dcim2devdb

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


def scanservers(hosts, hostdb):
    count = 1
    for hst in hosts:
        try:
            print "[%s] count: %s" % (hst, count)
            tasks.execute(fabtask.statistic, catchinfo.stats, hostdb, hosts=[hst])
            count += 1
        except NetworkError as nerr:
            print("Scanning %s failed. Go for scanning next host" % hst)
        except EOFError:
            pass
        except:
            print "Error: unknown problem while scanning server %s" % hst

def print_db(db, count):
    for it in db:
        print it, db[it] 

def loadDataFromDcim(devicedb):
    dcim = odcim.DcimApi()

    devices = dcim.devices()
    depts = dcim.departments()

    converter = dcim2devdb.HostDBFromDcim(devices, depts)
    converter.produce(devicedb)


def main():


    if len(sys.argv) == 1:
        usage_msg()
        exit()

    hosts_set = 'test'
    outp_file = 'myfile.json'

    if sys.argv[1] in ['all', 'test', 'dpdk']:
        hosts_set = sys.argv[1]
    else:
        print "Error: wrong hosts set given"
        exit()

    if len(sys.argv) >= 3:
        outp_file = sys.argv[2]


    devicedb = HostDB()

    exclude_hosts = ['dev-r-vrt-010', 'dev-r-vrt-011', 'dev-r-vrt-012', 'dev-r-vrt-013', 'dev-r-vrt-100', 'r-ufm89', 'r-aa-fatty10', 'hpc-arm-03', 'r-ufm116', 'r-ole17', 'r-ufm118', 'r-ufm88', 'rsws09', 'dragon7']

    loadDataFromDcim(devicedb)
    serversdb = devicedb.select({ 'type': 'server' })
    serversdb.remove(exclude_hosts)

    ## Configure fabric
    ## env.eagerly_disconnect = True
    ## env.parallel = True
    env.commands = False
    env.user = 'root'
    ssh.util.log_to_file("/tmp/paramiko.log", 10)

    test_hosts = ['hpchead', 'hpc-master', 'r-softiron-01', 'r-ufm189']

    dbhost = {}
    if hosts_set == 'test':
        dbhost = HostDB(test_hosts)
    elif hosts_set == 'dpdk':
        dbhost = serversdb.select({ 'owner': 'DPDK'})
        dbhost.remove(['dragon7'])
        print 'Process DPDK. Total amount %s servers...' % len(dbhost)
    elif hosts_set == 'all':
        dbhost = serversdb
        dbhost.remove(exclude_hosts)

    host_list = dbhost.keys()
    print "Total amount of servers to scan: %s" % len(host_list)

    try:
        scanservers(host_list, dbhost)

    finally:
        try:
            with open(outp_file, 'w') as outp:
                dbhost.store(outp)
        except IOError as err:
            print("Error: cannot write results to file")
    
    print("Complete!")

if __name__ == '__main__':
    main()

