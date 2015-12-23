# asciifier

Convert images to ASCII art

## Prerequisites:

	- Python 2.7
	- Pillow 3.x


## Installation

```
pip install Pillow
```


Usage:

```
asciifier.py 
  [-h]
  --image IMAGE
  --out OUT
  --psfont PSFONT
  --paper {a3,a4,letter}
  --resolution RESOLUTION
```

IMAGE: filename of image to be converted
OUT: name of Postscript file to write ASCII art to
PSFONT: name of Postscript to use
RESOLUTION: number of characters per line (default: 80)

Default for `--paper` is `a4`.
