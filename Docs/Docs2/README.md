# Documents track - Challange #2

When we unzip the challange file, we get a whole lot of documents, 1337 to be exact.

If we open a single document using LibreOffice, we see a document when looks very much like the embedded document we found in Docs1. Further examination reveals the document contains similar Macros and Custom Properties as in Docs1.

So, we're goind to have to automate what we did in Docs1. Good thing we translated VBA to Python :-)

1st, we need to conver the documents to a more computer-friendly format.
We will use *oletools* to convert to json, but we need another format that will expose the Custom Properties, since *oletools* can't see them. We'll use LibreOffice to convert to XML.

```bash
for ff in pkg/*.doc; do
    olevba -j ${ff}  > ${ff}.json
    soffice --headless --convert-to xml ${ff}
done
```
Now we can write the conversion script which will convert the *VBA* and *Properties* from each document into *Python*

Create some utility functions for the VBA->Python translation
```python
tab = '    '

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
```
Read the Custom Properties and write them as Python code
```python
import xml.etree.ElementTree

lab_json = sys.argv[1] + '.xml'
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
```
Read the VBA code and convert to Python: this is done using a series of stateful search/replace operations
```python
import json
import copy
import re
import base64

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

lab_json = sys.argv[1] + '.doc.json'

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
```
The output of running this script on each document results in a Python file similar to this one:
```python
import sys
import base64

def Mid(s, i, l):
    return s[i-1]

def At(s, i):
    return s[i]

def VarValue(v):
    return globals()[v]

def PrintRes(s):
    print s
    return s

Info="8535297daa9f55f6c7e7e59af82908bb47eedc7d8a877b559211a0e25e71168e"
cASaGCAtFuc=""
eLvkYqD="kxw"
kmrmwB="...<VERY LONG>..."
lxlHpgs="pCkHF"
nlbiG="eLx"
uUraddz="sGNq"
vziLSWEn="...<VERY LONG>..."
zJTxqS="...<VERY LONG>..."

def sUPofBHPpg(BJcRgNedRY,SSUsYPSWRa):
    
    vNyQDXSsCa = VarValue('zJTxqS')
    PkQzVmeRsW = ''
    hrBvomJTpj = 1
    while hrBvomJTpj < len(BJcRgNedRY)+1:
        bbSHicjpnn = hrBvomJTpj % len(vNyQDXSsCa)
        if bbSHicjpnn == 0:
            bbSHicjpnn = len(vNyQDXSsCa)
        PkQzVmeRsW = PkQzVmeRsW + chr(ord(Mid(vNyQDXSsCa, bbSHicjpnn + SSUsYPSWRa, 1)) ^ (At(BJcRgNedRY,hrBvomJTpj - 1)))
        hrBvomJTpj = hrBvomJTpj + 1
        
    return PrintRes( PkQzVmeRsW)
    
def GJmLhJxtSqFSSGx():
    mXHYDYcv = sUPofBHPpg([27, 30, 5, 1, 8, 11, 13, 92, 10, 29, 25, 85, 34, 17, 32, 16, 12, 46, 6, 15, 22, 
    34, 73, 124, 45, 1, 23, 35, 13, 21, 40, 0, 7, 17, 72, 42, 45, 16, 18], 561)
    BEChyIOD = sUPofBHPpg([33, 27, 59, 57, 23, 123, 57, 36, 40, 53, 21, 72, 32, 25, 38, 35, 25, 26, 119, 20, 41, 
    118, 15, 23, 49, 16, 119, 114, 114, 122, 36, 15, 18, 9, 22, 66, 117, 120, 0, 14, 57, 
    0, 56, 41, 22, 54, 77, 24, 109, 36, 112, 43, 51, 35, 43, 37, 15, 37, 27, 22, 117, 
    1, 56, 27, 37, 119, 112, 36, 9, 26, 42, 117, 27, 8, 1, 28, 57, 11, 7, 6, 48, 
    59, 15, 20, 121, 48, 76, 34, 25, 84, 32, 15, 14, 4, 10, 54, 12, 54, 2, 52, 14, 
    4, 37, 45, 43, 53, 37, 16, 13, 33, 14, 119, 18, 27, 56, 0, 4, 14, 42, 4, 38, 
    47, 22, 55, 36, 23, 98, 0, 54, 62, 5, 22, 23, 21, 36, 13, 48, 114, 40, 2, 36, 
    5, 119, 50, 16, 22, 112, 10, 49, 117, 51, 45, 59, 23, 3, 48, 24, 41, 22, 18, 58, 
    44, 56, 85, 46, 112, 11, 3, 28, 48, 21, 0, 46, 113, 119, 43, 40, 100, 16, 46, 39, 
    36, 124, 47, 29, 37, 15, 15, 40, 0, 15, 47, 16, 39, 118, 87, 8, 43, 97, 55, 49, 
    48, 27, 49, 19, 112, 34, 19, 63, 56, 47, 52, 12, 2, 13, 115, 44, 53, 55, 31, 8, 
    15, 114, 41, 43, 42, 38, 3, 39, 16], 13)
    vXdDrhSV = sUPofBHPpg([42, 23, 113, 4, 15, 2, 2, 34, 10, 11, 13, 30, 14, 9, 56, 0, 32, 119, 36, 120, 45, 
    15, 57, 44, 3, 121, 33, 57, 40, 94, 39, 15, 42, 20, 124, 114, 46, 51, 114, 50, 61, 
    52, 33, 20, 19, 47, 39, 2, 57, 53, 34, 52, 44, 38, 23, 49, 11, 116, 120, 45, 116, 
    87, 51, 115, 49, 46, 3, 45, 113, 53, 50, 33, 9, 47, 34, 45, 51, 16, 46, 112, 113, 
    46, 11, 37, 4, 51, 35, 12, 59, 6, 25, 121, 21, 107, 48, 10, 36, 34, 21, 27, 50, 
    13, 22, 122, 73, 37, 122, 6, 41, 2, 53, 53, 120, 23, 44, 50, 52, 124, 121, 15, 57, 
    23, 60, 6, 14, 62, 7, 119, 0, 50, 120, 41, 112, 86, 116, 51, 50, 20, 28, 22, 113, 
    51, 114, 115, 49, 51, 19, 116, 0, 49, 2, 48, 8, 44, 58, 19, 112, 16, 32, 119, 42, 
    47, 17, 15, 3, 119, 50, 19, 52, 55, 124, 53, 118, 23, 49, 117, 9, 3, 39, 15, 37, 
    15, 27, 123, 2, 119, 57, 8, 116, 12, 34, 15, 37, 23, 47, 55, 26, 1, 51, 116, 57, 
    27, 11, 18, 15, 116, 56, 32, 28, 49, 120, 49, 45, 14, 19, 49, 60, 5, 30, 42, 18, 
    127, 39, 32, 39, 120, 33, 0, 10, 76], 331)
    KWYNkLDy = sUPofBHPpg([117, 117, 24, 40, 31, 117, 9, 17, 6, 24, 29, 117, 9, 51, 27, 105, 49, 38, 12, 120, 26, 
    15, 34, 7, 44, 20, 124, 20, 15, 4, 12, 29, 25, 118, 3, 43, 117, 50, 119, 125, 114, 
    60, 23, 50, 90, 40, 9, 22, 36, 57, 7, 46, 98, 11, 53, 21, 22, 60, 8, 11, 10, 
    22, 46, 18, 56, 46, 18, 46, 59, 32, 115, 26, 51, 30, 105, 27, 37, 11, 123, 96, 22, 
    46, 41, 2, 49, 34, 50, 121], 243)
    VgafpjZU = mXHYDYcv + BEChyIOD + vXdDrhSV + KWYNkLDy
    VBodWvPv = sUPofBHPpg([99, 61, 107, 29, 44, 3, 60, 127], 600)
    
    return VgafpjZU, 1

if __name__ == '__main__':
    (t,x)=GJmLhJxtSqFSSGx()
    print base64.b64decode(t.split()[6]).replace('\x00', '')
```
And if we run it we get
```
$ python lab_1_file.py
powershell -win normal -ep bypass -enc 
JABvAHUAdAB0AHkAPQBAACIACgA8ACAATgBvAHQAaABpAG4AZwAgAEgAZQByAGUAIABGAHIAaQBlAG4AZAAgAD4ACgAgACAAIAAgACAAIAAgACAAXAAgACAAIABeAF8AXwBeAAoAIAAgACAAIAAgACAAIAAgACAAXAAgACAAKABvAG8AKQBcAF8AXwBfAF8AXwBfAF8ACgAgACAAIAAgACAAIAAgACAAIAAgAC
AAIAAoAF8AXwApAFwAIAAgACAAIAAgACAAIAApAFwALwBcAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAB8AHwALQAtAC0ALQB3ACAAfAAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfAB8ACAAIAAgACAAIAB8AHwACgBnAHMAcgB0AAoAIgBAAAoAJABvAHUAdAB0AHkAIAA9
ACAAJABvAHUAdAB0AHkAIAAqADEAMAAwADAAMAAKAFcAcgBpAHQAZQAtAEgAbwBzAHQAIAAkAG8AdQB0AHQAeQA=
POSITION
$outty=@"
< Nothing Here Friend >
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
gsrt
"@
$outty = $outty *10000
Write-Host $outty
```
The "Nothing Here Friend" should not discourage you - some files will show a different output.
Now, let's modify the script to do this for all the documents
```bash
for ff in *.doc; do
    olevba -j ${ff}  > ${ff}.json
    soffice --headless --convert-to xml ${ff}
    file="${f%.*}"
    python2 ../extract_vba.py ${file} > ${file}.py
    python2 ${file}.py > ${file}.out
    res=`grep -c "Nothing Here Friend" ${file}.out`
    if [ $res -eq 0 ]
    then 
        echo ${file}
        echo ${file} >> all_out
        cat ${file}.out >> all_out
        echo -e "\n----------------------" >> all_out
    fi
done
```
Now, if we examine *all_out* we will see that some of the scripts resulted in a different-looking output
```
lab_70_file
powershell -win normal -ep bypass -enc 
JABvAHUAdAB0AHkAPQBAACIACgBfAAoAIAAgACAAXwBfAF8AXwAgAAoAIAAgACgAIABfAF8AIAApAAoAIAAvACAAXwBfACAAIAB8AAoALwAgAC8AXwAvACAALwAgAAoAX
ABfAF8AXwBfAC8AIAAgAAoAZwBzAHIAdAAKACIAQAAKACQAbwB1AHQAdAB5ACAAPQAgACQAbwB1AHQAdAB5ACAAKgAxADAAMA
AwADAACgBXAHIAaQB0AGUALQBIAG8AcwB0ACAAJABvAHUAdAB0AHkA
FOURTEEN
$outty=@"
_
   ____ 
  ( __ )
 / __  |
/ /_/ / 
\____/  
gsrt
"@
$outty = $outty *10000
Write-Host $outty

----------------------
```
The interesting bits are
```
FOURTEEN
```
which obviously tells us the position of the character in the key, and
```
   ____ 
  ( __ )
 / __  |
/ /_/ / 
\____/  
```
which is a character in ASCII-art font named "slant"

```
FOURTEEN
   ____ 
  ( __ )
 / __  |
/ /_/ / 
\____/
NINE
       __
  ____/ /
 / __  / 
/ /_/ /
\__,_/ 
FOUR
     __
   _/_/
 _/_/
< <
/ /
\_\
EIGHT
   ____ 
  ( __ )
 / __  |
/ /_/ / 
\____/
FIFTEEN
   _____
  |__  /
   /_ < 
 ___/ / 
/____/
SEVENTEEN
     _ 
    | |
    / /
   _>_>
 _/_/
/_/
TWO
    ___ 
   /   |
  / /| |
 / ___ |
/_/  |_|
THREE
    _   __
   / | / /
  /  |/ / 
 / /|  /
/_/ |_/ 
SIXTEEN
    ____
   / __/
  / /_
 / __/
/_/
SEVEN
   ____ 
  / __ \
 / /_/ /
 \__, / 
/____/
THIRTEEN
 _____
/__  /
  / / 
 / /
/_/
ONE
    ____ 
   / __ \
  / /_/ /
 / ____/ 
/_/
TEN
    __  
   / /_ 
  / __ \
 / /_/ /
/_.___/ 
FIVE
   _____
  / ___/
 / __ \ 
/ /_/ / 
\____/
SIX
   _____
  |__  /
   /_ < 
 ___/ / 
/____/
ELEVEN
   ____ 
  ( __ )
 / __  |
/ /_/ / 
\____/
TWELVE
    ______
   / ____/
  /___ \
 ____/ /
/_____/

```
And after we sort all of the ASCII art according to the locations we get
```
    ____     ___       _   __     __   _____    _____    ____     ____         __   __       ____     ______   _____   ____     _____    ____   _ 
   / __ \   /   |     / | / /   _/_/  / ___/   |__  /   / __ \   ( __ )   ____/ /  / /_     ( __ )   / ____/  /__  /  ( __ )   |__  /   / __/  | |
  / /_/ /  / /| |    /  |/ /  _/_/   / __ \     /_ <   / /_/ /  / __  |  / __  /  / __ \   / __  |  /___ \      / /  / __  |    /_ <   / /_    / /
 / ____/  / ___ |   / /|  /  < <    / /_/ /   ___/ /   \__, /  / /_/ /  / /_/ /  / /_/ /  / /_/ /  ____/ /     / /  / /_/ /   ___/ /  / __/   _>_>
/_/      /_/  |_|  /_/ |_/   / /    \____/   /____/   /____/   \____/   \__,_/  /_.___/   \____/  /_____/     /_/   \____/   /____/  /_/    _/_/
                             \_\                                                                                                           /_/    
```

which translates to our flag
```
PAN{6398db85783f}
```
