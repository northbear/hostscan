#!/usr/bin/env python 

import requests
import urlparse
import json


class DcimApi:
    def __init__(self):
        self._base_url = 'https://dcim-swx.mtr.labs.mlnx/api/v1/*'
        self._auth = ( 'igoryu', 'KJy987dsf' )
        # self._auth = ( 'igoryu', 'ac00d3e3465946eab8e85e759f48fa72' )        
        self._verify = False
        
    def request(self, cmd = 'device'):
        req = urlparse.urljoin(self._base_url, cmd)
        resp = requests.get(req, auth=self._auth, verify=self._verify)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}

    def __getdict(self, resp, cmd):
        if cmd in resp:
            return resp[cmd]

    def devices(self):
        return self.__getdict(self.request('device'), 'device')
        
    def departments(self):
        return self.__getdict(self.request('department'), 'department')


class HostDBFromDcim(dict):
    def __init__(self, devs, depts):
        for d in devs: 
            if d['DeviceType'] == 'Server':
                 self.update({ d['Label'].lower(): {} })


class FilterInfo:
    def servedDepartments(self):
        return {13, 12, 3, 9, 2, 8, 6, 1, 10, 11, 7, 4}

    def getServedServers(self, dev):
        return ( info['Label'].lower() for info in dev if info['DeviceType'] == 'Server' and info['Owner'] in self.servedDepartments() )



def print_pretty(data):
    print(json.dumps(data, indent=2))

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
