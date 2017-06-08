##
##
from collections import namedtuple

from fabric.api   import env, settings, task, local, run 
# from fabric       import state
from fabric.tasks import execute

import json


class Query:
    Local  = 1
    Remote = 2

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
    rec = inp.split()
    return { 'fqdn':rec[0], 'ip':rec[-1]}
    
def uptime_info(inp):
    return { 'uptime': inp }

def empty_info(inp):
    return {}

@task
def query_local(cmd):
    with settings(warn_only=True):
        return local(cmd, capture=True)

@task
def query_remote(cmd):
    with settings(warn_only=True):
        return run("head -n 1 /proc/meminfo")

@task
def query(req):
    with settings(warn_only=True):
        if req[0] == Query.Local:
            return local(req[1], capture=True)
        else:
            return run(req[1])
        
@task
def statistic(stats, db):
    for stat in stats:
        if env.host not in db:
            db[env.host] = {}
        s = stat(env.host, db[env.host])
        s.run()


