##
##

from datetime import timedelta, datetime

class LastParser:
    pass

def parselastrows(inp):
    lst = inp.split("\n")[:-3]
    return lst

def reducelastrows(inp):
    return filter((lambda x: 'logged' not in x and 'system' not in x), inp)

def parselastrecord(inp):
    data = inp.split()
    user, console, logintime, duration = '', '', '', ''
    
    # data[1] = ' '.join(data[1:3])
    # data.pop(2)
    user, console = data[0], data[1]

    logintime = datetime.strptime(' '.join(data[3:7]), "%b %d %H:%M:%S %Y")
    logintime = logintime.replace(year=datetime.now().year)

    duration = data[-1][1:-1]
    if '+' in duration:
        day, tme = duration.split('+')
    else:
        day, tme = '0', duration
    hour, minute = tme.split(':')
    duration = timedelta(int(day), 0, 0, 0, int(minute), int(hour))
    dct = { 'user': user, 'console': console, 'logintime': logintime, 'duration': duration }
    return dct

def getstat(db):
    root = { 'user': 'root', 'amount': 0, 'duration': timedelta() }
    others = { 'user': 'others', 'amount': 0, 'duration': timedelta() }
    for k in db:
        if k['user'] == 'root':
            root['amount'] += 1
            root['duration'] += k['duration']
        else:
            others['amount'] += 1
            others['duration'] += k['duration']

    return [ root, others ] 

def stat2string(inp):
    resp = []
    for item in inp:
        if isinstance(item, dict):
            resp.append("%s:%s|%s" % (item.get('user', ''), item.get('amount', ''), item.get('duration', '')))
    return ';'.join(resp)

def trimelderrecs(recs, date):
    last = 0
    for rec in recs:
        last += 1
        if rec['logintime'] < date:
            break
    return recs[0:last-1]

