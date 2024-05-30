# Search Engine

## Project Overview
This project is a search engine, including a web application feature. It allows users to input search queries and displays relevant results from a set of documents. The application is built using Python for the backend and HTML/CSS for the front-end.

## Project Structure
The project consists of the following files:

1. **`app.py`**: Main script to run the web server.
2. **`home.html`**: The homepage of the search engine where users can enter their search queries.
3. **`results.html`**: The page that displays the search results of the user's query.
4. **`styles.css`**: Stylesheet for the web pages.
5. **`index.py`**: This script is responsible for building the search index.
6. **`search.py`**: This script handles the search functionality.
7. **`champion.py`**: This script creates champion list indexes given the original index and max champion list size

## Installation

### Prerequisites
- Python 3.x
- Flask
- Bootstrap (via CDN)
- nltk

### Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages:
    ```bash
    pip install flask
    pip install nltk
     ```
4. Run the index construction application(s)
    ```
    python3 index.py
        index.py will construct an index, document to document id mapping, and index of indexes from any zip file called developer.zip,
        though the zip file name read can be changed by modifying line number 461 in the python file. Optionally, you can also uncomment the lines 472-474 and 490-492 to get rid of duplicate or near duplicate content. The files generated are called FinalIndex, pickleDocMap, 
        and indexOfIndexes respectively, though the file names may be changed in the code if necessary at lines 441, 531, and 532. Additionally
        a statistics file called stats.txt will be generated alongside some other record keeping files.
    python3 champion.py <size>
        champion.py will take one argument, size, which must be a whole number greater than 0. It will go through the files named FinalIndex 
        and indexOfIndexes to construct the corresponding champion list files, where each term only takes its top size postings based
        on frequency. The corresponding files generated will be called FinalIndex<size> and indexOfIndexes<size> respectively, but the
        base names and name of the file taken can be modified in code at lines 8 and 9.
    ```
5. Run the search application(s):
    ```bash
    python3 app.py [size]
        app.py connects you to a port and gives a link to a web gui that enables you to search queries, given that you have an index file, an index of index file, and a document id mapping. It takes one optional argument size, which determines whether or not you use a champion list. If the argument is provided, it uses the files FinalIndex<size>, indexOfIndexes<size>, and pickleDocMap to run, otherwise the baseindex file names FinalIndex and indexOfIndexes are used instead of the champion lists. The base names can be changed in the file on lines 10-11. The generated gui enables users to search queries in the search bar. It also breaks up the results into pages of 10 results each, and allows users to navigate the next and previous pages through the next and prev buttons, or to return to the search page using the button: return to search.
    or
    pyton3 search.py [size]
        search.py when runs continuously prompts the user to enter a query or to exit the program, providing paged results when the former is chosen. It takes one optional argument size, which determines whether or not you use a champion list. If the argument is provided, it uses the files FinalIndex<size>, indexOfIndexes<size>, and pickleDocMap to run, otherwise the base index file names FinalIndex and indexOfIndexes are used instead of the champion lists. The base names can be changed in the file on lines 123-124. When the entered queryhas results, the program provides the first page of results before prompting the user to enter their next actions. The users can navigate between pages by entering next and prev into the prompt, or they can return to the search prompt by entering search. When the user wants to exit the program, they can ctrl + c or enter exit into the prompt.
    ```

### Usage
1. Open your web browser and navigate to http://localhost:5000.
2. Enter your search query in the input box on the homepage where it says, "Search for content," and click the search button.
3. View the search results on the results page. Click on the links to view the documents. Click the 'Next' and 'Previous' buttons to navigate the results pages. 

## File Descriptions

### Home Page (`home.html`)
The home page is where users can enter their queries in an input box and launch the search with a button. The form submits the query to the `/results` endpoint via a POST request.

### Search Results Page (`results.html`)
This page displays the search results for the user's query. If matching documents are found, they are displayed in a list with clickable links. If no documents match the query entered by the user, a message indicates that no results were found. 

### Styles (`styles.css`)
The CSS file includes styles for the home and results page, including background colors, fonts, and more. 

### Indexing (`index.py`)
This script builds the search index. It processes documents, tokenizes text, computes term frequencies, and creates postings. Partial indexing, merging indexes, and creating final searchable indexes are also handled. In the indexing process, documents are parsed, text is extracted, and relevant information is stored for retrieval. 

### Indexing2 (`champion.py`)
This script builds the champion index. It processes the index and index of indexes to generate corresponding champion versions of each based on the provided argument. Essentially, for each term it will sort the index by frequency and take the top N most results before generating a new index and index of indexes with them.

### Searching (`search.py`)
This script handles searching functionality. It processes user queries, tokenizes and stems the input, computes relevance, and retrieves and displays relevant search results. This file also supports pagination, which is driven in app.py. It ensures efficient and accurate retrieval of documents per users' query requests.

### Searching2 (`app.py`)
This script handles searching functionality with a GUI. It processes user queries, tokenizes and stems the input, computes relevance, and retrieves and displays relevant search results. This file also supports pagination and ease of navigation with buttons. It ensures efficient and accurate retrieval of documents per users' query requests.