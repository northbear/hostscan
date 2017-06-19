##
##

from abc import abstractmethod
from fabric import tasks
from fabric.api import execute

import fabtask
from fabtask import QueryType

class Catcher:
    def __init__(self, hostname, db):
        self._host = hostname
        self._db = db

    def run(self):
        if self.condition():
            resp = execute(fabtask.query, self.querystr(), hosts = self._host)
            info = self.postprocess(resp[self._host])
            try:
                self._db.update(info)
            except TypeError:
                print "Exception:", info, self.__name__

    @abstractmethod
    def condition(self):
        return True

    @abstractmethod
    def postprocess(self):
        pass

class HostResolve(Catcher):
    def querystr(self):
        return (QueryType.Local, "host %s" % self._host)
    
    def postprocess(self, inp):
        if inp.succeeded:
            rec = inp.split()
            return { 'status':'RESOLVABLE', 'fqdn':rec[0], 'ip':rec[-1] }
        else:
            return { 'status': 'UNKNOWN' }

class HostReach(Catcher):
    def condition(self):
        return 'status' in self._db and self._db['status'] == 'RESOLVABLE'

    def querystr(self):
        return (QueryType.Local, "ping -w 1 -c 1 %s" % self._host)

    def postprocess(self, inp):
        if not inp.failed:
            return { 'status': 'REACHABLE' }
        else:
            return { 'ping': inp }



class HostCPU(Catcher):
    def condition(self):
        return self._db.get('status', '') == 'REACHABLE'

    def querystr(self):
        return (QueryType.Remote, "grep 'model name' /proc/cpuinfo | head -n 1")

    def postprocess(self, inp):
        row = inp.split(':')
        try:
            return { 'cpu': row[1].strip() }
        except IndexError:
            return { 'cpu': row[0].strip() }


class HostMem(Catcher):
    def condition(self):
        return self._db.get('status', '') == 'REACHABLE'

    def querystr(self):
        return (QueryType.Remote, "free -g | grep 'Mem:'")
    
    def postprocess(self, inp):
        row = inp.split()
        return { 'ram': row[1].strip() }

class HostUsers(Catcher):
    def condition(self):
        return True 
## self._db.get('status', '') == 'REACHABLE'

    def querystr(self):
        return (QueryType.Remote, "last")
    
    def postprocess(self, inp):
        return { 'user_activity': inp }



class HostUptime(Catcher):
    def condition(self):
        return self._db.get('status', '') == 'REACHABLE'

    def querystr(self):
        return (QueryType.Remote, "uptime")
    
    def postprocess(self, inp):
        return { 'uptime': inp }

stats = [ HostResolve, HostReach, HostCPU, HostMem ]