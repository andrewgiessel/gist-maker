`gist-maker`
=================

### Introduction

This is a fork of [inkedmn's](https://github.com/inkedmn) [bbedit-gist-maker](inkedmn/bbedit-gist-maker), but removing the bbedit stuff, and updating some of the python code.

### Requirements

* An account on Github
* Python

### Usage

First, you'll need to change the two lines in the top of the file to reflect your username and password.  The code will attempt to grab your API key and store it in `~/.ghtoken`.  There probably is a better way to do this- please send a PR if you have ideas!

Anyway, after that, to use the code, run it like this:

`$ python makeGist.py -d "gist description" file.txt`

In this case, the filename is taken from the final argument (i.e. the name of the file).

Alternatively, you can use `STDIN`, like so:

`$ python makeGist.py -f file.txt -d "gist description" < file.txt`

Other notes:
* The filename and description arguments are optional.  
* By default, this script will create a private gist; to create a public gist, add the `-p` or `--public` flag.  
* If you run `chmod +x makeGist.py` you'll be able to run the code without having to prepend `python`.

### TODO

* Maybe add the ability to add multiple files?
* Check to see if `STDIN` is empty and bail if so?

