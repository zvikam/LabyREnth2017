# Threat track - Challange #1

When we unzip the challange file, we get a *pcap* file.

Opening it in wireshark reveals a series of DNS requests and responses.

Looking at a single request, we will see that the description says 
```
DNS	106	Standard query 0x14d9 A google.com
```
But the raw packet bytes look strange
```
0000   52 54 00 12 35 02 08 00 27 d3 43 a3 08 00 45 00  RT..5...'.C...E.
0010   00 5c 00 01 00 00 40 11 5e 72 0a 00 02 0f 08 08  .\....@.^r......
0020   08 08 00 35 00 35 00 48 1c 2f 14 d9 01 20 00 01  ...5.5.H./... ..
0030   00 00 00 00 00 00 c0 12 00 01 00 01 06 67 6f 6f  .............goo
0040   67 6c 65 c0 3b 55 45 73 44 42 42 51 41 41 41 41  gle.;UEsDBBQAAAA
0050   49 41 4f 43 49 72 30 71 4d 56 77 47 65 4b 51 41  IAOCIr0qMVwGeKQA
0060   41 41 43 6f 41 03 63 6f 6d 00                    AACoA.com.
```
The "query" appears to be `google;UEsDBBQAAAAIAOCIr0qMVwGeKQAAACoAcom` - there are a few bytes which are being skipped by the DNS protocol parser: `;UEsDBBQAAAAIAOCIr0qMVwGeKQAAACoA` as a result of using the *Message compression* feature of domain names.

Domain names are represented as a sequence of `<length><data>` blocks, but if `<length>` has the 2 upper bits on, the next octet is an offset, pointing to the next block. In our case, the 1st block is `0xc012`, which "points" to `<6>google`. It is followed by another "pointer" `0xc03b`, which **skips** our Base64 block and points to `<3>com`. The sequence is terminated by a `0x00`, as it should.

If we extract all these *extra* bytes from all the request packets we get the following sequence
```
UEsDBBQAAAAIAOCIr0qMVwGeKQAAACoAAAAIABwAZmlsZS5kYXRVVAkAA3QYGlmBGBpZdXgLAAEE6AMAAAToAwAAC3D0q3bMyQnIz8wrSS0q9sxz8QsOzsgvzUkBCzklJmeXJxalFNdyAQBQSwECHgMUAAAACADgiK9KjFcBnikAAAAqAAAACAAYAAAAAAABAAAAtIEAAAAAZmlsZS5kYXRVVAUAA3QYGll1eAsAAQToAwAABOgDAABQSwUGAAAAAAEAAQBOAAAAawAAAAAA
```
which is Base64, and decodes to a zip file
```bash
python -c 'import base64; import sys; print base64.b64decode(open(sys.argv[1],"rb").read())' data.b64 > data.zip
```
which, in turn, contains a single file that holds our key
```bash
$ unzip -p data.zip
PAN{AllPointersInDNSShouldPointBackwards}
```
