import re
import hashlib
import nltk
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from zipfile import ZipFile 

index = {}
docMap = {}
text_documents = set()

def build_index(text_documents):
    pass