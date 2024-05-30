import sys
import time
from flask import Flask, request, render_template
from nltk.stem import PorterStemmer
import pickle
from index import tokenize 
from search import makeQueryWeights, extractFromIndex, resultsByRelevance

app = Flask(__name__)

# Decide which index of index and index to use based on if a champion list argument is given
indexOfIndexName = "indexOfIndexes"
indexName = "FinalIndex"
# Construct string based on arguments
if len(sys.argv) == 2:
    indexOfIndexName = indexOfIndexName + sys.argv[1]
    indexName = indexName + sys.argv[1]

with open(indexOfIndexName, 'rb') as file:
    i_of_i = pickle.load(file)

with open("pickleDocMap", 'rb') as file:
    doc_map = pickle.load(file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST', 'GET'])
def results():
    query = request.args.get('query')

    if request.method == 'POST':
        query = request.form['query'].strip().lower()

    page = request.args.get('page', 1, type=int)
    max_per_page = 10
    start = (page - 1) * max_per_page
    end = start + max_per_page

    start_time = time.time()

    porter_stemmer = PorterStemmer()
    tokens = [porter_stemmer.stem(x) for x in tokenize(query)]
    weights = makeQueryWeights(tokens)
    results = extractFromIndex(weights.keys(), i_of_i, indexName)

    if any(x != [] for x in results.values()):
        sorted_results = resultsByRelevance(list(weights.values()), results)
        total_results = len(sorted_results)
        paginated_results = sorted_results[start:end]
        documents = [{'docid': x, 'url': doc_map[x]} for x in paginated_results]
    else:
        total_results = 0
        documents = []

    response_time = (time.time() - start_time) * 1000

    next_page = page + 1 if end < total_results else None
    prev_page = page - 1 if start > 0 else None

    return render_template('results.html', query=query, documents=documents, response_time=response_time, next_page=next_page, prev_page=prev_page)

if __name__ == "__main__":
    app.run(debug=True)
