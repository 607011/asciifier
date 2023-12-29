# asciifier

**Convert images to ASCII art**

## Prerequisites

 - Python 2.5 or later
 - Pillow 3.x
 - FPDF 1.7.x or later
 - numpy 1.x or later

## Download code

[Download asciifier.py](https://raw.githubusercontent.com/607011/asciifier/master/asciifier.py) from the
[ASCIIfier repository](https://github.com/607011/asciifier), or do

```
git clone https://github.com/607011/asciifier.git
```

to clone the repository into a local folder.


## Installation

```
git clone https://github.com/607011/asciifier.git
cd ascifiier
pipenv install
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
  --orientation {l,p}
  --resolution RESOLUTION
  --colorize
  --invert
  IMAGE
```

`IMAGE`: filename of image to be converted

`OUT`: name of file to write ASCII art to

`FONT`: name of font to use; only valid for PDF output; only tested with TTF under Windows;
just give the font file name here, the file location will be automatically detected

`FONTSCALE`: scale font by this factor (floating point number, default: 1.0)

`RESOLUTION`: number of characters per line (default: 80)

`PAPER`: paper format (default: a3); only valid for PDF output

`ASPECT`: estimated aspect ratio of terminal font (default: 2.0); only valid for text output

With `--colorize` (PDF only) the result is a colored ASCII art image where each pixel gets converted into a correspondingly
colored character randomly chosen from the set 'A', 'C', 'G', 'T'. The `--colorize` may only be used along with
PDF output.

With `--invert` the image will be inverted before processing.

With `--orientation` (PDF only) you can overwrite the otherwise automatically selected paper orientation.
Select `p` for portrait and `l` for landscape.


### Examples

Original image:

![toad](https://github.com/607011/asciifier/assets/2240271/05e21e26-1dbb-4934-a006-c195dc2a29ed)


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

#### PDF

Convert image to PDF, fitted to DIN A4 paper (default is A3),
with 120 characters per line (default is 80),
font size increased by 10 percent (scaled by 1.1),
built-in default font (Courier) is used:


```
asciifier.py toad.png \
    --out toad.pdf \
    --paper a4 \
    --fontscale 1.1 \
    --resolution 120
```


Convert image to PDF, the TrueType font Hack-Bold is used:

```
asciifier.py toad.png \
    --out toad.pdf \
    --font Hack-Bold.ttf
```


**Please note that currently only TrueType fonts are supported.**


Convert image to colored PDF,
Lucida Sans Typewriter Bold characters enlarged by 16 percent,
on A3 paper:

```
asciifier.py toad.png \
    --out toad.pdf \
    --paper a3 \
    --fontscale 1.16 \
    --font LTYPEB.TTF \
    --colorize
```

Result:

![toad-as-colored-pdf](https://github.com/607011/asciifier/assets/2240271/d426e277-c303-41bd-b066-5d1599f319aa)
