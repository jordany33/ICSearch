import os
import re
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import nltk
from nltk.tokenize import word_tokenize
import zipfile
import json

index = {}
docMap = {}
text_documents = set()
alphaNum = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]

import zipfile
import json
from bs4 import BeautifulSoup

#Extract and process JSON file content
def fileContents(zip_path):
    parsed_text = []
    with zipfile.ZipFile(zip_path, 'r') as zip:
        for file_info in zip.infolist():
            if file_info.filename.endswith('.json') and not file_info.is_dir():
                with zip.open(file_info) as file:
                    file_content = json.load(file)  
                    html_content = file_content.get('html', '')
                    html_parsed = BeautifulSoup(html_content, "html.parser")
                    text = html_parsed.get_text()
                    parsed_text.append(text)  
    return parsed_text

#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenAlNum(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False

#Generate unique Doc ID for each document
def generateDocID(document):
    return hashlib.md5(document.encode()).hexdigest()


def build_index(text_documents):
    pass