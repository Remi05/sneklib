#Author: Rémi Pelletier
#File:   rp_files.py
#Desc.:  A module containing useful functions related to files.

import os
import sys
import urllib.request
import unicodedata


INVALID_FILE_NAME_CHARS = { '<', '>', ':', '"', '/', '\\', '|', '?', '*' }

#Remove accented characters from a given string.
def removeAccents(string):
    return ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')


#Cleans a file name of invalid characters.
def cleanFileName(file_name):
    return ''.join(c for c in removeAccents(file_name) if not c in INVALID_FILE_NAME_CHARS)