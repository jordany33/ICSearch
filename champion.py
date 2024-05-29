import sys
import pickle
from index import Posting, tokenize, parseStr, createIndexofIndexes

#Makes champion list index given size of champion list
def makeChampionList(size):
    #Build unique filename for that index and it's index of indexes
    fileName = "FinalIndex" + str(size)
    fileIndex = "indexOfIndexes" + str(size)
    file = open("indexOfIndexes", 'rb')
    #Load the index of indexes of the original index and also open it for reading, and then open the fileName for writing
    indOfInd = pickle.load(file)
    file.close()
    file1 = open("FinalIndex", 'r')
    file2 = open(fileName, 'w')
    #Iterate through each term using index of indexes
    for term, num in indOfInd.items():
        #Seek file and readline
        file1.seek(num)
        line = file1.readline().strip()
        #Get the posts and term, sort the posts by their count and only get up to size postings, then resort them by their docid, then output to file
        term, posts = parseStr(line)
        posts = sorted(posts, key = (lambda x: -(x.getCount())))
        if len(posts) > size:
            posts = sorted(posts, key = (lambda x: -(x.getDoc())))[:size]
        print(term, end = '', file = file2)
        for post in posts:
            print(str(post), end = '', file = file2)
        print(file=file2)
    file1.close()
    file2.close()
    newIndOfInd = createIndexofIndexes(fileName)
    file = open(fileIndex, "wb")
    pickle.dump(newIndOfInd, file)
    file.close()


if __name__ == '__main__':
    #Make sure the only argument passed in champion list size
    if len(sys.argv)==2:
        makeChampionList(int(sys.argv[1]))
    