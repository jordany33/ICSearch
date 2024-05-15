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
import io

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


#Posting class based on slides
class Posting:
    def __init__(self, docid, tfidf, fields , positions):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        self.positions = positions
        self.fields = fields
    #String print for our posting object
    def __str__(self):
        return(f':{self.docid}|{self.tfidf}|{self.positions}|{self.fields}')
    #String representation of posting object
    def __repr__(self):
        return(f':{self.docid}|{self.tfidf}|{self.positions}|{self.fields}')
    #Increment count and position list
    def addCount(self, pos):
        self.tfidf += 1
        self.positions.append(pos)
    #Returns doc number of our post
    def getDoc(self):
        return self.docid
    #Returns tfidf of our post
    def getTfidf(self):
        return self.tfidf
    #Adds the val to fields for the posting object
    def addField(self, val):
        self.fields.append(val)
        self.tfidf += 1
    #Updates the tfidf value to be newVal
    def updateTfidf(self, newVal):
        self.tfidf = newVal

#Computes posting lists for the tokens provided for the given doc
def computeWordFrequencies(tokens) -> dict():
    global curNum
    #The mapped tokens to frequencies we return
    freq = dict()
    #Iterate through tokens, if not yet in dict, initialize the count to 1, otherwise increment the count by 1
    for t in range(len(tokens)):
        tok = tokens[t]
        if tok not in freq:
            freq[tok] = Posting(curNum, 1, [], [t])
        else:
            freq[tok].addCount(t)
    return freq

#Reads the content and returns a list of the alphanumeric tokens within it
def tokenize(content: str) -> list['Tokens']:
    #Vars below are our current token we are building and the list of tokens respectively
    curTok = ''
    tokens = []
    file = None
    cur = 0
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
                tokens.append(curTok)
                curTok = ''
        cur = cur + 1
    #For when we reach the end of the content, check what our last token is
    #If our curTok isn't empty, add it to token list
    if curTok != '':
        tokens.append(curTok)
    return tokens

#Attempts to save our partial index using pickle
def pickleIndex() ->None:
    global index
    file = open("pickleIndex", "wb")
    pickle.dump(index, file)
    file.close()
    return

#Attempts to save our partial index
def partialIndex(partialNum) ->None:
    global index
    file = open(("partialIndex"+str(partialNum)), "w")
    for t,f in sorted(index.items(), key=(lambda x : (x[0])) ):
        print(t+":"+str(f), file = file)
    file.close()
    return

#Attempts to save seem our index using pickle
def pickleDocMap() ->None:
    global docMap
    file = open("pickleDocMap", "wb")
    pickle.dump(docMap, file)
    file.close()
    return

#Function that returns a bool indicating if token is valid or not (not all non-alphanumeric)
def tokenValid(token) -> bool:
    for x in token:
        if x in alphaNum:
            return True
    return False

#Add fields to the posting objects given which fields to add
def addFields(postings, soup, field, stemmer):
    #Gets all tags and texts associated with the given tag
    texts = soup.find_all(field)
    #Extracts the text
    for text in texts:
        content = text.get_text()
        #tokenizes text
        tokens = [stemmer.stem(x) for x in tokenize(content)]
        #Updates the field list or creates new posting is term not yet seen
        #Can't really track positions of headers and bold reliably so we don't track positions for these tags, but
        #we still do for the regular tokens
        for tok in tokens:
            if tok in postings:
                postings[tok].addField(field)
            else:
                postings[tok] = Posting(curNum, 1, [field], [])

#Function that returns a bool indicating if token is valid or not (all alphanumeric)
def tokenValid2(token) -> bool:
    for x in token:
        if x not in alphaNum:
            return False
    return True

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
    global index
    partialInd = 0
    terms = set()
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
                    encode = 'utf8'
                    content = file.get('content')
                    if file.get('encoding'):
                        encode = file.get('encoding')
                        content.encode(encode)
                    parsed_text = BeautifulSoup(content, "html.parser", from_encoding = encode)
                    #Checks if parsed content is there
                    if parsed_text:
                        #Gets tokens then uses then for index, adding our cur doc to the index[token] for each token if not already there
                        ps = PorterStemmer()
                        text = parsed_text.get_text()
                        #Nltk tokenizer not sure if we're going to keep
                        #tokens = [ps.stem(x) for x in removeClutter(word_tokenize(text))]
                        tokens = [ps.stem(x) for x in tokenize(text)]
                        postings = computeWordFrequencies(tokens)
                        addFields(postings, parsed_text, 'b', ps)
                        addFields(postings, parsed_text, 'h1', ps)
                        addFields(postings, parsed_text, 'h2', ps)
                        addFields(postings, parsed_text, 'h3', ps)
                        addFields(postings, parsed_text, 'strong', ps)
                        for term, post in postings.items():
                            #If not yet added but the term exist
                            if term in index:
                                index[term].append(post)
                            elif term not in index:
                                index[term] = [post]
                record = open("record.txt", "a")
                print(f"Current doc is {curNum}", file = record)
                print(f"Posting list for it is: {postings.keys()}", file = record)
                print(f"Index length is: {len(index)}", file = record)
                record.close()
                curNum += 1
                if curNum % 30 == 0 and curNum != 0:
                    partialIndex(partialInd)
                    partialInd += 1
                    index.clear()
    #pickleIndex()
    partialIndex(partialInd)
    pickleDocMap()
    size = sys.getsizeof(index)
    stats = open("stats.txt", "w")
    print(f"Number of docs is: {curNum}", file = stats)
    print(f"Number of unique tokens/words is: {len(index)}", file = stats)
    print(f"Size of index in bytes is : {size}", file = stats)
    print(index, file = stats)
    stats.close()
if __name__ == "__main__":
    build_index()
