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

## Installation

### Prerequisites
- Python 3.x
- Flask
- Bootstrap (via CDN)

### Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages:
    ```bash
    pip install flask
     ```
4. Run the application:
    ```bash
    python3 app.py
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

### Searching (`search.py`)
This script handles searching functionality. It processes user queries, tokenizes and stems the input, computes relevance, and retrieves and displays relevant search results. This file also supports pagination, which is driven in app.py. It ensures efficient and accurate retrieval of documents per users' query requests.