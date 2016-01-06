# asciifier

**Convert images to ASCII art**

## Prerequisites

 - Python 2.5 or later
 - Pillow 3.x
 - FPDF 1.7.x or later
 - numpy 1.x or later

## Download code

[Download asciifier.py](https://raw.githubusercontent.com/ola-ct/asciifier/master/asciifier.py) from the
[ASCIIfier repository](https://github.com/ola-ct/asciifier), or do

```
git clone https://github.com/ola-ct/asciifier.git
```

to clone the repository into a local folder.


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

Install Python 2.5 or later with your distribution specific package manager.

Then install the [Python Imaging Library](https://github.com/python-pillow/Pillow):

```
pip install Pillow
```

## Usage

### General usage

```
asciifier.py 
  [-h] [--help]
  --out OUT
  --aspect ASPECT
  --font FONT
  --fontscale FONTSCALE
  --paper {a2,a3,a4,a5,letter,legal}
  --resolution RESOLUTION
  IMAGE
```

`IMAGE`: filename of image to be converted

`OUT`: name of file to write ASCII art to

`FONT`: name of font to use; only valid for PDF output; only tested with TTF under Windows;
just give the font file name here, the file location will be automatically detected

`FONTSCALE`: scale font by this factor (floating point number, default: 1.0)

`RESOLUTION`: number of characters per line (default: 80)

`PAPER`: paper format (default: a4); only valid for PDF output

`ASPECT`: estimated aspect ratio of terminal font (default: 2.0); only valid for text output


### Examples

![Toad](examples/images/toad.png)

#### PDF

Convert image to PDF, fitted to DIN A3 paper (default is A4),
with 120 characters per line (default is 80),
font size increased by 10 percent (scaled by 1.1),
built-in default font (Courier) is used:


```
asciifier.py toad.png \
    --out toad.pdf \
    --paper a3 \
    --fontscale 1.1 \
    --resolution 120
```


Convert image to PDF, the true-type font Hack-Bold is used

```
asciifier.py toad.png \
    --out toad.pdf \
    --font Hack-Bold.ttf

```


#### Pure ASCII text

Convert image to ASCII with 69 characters per line;
assumed aspect ratio of terminal font is 2.4 (default is 2.0):

```
asciifier.py toad.png \
    --out toad.txt \
    --aspect 2.4 \
    --resolution 69
```

Result:

```
                       ~*|7+77<>>||!!****//;~.
                   ;<=}}{1{}lczJuuJzjr?=7!;;**/;:-
                *=lccr?lofZhGP@@PGUheTZSkLnc<;/////;-
             .7rJJzjlcwGAAdD8PGUheZO05CJInSZkz/!;;;///~
            <jo22uIJi9gbD8888@PPGGFhXTkL5&$$kX<;/;;;;;//-
          .}VCCCsCV2zcwPbbbKd8888@PPPP@@PFyIor;**///;;;;!+.
          u0sx4nnCV2uzl3n0OeFGGGFFhTSO64ut]/~ /!*******/>9i
         +TO4Y44nnCV2uJ3rvivrrviii}{=[7>||><>>||!!*****/}kC:
         rT9snCC%Vo2uJz33jctrlv}??{{{{{{1=][[7<<>>||!!!/ih&[
         iksoo2uJIIz33jcctrrllvii}?{{{111====]][+77<>>||7a51
         +LzIz3j3jjjccctttrrlrlllvii}}?{{1==]]]][[[++7<<|on*
          uJttcccccccjj3Iu2uIzjtli?{]]][]]]===]][[[[+77<|rv
          ~}jcccccjj3IuCxxsIv===[7>!/;~:;*!|<+]][[++77<<|*.
            |}cjjjjjzu%4n%zIyk?77>!!!/25?~;//!7[++++77<!~
              /]iczIIJVsoucsXZi[+7>||*Jz}:///;<=[[[7>/-
                 ;<{l3Cs%23l{+]]+7<>!/..:*///;*=7|/-
                     rV%%2Ij3%zi}1=1{{c?*****/~.
                     73cc33jCJIzz3jcv==v<>|!!*.
                   ~t%n4sJctlvvi}?1][[+7]]{i+~:~.
                  [C4xXFXxI2J3rli{1]+!>>{4Vou}~::-
               ~<r2rzkXO&u2ujr}1]+<|*/;;:zxzJJ{?!:~.
               ]3ci[t0Tfsour?=+|*/:~-    -n4J2%z?[<|~
                   . ~luJzjri{]+<>!*;~-.. 7It{>-.~-.
                        l%2Ici1]+7>|><>7]{=:
                      +z5ehTOa5%C49y$$Lay$6c+~
                     cGAA@GhkOThPbpgd@Gh$LkZ0c:
                     9dbKKD@POSXU#WmKd8PGk$XT4>
                     CTXUhheTS$OXDdPFheeZSOyfC!

```
