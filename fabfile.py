##
##
from fabric.api import task, local, run, env

# env.use_ssh_config = True


def dello():
    print "Hello, %s" % env.host

def resolvable():
    with settings(warn_only=True):
        result = local("host %s" % env.host)
        # print type(result)
        if result.failed: 
            print "wrong, wrong server - %s" % env.host
            return False
        return True


def reachable():
    with settings(warn_only=True):
        result = local( "ping -w 1 -c %d %s" % (1, env.host) )
        if result.failed:
            print "server %s is unavailable" % env.host
            return False
        return True

def getStatus(): 
    status = None
    if resolvable():
        status = 'RESOLVABLE'
    elif  reachable():
        status = 'REACHABLE'
    print "Server %s status is %s" % (env.host, status)

def uname():
    resp = run('uname -a')
    return resp
