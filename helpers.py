##
##

from datetime import date, time, datetime

def parselastrows(inp):
    lst = inp.split("\n")[:-3]
    return lst

def parselastrecord(inp):
    data = inp.split()
    user, console, frm, dttm, duration = '', '', '', '', ''
    try:
        user, console, frm = data[0], data[1], data[2]
        dttm = ' '.join(data[3:7])
    except IndexError:
        pass
    dct = { 'user': user, 'console': console, 'from': frm, 'logintime': dttm, 'duration': duration }
    return dct
