#Author: Rémi Pelletier
#File:   rp_web.py
#Desc.:  A module containing useful functions related to web operations.

import os
import urllib.request
import urllib.parse
import http.client

CONTENT_TYPE_HTML       = 'text/html'
CONTENT_TYPE_CSS        = 'text/css'
CONTENT_TYPE_JAVASCRIPT = 'text/script'


#TODO: Add URL encoding for search requests.


#Gets the hostname of the given URL.
def getHostname(url):
    return urllib.parse.urlparse(url).hostname


#Checks if the file at the given URL is an HTML file.
def isHtml(url):
    return urllib.request.urlopen(url).info().get_content_type() == CONTENT_TYPE_HTML


#Reads a file from a given URL.
def readFile(src_url):
    return urllib.request.urlopen(src_url).read()


#Downloads a file from a given URL and saves it with the given file name.
def downloadFile(src_url, file_name, file_mode = 'wb', overwrite = False):
    if not os.path.exists(file_name) or overwrite:
        content = readFile(src_url)
        with open(file_name, file_mode) as file:
            file.write(content)
