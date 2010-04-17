#!/usr/bin/env python
#
# debarkoder - a simple barcode recognition utility
# http://github.com/lkraider/debarkoder
#
# Copyright 2010, Paul Eipper
# Licensed under BSD style license
# There are no warranties, expressed or implied. Use at your own risk.
# Share, understand, and enjoy.

"""
debarkoder is a simple barcode recognition utility.
call the process() method with an image file path to decode it.
"""

import Image, ImageChops
import itertools

import format_2of5 as barcode_format

def recognize(img):
    """
    Return the string of digits decoded from the barcode image.

    Image rows are iterated until a good recognition is made.
    Digits not recognized are returned as '?' chars in the string, and
    it means the source image is not good enough and you should get
    a better one, ie. the image should still display the bars correctly
    when converted to 1 bit black and white format.
    """
    (w, h) = img.size
    error_count = -1
    best = [None]
    for scanline in range(0, h-1):
        row = img.crop((0, scanline, w, scanline + 1)).getdata()
        rle = to_rle(row)
        if not len(rle): continue
        decoded = barcode_format.process(rle)
        if not decoded: continue
        decode_errors = len([x for x in decoded if x is None])
        if not decode_errors:
            # row was fully decoded, my job here is done
            return to_string(decoded)
        else:
            # search a row with least ammount of errors
            if error_count < 0:
                error_count = decode_errors
                best = decoded
            elif decode_errors < error_count:
                best = decoded
    return to_string(best)

def to_rle(row):
    """
    Return a run-length encoding of the row data as a list of (len, color) tuples.
    Strip leading and trailing whitespace if any.

    >>> to_rle([0, 255, 255, 0, 0, 0])
    [(1, 'b'), (2, 'w'), (3, 'b')]
    >>> to_rle([255, 0, 255])
    [(1, 'b')]
    """
    colormap = {0: 'b', 255: 'w'}
    rle = [(len(list(g)), colormap[k]) for k,g in itertools.groupby(row)]
    if rle[ 0][1] == 'w': rle = rle[1:]
    if rle[-1][1] == 'w': rle = rle[:-1]
    return rle

def to_string(decoded):
    """ Convert list of digits into string, with None values represented as '?'. """
    return str.join('', (str(i) if i is not None else '?' for i in decoded))

def autocrop(img):
    """ Crop white borders from image. """
    bg = Image.new('1', img.size, 255)
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img

def process(img_path):
    """
    Process a barcode image file and return the decoded string data.

    >>> process('test/01.png')
    '01'
    >>> process('test/01234567891011121314151617181920212223242526.jpg')
    '01234567891011121314151617181920212223242526'
    """
    img = Image.open(img_path)
    img = img.convert('1', dither=0)
    img = autocrop(img)
    return recognize(img)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1 or sys.argv[1].startswith('-'):
        import doctest
        doctest.testmod()
    else:
        for i in sys.argv[1:]:
            print process(i)
