#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Convert an image to ASCII art.
#
# Copyright (c) 2015 Oliver Lau <ola@ct.de>, Heise Medien GmbH & Co. KG
# All rights reserved.

from PIL import Image, ImageFont, ImageDraw, ImageColor
from datetime import datetime
import os
import sys
import string
import argparse


class Asciifier:
    PAPER_SIZES = {
        'a4': (210.0, 297.0),
        'a3': (297.0, 420.0),
        'letter': (215.9, 279.4)
    }
    TYPE_CHOICES = [ 'text', 'postscript' ]
    PAPER_CHOICES = PAPER_SIZES.keys()
    result = None
    font_name = 'Hack-Bold'
    margins = (10, 10)
    im = None
    luminosity = ['B', '@', 'M', 'Q', 'W', 'N', 'g', 'R', 'D', '#', 'H', 'O', '&', '0', 'K', '8', 'U', 'd', 'b', '6', 'p', 'q', '9', 'G', 'E', 'A', '$', 'm', 'h', 'P', 'Z', 'k', 'X', 'S', 'V', 'a', 'e', '5', '4', '3', 'y', 'w', '2', 'F', 'I', 'o', 'u', 'n', 'j', 'C', 'Y', '1', 'f', 't', 'J', '{', '}', 'z', '%', 'x', 'T', 's', 'l', '7', 'L', '[', 'v', ']', 'i', 'c', '=', ')', '(', '+', '|', '<', '>', 'r', '?', '*', '\\', '/', '!', ';', '"', '^', '~', '-', ':', '_', ',', "'", '.', '`', ' ']

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
            intensity.append({ 'l': l, 'c': chr(c)})
        self.luminosity = map(lambda i: i['c'], sorted(intensity, key=lambda lum: lum['l']))

    def to_plain_text(self):
        return "\n".join([''.join(line).rstrip() for line in self.result])

    def to_postscript(self, **kwargs):
        paper = 'a4'
        if 'paper' in kwargs and kwargs['paper'] is not None:
            paper = kwargs['paper']
        font_name = 'Hack-Bold'
        if 'font_name' in kwargs and kwargs['font_name'] is not None:
            font_name = kwargs['font_name']
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
            "% Image converted to ASCII by ascii-art.py",
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
        y = self.im.height * grid_points
        for scan_line in self.result:
            x = 0
            for c in scan_line:
                if c != ' ':
                    c = string.replace(c, '\\', "\\\\")
                    c = string.replace(c, '(', "\\(")
                    c = string.replace(c, ')', "\\)")
                    lines.append("(%s) %d %d pc" % (c, x, y))
                x += grid_points
            y -= grid_points
        
        lines += [
            "",
            "showpage"
        ]
        return "\n".join(lines)
    
    def process(self, image_filename, **kwargs):
        resolution = 80
        if 'resolution' in kwargs:
            resolution = kwargs['resolution']
        self.im = Image.open(image_filename)
        if 'aspect_ratio' in kwargs:
            aspect_ratio = kwargs['aspect_ratio']
            self.im = self.im.resize((int(self.im.width * aspect_ratio), self.im.height), Image.BILINEAR)
        self.im.thumbnail((resolution, self.im.height), Image.ANTIALIAS)
        num_chars = len(self.luminosity)
        self.result = []
        scan_line = []
        w = 0
        for pixel in self.im.getdata():
            r, g, b = pixel
            l = 0.2126 * r + 0.7152 * g + 0.0722 * b
            i = int(l * num_chars / 255)
            scan_line.append(self.luminosity[i])
            w += 1
            if w >= self.im.width:
                self.result.append(scan_line)
                scan_line = []
                w = 0
    
    
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
    if args.out is not None:
        if args.out.endswith('.ps'):
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
