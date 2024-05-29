import sys
import index
import pickle
import time
import math
from index import Posting, tokenize, parseStr
from nltk.stem import PorterStemmer

#Extracts the boolean query results from index
def extractFromIndex(tokens, indOfInd) -> list:
    file = open("FinalIndex")
    results = {}
    #Checks to see if all query words are in index
    for x in tokens:
        #Return [] if the token doesn't exist for boolean search
        if x not in results:
            results[x] = []
            if x in indOfInd:
                file.seek(indOfInd[x])
                line = file.readline()
                term, posts = parseStr(line)
                results[x] = posts
                # if results == []:
                #     #If results are empty, its equal to first set of docs it sees
                #     results = [post.getDoc() for post in index[x]]
                # else:
                #     #Else results is the intersection
                #     results = findIntersection(results, [post.getDoc() for post in index[x]])
    file.close()
    return results

#Returns a list of the docIDs in common from the two list of ids
def findIntersection(list1, list2) -> list:
    common = []
    ind1 = 0
    ind2 = 0
    len1 = len(list1)
    len2 = len(list2)
    if (len1 == 0 or len2 == 0):
        return common
    while ind1< len1 and ind2 < len2:
        if list1[ind1] < list2[ind2]:
            ind1 += 1
        elif list1[ind1] > list2[ind2]:
            ind2 += 1
        elif list1[ind1] == list2[ind2]:
            common.append(list1[ind1])
            ind1 += 1
            ind2 += 1
    return common

#Returns relevance of document given weights, list of tfidfs, and the square root squared sum of weights, and a promoter value
def relevance(weights, docTfidfs, qSq, pVal) -> int:
    score = 0
    #The variable to keep track of the sqrt of the sum of squared tfids
    sqrtSqaureTfidf = 0
    #Prod will keep track of the sum of products between weights and tfidfs
    prod = 0
    for x in range(len(docTfidfs)):
        #This is doing the part of scoring where we sum tfidf
        score += docTfidfs[x]
        #Keeping track of sum of squares/sum of products
        sqrtSqaureTfidf += (docTfidfs[x] * docTfidfs[x])
        prod += weights[x]*docTfidfs[x]
    #Square root the sum of squares
    sqrtSqaureTfidf = math.sqrt(sqrtSqaureTfidf)
    if pVal > 0:
        score = 0.685*(score+(0.35*math.log(pVal))) + (1-0.685)*(prod/(sqrtSqaureTfidf*qSq))
    else:
        score = 0.685*(score) + (1-0.685)*(prod/(sqrtSqaureTfidf*qSq))
    return score

#Returns results sorted by relevance
def resultsByRelevance(weights, results) -> list:
    scores = {}
    termCnt = 0
    #Calculate the sqrt of the sum of squares of the query coordinates, done here and passed as param later so don't need to repeat calculations
    sqrtSquareSumWeights = 0
    for x in weights:
        sqrtSquareSumWeights += (x*x)
    sqrtSquareSumWeights = math.sqrt(sqrtSquareSumWeights)
    #Get number of terms for creating our list of doc coordinates
    totTerms = len(weights)
    #Create doc coordinates using tfidf at corresponding index in the list, terms are guranteed to already be in same order
    for term, posts in results.items():
        for post in posts:
            docId = post.getDoc()
            if docId not in scores:
                scores[docId] = [[], 0]
                #Add in the necessary number of zeroes to build initial list
                for x in range(totTerms):
                    scores[docId][0].append(0)
            #Update list at index if valid
            scores[docId][0][termCnt] = post.getTfidf()
            scores[docId][1] += post.getImpTxt()*post.getTfidf()
        termCnt += 1
    return sorted(scores.keys(), key=(lambda x : -relevance(weights, scores[x][0], sqrtSquareSumWeights, scores[x][1])) )

#Given list of tokens, goes through them and returns a dict representing query and their weights, currently using freq in query
def makeQueryWeights(tokens):
    weights = {}
    #Iterate through tokens, if not yet in dict, initialize the count to 1, otherwise increment the count by 1
    for t in tokens:
        if t not in weights:
            weights[t] = 1
        else:
            weights[t] += 1
    return weights

if __name__ == "__main__":
    # global index
    global docMap
    # file = open("pickleIndex", "rb")
    # index = pickle.load(file)
    # file.close()
    file = open("indexOfIndexes", 'rb')
    indOfInd = pickle.load(file)
    file.close()
    file = open("pickleDocMap", "rb")
    docMap = pickle.load(file)
    file.close()
    print('Done loading')
    while True:
        query = input("Enter query (or type 'exit' to quit prompt): ").strip().lower()
        
        if query == 'exit':
            break
        start_time = time.time()
        #process the query here
        #Tokenize and stem query
        ps = PorterStemmer()
        tokens = [ps.stem(x) for x in tokenize(query)]
        #Calculate weight of tokens in query
        weights = makeQueryWeights(tokens)
        #Get relevant results
        results = extractFromIndex(weights.keys(), indOfInd)
        #show results
        if any(x != [] for x in results.values()):
            print(f"Documents matching query '{query}':")
            #Get sorted results and print top 10
            sortedResults = resultsByRelevance(list(weights.values()), results)
            if len(sortedResults)>10:
                sortedResults = sortedResults[:10]
            for x in sortedResults:
                print(f'Docid: {x}\nURL: {docMap[x]}')
        else:
            print(f"No documents found for query '{query}'")
        print("--- %s seconds ---" % (time.time() - start_time))