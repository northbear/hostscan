#!/usr/bin/env python 

import requests
import urlparse
import json


class HostDBFromDcim:
    def __init__(self, devs, depts):
        self.dictionaries = {}

        self.dictionaries['owner'] = {}
        for dept in depts:
            self.dictionaries['owner'][dept['DeptID']] = dept['Name']

        self.devices = devs

    def makerec(self, rec, dcts):
        # print rec['Owner'], dcts
        resp = {}
        resp['host'] = rec['Label'].lower()
        resp['owner'] = dcts['owner'].get(str(rec['Owner']), 'unknown')
        resp['type'] = rec['DeviceType'].lower()
        return resp

    def produce(self, devdb):
        for d in self.devices: 
            devdb.update({ d['Label'].lower(): self.makerec(d, self.dictionaries) })

        

def print_pretty(data):
    print json.dumps(data, indent=2)

def main():
    dcim = DcimApi()
    resp = dcim.request()

    devinfo = dcim.devices() 
    # print_pretty(devinfo)
    # print_pretty(dcim.request('department'))
    # print_pretty(dcim.departments())
    for h in FilterInfo().getServedServers(devinfo):
       print h


if __name__ == '__main__':
    main()
