#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Convert an image to ASCII art.
#
# Copyright (c) 2015 Oliver Lau <ola@ct.de>, Heise Medien GmbH & Co. KG
# All rights reserved.

from PIL import Image, ImageFont, ImageDraw, ImageColor
from math import ceil
from ttfquery import findsystem
import sys
import string
import argparse


verbosity = 0


def cumsum(arr):
    s = 0
    result = []
    for x in arr:
        s += x
        result.append(s)
    return result


def mm2pt(mm):
    return 2.834645669 * mm


class Size:
    """ Class to store the size of a rectangle."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def to_tuple(self):
        return self.width, self.height


class Point:
    """ Class to store a point on a 2D plane."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Margin:
    """ Class to store the margins of a rectangular boundary."""

    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class Luminosity:

    def __init__(self, l, c):
        self.l = l
        self.c = c



class Asciifier:
    """ Class to convert a pixel image to ASCII art."""

    PAPER_SIZES = {
        'a5': Size(148, 210),
        'a4': Size(210, 297),
        'a3': Size(297, 420),
        'letter': Size(215.9, 279.4),
        'legal': Size(215.9, 355.6)
    }
    PAPER_CHOICES = PAPER_SIZES.keys()
    VALID_CHARS = ['H', 'R', 'B', 'E', 'p', 'M', 'q', 'Q', 'N', 'W', 'g', '#', 'm', 'b', 'A', 'K', 'd', 'D', '8', '@',
                   'P', 'G', 'F', 'U', 'h', 'X', 'e', 'T', 'Z', 'S', 'k', 'O', '$', 'y', 'a', 'L', 'f', '6', '0', 'w',
                   '9', '&', '5', 'Y', 'x', '4', 'n', 's', 'C', '%', 'V', 'o', '2', 'u', 'J', 'I', 'z', '3', 'j', 'c',
                   't', 'r', 'l', 'v', 'i', '}', '?', '{', '1', '=', ']', '[', '+', '7', '<', '>', '|', '!', '*', '/',
                   ';', ':', '~', '-', '.', ' ']
    COLOR_CHARS = ['A', 'C', 'G', 'T']

    def __init__(self, **kwargs):
        self.margins = kwargs.get('margin', Margin(10, 10, 10, 10))
        self.result = None
        self.im = None
        self.luminosity = Asciifier.VALID_CHARS

    def generate_luminosity_mapping(self, font_file):
        import numpy as np
        n = 64
        font = ImageFont.truetype(font_file, int(round(0.8 * n)))
        image_size = Size(n, n)
        intensity = []
        for c in Asciifier.VALID_CHARS:
            image = Image.new('RGB', image_size.to_tuple(), ImageColor.getrgb('#ffffff'))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), c, font=font, fill=(0, 0, 0))
            l = np.sum(np.array(image, np.long) * [2126, 7152, 722])
            intensity.append(Luminosity(l, c))
        self.luminosity = map(lambda i: i.c, sorted(intensity, key=lambda lum: lum.l))

    def to_pdf(self, **kwargs):
        from fpdf import FPDF
        import random
        paper_format = kwargs.get('paper_format', 'a4')
        font_scale = kwargs.get('font_scale', 1)
        font_name = kwargs.get('font_name')
        colorize = kwargs.get('colorize', False)
        if font_name is not None and not colorize:
            self.generate_luminosity_mapping(font_name)
        paper = self.PAPER_SIZES[string.lower(paper_format)]
        inner = Size(ceil(paper.width - self.margins.left - self.margins.right),
                     ceil(paper.height - self.margins.top - self.margins.bottom))
        total = Size(self.im.width, self.im.height)
        scale = inner.width / total.width
        offset = Point(self.margins.left + (inner.width - total.width * scale) / 2,
                       self.margins.bottom + (inner.height - total.height * scale) / 2)
        pdf = FPDF(unit='mm', format=paper_format.upper())
        pdf.set_compression(True)
        pdf.set_title('ASCII Art')
        pdf.set_author('Oliver Lau <ola@ct.de> - Heise Medien GmbH & Co. KG')
        pdf.set_creator('asciifier')
        pdf.set_keywords('retro computing art fun')
        pdf.add_page()
        if font_name is not None:
            pdf.add_font(font_name, fname=font_name, uni=True)
        else:
            font_name = 'Courier'
        pdf.set_font(font_name, '', mm2pt(scale * font_scale))
        for y in range(0, self.im.height):
            yy = offset.y + scale * y
            for x in range(0, self.im.width):
                c = self.result[x][y]
                if c != ' ':
                    if colorize is True:
                        r, g, b = self.im.getpixel((x, y))
                        pdf.set_text_color(r, g, b)
                        pdf.text(offset.x + x * scale, yy, random.choice(Asciifier.COLOR_CHARS))
                    else:
                        pdf.text(offset.x + x * scale, yy, c)
        return pdf.output(dest='S')

    def to_plain_text(self):
        txt = zip(*self.result)
        return '\n'.join([''.join(line).rstrip() for line in txt])

    def process(self, image_filename, **kwargs):
        self.im = Image.open(image_filename)
        if 'aspect_ratio' in kwargs:
            self.im = self.im.resize((int(self.im.width * kwargs['aspect_ratio']), self.im.height), Image.BILINEAR)
        resolution = kwargs.get('resolution', 80)
        self.im.thumbnail((resolution, self.im.height), Image.ANTIALIAS)
        w, h = self.im.size
        nchars = len(self.luminosity)
        self.result = [a[:] for a in [[' '] * h] * w]
        for x in range(0, w):
            for y in range(0, h):
                r, g, b = self.im.getpixel((x, y))
                l = 0.2126 * r + 0.7152 * g + 0.0722 * b
                self.result[x][y] = self.luminosity[int(l * nchars / 255)]


def main():
    global verbosity

    parser = argparse.ArgumentParser(description='Convert images to ASCII art.')
    parser.add_argument('image', type=str, help='file name of image to be converted')
    parser.add_argument('--out', type=str, help='file name of postscript file to write.')
    parser.add_argument('--aspect', type=float, help='aspect ratio of terminal font.')
    parser.add_argument('--font', type=str, help='file name of font to be used.')
    parser.add_argument('--paper', type=str, choices=Asciifier.PAPER_CHOICES, help='paper size.')
    parser.add_argument('--resolution', type=int, help='number of characters per line.')
    parser.add_argument('--fontscale', type=float, help='factor to scale font by.')
    parser.add_argument('--colorize', nargs='?', const=True, help='generate colored output instead of b/w.')
    parser.add_argument('-v', type=int, help='verbosity level.')
    args = parser.parse_args()

    asciifier = Asciifier()

    output_type = 'text'
    if args.out is not None:
        if args.out.endswith('.pdf'):
            output_type = 'pdf'

    if args.v is not None:
        verbosity = args.v

    colorize = args.colorize

    font_scale = 1.0
    if args.fontscale is not None:
        font_scale = float(args.fontscale)

    aspect_ratio = 2.0
    if args.aspect is not None:
        aspect_ratio = args.aspect

    resolution = 80
    if args.resolution is not None:
        resolution = args.resolution

    paper_format = 'a3'
    if args.paper is not None:
        paper_format = args.paper

    font_name = args.font
    if font_name is not None:
        font_name = font_name.lower()
        font_paths = filter(lambda font_file: font_file.lower().find(font_name) >= 0, findsystem.findFonts())
        if font_paths:
            font_name = font_paths[0]
        else:
            sys.stderr.write('Font "{}" not found\n'.format(font_name))
            font_name = None

    if output_type == 'text':
        asciifier.process(args.image, resolution=resolution, aspect_ratio=aspect_ratio)
        result = asciifier.to_plain_text()
    elif output_type == 'pdf':
        asciifier.process(args.image, resolution=resolution)
        result = asciifier.to_pdf(paper_format=paper_format, font_name=font_name, font_scale=font_scale, colorize=colorize)
    else:
        result = '<invalid type>'

    if args.out is None:
        print(result)
    else:
        with open(args.out, 'wb+') as f:
            f.write(result)


if __name__ == '__main__':
    main()
