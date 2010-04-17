#README

*debarkode* is a simple barcode recognition utility, initially developed to decode the I25 format but should be easily extendable to support other formats if needed.


# REQUIREMENTS

Tested with:

- Python 2.6
- PIL 1.1.7

May work with older versions


# USAGE

`python debarkode.py barcode_image.png`

You can test with the test barcode images available in the git tree.


# CAVEATS

The image recognition is not rubust, and also doesn't try to locate the barcode position inside the image; instead it expects a somewhat clean image depicting the barcode only. White borders are handled by the program, so it doesn't need to be a perfectly cropped image (my use case is a quick crop from a screenshot of a PDF document).

Small images, antialiased bars, etc. all compromise the correct decoding of the barcode, so try to get the best source you can.


# ACKNOWLEDGEMENTS

The code was inspired on original article and code by Eric Soroos: <http://www.wiredfool.com/2006/07/04/barcode-recognition/>


# LICENSE

Simplified BSD License (FreeBSD License)

	Copyright (c) 2010, Paul Eipper
	All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

	1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

	2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.