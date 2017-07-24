# Documents track - Challange #1

When we unzip the challange file, we get a single document: find_bbz_challenge_file.rtf .

We open it using LibreOffice Writer, and we see it contains an embedded document.

we Double-click it to open, and then navigate to the macro editor (Tools -> Macros -> Edit Macros)

We find several macros: Document_Open is not very interesting, but another VBA module contains a more interesting-looking macro:

```vbnet
Rem Attribute VBA_ModuleType=VBAModule
Option VBASupport 1
Private Function jlETByoSKP(GdrcfxpgXc As Variant, FbuSrdOMYW As Integer)
Dim RikXPlcMKM, UyhoTAiIgk As String, JObtuRmczB, awgCsKrqKP
UyhoTAiIgk = ActiveDocument.Variables("wfozoV").Value()
RikXPlcMKM = ""
JObtuRmczB = 1
While JObtuRmczB < UBound(GdrcfxpgXc) + 2
awgCsKrqKP = JObtuRmczB Mod Len(UyhoTAiIgk): If awgCsKrqKP = 0 Then awgCsKrqKP = Len(UyhoTAiIgk)
RikXPlcMKM = RikXPlcMKM + Chr(Asc(Mid(UyhoTAiIgk, awgCsKrqKP + FbuSrdOMYW, 1)) Xor CInt(GdrcfxpgXc(JObtuRmczB - 1)))
JObtuRmczB = JObtuRmczB + 1
Wend
jlETByoSKP = RikXPlcMKM
End Function
Public Function dLMNiMbhMkYVvgR()
yHTtdcBj = jlETByoSKP(Array(4, 43, 17, 85, 47, 5, 62, 60, 75, 35, 15, 33, 10, 18, 87, 34, 89, 1, 15, 13, 30, _
107, 37, 55, 23, 38, 34, 71, 11, 46, 101, 41, 39, 20, 26, 126, 116, 24, 30, 16, 48, _
115, 6, 17, 90, 6, 91, 31, 106, 27, 37, 5, 61, 29, 66, 94, 12, 16, 63, 46, 7, _
34, 81, 62, 55, 60, 86, 34, 33, 78, 82, 20, 94, 4, 49, 121, 38, 43, 38, 70, 29, _
34, 27, 45, 88, 65, 127, 75, 56, 1, 36, 120, 18, 89, 83, 11, 56, 99, 10, 47, 39, _
111, 94, 88, 0, 16, 73, 14, 27, 39, 32, 65, 90, 52, 11, 13, 110, 69, 88, 21, 3, _
3, 74, 50, 13, 84, 81, 0, 37, 17, 54, 120, 31, 89, 39, 41, 84, 72, 82, 8, 50, _
65, 49, 11, 93, 98, 9, 41, 93, 32, 60, 73, 116, 89, 23, 122, 60, 86, 16, 115, 34, _
6, 27, 42, 22, 122, 19, 55, 14, 85, 66, 51, 24, 87, 22, 63, 3, 61, 73, 111, 119, _
4, 6, 113, 49, 51, 110, 34, 8, 105, 44, 48, 59, 10, 65, 14, 98, 42, 39, 58, 60, _
32, 78, 3, 59, 26, 30, 70, 14, 28, 99, 86, 51, 63, 15, 119, 26, 61, 52, 88, 110, _
55, 80, 2, 80, 58, 121, 68, 93, 36, 112, 19, 25, 72, 24, 83, 13, 95, 44, 127), 0)
MsgBox yHTtdcBj
vCThVRLmOgMJ = jlETByoSKP(Array(101, 57, 10, 111, 9, 61, 12, 43, 73, 49, 56, 95, 85, 106, 91, 0, 67, 18, 64, 33, 54, _
118, 27, 94, 106, 66, 92, 5, 9, 39, 99, 80, 57, 20, 26, 87, 86, 40, 24, 59, 67, _
69, 37, 25, 7, 5, 39, 34, 108, 33, 35, 24, 6, 58, 97, 4, 46, 4, 41, 56, 18, _
25, 89, 28, 44, 10, 32, 63, 57, 78, 50, 2, 33, 36, 83, 83, 17, 88, 82, 75, 5, _
19, 2, 87, 92, 61, 76, 77, 97, 10, 27, 18, 26, 31, 50, 41, 85, 101, 89, 4, 7, _
120, 31, 42, 4, 31, 74, 49, 57, 60, 91, 111, 75, 61, 40, 20, 109, 60, 11, 82, 25, _
35, 106, 43, 5, 12, 83, 42, 6, 24, 46, 110, 49, 10, 80, 41, 66, 88, 8, 22, 48, _
114, 18, 85, 30, 77, 59, 42, 93, 30, 28, 77, 83, 57, 4, 106, 32, 92, 31, 76, 66, _
36, 4, 63, 34, 84, 95, 40, 45, 35, 21, 1, 27, 109, 56, 95, 84, 39, 76, 76, 116, _
59, 54, 18, 29, 28, 17, 38, 33, 102, 78, 84, 87, 32, 7, 58, 116, 55, 61, 22, 52, _
15, 75, 25, 38, 46, 47, 19, 29, 30, 88, 100, 59, 59, 34, 17, 49, 3, 24, 93, 117, _
6, 84, 0, 41, 21, 83, 74, 46, 39, 70, 27, 21, 119, 81, 80, 4, 46, 59, 26), 309)
XiMn = jlETByoSKP(Array(21, 21, 15, 60, 104, 89, 5, 82, 108, 89, 90, 14, 3, 124, 94, 120, 16, 6, 80, 60, 42, _
127, 91, 94, 66, 121, 44, 20, 41, 79, 16, 117, 8, 96, 121, 0, 117, 125, 92, 118, 20, _
87, 86, 84, 30, 6, 13, 14, 117, 119, 50, 122, 39, 85, 14, 15, 108, 66, 67, 47, 110, _
115, 107, 51, 55, 94, 88, 121, 21), 240)
Application.UserAddress = XiMn
End Function
```
Since we're on a Linux box and we like Python, we translate it to Python (this will prove useful later...):
```python
import sys

def jlETByoSKP(GdrcfxpgXc, FbuSrdOMYW):
    _ret = None
    UyhoTAiIgk = wfozoV
    RikXPlcMKM = ''
    JObtuRmczB = 1
    while JObtuRmczB < len(GdrcfxpgXc) + 1:
        awgCsKrqKP = JObtuRmczB % len(UyhoTAiIgk)
        if awgCsKrqKP == 0:
            awgCsKrqKP = len(UyhoTAiIgk)
        RikXPlcMKM = RikXPlcMKM + chr(ord(UyhoTAiIgk[awgCsKrqKP + FbuSrdOMYW-1]) ^ GdrcfxpgXc[JObtuRmczB - 1])
        JObtuRmczB = JObtuRmczB + 1
    _ret = RikXPlcMKM
    return _ret

array1 = [4, 43, 17, 85, 47, 5, 62, 60, 75, 35, 15, 33, 10, 18, 87, 34, 89, 1, 15, 13, 30, 107, 37, 55, 23, 38, 34, 71, 11, 46, 101, 41, 39, 20, 26, 126, 116, 24, 30, 16, 48, 115, 6, 17, 90, 6, 91, 31, 106, 27, 37, 5, 61, 29, 66, 94, 12, 16, 63, 46, 7, 34, 81, 62, 55, 60, 86, 34, 33, 78, 82, 20, 94, 4, 49, 121, 38, 43, 38, 70, 29, 34, 27, 45, 88, 65, 127, 75, 56, 1, 36, 120, 18, 89, 83, 11, 56, 99, 10, 47, 39, 111, 94, 88, 0, 16, 73, 14, 27, 39, 32, 65, 90, 52, 11, 13, 110, 69, 88, 21, 3, 3, 74, 50, 13, 84, 81, 0, 37, 17, 54, 120, 31, 89, 39, 41, 84, 72, 82, 8, 50, 65, 49, 11, 93, 98, 9, 41, 93, 32, 60, 73, 116, 89, 23, 122, 60, 86, 16, 115, 34, 6, 27, 42, 22, 122, 19, 55, 14, 85, 66, 51, 24, 87, 22, 63, 3, 61, 73, 111, 119, 4, 6, 113, 49, 51, 110, 34, 8, 105, 44, 48, 59, 10, 65, 14, 98, 42, 39, 58, 60, 32, 78, 3, 59, 26, 30, 70, 14, 28, 99, 86, 51, 63, 15, 119, 26, 61, 52, 88, 110, 55, 80, 2, 80, 58, 121, 68, 93, 36, 112, 19, 25, 72, 24, 83, 13, 95, 44, 127]

array2 = [101, 57, 10, 111, 9, 61, 12, 43, 73, 49, 56, 95, 85, 106, 91, 0, 67, 18, 64, 33, 54, 118, 27, 94, 106, 66, 92, 5, 9, 39, 99, 80, 57, 20, 26, 87, 86, 40, 24, 59, 67, 69, 37, 25, 7, 5, 39, 34, 108, 33, 35, 24, 6, 58, 97, 4, 46, 4, 41, 56, 18, 25, 89, 28, 44, 10, 32, 63, 57, 78, 50, 2, 33, 36, 83, 83, 17, 88, 82, 75, 5, 19, 2, 87, 92, 61, 76, 77, 97, 10, 27, 18, 26, 31, 50, 41, 85, 101, 89, 4, 7, 120, 31, 42, 4, 31, 74, 49, 57, 60, 91, 111, 75, 61, 40, 20, 109, 60, 11, 82, 25, 35, 106, 43, 5, 12, 83, 42, 6, 24, 46, 110, 49, 10, 80, 41, 66, 88, 8, 22, 48, 114, 18, 85, 30, 77, 59, 42, 93, 30, 28, 77, 83, 57, 4, 106, 32, 92, 31, 76, 66, 36, 4, 63, 34, 84, 95, 40, 45, 35, 21, 1, 27, 109, 56, 95, 84, 39, 76, 76, 116, 59, 54, 18, 29, 28, 17, 38, 33, 102, 78, 84, 87, 32, 7, 58, 116, 55, 61, 22, 52, 15, 75, 25, 38, 46, 47, 19, 29, 30, 88, 100, 59, 59, 34, 17, 49, 3, 24, 93, 117, 6, 84, 0, 41, 21, 83, 74, 46, 39, 70, 27, 21, 119, 81, 80, 4, 46, 59, 26]

array3 = [21, 21, 15, 60, 104, 89, 5, 82, 108, 89, 90, 14, 3, 124, 94, 120, 16, 6, 80, 60, 42, 127, 91, 94, 66, 121, 44, 20, 41, 79, 16, 117, 8, 96, 121, 0, 117, 125, 92, 118, 20, 87, 86, 84, 30, 6, 13, 14, 117, 119, 50, 122, 39, 85, 14, 15, 108, 66, 67, 47, 110, 115, 107, 51, 55, 94, 88, 121, 21]

def dLMNiMbhMkYVvgR():
    yHTtdcBj = jlETByoSKP(array1, 0)
    print yHTtdcBj
    vCThVRLmOgMJ = jlETByoSKP(array2, 309)
    print vCThVRLmOgMJ
    XiMn = jlETByoSKP(array3, 240)
    print XiMn

if __name__ == '__main__':
    dLMNiMbhMkYVvgR()
```
We're still missing some data, which turns out to be the document properties (File -> Properties -> Custom Properties):

```python
Info='8535297daa9f55f6c7e7e59af82908bb47eedc7d8a877b559211a0e25e71168e'
aLMURaAUv='...<VERY LONG>...'
aXkooEpEZJx='CWJTzDpbBt'
ckZsXojQ='...<VERY LONG>...'
jtMoUkr='RWVGMUuTx'
oCldUgvpK='ybyDZyuNV'
sWcxUcOBA='...<VERY LONG>...'
uriEKtsNt='jcoBjXckEj'
wfozoV='...<VERY LONG>...'
```
We copy them to the Python code and run the script:

```
$ python macros.py
The moon will be full in three days. Your spirit shall forever remain among the humans. You shall age like them, you shall die like them, and all memory of you shall fade in time. And we'll vanish along with it. You will never see us again.
The moon will be full in three days. Your spirit shall forever remain among the humans. You shall age like them, you shall die like them, and all memory of you shall fade in time. And we'll vanish along with it. You will never see us again.
PAN{954b525be189a7fee40084bce8a1d9380280d109d64695e0c09b940c708aa274}
```

And we're presented with the flag.
