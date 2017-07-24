#!/bin/python2

import sys
import json
import xml.etree.ElementTree
import copy
import re
import base64

tab = '    '
main_func = ''

class State:
    def __init__(self):
        self.is_func = False 
        self.is_array = False
        self.is_loop = False
        self.is_if = False
        self.func_name = ''
        self.func_args = []
    
    def indent(self):
        return self.is_if + self.is_loop + self.is_func

def drop(state, line):
    return ''

def fix_return(state, line):
    parts = line.split('=')
    if len(parts) == 2:
        if len(state.func_args) > 0:
            line = 'return PrintRes('+parts[1]+')'
        else:
            line = 'return ' + parts[1]
    return line

def break_if(state, line):
    state.is_if = True
    parts=re.split(' If | Then ',line)
    line = parts[0] + ' if ' + parts[1].replace('=','==') + ':\n%s' % (tab*state.indent()) + parts[2]
    state.is_if = False
    return line

def break_line(state, line):
    line = line.replace(': ', '\n%s' % (tab*state.indent()))
    return line

def start_func(state, line):
    global main_func
    state.is_func = True
    parts = re.split('\(|\)| ',line)
    state.func_name = parts[2]
    if len(parts[3]) == 0:
        main_func = state.func_name
    else:
        state.func_args = parts[3].split(',')
    return line + ':'
    
def modify_array_access(state, line):
    if state.is_func:
        for a in state.func_args:
            line = line.replace(a+'(', 'At('+a+',')
    return line

def end_func(state, line):
    state.is_func = False
    state.func_name = ''
    state.func_args = []
    return ''

def start_loop(state, line):
    state.is_loop = True
    return line + ':'
    
def end_loop(state, line):
    if state.is_loop:
        state.is_loop = False
    return ''

def start_array(state, line):
    state.is_array = True
    line = line.replace('Array(', '[')
    return line
    
def end_array(state, line):
    if (state.is_array):
        state.is_array = False
        line = line.replace(')', ']', 1)
    return line

def remove_type(state, line):
    l = ''
    parts = re.split('\(|\)|,',line)
    for i in range(len(parts)):
        p = parts[i]
        if p.find(' As ') >= 0:
            skip = False
            words = p.split(' ')
            for w in words:
                if w == '':
                    continue
                if w == 'As':
                    skip = True
                else:
                    if not skip:
                        if not i == 1:
                            l += ','              
                        l += w
                    skip = False
        else:
            l += p
            if i == 0:
                l += '('
    l += ')'
    return l
    
translations = [
    { 'from': 'Dim ', 'to': drop},
    { 'from': '_', 'to': ''},
    { 'from': ':', 'to': break_line },
    { 'from': 'Then', 'to': break_if },
    { 'from': 'Set ', 'to': ''},
    { 'from': ' Mod ', 'to': ' % '},
    { 'from': ' Xor ', 'to': modify_array_access},
    { 'from': ' Xor ', 'to': ' ^ '},
    { 'from': 'Obj.Run', 'to': 'return'},
    { 'from': 'UBound', 'to': 'len'},
    { 'from': 'Len', 'to': 'len'},
    { 'from': 'Chr', 'to': 'chr'},
    { 'from': 'Asc', 'to': 'ord'},
    { 'from': 'CInt', 'to': ''},
    { 'from': ' + 2', 'to': '+1'},
    { 'from': 'CreateObject', 'to': drop},
    { 'from': 'While', 'to': start_loop },
    { 'from': 'Wend', 'to': end_loop },
    { 'from': ' As ', 'to': remove_type },
    { 'from': ' Function ', 'to': start_func },
    { 'from': 'End Function', 'to': end_func },
    { 'from': 'Array(', 'to': start_array },
    { 'from': ')', 'to': end_array },
    { 'from': 'While ', 'to': 'while '},
    { 'from': '.Value()', 'to': ''},
    { 'from': '"', 'to': '\''},
    { 'from': 'ActiveDocument.Variables', 'to': 'VarValue'},
    { 'from': 'Public Function', 'to': 'def' },
    { 'from': 'Private Function', 'to': 'def' }
]

lab = sys.argv[1]
lab_json = lab + '.doc.json'
lab_xml = lab + '.xml'

print 'import sys'
print 'import base64'
print ''
print 'def Mid(s, i, l):'
print tab+'return s[i-1]'
print ''
print 'def At(s, i):'
print tab+'return s[i]'
print ''
print 'def VarValue(v):'
print tab+'return globals()[v]'
print ''
print 'def PrintRes(s):'
print tab+'print s'
print tab+'return s'
print ''

x = xml.etree.ElementTree.parse(lab_xml)
r = x.getroot()

c = r.find('{urn:schemas-microsoft-com:office:office}CustomDocumentProperties')
for cc in c:
    tag = cc.tag.split('}')[1]
    if tag == 'Editor':
        continue;
    if tag == 'Language':
        continue
    print( '%s="%s"' % (tag, cc.text) )
print ''

with open(lab_json, "r") as file:
    data = file.read()

j = json.loads(data)
l = len(j[1]['macros'])
code_lines = j[1]['macros'][l-1]['code'].split('\n')
s = State()
for l in code_lines:
    os = copy.deepcopy(s)
    for r in translations:
        if type(r['to']).__name__ == 'str':
            l = l.replace(r['from'], r['to'])
        elif type(r['to']).__name__ == 'function' and l.find(r['from']) >= 0:
            l = r['to'](s, l)
    #print "***"+os.func_name+"***"
    if os.is_func and l.find(os.func_name) >= 0:
        l = fix_return(s, l)
    print '%s%s' % (tab*os.indent(),l)

print ''
print 'if __name__ == \'__main__\':'
print tab+'(t,x)='+main_func+'()'
print tab+'print base64.b64decode(t.split()[6]).replace(\'\\x00\', \'\')'

