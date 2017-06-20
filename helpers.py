##
##

from datetime import date, time, datetime

class LastParser:
    pass

def parselastrows(inp):
    lst = inp.split("\n")[:-3]
    return lst

def reducelastrows(inp):
    return filter((lambda x: 'logged' not in x), inp)

def parselastrecord(inp):
    data = inp.split()
    user, console, frm, logintime, duration = '', '', '', '', ''
    try:
        user, console, frm = data[0], data[1], data[2]
        logintime = datetime.strptime(' '.join(data[3:7]), "%a %b %d %H:%M")
        logintime = logintime.replace(year=datetime.now().year)
    except IndexError:
        pass
    dct = { 'user': user, 'console': console, 'from': frm, 'logintime': logintime, 'duration': duration }
    return dct
