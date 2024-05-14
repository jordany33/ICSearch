import sys
from index import build_index

if __name__ == "__main__":
    inverted_index = build_index(...)

    while True:
        query = input("Enter query (or type 'exit' to quit prompt): ").strip().lower()
        
        if query == 'exit':
            break
        
        #process the query here
        ...


        #show results
        if ...:
            print(f"Documents matching query '{query}': {sorted(...)}")
        else:
            print(f"No documents found for query '{query}'")
