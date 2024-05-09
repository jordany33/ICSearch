import os
import re
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
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


#Reads the content and returns a list of the alphanumeric tokens not including stop words within it and total num of tokens including stop words
#I also got rid of single char tokens because most of them were from junk in the file and they weren't really words
def tokenize(content: str) -> (list, int):
    #Vars below are our current token we are building and the list of tokens respectively
    curTok = ''
    tokens = []
    file = None
    cur = 0
    size = 0
    #Going through the content string at a time
    while cur < len(content):
        #Read at most 5 chars
        c = content[cur]
        #converts character to lowercase if it is alpha, done since we don't care about capitalization, makes it easier to check given
        #we made our list's alpha characters only lowercase
        c = c.lower()
        #If c is alphanum, concatenate it to our current token, else add the current token to list if not empty string and start on a new token
        if c in alphaNum:
            curTok = curTok + c
        else:
            if curTok != '':
                if len(curTok) > 1:
                    tokens.append(curTok)
                    size = size + 1
                curTok = ''
        cur = cur + 1
    #For when we reach the end of the content, check what our last token is
    #If our curTok isn't empty, add it to token list
    if curTok != '':
        if len(curTok) > 1:
            tokens.append(curTok)
            size = size+1
    return tokens, size


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