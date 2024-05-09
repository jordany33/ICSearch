import os
import re
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import nltk
import zipfile
import json

index = {}
docMap = {}
text_documents = set()
alphaNum = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]

#Gets content of JSON files
def fileContents(file):
    with open(file, 'r') as json_file:
        content = json.load(json_file)
    return content


#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenAlNum(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False

#Generate unique Doc ID for each document
def generateDocID(document):
    return hashlib.md5(document.encode()).hexdigest()

def index(document):

    docID = generateDocID(document)
    tokens = tokenize(document)
    
    for token in set(tokens):
        if token in index:
            index[token].append(docID)
        else:
            index[token] = [docID]


def build_index(text_documents):
    pass