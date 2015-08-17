
def rmload_start_end(el, field, startstr, endstr):
    value = el.get_output_value(field)
    if value is not None:
        spos = value.find(startstr)
        if spos != -1:
            epos = value.find(endstr, spos+len(startstr))
            if epos != -1:
                newvalue = value[:spos] + value[epos + len(endstr):]
                el.replace_value(field, newvalue)
    return el

def rmload_string(el, field, str):
    value = el.get_output_value(field)
    if value is not None:
        pos = value.find(str)
        if pos != -1:
            newvalue = value[:pos] + value[pos+len(str):]
            el.replace_value(field, newvalue)
    return el
        


