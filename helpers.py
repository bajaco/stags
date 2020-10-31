def attributes_pair_add(adict,key,value):
    if not key in adict:
        adict[key] = value
    else:
        if isinstance(adict[key], list):
            adict[key].append(value)
        else:
            adict[key] = [adict[key], value]


def attributes_pairs(text):
    attributes = {}
    key = ''
    value = ''
    first = True
    opener = ''
    for c in text:
        if first:
            if c != ' ':
                if c != '=':
                    key += c
                else:
                    first = False
        else:
            if len(value) == 0 and opener == '':
                if c != ' ':
                    opener = c
               
            else:
                if c == opener:
                    
                    attributes_pair_add(attributes, key, value)
                    key = ''
                    value = ''
                    opener = ''
                    first = True
                elif c == ' ':
                    attributes_pair_add(attributes, key, value)
                    
                    value = ''
                else:
                    value += c

    return attributes


