#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Open Tech Strategies, LLC
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Create directory 'test-tree/challenging-names' containing files with pathological names.
(If 'test-tree/challenging-names' already exists, delete it and recreate it.)
You must run this from this directory because sample source data is here.
"""

import os
import sys
import shutil

def main():
    test_tree_top = "test-tree/challenging-names"

    # Filename components.
    front = "front"
    back = "back"
    text_ext = "txt"
    image_ext = "png"

    # Ensure that an empty test_tree_top dir exists.
    if os.path.exists(test_tree_top):
        shutil.rmtree(test_tree_top)
    os.makedirs(test_tree_top)

    # Create all the files in test_tree_top.
    # 
    # A really rigorous test would try every UTF-8 character.  We're
    # not going to do that, though: it would be too many files and
    # take too long to upload/download over the network.  But we will
    # cover all the funny stops on the 7-bit ASCII railroad at least.
    # We try all the non-alphanumerics, including the lower-ASCII
    # control chars, at the front, middle, pre-extension end,
    # post-extension end, post-dot end, and raw end of the basename:
    #
    #   %frontback.txt
    #   front%back.txt
    #   frontback%.txt
    #   frontback.txt%
    #   frontback.%
    #   frontback%
    # 
    # We also do the same with ".img" instead of ".txt".
    # 
    # Note that we skip '/' because there's no way on a normal Unix
    # filesystem to create a file with '/' in its name.  There might
    # be a way to persuade rclone to *send* such a filename, however,
    # and that's something we should try at some point.
    #
    # We skip 0 (NULL) because null bytes cause all sorts of trouble
    # -- which you would think would mean we *want* to include it, but
    # in practice Python's path-accepting functions don't like NULL
    # bytes either and it's quite unlikely to be found in a user's
    # filename... I think?  I dunno.  <shrug>  If we need to test it,
    # we'll figure out how to get it through to disk below.  For now,
    # I'm skipping it in the interests of not letting a perfect yak be
    # the enemy of a perfectly okay yak.
    for ch in (list(range(1, ord('/')))           # SOH through '.'
               + list(range(ord(':'), ord('A')))  # ':" through '@'
               + list(range(ord('['), ord('a')))  # '[" through '`'
               + list(range(ord('{'), 128))):     # '{" through DEL
        ch = chr(ch)
        for ext in (text_ext, image_ext,):
            for fname in (ch + front + back + "." + ext,
                          front + ch + back + "." + ext,
                          front + back + ch + "." + ext,
                          front + back + "." + ch + ext,
                          front + back + "." + ch,):
                if ext == "txt":  # text: use the tiny sample text
                    src = os.path.join("sample-sources", "text-small.txt")
                else:             # image: use the PNG
                    src = os.path.join("sample-sources", "single-pixel.png")
                dst = os.path.join(test_tree_top, fname)
                # sys.stderr.write(f"DEBUG: creating {dst}\n")
                shutil.copy(src, dst)


if __name__ == '__main__':
  main()
