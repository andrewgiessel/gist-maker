`gist-maker`
=================

### Introduction

This is a fork of [inkedmn's](https://github.com/inkedmn) [bbedit-gist-maker](inkedmn/bbedit-gist-maker), but removing the bbedit stuff, and updating some of the python code.

### Requirements

* An account on Github
* Python

### Usage

To use the Python program on its own, run it like this:

`$ python makeGist.py -d "gist description" file.txt`

In this case, the filename is taken from the final, required argument.

Alternatively, you can use `STDIN`, like so:

`$ python makeGist.py -f file.txt -d "gist description" < file.txt`

The filename and description arguments are optional.  By default, this script will create a private gist; to create a public gist, add the `-p` or `--public` flag.

### TODO

* Maybe add the ability to add multiple files?
* Check to see if `STDIN` is empty and bail if so?

