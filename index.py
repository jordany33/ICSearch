import re
import hashlib
import nltk
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from zipfile import ZipFile
from nltk.tokenize import sent_tokenize, word_tokenize 

index = {}
docMap = {}
text_documents = set()
alphaNum = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]

#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenAlNum(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False


def build_index(text_documents):
    pass