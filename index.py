import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import hashlib
import nltk

index = {}
docMap = {}
text_documents = set()

def build_index(text_documents):
    pass
