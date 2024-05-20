import sys
import index
import pickle
import time
from index import Posting, tokenize
from nltk.stem import PorterStemmer

#Extracts the boolean query results from index
def extractFromIndex(tokens) -> list:
    global index
    results = []
    #Checks to see if all query words are in index
    for x in tokens:
        #Return [] if the token doesn't exist for boolean search
        if x not in index:
            return []
        else:
            if results == []:
                #If results are empty, its equal to first set of docs it sees
                results = [post.getDoc() for post in index[x]]
            else:
                #Else results is the intersection
                results = findIntersection(results, [post.getDoc() for post in index[x]])
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

#Returns relevance of document
def relevance(tokens, docid) -> int:
    global index
    count = 0
    for x in tokens:
        if x in index:
            for post in index[x]:
                if post.getDoc() == docid:
                    count += post.getTfidf()
                    break
    return count

#Returns results sorted by relevance
def resultsByRelevance(tokens, results) -> list:
    return sorted(results, key=(lambda x : (-relevance(tokens, x))) )

if __name__ == "__main__":
    global index
    global docMap
    file = open("pickleIndex", "rb")
    index = pickle.load(file)
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
        results = extractFromIndex(tokens)
        #show results
        if results != []:
            print(f"Documents matching query '{query}':")
            sortedResults = resultsByRelevance(tokens, results)
            for x in sortedResults:
                print(f'Docid: {x}\nURL: {docMap[x]}')
        else:
            print(f"No documents found for query '{query}'")
        print("--- %s seconds ---" % (time.time() - start_time))