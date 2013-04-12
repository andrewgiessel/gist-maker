#!/usr/bin/env python

# Modified by Andrew Giessel in 2013; the same license below applies.
# Copyright (c) 2012 Brett Kelly
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib2
import urllib
import base64
import json
import argparse
import os.path
import sys

github_user = 'your github username'
github_pass = 'your github password'

auth_url = 'https://api.github.com/authorizations'
gist_url = 'https://api.github.com/gists'

# tokens are shoved into ~/.ghtoken because why the hell not.
token_file = os.path.join(os.path.expanduser('~'),'.ghtoken')

class Gist(object):
    "Represents a single gist"
    def __init__(self, description, files, public):
        self.description = description
        if type(files) != list: 
        	files = [files]
	self.files = files
        self.public = public
    
    @property
    def asJSON(self):
    	"Return Gist as a JSON block"
        data = {
            'description': self.description,
            'public': self.public,
            'files': {}
        }
        for f in self.files:
            data['files'][f.name] = {'content': f.content}
        return json.dumps(data)
    
class GistFile(object):
    "A file attached to a gist"
    def __init__(self, name, content):
        self.name = name
        self.content = content
        
def makeOptsParser():
    "options for Filename, description, public/private"
    parser = argparse.ArgumentParser(description='Create a gist from the commandline.')
    parser.add_argument('-f', '--filename', help='Filename for gist')
    parser.add_argument('-d', '--description', default='', help='Description string for gist')
    parser.add_argument('-p', '--public', action="store_true", default=False, help='Make the Gist public')
    parser.add_argument('file', nargs='?', default=sys.stdin)
    return parser.parse_args()

def loadGithubAuthToken():
    "Get a stored auth token if we already have one"
    if os.path.exists(token_file):
        return open(token_file).read()
    return None

def saveGithubAuthToken(token):
    "Write our auth token to a dotfile in the user's home directory"
    with open(token_file, 'w+') as fd:
        fd.write(token)
    
def getGithubAuthToken():
    "Get a Github auth token and return it"
    gist_data = json.dumps({"scopes":["gist"], "note":"Accessing gists"})
    req = urllib2.Request(auth_url)
    base64str = base64.encodestring("%s:%s" % \
        (github_user, github_pass)).replace('\n','')
    req.add_header("Authorization", "Basic %s" % base64str);
    req.add_data(gist_data)

    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "Something broke connecting to Github: %s" % e
        return None
         
    if response.getcode() == 201:
        jresp = json.loads('\n'.join(response.readlines()))
        return jresp['token']
    return None 

def createGist(token, gist):
    "Create a github gist and return the URL"
    req = urllib2.Request(gist_url, gist.asJSON)
    req.add_header("Authorization", "token %s" % token)
    
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        return None
    
    if response.getcode() == 201:
        jresp = json.loads('\n'.join(response.readlines()))
        return jresp['html_url']
    return None

if __name__=="__main__":
    
    args = makeOptsParser()

    ## First, attempt to load the existing token
    token = loadGithubAuthToken()
 
    ## If no token exists, get a new one and save it    
    if not token:
        token = getGithubAuthToken()
        if not token:
            raise SystemExit('Broken')
        saveGithubAuthToken(token)

    ### let's use stdin for the source of the file
    if not os.isatty(0):
        with args.file as f:
            fileContents = f.read()
    else:
        with open(args.file) as f:
            fileContents = f.read()
        args.filename = args.file
        

    gFile = GistFile(args.filename, fileContents)
    gist = Gist(args.description, gFile, args.public)
    gistUrl = createGist(token, gist)

    print gistUrl
    print 'if this is a ipynb file, you can view it on nbviewer here: ' + 'http://nbviewer.ipython.org/' + gistUrl.split('/')[3]
