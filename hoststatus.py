##
##
# from collections import namedtuple

# from fabric.api   import env, settings, task, local, run 
from fabric       import state
from fabric.tasks import execute

import fabtask

class Host:
    def __init__(self, name, user=None):
        self._hostname = name
        self._status = HostStatus(name)
        self._access_user = user
        self._info = { 'host': name }

    def hostname(self):
        return self._hostname

    def accessname(self):
        if self._access_user != None:
            return "%s@%s" % (self._access_user, self._hostname)
        else:
            return self._hostname

    def status(self):
        return self._info['status']

    def isaccessible(self):
        return self._info['status'] == 'ACCESSIBLE'

    def queryinfo(self):
        self._status.query()
        self._info.update(self._status.info())
        return self._info

    def getinfo(self):
        self._status.query()
        self._info.update(self._status.info())
        return self._info

class HostStatus:
    def __init__(self, host):
        self._host = host
        self._info = { 'status': 0 }

    def query(self):
        host = self._host
        for state in fabtask.HostStates:
            result = execute(state.action, hosts=[self._host])
            if result[host].failed:
                break
            else:
                info = state.info(result[self._host])
                self._info.update(info)
                self._info['status'] = state.name

    def info(self):
        return self._info

class Grabber: 
    def __init__(self):
        pass
    def condition():
        pass

def HostRecord(name):
    return { name: { 'host': name }}

def main():
    state.output['everything'] = False
    # result = execute(getStatus, hosts=['hpchead','hpc-master', 'r-ufm93-ilo', 'r-ufm89-ilo'])
    # print result
    # host = Host('hpc-master')
    # print "host %s has status %s" % (host.hostname(), host.status())

    # for host in ['hpchead', 'hpc-master']:
    #     status = Host(host)
    #     print status.queryinfo()
    hostdb = {}
    hostdb.update(HostRecord('myhost1'))
    hostdb.update(HostRecord('myhost2'))

    print hostdb

if __name__ == '__main__':
    main()

