import sys
import time
import openai
import requests
from flask import Flask, request, render_template
from nltk.stem import PorterStemmer
import pickle
from index import tokenize 
from search import makeQueryWeights, extractFromIndex, resultsByRelevance
from bs4 import BeautifulSoup

app = Flask(__name__)

# OpenAI API key
# openai.api_key = 'sk-proj-EFWRvbuNRhcDkIaBUOgYT3BlbkFJmgGomhRjJwSvwAPH9hU4'

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

# # Fetch the content of each URL and summarize
# def fetch(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             page_content = response.text
#             summary = summarize(page_content)
#             return summary
#         else:
#             return "Failed to retrieve page's content."
#     except requests.exceptions.SSLError:
#         return "SSL certificate verification failed. Unable to retrieve content."
#     except Exception as e:
#         return str(e)

# # Summarizes the content using OpenAI API
# def summarize(content):
#     try:
#         # Extract text from HTML
#         extract_text = BeautifulSoup(content, 'html.parser')
#         html_to_text = extract_text.get_text()

#         # Summarize content using OpenAI API gpt-3.5-turbo
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Summarize the following content."},
#                 {"role": "user", "content": html_to_text}
#             ],
#             max_tokens=150
#         )
#         summary = response['choices'][0]['message']['content'].strip()
#         return summary
#     except Exception as e:
#         return str(e)

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
        documents = []
        for docid in paginated_results:
            url = doc_map[docid]
            # summary = fetch(url)
            # documents.append({'docid': docid, 'url': url, 'summary': summary})            
            documents.append({'docid': docid, 'url': url})
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