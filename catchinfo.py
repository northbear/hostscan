##
##

from abc import abstractmethod
from fabric import tasks


class Catcher:
    def __init__(self, hostname, db):
        self._host = hostname
        self._db = db

    def run(self):
        if self.condition():
            resp = execute(query, self.querystr(), hosts = self._host)
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
        return (Query.Local, "host %s" % self._host)
    
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
        return (Query.Local, "ping -w 1 -c 1 %s" % self._host)

    def postprocess(self, inp):
        if not inp.failed:
            return { 'status': 'REACHABLE' }
        else:
            return { 'ping': inp }

class HostUptime(Catcher):
    def condition(self):
        return self._db.get('status', '') == 'REACHABLE'

    def querystr(self):
        return (Query.Remote, "uptime")
    
    def postprocess(self, inp):
        return { 'uptime': inp }

stats = [ HostResolve, HostReach, HostUptime ]
