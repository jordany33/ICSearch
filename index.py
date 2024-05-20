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
        postStr = f':{self.docid}|{self.tfidf}|'
        if self.fields == []:
            postStr = postStr + 'None'
        for x in self.fields:
            postStr = postStr + ' ' +  str(x)
        postStr = postStr + '|'
        if self.positions == []:
            postStr = postStr + 'None'
        for x in self.positions:
            postStr = postStr + ' ' +  str(x)
        return postStr
    #String representation of posting object
    def __repr__(self):
        postStr = f':{self.docid}|{self.tfidf}|'
        if self.fields == []:
            postStr = postStr + 'None'
        for x in self.fields:
            postStr = postStr + ' ' +  str(x)
        postStr = postStr + '|'
        if self.positions == []:
            postStr = postStr + 'None'
        for x in self.positions:
            postStr = postStr + ' ' +  str(x)
        return postStr
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

def map_first_word_positions(filename):
    positions = []
    current_position = 0

    with open(filename, 'r') as file:
        while True:
            file.seek(current_position)
            line = file.readline()

            if not line:
                break

            word_start = None
            first_word = ""
            for i in range(len(line)):
                if line[i].lower() in alphaNum:
                    if word_start is None:
                        word_start = current_position + i
                    first_word += line[i]
                elif word_start is not None:
                    break

            if word_start is not None:
                positions.append(word_start)
                print(f"'{first_word}' starts at position: {word_start}")

            current_position += len(line) + 1

    return positions

def combinePartialindexes(indexes_list):
    big_dict = {}

    for filename in indexes_list:
        with open(filename, 'r') as index:
            positions = map_first_word_positions(filename)

            for i, line in enumerate(index):
                term, posting = parseStr(line)

                if term not in big_dict:
                    big_dict[term] = [positions[i]]
                else:
                    big_dict[term].append(positions[i])


#Parses a line of input from the index and returns the corresponding term and list of postings that it parses and recreates
def parseStr(line):
    remadePosts = []
    #Splits it by delimiter to separate term and posts
    obj = line.split(':')
    #Gets term and slices it off so we have a list of just post strings
    term = obj[0]
    obj = obj[1:]
    #Recreates each post from each post str
    for post in obj:
        remadePosts.append(parsePost(post))
    #Returns term and post
    return term, remadePosts

#Parses a post str and turns it into a posting object which it returns
def parsePost(postStr):
    #Splits to get posting attributes
    attr = postStr.split('|')
    #Gets docid and tfidf by just getting the index because they're just an int
    docId = attr[0]
    tfidf = attr[1]
    #Parses the list string to get the list values for fields and pos
    fields = parseAttrList(attr[2])
    pos = parseAttrList(attr[3])
    #Creates and returns posting object
    return (Posting(docId, tfidf, fields, pos))

#Parses a list string and returns a recreated list
def parseAttrList(listStr):
    #Represented empty lists as 'None' in our string representation of our posting, so if we see it return []
    if listStr == 'None':
        return []
    #Split the list str to get each element
    attrList = []
    elems = listStr.split()
    #Add each element to list we return, ensure no empty string is appended
    for x in elems:
        if x != '':
            attrList.append(x)
    #return the list
    return attrList

#Creates an index of indexes given the partial index name
def createIndexofIndexes(filename):
    #Initializes mapping and current position in file
    positions = {}
    current_position = 0

    #Opens file
    file = open(filename, 'r')
    while True:
        #While condition holds, go to the curPos value using seek and read the line
        file.seek(current_position)
        line = file.readline()

        #If no line, breaks
        if not line:
            break

        #Split by : and get the first element to get the word
        objs = line.split(':')
        word = objs[0]
        #Update mapping with word and its current position
        positions[word] = current_position

        #Move curPos pointer to the next line
        current_position += len(line)
    return positions

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
        print(t, end = '', file = file)
        for post in f:
            print(str(post), end = '', file = file)
        print(file=file)
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
    zip = zipfile.ZipFile("developer.zip", "r")
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
                # if curNum % 30 == 0 and curNum != 0:
                #     partialIndex(partialInd)
                #     partialInd += 1
                #     index.clear()
    pickleIndex()
    #partialIndex(partialInd)
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
