##
##
from collections import namedtuple

from fabric.api   import env, settings, task, local, run 
# from fabric       import state
# from fabric.tasks import execute


@task
def empty():
    return ''

@task
def resolve():
    with settings(warn_only=True):
        return local("host %s" % env.host, capture=True)

@task
def ping():
    with settings(warn_only=True):
        return local("ping -w 1 -c 1 %s" % env.host, capture=True)

@task
def sshaccess():
    with settings(warn_only=True):
        return run("uptime")

@task
def getcpuinfo():
    with settings(warn_only=True):
        return run("grep 'model name' /proc/cpuinfo | head -n 1")

@task
def getmeminfo():
    with settings(warn_only=True):
        return run("head -n 1 /proc/meminfo")

def resolve_info(inp):
    info = {}
    data = inp.split()
    info['fqdn'] = data[0]
    info['ip'] = data[-1]
    return info
    
def uptime_info(inp):
    return { 'uptime': inp }

def empty_info(imp):
    return {}

HostState = namedtuple('HostState','name action info' )

Initial = HostState('UNKNOWN', empty, empty_info)
Resolvable = HostState('RESOLVABLE', resolve, resolve_info)
Reachable = HostState('REACHABLE', ping, empty_info)
Accessible = HostState('ACCESSIBLE', sshaccess, uptime_info)

HostStates = [Resolvable, Reachable, Accessible]

