from flask import Flask, request, render_template
from nltk.stem import PorterStemmer
import pickle
from index import tokenize 
from search import makeQueryWeights, extractFromIndex, resultsByRelevance

app = Flask(__name__)

with open("indexOfIndexes", 'rb') as file:
    i_of_i = pickle.load(file)

with open("pickleDocMap", 'rb') as file:
    doc_map = pickle.load(file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query'].strip().lower()
    porter_stemmer = PorterStemmer()
    tokens = [porter_stemmer.stem(x) for x in tokenize(query)]
    weights = makeQueryWeights(tokens)
    results = extractFromIndex(weights.keys(), i_of_i)
    
    if any(x != [] for x in results.values()):
        sorted_results = resultsByRelevance(list(weights.values()), results)[:10]
        documents = [{'docid': x, 'url': doc_map[x]} for x in sorted_results]
    else:
        documents = []

    return render_template('results.html', query=query, documents=documents)

if __name__ == "__main__":
    app.run(debug=True)