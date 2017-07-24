import sys
import json
import fileinput
import copy
from os import walk

min_length = 298

def convert_to_builtin_type(obj):
    d = {}
    try:
        d = obj.toJSON()
    except:
        # Convert objects to a dictionary of their representation
        d.update(obj.__dict__)
    return d

class Function:
    def __init__(self, offset):
        self.offset = offset
        self.length = 0
        self.code = []
        self.code_length = 0
    
class Malware:
    def __init__(self, name):
        self.functions = []
        self.name = name
        
        print 'reading %s...' % name
        begin = False
        base = 0
        function = Function(-1)
        for line in open(name).readlines():
            if line.find('<.text>') >= 0:
                begin = True
                parts = line.split(' ')
                base = int(parts[0], 16)
                continue
            
            if not begin:
                continue
            
            parts = line.split(':')
            offset = int(parts[0], 16)
            
            if function.offset == -1:
                function.offset = offset - base
            
            ops = [ x for x in parts[1].split('\t')[1].split(' ') if len(x) == 2 ]
            code = []
            for o in ops:
                op = int(o,16)
                code.append(hex((op & 0xf0) >> 4)[2:])
                code.append(hex(op & 0x0f)[2:])
            function.code.extend(code)
            if parts[1].find('ret') > 0:
                function.length = (offset - base) - function.offset + 1
                function.code_length = len(function.code)
                self.functions.append(function)
                function = Function(offset - base + 1)
                

malwares = []
files = []
for (dirpath, dirnames, filenames) in walk('./objdump'):
    files.extend(filenames)
    break

for f in files:
    m = Malware('./objdump/'+f)
    malwares.append(m)
    
#data_json = json.dumps(malwares, indent=2, default=convert_to_builtin_type)
#print data_json
'''
commons = None
for m in malwares:
    unique = list(set([f.length for f in m.functions if f.length >= min_length]))
    print m.name, unique
    if commons == None:
        commons = unique
    else:
        m_lengths = unique
        #print m.name, sorted(m_lengths)
        commons = list(set([i for i in commons if i in m_lengths]))
'''
commons = [ 298 ]

suspects = {}
for c in commons:
    suspects[c] = {}
for m in malwares:
    for c in commons:
        funcs = list(set([f for f in m.functions if f.length == c]))
        for f in funcs:
            suspects[c].setdefault(f.code[0], []).append({'name': m.name, 'func': f})

for l, scommon in suspects.iteritems():
    print '****************************************', l
    for p, s in scommon.iteritems():
        data = None
        for f in s:
            if data == None:
                data = copy.deepcopy(f['func'].code)
            else:
                for i in range(0, len(data)):
                    if not data[i] == f['func'].code[i]:
                        data[i] = '?'
        pdata = ''
        d = 0
        while d < len(data):
            if d > 0:
                pdata += ' '
            pdata += str(data[d]) + str(data[d+1])
            d += 2
        print '[%u/%u]' % (pdata.count('?'), len(pdata)), pdata
        
#data_json = json.dumps(malwares, indent=2, default=convert_to_builtin_type)
#print data_json

#data_json = json.dumps(suspects, indent=2, default=convert_to_builtin_type)
#print data_json


