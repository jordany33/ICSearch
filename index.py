import re
import hashlib
#Only needed when downloading the punkt for the first time
#import nltk
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import zipfile
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import json
import pickle
import sys

#Our index
index = {}
#Map of docid to URL
docMap = {}
#Alphanum constant
alphaNum = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
#How we track doc ID
curNum = 0

#When running first time only
#nltk.download('punkt') 

class Posting:
    def __init__(self, docid, tfidf, positions):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        self.positions = positions
    def __str__(self):
        return(f'Docid is {self.docid}, frequency count is {self.tfidf}, position lists is {self.positions}')
    def __repr__(self):
        return(f'Docid is {self.docid}, frequency count is {self.tfidf}, position lists is {self.positions}')
    def addCount(self, pos):
        self.tfidf += 1
        self.positions.append(pos)

#Computes posting lists for the tokens provided for the given doc
def computeWordFrequencies(tokens) -> dict():
    global curNum
    #The mapped tokens to frequencies we return
    freq = dict()
    #Iterate through tokens, if not yet in dict, initialize the count to 1, otherwise increment the count by 1
    for t in range(len(tokens)):
        tok = tokens[t]
        if tok not in freq:
            freq[tok] = Posting(curNum, 1, [t])
        else:
            freq[tok].addCount(t)
    return freq

#Attempts to save seem our index using pickle
def pickleIndex() ->None:
    global index
    file = open("pickleIndex", "wb")
    pickle.dump(index, file)
    file.close
    return

#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenValid(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False

#Gets rid of tokens that are nonvalid according to token valid from the given list
def removeClutter(tokens) -> list:
    toRemove = []
    #Gathers a list of invalid tokens to remove
    for tok in tokens:
        if not tokenValid(tok):
            toRemove.append(tok)
    #Removes tokens
    for tok in toRemove:
        tokens.remove(tok)
    return tokens

def build_index():
    global curNum
    #Opens zip file
    zip = zipfile.ZipFile("DEVTest.zip", "r")
    #Iterates through all file in zip file
    for file in zip.infolist():
        #Checks its not a directory
        if not file.is_dir():
            #Opens json file and loads it
            doc = zip.open(file, 'r')
            file = json.load(doc)
            #Checks to see if it has a url field
            if file.get('url'):
                #Maps url to docid
                docMap[curNum] = (file.get('url'))
                #Checks if there is content
                if file.get('content'):
                    #Parses it
                    parsed_text = BeautifulSoup(file.get('content'), "html.parser")
                    #Checks if parsed content is there
                    if parsed_text:
                        #Gets tokens then uses then for index, adding our cur doc to the index[token] for each token if not already there
                        ps = PorterStemmer()
                        text = parsed_text.get_text()
                        tokens = [ps.stem(x) for x in removeClutter(word_tokenize(text))]
                        postings = computeWordFrequencies(tokens)
                        for term, post in postings.items():
                            #If not yet added but the term exist
                            if term in index:
                                index[term].append(post)
                            elif term not in index:
                                index[term] = [post]
                curNum += 1
    pickleIndex()
    size = sys.getsizeof(index)
    stats = open("stats.txt", "w")
    print(f"Size of index in bytes is : {size}", file = stats)
    print(f"Number of docs is: {curNum}", file = stats)
    print(f"Humber of tokens is: {len(index)}", file = stats)
    # for term, posts in index.items():
    #     printf(f"Term is {term}, Postings:", file = stats)
    print(f"Index: {index}", file = stats)
    stats.close()
build_index()