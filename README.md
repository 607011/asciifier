# asciifier

Convert images to ASCII art

## Prerequisites:

 - Python 2.7
 - Pillow 3.x


## Installation

```
pip install Pillow
```


## Usage

```
asciifier.py 
  [-h]
  --image IMAGE
  --out OUT
  --type {text,postscript}
  --psfont PSFONT
  --paper {a3,a4,letter}
  --resolution RESOLUTION
```

IMAGE: filename of image to be converted
OUT: name of Postscript file to write ASCII art to
PSFONT: name of Postscript to use
RESOLUTION: number of characters per line (default: 80)

Default for `--paper` is `a4`.


### Examples

Convert image to postscript, fitted to DIN A3 paper (default is A4),
with 100 characters per line (default is 80);
type is implicitly determined by file extension:

```
asciifier.py --image toad.png \
             --out toad.ps \
             --paper a3 \
             --resolution 100
```


Convert image to ASCII with 69 characters per line;
assumed aspect ratio of terminal font is 2.1 (default is 2.0);
type is implicitly determined by file extension:

```
asciifier.py --image toad.png \
              --out toad.txt \
              --aspect 2.1 \
              --resolution 69
```

Result:

```
                `_^!****/!!!;;""^^~:,.`
            `-/<((<>rr|()==)+<?!^-::~"~:_.
          ~>cvv=|)%nySP$EE$mhZXe3o}c;,:-~~-_'
       `/ill[v)[IAddb6qGAmPkV3wIIySZef/--_::--,
      ![%xs77=J6Kd6pppq9GA$hk42YTcs4ahy^~:::::--'
    `)}}z}}x%cn&Ub66ppp99GGGEEA$mkXX45S;_-__::_:-_
   ,[Jtffft{zsctmUK8Ubppppq99G999AhwcL*,^~~--:::_^('
   }2fjY1ft{zxs]v}o5ZAGGGEAmZSa2tl=/-'`-~~~~~~~~:;Fc
  \ZSYjCYY1t{%xxl]c)=ci=)))(<r*/;";!/!;""^~~~--~:(VJ,
  ]PF1YfffJ{z%Ts777Lv]c=(++|||||<>r??\/!;;;"^^~~:c$o\
  cSC{J}z%xTsslL[[v]iii==)(+|||<<<>>rr?*\//!;;""^rXo<
  |e%%Tsll77LL[[vvv]iccc==))(+||<<<>rrrr??**\/!;!"CC\
  -I77LL[[[[[[vvvv[[[[vv]]c=)()|||<>>rr????***\//^s}.
   cxvvvvvv[[[L7TzJJ}xl[c)|>?!;/!\\*?r>???****\/!"+*
    r[vv[[[LLls%fjjt7(?*?\!"~-_'_,-~^;/???**\\/!!"_
     ~([LL[[LlxJY1{7sXh)//;"^^:Jw=,::-^/?**\\//!~.
       ~>iLllsx{f}%[YA$=*\/;"^-}Tc,-:-:!r***/!~'
         .^>i7ltfJ%7c)?rr?\/!"-`'_----:^<?/;,`
             ,[tttzl[=7=r?\/!!\+;~~--~-_:.
              rsTxxsLYYJTs[[LL)vL"^^~^-.
             .+s[vvvv7=ccii=+?\!**!!"^:'.
            !tjF43J7[vvic)|>rr??*>(]l(__,'
          `=CJCAEZYs}T7i=(|r*/-""<uJ%zv,_,'
        ,/[%(lSPanxzTLi(>?\!"~:__'[jlTT+)^,'`
        >s7i>74Zy1z%]+r*"~-_'.    'Y1T%tx(?/",
         ...' ^zfsT7i(<?\;^~:_...' |Jl]>:':_'
                :7sLvc(<r?\!"-__,_-~^:
                _]53Fj}[=+((vTzxJjut/
              ~tSAEG$PmkeXm80bG$ZeaVus/
              {U0d6G$SyShA8#Up9GAk3ama%~
              Ip8ddbqqkk$EO#&8bpGEkVPZC;
             {ZPmmmZkSeePppE$hPZkSa5wJ^
```
