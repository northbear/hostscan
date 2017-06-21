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
    user, console, frm, logintime, duration = '', '', '', '', ''
    try:
        if 'system' in data[1]:
            data[1] = ' '.join(data[1:3])
            data.pop(2)
        user, console, frm = data[0], data[1], data[2]

        logintime = datetime.strptime(' '.join(data[3:7]), "%a %b %d %H:%M")
        logintime = logintime.replace(year=datetime.now().year)

        duration = data[9][1:-1]
        if '+' in duration:
            day, tme = duration.split('+')
        else:
            day, tme = '0', duration
        hour, minute = tme.split(':')
        duration = timedelta(int(day), 0, 0, 0, int(minute), int(hour))
    except IndexError:
        pass
    dct = { 'user': user, 'console': console, 'from': frm, 'logintime': logintime, 'duration': duration }
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
