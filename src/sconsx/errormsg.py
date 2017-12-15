

def critical(txt, *arg):
    raise ValueError(txt, *arg)

def error(txt, *arg):
    msg = '*** Error :' + txt
    if len(arg) > 0 : msg += ' : ' + map(str,arg)
    print(msg)

def warning(txt, *arg):
    msg = '*** Warning :' + txt
    if len(arg) > 0 : msg += ' : ' + map(str,arg)
    print(msg)

