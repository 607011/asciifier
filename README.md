# asciifier

**Convert images to ASCII art**

## Prerequisites:

 - Python 2.7
 - Pillow 3.x


## Installation

### Windows

[Get Python 2.7.11](https://www.python.org/downloads/release/python-2711/) or later from
[python.org download page](https://www.python.org/downloads/).
Install Python into a folder of your choice, e.g. D:\Python27.

Then install the [Python Imaging Library](https://github.com/python-pillow/Pillow) on the command line by typing:

```
D:\Python27\Scripts\pip.exe install Pillow
```


### Linux

Install Python 2.x with your distribution specific package manager.

Then install the [Python Imaging Library](https://github.com/python-pillow/Pillow):

```
pip install Pillow
```

## Download

[Download asciifier.py](https://raw.githubusercontent.com/ola-ct/asciifier/master/asciifier.py) from the
[ASCIIfier repository](https://github.com/ola-ct/asciifier) or do

`git clone https://github.com/ola-ct/asciifier.git`

to clone the repository into a local folder.


## Usage

### General usage

```
asciifier.py 
  [-h]
  --out OUT
  --type {text,postscript,pdf}
  --aspect ASPECT
  --font FONT
  --paper {a0,a1,a2,a3,a4,letter}
  --resolution RESOLUTION
  IMAGE
```

`IMAGE`: filename of image to be converted

`OUT`: name of file to write ASCII art to

`FONT`: name of font to use; only valid for postscript or pdf output

`RESOLUTION`: number of characters per line (default: 80)

`PAPER`: paper dimensions (default: a4); only valid for postscript output

`ASPECT`: estimated aspect ratio of terminal font (default: 2.0); only valid for text output


### Examples

![Toad](examples/images/toad.png)

Convert image to PDF, fitted to DIN A2 paper (default is A4),
with 120 characters per line (default is 80);
type is implicitly determined by file extension:

```
asciifier.py toad.png \
             --out toad.pdf \
             --paper a2\
             --resolution 120
```


Convert image to postscript, fitted to DIN A3 paper,
with 100 characters per line;
type is implicitly determined by file extension:

```
asciifier.py toad.png \
             --out toad.ps \
             --paper a3 \
             --resolution 100
```


Convert image to ASCII with 69 characters per line;
assumed aspect ratio of terminal font is 2.1 (default is 2.0);
type is implicitly determined by file extension:

```
asciifier.py toad.png \
             --out toad.txt \
             --aspect 2.4 \
             --resolution 69
```

Result:

```
                 ,~"/\\//!;""^^~~~---_'`
              :!>((<<|(c[lTxxTlL]+r/^:_-~-:,.
           ~>i[[]+c}ykmG9qq9EAmhZkXS31v/_-----_'
        `/]TTl[i[FGUUb6p9EAmPkV2utTsYXkSl-^_:::-:,
       !Lzz%xTT)I&K6ppppq99GGA$hZS4uoeeSh!_-__:_:-:.
     `({tttft}zl[F98K8Ubppppq9999qq9Ees}i_~~--::::_^\`
     x2fjY11t{zxli712aPAEEGEAmZXVwY%vr-' -~~~~~~-~:;o)
    *ZVYjYYY1t{%%x7]c==i]c=))(|r?\;"";/!;""^^~~~-~:)St_
    ]ZIf1ttJ{}%%Tl77L[vic=((+||||||<>r?*/!!;;""^^^:=$o*
    =Vf}zzxTssllL[[[v]iic=))(+|||<<>>>rrr?**\/!;;""\4u<
    \3ssl7LLLLL[vvv]]]]iiiicc=))(+||<>rrrr???**\/!/"}1~
    `%Tvv[[[vv[[[L7sx%%TlL]c)+<r?r?r?r>>r???****\//"ic
     '(Lvv[[[[L7s%tCjfT=>>>*/;^-_',_~^;/*r??***\/!!;~`
       "([LLL[LlxJY1{lseS+//;^^^:%n+,::-^\?**\\\/!~'
         -?=[lsTT{f}%[fhk=*\/!""~xl(_-:-:!r??*/;-.
            _!<cltfJ%7i|*??*\!;~-``_----:~>/"-.
                i{J{zs[7Jl=(>><||[+~~~~~-'.
             `  /7[[77Ltxsll7L[=>>=/;^~^~.
              ']J1Y1T[vic=)(+<r*?*\r?|)*',,`
             ?tYChEhCszT7]c)|>?\^;!|Y{}x(,,,.
          ,!]zilShVuxzxL](<?\!"~:_:_ljlTT<+^,'`
          ?L[=?]2Zyfzx]+r*"~-_'.    .1Yx%Js+*!^'
              ` ,ixTsLi)|r*!;^~:'.`` \s]|;.`''.
                   c{%s[=<r*/;";!;\r|>_
                 *lnhmZV4nJtYI5aa45eay[\'
                [G8UqEmSVPmGKNObqGma3Sk2[_
                IbKdd6qGaXmA&H0Ubp9GSamZY;
                tZh$$mPZXeVh6b9AmhPkXVeyJ^
```
