# Threat track - Challange #2

Our challange is to write a YARA rule that will match all the given malware samples.

Since I insisted on using automation and keeping my environment Linux only, I decided to use the simple tools at hand
* objdump
* python

plus the given hints
* There are wildcards ("?") in the answer, speciaifically, 308 of them
* The rule matches a 298-byte-long block of code

So, 1st thing's 1st, *objdump* all the files
```bash
for ff in labyrenth/*; do objdump -d ${ff} > ${ff}.od; done
```

Now we automate the search process using Python.

1st, we read each file and convert it back into a list of "functions". As we'll see later, this is not an exact science and did not give the best results
```python
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
```

The code basically follows this algorithm
* skip all lines until we see `<.text>`
* extract hex byte values from line and append to current *function* object
* if assembly mnemonics include `ret`, wrap-up current function and start a new one

Now, my 1st approach was to try and find functions with identical size in all the binaries
```python
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
```
but that turned out to be too simplistic, and did not output the desired results

so, following the hint we got, I just set
```python
commons = [ 298 ]
```
It turns out that almost all the malwares had a function with this size, so I just ignored the ones that did not and moved on.
```python
suspects = {}
for c in commons:
    suspects[c] = {}
for m in malwares:
    for c in commons:
        funcs = list(set([f for f in m.functions if f.length == c]))
        for f in funcs:
            suspects[c].setdefault(f.code[0], []).append({'name': m.name, 'func': f})
```
The next step was to scan and compare all the "298-byte-function" instances in all the "malwares" and keep only the common parts
```python
for l, scommon in suspects.iteritems():
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
```
Basically, if a nibble ("half-byte") is identical in all the samples then it is written to the final array, otherwise a wildcard ('?') is written

And so, we get
```
[308/893] 53 56 8b 35 ?? ?? ?? ?0 57 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 8b f8 ff d6 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 ff d6 8b 35 ?? ?? ?? ?0 68 ?? ?? ?? ?0 57 8b d8 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 a3 ?? ?? ?? ?0 57 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 5f 5e a3 ?? ?? ?? ?0 5b c3
```
Which we paste into the supplied *yara* skeleton to get the solution
```
rule yara_challenge
{
    strings:
        $yara_challenge = { 53 56 8b 35 ?? ?? ?? ?0 57 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 8b f8 ff d6 68 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 ff d6 8b 35 ?? ?? ?? ?0 68 ?? ?? ?? ?0 57 8b d8 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 53 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 a3 ?? ?? ?? ?0 57 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 68 ?? ?? ?? ?0 57 a3 ?? ?? ?? ?0 ff d6 5f 5e a3 ?? ?? ?? ?0 5b c3 }
    condition:
        all of them 
}
```
