

def read_variable(varname, fname):
    import re
    stream = file(fname, 'r')
    text = stream.read()
    pattern = '#define\s+?'+varname+'\s+?(.+?)\s*?$'
    res = re.findall(pattern, text, re.M)
    if not res is None and len(res) > 0:
        res = res[0]
        try:
            res = eval(res)
        except:
            pass
    else : return None
    return res

def version_from_hex(hex_version):
    major = ((hex_version & 0xff0000) >> 16)
    minor = ((hex_version & 0x00ff00) >> 8)
    rev = (hex_version & 0x0000ff)
    return major, minor, rev

def strversion_from_hex(hex_version):
    major, minor, rev = version_from_hex(hex_version)
    return str(major)+'.'+str(minor)+'.'+str(rev)
