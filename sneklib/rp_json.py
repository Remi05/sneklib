#Author: Rémi Pelletier
#File:   rp_json.py
#Desc.:  A module containing useful functions related to JSON.

import sys
import os
import json

from . import rp_web


#Gets a JSON dictionnary from a given URL.
def getJsonDictionnary(src_url):
    content = rp_web.readFile(src_url)
    content_str = str(content, 'utf-8')
    return json.loads(content_str)


#Gets the "items" dictionnary from a JSON dictionnary found at a given URL.
def getJsonItems(src_url):
    content_dict = getJsonDictionnary(src_url)
    return content_dict['items']
