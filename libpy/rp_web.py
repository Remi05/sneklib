#Author: Rémi Pelletier
#File:   rp_web.py
#Desc.:  A module containing useful functions related to web operations.

import os
import urllib.request
import urllib.parse
import http.client

HTML_TYPE = 'text/html'
COMMENT_OPEN_TAG = '<!--'
COMMENT_CLOSE_TAG = '-->'


#TODO: Add URL encoding for search requests.


#Gets the hostname of the given URL.
def getHostname(url):
    return urllib.parse.urlparse(url).hostname


#Checks if the file at the given URL is an HTML file.
def isHtml(url):
    return urllib.request.urlopen(url).info().get_content_type() == HTML_TYPE


#Checks if the specified index in a given line is within an HTML comment.
def isInHtmlComment(line, index):
    return COMMENT_OPEN_TAG in line and COMMENT_CLOSE_TAG in line and line.index(COMMENT_OPEN_TAG) < index and line.index(COMMENT_CLOSE_TAG) > index


#Reads a file from a given URL.
def readFile(src_url):
    return urllib.request.urlopen(src_url).read()


#Downloads a file from a given URL and saves it with the given file name.
def downloadFile(src_url, file_name, file_mode = 'wb', overwrite = False):
    if not os.path.exists(file_name) or overwrite:
        content = readFile(src_url)
        with open(file_name, file_mode) as file:
            file.write(content)