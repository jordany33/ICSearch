import re
import hashlib
import nltk
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import zipfile
from nltk.tokenize import sent_tokenize, word_tokenize
import json

index = {}
docMap = {}
alphaNum = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
curNum = 1

#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenValid(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False


def build_index():
    zip = zipfile.ZipFile("DEVTest.zip", "r")
    for file in zip.infolist():
        if not file.is_dir():
            doc = zip.open(file, 'r')
            file = json.load(doc)
            if file.get('url'):
                docMap[curNum] = (file.get('url'))
                if file.get('content'):
                    if curNum == 1:
                        print(file.get('content'))
                curNum += 1
    print(len(urls))
    print(len(docMap))