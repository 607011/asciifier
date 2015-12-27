#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Convert an image to ASCII art.
#
# Copyright (c) 2015 Oliver Lau <ola@ct.de>, Heise Medien GmbH & Co. KG
# All rights reserved.

from PIL import Image, ImageFont, ImageDraw, ImageColor
from datetime import datetime
import string
import argparse


class Asciifier:
    PAPER_SIZES = {
        'a6': (105, 148),
        'a5': (148, 210),
        'a4': (210, 297),
        'a3': (297, 420),
        'a2': (420, 594),
        'a1': (594, 841),
        'a0': (841, 1189),
        'letter': (215.9, 279.4)
    }
    TYPE_CHOICES = ['text', 'postscript']
    PAPER_CHOICES = PAPER_SIZES.keys()
    result = [[]]
    margins = (10, 10)
    im = None
    luminosity = ['B', '@', 'M', 'Q', 'W', 'N', 'g', 'R', 'D', '#', 'H', 'O', '&', '0', 'K', '8', 'U', 'd', 'b', '6',
                  'p', 'q', '9', 'G', 'E', 'A', '$', 'm', 'h', 'P', 'Z', 'k', 'X', 'S', 'V', 'a', 'e', '5', '4', '3',
                  'y', 'w', '2', 'F', 'I', 'o', 'u', 'n', 'j', 'C', 'Y', '1', 'f', 't', 'J', '{', '}', 'z', '%', 'x',
                  'T', 's', 'l', '7', 'L', '[', 'v', ']', 'i', 'c', '=', ')', '(', '+', '|', '<', '>', 'r', '?', '*',
                  '/', '!', ';', '~', '-', ':', '.', ' ']

    def __init__(self, font_file):
        if font_file is not None:
            self.generate_luminosity_mapping(font_file)

    @staticmethod
    def mm_to_point(mm):
        return 2.834645669 * mm

    def generate_luminosity_mapping(self, font_file):
        n = 64
        image_size = (n, n)
        font = ImageFont.truetype(font_file, int(3 * n / 4))
        self.luminosity = []
        intensity = []
        for c in range(32, 127):
            image = Image.new('RGB', image_size, ImageColor.getrgb('#ffffff'))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), chr(c), font=font, fill=(0, 0, 0))
            l = 0
            for pixel in image.getdata():
                r, g, b = pixel
                l += 0.2126 * r + 0.7152 * g + 0.0722 * b
            intensity.append({l: l, c: chr(c)})
        self.luminosity = map(lambda i: i['c'], sorted(intensity, key=lambda lum: lum['l']))

    def to_plain_text(self):
        txt = zip(*self.result)
        return "\n".join([''.join(line).rstrip() for line in txt])

    def to_postscript(self, **kwargs):
        paper = kwargs.get('paper', 'a4')
        font_name = kwargs.get('font_name', 'Hack-Bold')
        paper_size = self.PAPER_SIZES[string.lower(paper)]
        paper_width_points = Asciifier.mm_to_point(paper_size[0])
        paper_height_points = Asciifier.mm_to_point(paper_size[1])
        width_points = Asciifier.mm_to_point(paper_size[0] - 2 * self.margins[0])
        height_points = Asciifier.mm_to_point(paper_size[1] - 2 * self.margins[1])
        grid_points = 12
        font_points = 12
        scale = width_points / (self.im.width * grid_points)
        now = datetime.today()
        lines = [
            "%!PS-Adobe-3.0",
            "%%%%BoundingBox: 0 0 %d %d" % (width_points, height_points),
            "%%Creator: asciifier",
            "%%%%CreationDate: %s" % now.isoformat(),
            "%%%%DocumentMedia: %s %d %d 80 white ()" % (paper, paper_width_points, paper_height_points),
            "%%Pages: 1",
            "%%EndComments",
            "%%BeginSetup",
            "  % A4, unrotated",
            "  << /PageSize [%d %d] /Orientation 0 >> setpagedevice" % (paper_width_points, paper_height_points),
            "%%EndSetup",
            "%Copyright: Copyright (c) 2015 Oliver Lau <ola@ct.de>, Heise Medien GmbH & Co. KG",
            "%Copyright: All rights reserved.",
            "% Image converted to ASCII by asciifier.py (https://github.com/ola-ct/asciifier)",
            "",
            "/%s findfont" % font_name,
            "%d scalefont" % font_points,
            "setfont",
            "",
            "/pc { moveto show } def",
            "",
            "%d %d translate" % self.margins,
            "%f %f scale" % (scale, scale)
        ]
        for y in range(0, self.im.height):
            for x in range(0, self.im.width):
                c = self.result[x][y]
                if c != ' ':
                    c = string.replace(c, '\\', "\\\\")
                    c = string.replace(c, '(', "\\(")
                    c = string.replace(c, ')', "\\)")
                    lines.append("(%s) %d %d pc" % (c, x * grid_points, (self.im.height - y) * grid_points))

        lines += [
            "",
            "showpage"
        ]
        return "\n".join(lines)

    def process(self, image_filename, **kwargs):
        self.im = Image.open(image_filename)
        if 'aspect_ratio' in kwargs:
            self.im = self.im.resize((int(self.im.width * kwargs['aspect_ratio']), self.im.height), Image.BILINEAR)
        resolution = kwargs.get('resolution', 80)
        self.im.thumbnail((resolution, self.im.height), Image.ANTIALIAS)
        num_chars = len(self.luminosity)
        self.result = [[' ' for x in range(self.im.height)] for x in range(self.im.width)]
        for x in range(0, self.im.width):
            for y in range(0, self.im.height):
                r, g, b = self.im.getpixel((x, y))
                l = 0.2126 * r + 0.7152 * g + 0.0722 * b
                self.result[x][y] = self.luminosity[int(l * num_chars / 255)]


def main():
    parser = argparse.ArgumentParser(description='Convert images to ASCII art.')
    parser.add_argument('--image', type=str, help='file name of image to be converted')
    parser.add_argument('--out', type=str, help='file name of postscript file to write.')
    parser.add_argument('--type', type=str, choices=Asciifier.TYPE_CHOICES, help='output type.')
    parser.add_argument('--aspect', type=float, help='aspect ratio of terminal font.')
    parser.add_argument('--psfont', type=str, help='file name of Postscript font to use.')
    parser.add_argument('--paper', type=str, choices=Asciifier.PAPER_CHOICES, help='paper size.')
    parser.add_argument('--resolution', type=int, help='number of characters per line.')
    args = parser.parse_args()

    font_path = args.psfont
        
    asciifier = Asciifier(font_path)

    output_type = 'text'
    if args.out is not None and args.out.endswith('.ps'):
            output_type = 'postscript'
    if args.type == 'postscript':
        output_type = 'postscript'

    aspect_ratio = 2.0
    if args.aspect is not None:
        aspect_ratio = args.aspect

    resolution = 80
    if args.resolution is not None:
        resolution = args.resolution

    if output_type == 'text':
        asciifier.process(args.image, resolution=resolution, aspect_ratio=aspect_ratio)
        result = asciifier.to_plain_text()
    elif output_type == 'postscript':
        asciifier.process(args.image, resolution=resolution)
        result = asciifier.to_postscript(paper=args.paper, font_name=args.psfont)
    else:
        result = ''

    if args.out is None:
        print result
    else:
        with open(args.out, 'w+') as f:
            f.write(result)


if __name__ == '__main__':
    main()
