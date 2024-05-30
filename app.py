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

# Load the indexOfIndexes from the pickle file
with open(indexOfIndexName, 'rb') as file:
    i_of_i = pickle.load(file)

# Load the pickleDocMap from the pickle file
with open("pickleDocMap", 'rb') as file:
    doc_map = pickle.load(file)

# This is the home route
@app.route('/')
def home():
    return render_template('home.html')

# This is the results route for handling queries and results
@app.route('/results', methods=['POST', 'GET'])
def results():
    # URL query parameter
    query = request.args.get('query')

    # If the request method is POST, get the query from the form data
    if request.method == 'POST':
        query = request.form['query'].strip().lower()

    # Get the current page number, 1 is default if not provided
    page = request.args.get('page', 1, type=int)
    max_per_page = 10  # Max number of results per page
    start = (page - 1) * max_per_page  # Calculate the starting index for the current page
    end = start + max_per_page  # Calculate the ending index for the current page

    # Measure the start time for query processing
    start_time = time.time()

    # Tokenize and stem the query
    porter_stemmer = PorterStemmer()
    tokens = [porter_stemmer.stem(x) for x in tokenize(query)]
    weights = makeQueryWeights(tokens)  # Query weights
    results = extractFromIndex(weights.keys(), i_of_i, indexName)  # Extract results from the index

    # Check if there are any results
    if any(x != [] for x in results.values()):
        sorted_results = resultsByRelevance(list(weights.values()), results)  # Sort results by relevance
        total_results = len(sorted_results)  # Get the total number of results
        paginated_results = sorted_results[start:end]  # Paginate the results
        documents = [{'docid': x, 'url': doc_map[x]} for x in paginated_results]  # Map document IDs to URLs
        total_pages = (total_results + max_per_page - 1) // max_per_page  # Calculate the total number of pages
    else:
        total_results = 0  # No results found
        documents = []
        total_pages = 0

    # Calculate the response time in milliseconds
    response_time = (time.time() - start_time) * 1000
    curr_page_count = len(paginated_results)  # Count of results on the current page

    # Next and previous pages
    next_page = page + 1 if end < total_results else None
    prev_page = page - 1 if start > 0 else None

    # Render the results template
    return render_template('results.html', query=query, documents=documents, response_time=response_time, 
                           next_page=next_page, prev_page=prev_page, current_page=page, total_pages=total_pages, 
                           current_page_count=curr_page_count, total_results=total_results)

# Run app.py
if __name__ == "__main__":
    app.run(debug=True)