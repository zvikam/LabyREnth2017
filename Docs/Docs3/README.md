# Documents track - Challange #3

Unzipping our challange file, we get a single file `Secret Beach Party Invite.msg`.

We remember our rule of "Linux only" and start the investigation
```bash
$ file 'Secret Beach Party Invite.msg'
Secret Beach Party Invite.msg: CDFV2 Microsoft Outlook Message
```
I found this `msgconvert` Perl script at http://www.matijs.net/software/msgconv/ and used it to convert the file
```bash
$ msgconvert 'Secret Beach Party Invite.msg'
$ ls
'Secret Beach Party Invite.eml'
$ file 'Secret Beach Party Invite.eml'
Secret Beach Party Invite.eml: UTF-8 Unicode text, with CRLF line terminators
```
Looking at the file we see that it is an email with attachments, written as a multipart MIME document.

I used `munpack` from ftp://ftp.andrew.cmu.edu/pub/mpack/ to extract each part to a separate file
```bash
$ munpack -f -t 'Secret Beach Party Invite.eml' 
part3 (text/plain)
part4 (application/rtf)
secret.invite.pdf.7z (application/octet-stream)
```
Now, `part3` is text, so let's look inside. It actually contains many newlines, so I'll clean it up a bit
```bash
$ cat part3
おはようございます
ビーチパーティーの招待を受け入れてください。
...<MANY NEWLINES>...
hxxp://www.reversing.sg/B3@chP@r7y/
```
And we have a link: http://www.reversing.sg/B3@chP@r7y/

We follow the link and see a nice page with some ASCII art displaying in a loop. Since it does not contain any useful information, we go to the source.

The 1st half is the JavaScript code to display the ASCII art, but then we find some hidden paragraphs:
```html
<pre style="display:none;">
.____          ___.                                 __  .__      _______________  _____________ 
|    |   _____ \_ |__ ___.__._______   ____   _____/  |_|  |__   \_____  \   _  \/_   \______  \
|    |   \__  \ | __ <   |  |\_  __ \_/ __ \ /    \   __\  |  \   /  ____/  /_\  \|   |   /    /
|    |___ / __ \| \_\ \___  | |  | \/\  ___/|   |  \  | |   Y  \ /       \  \_/   \   |  /    / 
|_______ (____  /___  / ____| |__|    \___  >___|  /__| |___|  / \_______ \_____  /___| /____/  
        \/    \/    \/\/                  \/     \/          \/          \/     \/              
</pre>
<pre style="display:none;">
    :@######################################################################################################################      
     #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++      
     #+#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#++      
     #++'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#+      
     #++'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#'#+      
     #+++`                                                                                                               #'#+      
     #+++`                                                                                                               #'#+      
     #+++`                 00000000  57 65 5F 68 61 64 5F 6a 6f 79 2c 5F 77 65 5F 68  |R3JlYXQgc3RhcnQg|                 #'#+      
     #+++`                 00000010  61 64 5F 66 75 6e 2c 5F 77 65 5F 68 61 64 5F 73  |aW4gZmluZGluZyB0|                 #'#+      
     #+++`                 00000020  65 61 73 6f 6e 73 5F 69 6e 5F 74 68 65 5F 73 75  |aGlzIGNsdWUuICAN|                 #'#+      
     #+++`                 00000030  6e 2E 2E 42 75 74 5F 74 68 65 5F 77 69 6e 65 5F  |CldlIGhvcGUgdGhh|                 #'#+      
     #+++`                 00000040  61 6e 64 5F 74 68 65 5F 73 6f 6e 67 5F 6c 69 6b  |dCB5b3UgbGlrZSBo|                 #'#+      
     #+++`                 00000050  65 5F 74 68 65 5F 73 65 61 73 6f 6e 73 5F 68 61  |dW50aW5nLiANCkFz|                 #'#+      
     #+++`                 00000060  76 65 5F 61 6c 6c 5F 67 6f 6e 65 2E 2E 57 65 5F  |IHRoZXJlIGFyZSBz|                 #'#+      
     #+++`                 00000070  68 61 64 5F 6a 6f 79 2c 5F 77 65 5F 68 61 64 5F  |ZXZlcmFsIHRoaW5n|                 #'#+      
     #+++`                 00000080  66 75 6e 2c 5F 77 65 5F 68 61 64 5F 73 65 61 73  |cyBmb3IgeW91IHRv|                 #+++#     
     #+++`                 00000090  6f 6e 73 5F 69 6e 5F 74 68 65 5F 73 75 6e 2E 2E  |IGh1bnQgZm9yLg0K|                 #,...#    
     #+++`                 000000a0  42 75 74 5F 74 68 65 5F 77 69 6e 65 5F 61 6e 64  |DQpUaGUgaGludCB0|                 #.....#   
     #+++`                 000000b0  5F 74 68 65 5F 73 6f 6e 67 5F 6c 69 6b 65 5F 74  |byBsb2dpbiBpczog|                 #.....,;  
     ##+#,                 000000c0  53 68 69 74 69 73 72 65 61 6c 6c 79 62 72 6f 6b  |DQpvbWd3dGZub2Ji|                `+......#  
    ':...;`;#+.            000000d0  63 51 3d 3d                                      |cQ==|                           +::@,....'  
   #,....:+...:,                                                                                                      :....;;...:  
  ;,....':.....+                                                                                                      #.....,+..,  
  '....#.......#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::+.......+.;  
 #....:,......;+''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''+;......::+  
 ;....+......;#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++@.......##  
 ,....;.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++......;'  
 :....;.....#######+++++++++++++++++++++++++++++++++++++++++++###+++++++++++++++++++++++++++++++++++++++++++++#######+++#......:   
 #....+....,,......#.........................................,,..+............................................#.....+...#......+   
 ',...:,....;.....'                                           ...+                                            +.....,+ ;,......+   
  #....#,,,:+,....+                                          '...#                                            .:....:'@@++;;,.+    
   #++',,.....,:'#',                                         '...#                                             #,+',.........;+'   
   +...............,+;                                       +...+                                             +,...............;' 
   +.................#                                      '#+++#+                                            +.................+ 
   +.................+                                     #.``````;;                                          '.................+ 
   +................,,                                    '`````````#                                           ,................+ 
   +................+                                    ;#;+++++++:#;:                                         ;................' 
   '................+                                 '#:.............,'#'                                      #...............,  
    ,..............'                                #'....................+'                                    #...............'  
    ;..............+                               #........................#                                   '...............#  
    +.............+                               '..........................'                                   :..............+  
    #............,'                              +............................#                                  #.............,   
    ':;++###+#';.#                              #..............................#                                 ',............+   
    ':,,,,,,,,,,'.                             ;:..............................;                                  ##+';:''+#+;.+   
    ',,,,,,,,,,,:                              #................................+                                 +,,,,,,,,,,,;.   
    ',,,,,,,,,,,:                              ;................................#                                 ',,,,,,,,,,,:    
    ',,,,,,,,,,,:                             '.................................;                                 ',,,,,,,,,,,:    
    ',,,,,,,,,,,:                             #.................................:                                  ,,,,,,,,,,,:    
    ',,,,,,,,,,,:                             #.................................:                                  ,,,,,,,,,,,'    
    ',,,,,,,,,,,:                             ';;++'':::::::.,,,,,,,,,,,,,,,,,.:;'#':                              ,,,,,,,,,,,+    
    ',,,,,,,,,,,:                          '+:.````````````....................`````,+'                            ,,,,,,,,,,,+    
    ',,,,,,,,,,,:                         #``.;+####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##:``.#                           ,,,,,,,,,,,#    
    +,,,,,,,,,,,:                        #`,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'`.#                          ,,,,,,,,,,,#    
    +,,,,,,,,,,,:                       +`.@@@@@@@#'.```.'#@@@@@@@@@@@@#',,.,'@@@@@@@@+`:                          ,,,,,,,,,,,#    
    +,,,:;';:,,,:                       '`#@@@@@#```````````@@@@@@@@@'`````````,@@@@@@@``#                         ,,,,,,,,,,,+    
    +:#;,,,,,:++:                      '.,@@@@@;`````````````#@@@@@@.````````````#@@@@@;`'                         #+:;'+#',,,+    
    #;,,,,,,,,,,+                      #`+@@@@+```````````````@@@@@,``````````````@@@@@#`,                         ,,,,,,,,;#:+    
    +,,,,,,,,,,,,                      ;`#@@@@,:,`````````````'@@@#```````````````'@@@@@`.                        :,,,,,,,,,,;'    
    +,,,,,,,,,,,,:                     ,`@@@@##@@`````````````,@@@'@@+````````````,@@@@#`.                        ',,,,,,,,,,,'    
    +,,,,,,,,,,,,'                     .`@@@@#:';``````````````@@@,#@;`````````````@@@@+`.                        ',,,,,,,,,,,     
    +,,,,,,,,,,,,'                     .`@@@@# ```````````````.@@@:```````````````.@@@@,`,                        +,,,,,,,,,,,     
    +,,,,,,,,,,,,'                     ;`#@@@@``````````````` ,@@@;```````````````,@@@#``;                        +,,,,,,,,,,:     
    +,,,,,,,,,,,,+                     #`,@@@@.```````````````#@@@@```````````````#@@@,``#                        #,,,,,,,,,,:     
    +,,,,,,,,,,,,+                     ,,`:@@@# `````````````.@@@@@,`````````````:@@#.``,,                        #,,,,,,,,,,'     
    +,,,,,,,,,,,,+                      #```:+@;.````````````@@@@@@@````````````,@#,````#                         +,,,,,,,,,,'     
    +,,,,,,,,,,,,#                       #`````````.,,,,,,,,.........,,,,,,,,,,,.``````#                          ',,,,,,,,,,+     
    ',,,;#+';:;'##                        #```````````````````````````````````````````+                           '+###':,,,,#     
    ',+',,,,,,,,,+                         #`````````````````````````````````````````'.                           :,,,,,:;#;,#     
    ,#,,,,,,,,,,,+                          #```````````````````````````````````````',                            ,,,,,,,,,:#+     
     ,,,,,,,,,,,,;                           #.``````````..........````````````````#                             ',,,,,,,,,,,'     
     :,,,,,,,,,,,:                            #+++++#++;,,.........,,:;+#++';;;;++'.                             +,,,,,,,,,,,'     
     ;,,,,,,,,,,,,                            +....................................                              #,,,,,,,,,,,      
     +,,,,,,,,,,,,;                           +....................................                              +,,,,,,,,,,:      
     #,,,,,,,,,,,,'                           +....................................                              ;,,,,,,,,,,'      
     #,,,,,,,,,,,,+                           +....................................                              ,,,,,,,,,,,+      
     +,,,,,,,,,,,,#                           +.......,++''::...'...,::'#+;........                             ',,,,,,,,,,,#      
     ',,,,,,,,,,,,#                           +.....;'.```,`````'```````,``.+;.....                             +,,,,,,,,,,,#      
      :,,,,,,,::,,+                           +....##`````,`````' ``````,````,#....                             #,,,,,,,,,,,+      
      ;,,;#'::,:;+#                           +...#`+`````,`````'```````,````,`#...                             +;'';:,,,,,,'      
      +;#:,,,,,,,,,                           +..;``+`````,`````'```````,````,``'..                             ;,,,,:++:,,:       
      #;,,,,,,,,,,,'                          +..+``+`````:..,:;+;;;;;;,:.`` ,``+..                            ',,,,,,,,:#:'       
      ',,,,,,,,,,,,#                          +..;.;@+;:..,``` `;      `,`.:;++;:..                            #,,,,,,,,,,'#       
      .:,,,,,,,,,,,+                          +..:``+`````,`````'```````,````,``...                            #,,,,,,,,,,,+       
       ',,,,,,,,,,,;                          +..```+`````,`````' ``````,````, ``,.                            ;,,,,,,,,,,,'       
       #,,,,,,,,,,,:                          +..```+`````,`````'```````,````,```:.                           :,,,,,,,,,,,:        
       +,,,,,,,,,,,,+                         +..,``+`````,`````'```````,````,```..                           +,,,,,,,,,,,'        
       .:,,,,,,,,,,,#                         +..:`:#+#'''+'''::+:::::::'''++':....                           #,,,,,,,,,,,#        
        ',,,,,,,,,,,+                         +..'.`+`````,`````' ``````,````,``:..                           ;,,,,,,,,,,,+        
        #,,,,,,,,,,,;                         +..+``+`````,`````' ``````,````,``;..                          ':;':,,,,,,,,'        
        ',,,,,,,,,,,,;                        +..,,`+`````,`````' ``````,````,``#..                          #:,,,;++,,,,;         
         ',,,,,:+##+;+                        +...':#`````:.````+```````,````,`:,..                          +,,,,,,,;#,,#         
         #,,,'+:,,,,,+                        +.....,,,.............,:,,:;'++++,...                          :,,,,,,,,,#:+         
         ',,#,,,,,,,,;                        +....................................                         +,,,,,,,,,,,+.         
          '#,,,,,,,,,,'                       +....................................                         #,,,,,,,,,,,'          
          #,,,,,,,,,,,#                       +:;;++++#+++++++++++++++++++#+++++;;;;                        ;,,,,,,,,,,,#          
          +,,,,,,,,,,,;                     :#,````````````````````````````````````.+'                     ',,,,,,,,,,,,'          
           ;,,,,,,,,,,,+                   #:````````````````````````````````````````.+;                   #,,,,,,,,,,,;           
           #,,,,,,,,,,,#                 ;'````````````````````````````````````````````,#                  ;,,,,,,,,,,,#           
           ',,,,,,,,,,,::               #,```````````````````````````````````````````````+:               ',,,,,,,,,,,:'           
            +,,,,,,,,,,,#              #.`````````````````````````````````````````````````,+              #++',,,,,,,,+            
            +,,,,,,,,,,,;             #````````````````````````````````````````````````````.#             ;,,,;#,,,,,,#            
            .;,,,,,,,,,,,#           #```````````````````````````````````````````````````````#           +,,,,,,+;,,,;.            
             #,,,,,,,;++++          +`````````````````````````````````````````````````````````#          +,,,,,,,;+,,#             
             ':,,,:#;,,,,,#        +```````````````````````````````````````````````````````````+        ;:,,,,,,,,:+:'             
              #,,#;,,,,,,,:'      #`````````````````````````````````````````````````````````````#       #,,,,,,,,,,:#              
              ':':,,,,,,,,,'     #```````````````````````````````````````````````````````````````###+#  ;,,,,,,,,,,:'              
               #+,,,,,,,,,,,##;:#.````````````````````````````````````````````````````````````````#...;#,,,,,,,,,,,+               
               ':,,,,,,,,,,';...:`````````````````````````````````````````````````````````````````.+....+,,,,,,,,,,'               
                #,,,,,,,,,;,...+````````...,;;;'+++676f6f2e676c2f795632744673+++++;;;;;...`````````,,...,;,,,,,,,,#                
                ':,,,,,,,,'...,;+#+;;;:,,................................................,,:;++++',`#....+,,,,,,,;,                
                 #,,,,,,,+....:....................................................................:+,....+,,,,,,#                 
                 .',,,,,,'....:......................................................................:....+,,,,,'                  
                  +,,,,,'.....'......................................................................'....,,,,,:+                  
                   #,,,,+.....'......................................................................'.....;,,,#                   
                   .',,,#.....:......................................................................;.....+,,+                    
                    ':,,+.....:....................,,,:;;;'+++++++++++';;;,,,,.......................:.....#,;,                    
                     +,,+.....:.............:+#++:,,.........................,,,,;;;++#';:,..........:.....#:+                     
                      #,#.....:............#..............................................,';........,.....##                      
                       #+.....,............#................................................;..............#                       
                        @..................'................................................:.......,......'                       
                        .;.....:...........'........................................................:.....;                        
                         #.....:...........'........................................................:.....#                        
                         .:....:...........'...............................................:........'....'                         
                          +,...;...........'...............................................;........#...:.                         
                           +:..+...........'...............................................+........#..+,                          
                            ,+.#...........'...............................................#........;+#                            
                              '#...........:...............................................#........+                              
                               +...........:...............................................'.........                              
                               +...........:...............................................;.......,                               
                               '...........:...............................................:.......;                               
                                ...........,.......................................................+                               
                                ,..................................................................#                               
                                ;.........................................................:........#                               
</pre>
```
Bender RULEZ!

There are 2 interesting bits here:
1. The content of Bender's sign contains a hex dump which looks like Base64
`R3JlYXQgc3RhcnQgaW4gZmluZGluZyB0aGlzIGNsdWUuICANCldlIGhvcGUgdGhhdCB5b3UgbGlrZSBodW50aW5nLiANCkFzIHRoZXJlIGFyZSBzZXZlcmFsIHRoaW5ncyBmb3IgeW91IHRvIGh1bnQgZm9yLg0KDQpUaGUgaGludCB0byBsb2dpbiBpczogDQpvbWd3dGZub2JicQ==`
which decodes to 
```bash
$ python -c 'import base64; import sys; print base64.b64decode(sys.argv[1])' 'R3JlYXQgc3RhcnQgaW4gZmluZGluZyB0aGlzIGNsdWUuICANCldlIGhvcGUgdGhhdCB5b3UgbGlrZSBodW50aW5nLiANCkFzIHRoZXJlIGFyZSBzZXZlcmFsIHRoaW5ncyBmb3IgeW91IHRvIGh1bnQgZm9yLg0KDQpUaGUgaGludCB0byBsb2dpbiBpczogDQpvbWd3dGZub2JicQ=='
Great start in finding this clue.  
We hope that you like hunting. 
As there are several things for you to hunt for.

The hint to login is: 
omgwtfnobbq
```
2.Bender's chest holds a 2nd string `676f6f2e676c2f795632744673` which looks like a hex string, and decodes to
```bash
$ python -c 'import sys; print sys.argv[1].decode("hex")' '676f6f2e676c2f795632744673'
goo.gl/yV2tFs
```
We visit this link `http://goo.gl/yV2tFs`, which turns out to be `http://www.reversing.sg/B3@chP@r7y/Part1.png` - an image which contains the left half of the complete flag image
[logo] http://www.reversing.sg/B3@chP@r7y/Part1.png "1/2 down, 1/2 to go"

We now go back to our MIME email, and see we have another file to process: `secret.invite.pdf.7z`.

We try to extract the contents
```bash
$ 7z x secret.invite.pdf.7z
Extracting archive: secret.invite.pdf.7z
Enter password (will not be echoed):
```
Password? Where am I going to find a passw... ohh, wait! Bender gave us a clue:
```
The hint to login is: 
omgwtfnobbq
```
And sure enough, it works!
```bash
--
Path = secret.invite.pdf.7z
Type = 7z
Physical Size = 70617
Headers Size = 201
Method = LZMA:96k 7zAES
Solid = -
Blocks = 1

Everything is Ok

Size:       70592
Compressed: 70617
```
Opening the extracted PDF file shows s single line of text:
```
Please open attached CNJYY62W.docm file"
```
So we extract the embedded file using `pdftk` and find a single file
```bash
$ pdftk secret.invite.pdf unpack_files
$ file secret.invite.hwp
secret.invite.hwp: Hangul (Korean) Word Processor File 5.x
```
WTF is `Hangul Word Processor` ?

Turning to google, we find (big surprise) `pyhwp: HWP Document Format v5 parser & processor` at https://pypi.python.org/pypi/pyhwp . Station!
```bash
$ hwp5proc unpack --vstreams secret.invite.hwp
```
which gives us a whole directory `secret.invite` of extracted files and metadata. The subdirectory 'Scripts' does not contain anything useful, but `BinData` contains an interesting file `secret.invite/BinData/BIN0001.OLE`, but it is not identified as a valid OLE file
```bash
$ file secret.invite/BinData/BIN0001.OLE
secret.invite/BinData/BIN0001.OLE: data
```
If we take a look at the file using *hexdump* we see the following data
```
00000000  00 ca 01 00 d0 cf 11 e0  a1 b1 1a e1 00 00 00 00  |................|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 3e 00 03 00  |............>...|
00000020  fe ff 09 00 06 00 00 00  00 00 00 00 00 00 00 00  |................|
00000030  02 00 00 00 01 00 00 00  00 00 00 00 00 10 00 00  |................|
```
but google says the OLE header starts with `D0 CF 11 E0 A1 B1 1A E1` so we strip the 1st 4 bytes from the file
```bash
$ dd bs=1 skip=4 if=secret.invite/BinData/BIN0001.OLE of=BIN0001.clean.OLE
117248+0 records in
117248+0 records out
117248 bytes (117 kB, 114 KiB) copied, 0.183056 s, 641 kB/s
```
and sure enough
```bash
$ file BIN0001.clean.OLE
BIN0001.clean.OLE: Composite Document File V2 Document, Cannot read section info
```
Using `olebrowse` we see there's a single stream embedded and save it to `stream.bin`, but it turns out to be just `data`.

Still, opening it reveals that it is mostly text. The header references a *troll.js*
```bash
$ dd bs=1 count=128 if=stream.bin | hexdump -vC
00000000  41 c0 01 00 02 00 73 65  63 72 65 74 20 69 6e 76  |A.....secret inv|
00000010  69 74 65 00 43 3a 5c 55  73 65 72 73 5c 52 45 5c  |ite.C:\Users\RE\|
00000020  44 65 73 6b 74 6f 70 5c  50 44 46 2d 48 57 50 5c  |Desktop\PDF-HWP\|
00000030  74 72 6f 6c 6c 2e 6a 73  00 00 00 03 00 28 00 00  |troll.js.....(..|
00000040  00 43 3a 5c 55 73 65 72  73 5c 52 45 5c 41 70 70  |.C:\Users\RE\App|
00000050  44 61 74 61 5c 4c 6f 63  61 6c 5c 54 65 6d 70 5c  |Data\Local\Temp\|
00000060  74 72 6f 6c 6c 2e 6a 73  00 1c bf 01 00 66 6f 72  |troll.js.....for|
00000070  20 28 76 61 72 20 4e 33  68 41 20 3d 20 35 32 30  | (var N3hA = 520|
```
so just cut the binary "header" (there's a footer, too, so let's drop it as well)
```bash
$ dd bs=1 skip=109 count=114460 if=stream.bin of=troll.js
```
running this script results in an error, because we're on Linux
```js
$ node troll.js 
undefined:2
function getDataFromUrl(url, callback) {try {var xmlHttp = new ActiveXObject("MSXML2.XMLHTTP"); xmlHttp.open("GET", url, false); xmlHttp.send(); if (xmlHttp.status == 200) {return callback(xmlHttp.ResponseBody, false); } else {return callback(null, true); } } catch (error) {return callback(null, true); } } function getData(callback) {try {getDataFromUrl("http://r.u.kidding.me69/DAB58154yc/", function(result, error) {if ( ! error) {return callback(result, false); } else {getDataFromUrl("http://shall.we.playctfga.me69/ni95716oSOsA/", function(result, error) {if ( ! error) {return callback(result, false); } else {getDataFromUrl("http://omgwtfbbq.no69/VqCj49674sPnb/", function(result, error) {if ( ! error) {return callback(result, false); } else {getDataFromUrl("http://nono.thiscannot.be69/Isb50659TZdS/", function(result, error) {if ( ! error) {return callback(result, false); } else {getDataFromUrl("http://reversing.sg/pdfHWP/part1.flag.exe", function(result, error) {if ( ! error) {return callback(r

ReferenceError: WScript is not defined
    at eval (eval at <anonymous> (/tmp/docs3/troll.js:3387:12), <anonymous>:2:1851)
    at getData (eval at <anonymous> (/tmp/docs3/troll.js:3387:12), <anonymous>:2:1117)
    at eval (eval at <anonymous> (/tmp/docs3/troll.js:3387:12), <anonymous>:2:1808)
    at Object.<anonymous> (/tmp/docs3/troll.js:3392:1)
    at Module._compile (module.js:569:30)
    at Object.Module._extensions..js (module.js:580:10)
    at Module.load (module.js:503:32)
    at tryModuleLoad (module.js:466:12)
    at Function.Module._load (module.js:458:3)
    at Function.Module.runMain (module.js:605:10)
```
but still, we can see some URLs in there:
* http://r.u.kidding.me69/DAB58154yc/
* http://shall.we.playctfga.me69/ni95716oSOsA/
* http://omgwtfbbq.no69/VqCj49674sPnb/
* http://nono.thiscannot.be69/Isb50659TZdS/
* http://reversing.sg/pdfHWP/part1.flag.exe
 
It's easy to see they're all just except the last one, so we grab the file
```bash
$ curl -L -o part1.flag.exe http://reversing.sg/pdfHWP/part1.flag.exe
```
and thank god this file is a .NET executable, who has the time to reverse a binary
```bash
$ file part1.flag.exe 
part1.flag.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```
We open the file in `MonoDevelop` which reveals the C# code. We look at the code for the `Submit` button
```cs
private void btnSubmit_Click (object sender, EventArgs e)
{
	if (!(this.txtInput.Text != "") || this.txtInput.TextLength != 16) {
		MessageBox.Show ("Either empty string or string length is wrong!");
		return;
	}
	if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szmidkey) {
		string str = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.trollMum)), Form1.szKeyValue);
		MessageBox.Show ("Do you know  " + str);
		return;
	}
	if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szlowkey) {
		string str2 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.MagicNum)), Form1.szKeyValue);
		MessageBox.Show ("Do you know  " + str2);
		return;
	}
	if (Form1.xorToString (Form1.Encrypt (this.txtInput.Text, Form1.szKeyValue)) == Form1.szhighkey) {
		string str3 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.MagicMum)), Form1.szKeyValue);
		MessageBox.Show ("Do you know  " + str3);
		return;
	}
	string str4 = Form1.Decrypt (Form1.StringToXOR (Form1.ByteToStr (Form1.trollNum)), Form1.szKeyValue);
	MessageBox.Show ("Do you know  " + str4);
}
```
We copy the entire code of `Doors.Form1` class to a text file, and modify `Form1` constructor: we take each `Encrypt` call, and create the reverse code for it - for every call to `xorToString(Encrypt(input,keyValue)) == key` we do `input = Decrypt(xorToString(key),keyvalue)`
```cs
public Form1 ()
{
    this.InitializeComponent ();
    Console.WriteLine(Form1.Decrypt(Form1.xorToString(Form1.szmidkey), Form1.szKeyValue));
    Console.WriteLine(Form1.Decrypt(Form1.xorToString(Form1.szlowkey), Form1.szKeyValue));
    Console.WriteLine(Form1.Decrypt(Form1.xorToString(Form1.szhighkey), Form1.szKeyValue));
}
```
save it as `Doors.cs' and recompile the code
```bash
$ dmcs -r:System.Windows.Forms.dll -r:System.Drawing.dll Doors.cs -out:Doors.exe
```
Running it now will show the GUI as before, but our console will show the following keys
```bash
$ mono my.exe
5388080131435925
5203344587564335
7708807458395240
```
Since we don't like manual labor, we modify the constructor once more
```cs
public Form1 ()
{
    this.InitializeComponent ();
    this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szmidkey), Form1.szKeyValue);
    btnSubmit_Click(null, null);
    this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szlowkey), Form1.szKeyValue);
    btnSubmit_Click(null, null);
    this.txtInput.Text = Form1.Decrypt(Form1.xorToString(Form1.szhighkey), Form1.szKeyValue);
    btnSubmit_Click(null, null);
}
```
recompile again and now when the program starts we get 3 dialog boxes with text:
* Do you know  There are images within the usb.pcap!
* Do you know  The key to decrypt the flag is XOR 0x21
* Do you know  You got to try harder than this!

If we go back to MonoDevelop we see there are other classes in the executable, namely `rickroll`, which contains a method named `usb` which appears to extract a byte array stored as a resource.

Next, we use `monodis` to disassemble the executable, which also gives us the resources
```bash
$ monodis --output=part1.flag.cs part1.flag.exe
```
and we see it extracted a file named `Doors.rickroll.resources`.

Let's write a small C# program to extract the resources from that file
```cs
using System;
public class Example
{
    public static int Main(string[] args)
    {
        System.Resources.ResourceReader res = new System.Resources.ResourceReader(args[0]);
        string type = "";
        Byte[] value = null;
        res.GetResourceData(args[1], out type, out value);
        using (System.IO.Stream stdout = Console.OpenStandardOutput())
        {
            stdout.Write(value, 4, value.Length-4);
        }
        res.Close();
        return 0;
    }
}
```
and now compile and run it
```bash
$ dmcs get_resource.cs -out:get_resource.exe
$ mono get_resource.exe Doors.rickroll.resources usb > usb.cap
$ file usb.cap 
usb.cap: tcpdump capture file (little-endian) - version 2.4, capture length 65535)
```
We now open the `usb.cap` file with Wireshark and see a whole lot of USB traffic. We know we're looking for images, and if we examine the `URB_BULK` packets we see references to JPG files. So we Search the packet bytes for 'JFIF' and find 4 packets (number 187, 234, 311, 357), all of them of type `URB_BULK`. Packets 234 and 311 are 65536 bytes and are followed by another `URB_BULK` packet, so we conclude the file is simply too big to be contained in a single packet.

For easier access, let's create a filter expression to show only interesting packets: `usb.data_len > 5000` and Wireshark displays 7 packets (why 7? we'll see later). For each packet we go to the details window and right click on `Leftover Capture Data` -> `Export Packet Bytes`. We'll use the packet number as filename for convenience.
```bash
$ ls -1s --block-size=1  *.bin
 40960 187.bin
 65536 234.bin
 12288 238.bin
 65536 280.bin
 65536 311.bin
 40960 315.bin
 20480 357.bin
```
We will now concatenate the 65536-byte packets (234, 311) each with the packet following it (238, 315)
```bash
$ cat 234.bin 238.bin > 234+238.bin
$ cat 311.bin 315.bin > 311+315.bin
```
and look at the files we have
```bash
$ file *.bin
187.bin:     JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 640x480, frames 3
234+238.bin: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 426x426, frames 3
280.bin:     data
311+315.bin: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, little-endian, direntries=10, manufacturer=Canon, model=Canon EOS 5D, orientation=[*0*], xresolution=153, yresolution=161, resolutionunit=2, software=Adobe Photoshop CS2 Macintosh, datetime=2009:02:25 14:27:16], baseline, precision 8, 800x533, frames 3
357.bin:     JPEG image data, JFIF standard 1.02, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 500x371, frames 3
```
The images turn out to be famouse MEME images, but are a dead end (yes, even the corrupt one - 311+315, which I spent 30 minutes figuring out that there are missing bytes in it, located the original image online and extracted those bytes).

But we see that 1 file, `218.bin`, is not identified as an image. Since the clue said there are **images** in `usb.cap`, we conclude this file is an image, but encrypted. The 2nd cluse said `The key to decrypt the flag is XOR 0x21`, so we get to work
```bash
$ python -c 'import sys; print "".join([chr(ord(b) ^ 0x21) for b in open(sys.argv[1],"rb").read()]);' 280.bin > 280.xor21
$ file 280.xor21
280.xor21: PNG image data, 567 x 800, 8-bit/color RGBA, non-interlaced
```
and VOILA! the right half of the image!
