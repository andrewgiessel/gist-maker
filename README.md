`gist-maker`
=================

### Introduction

This is a fork of [inkedmn's](https://github.com/inkedmn) [bbedit-gist-maker](inkedmn/bbedit-gist-maker), but removing the bbedit stuff, and updating some of the python code.

### Requirements

* An account on Github
* Python

### Usage

To use the Python program on its own, run it like this:

`$ python makeGist.py -f filename.txt -d "gist description" -c "contents of the gist"`

This will create a private gist; to create a public gist, add the `-p` flag.

### TODO

Fix?  Doesn't seem to work as above...
Change optparse into argparse
