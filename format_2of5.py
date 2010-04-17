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
I25 barcode format recognizer.
call the process method with run-length encoded barcode data to decode it.
"""

# I25 barcode (interleaved 2 of 5)
# digit encoding format:
# five bars for each digit
code_length = 5

# there's always two 1's and three 0's for each code
# in the barcode, a narrow bar means 0 and a wide bar means 1
wide_count = 2
narrow_count = 3

# the wide bars are three times larger than the narrow bars
widebar_mult = 3

# there is a header made of 4 bars and a tail made of 3 bars
extra_bars = 7
head_data = '0000'
tail_data = '100'

# the bit weights are 1, 2, 4, 7, 0
# the code for 0 has a value of 11
table = {
    '00110': 0,
    '10001': 1,
    '01001': 2,
    '11000': 3,
    '00101': 4,
    '10100': 5,
    '01100': 6,
    '00011': 7,
    '10010': 8,
    '01010': 9,
}

# the smaller I25 barcode has 17 bars (counting head, tail, and 2 encoded digits)
minimum_size = 17


def group(data, size):
    """ Return a batch of requested size from the supplied data at each iteration. """
    for i in range(0, len(data), size):
        yield data[i:i+size]

def convert(encoded):
    """ Convert data encoded in tuple format to string buffer format. """
    return str.join('', (str(v) for v,c in encoded))

def deinterleave(encoded):
    """
    Return the encoded data in the correct order and format for decoding.

    Parse the encoded data into 5 black bars, followed by 5 white bars and so on,
    verifying first the header and tail and skipping them on conversion.

    >>> deinterleave([(0, 'b'), (0, 'w'), (0, 'b'), (0, 'w'), \
                      (0, 'b'), (0, 'w'), (0, 'b'), (0, 'w'), (1, 'b'), \
                      (0, 'w'), (1, 'b'), (0, 'w'), (0, 'b'), (1, 'w'), \
                      (1, 'b'), (0, 'w'), (0, 'b')])
    '0011000001'
    """
    head = convert(encoded[:4])
    tail = convert(encoded[-3:])
    if head != head_data or tail != tail_data:
        return None
    black = encoded[4:-3:2]
    white = encoded[5:-3:2]
    data = ''
    for bline, wline in zip(group(black, 5), group(white, 5)):
        data += convert(bline) + convert(wline)
    return data

def decode(data):
    """
    Return a list of the numeric codes decoded from a string buffer of 1's and 0's.

    Each code is 5 chars long and converts to a single digit.
    If an invalid or incomplete code is found in the data it is decoded as None.

    >>> decode('00110100010100111000001011010001100000111001001010')
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> decode('001101')
    [0, None]
    """
    result = []
    for i in group(data, 5):
        result.append(table.get(i))
    return result

def threshold(rle):
    """ Calculate the cutoff size to identify a bar as narrow or wide. """
    # mean_len = ((min(rle)[0] + max(rle)[0]) / 2) - 1
    # I was using the mean pixel length of the bars,
    # but the calc below should be more accurate
    n = (len(rle) - extra_bars) / code_length # number of digits in data
    pxlen = sum(map(lambda x: x[0], rle[4:-3])) # sum of pixel length of all digits
    pxmult = narrow_count + (wide_count * widebar_mult)
    cutoff = 2 * (pxlen / (pxmult * n))
    return cutoff

def process(rle):
    """ Full I25 processing. Return None for invalid input. """
    if len(rle) < minimum_size: return None
    cutoff = threshold(rle)
    encoded = [(int(l > cutoff), c) for l,c in rle]
    result = decode(deinterleave(encoded))
    return result or None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
