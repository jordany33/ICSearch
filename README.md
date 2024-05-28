# Search Engine

## Project Overview
This project is a search engine, including a web application feature. It allows users to input search queries and displays relevant results from a set of documents. The application is built using Python for the backend and HTML/CSS for the frontend.

## Project Structure
The project consists of the following files:

1. **`app.py`**: Main script to run the web server.
2. **`home.html`**: The homepage of the search engine where users can enter their search queries.
3. **`results.html`**: The page that displays the search results of the user's query.
4. **`styles.css`**: Stylesheet for the web pages.
5. **`index.py`**: ...
6. **`search.py`**: ...

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
    python app.py
    ```

## File Descriptions

### Home Page (`home.html`)
The home page is where users can enter their queries in an input box and launch the search with a button. The form submits the query to the `/results` endpoint via a POST request.

### Search Results Page (`results.html`)
This page displays the search results for the query entered by the user. If there are matching documents, they are displayed in a list with clickable links. A message is shown indicating that no results were found if no documents match the query entered by the user. 

### Styles (`styles.css`)
The CSS file includes styles for the home and results page including background colors, fonts, and more. 