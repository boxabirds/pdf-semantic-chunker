import os
import argparse
import PyPDF2
import requests

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = [page.extract_text() for page in reader.pages if page.extract_text() is not None]
    return text

def chunk_text(text, chunk_size=500):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

def index_chunks(chunks, source_file, page_number):
    url = 'http://localhost:8081/v1/objects'
    for chunk in chunks:
        data = {
            "class": "TextChunk",
            "properties": {
                "sourceFile": source_file,
                "chunkText": chunk,
                "page": page_number
            }
        }
        response = requests.post(url, json=data)
        print(response.json())

def search_query(query):
    url = 'http://localhost:8081/v1/graphql'
    query = {
        "query": f"""
        {{
            Get {{
                TextChunk(
                    nearText: {{
                        concepts: ["{query}"],
                        certainty: 0.7
                    }}
                ) {{
                    sourceFile
                    chunkText
                    page
                }}
            }}
        }}
        """
    }
    response = requests.post(url, json=query)
    return response.json()

def main(source_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith('.pdf'):
            file_path = os.path.join(source_folder, filename)
            pages = read_pdf(file_path)
            for page_number, page_text in enumerate(pages, start=1):
                chunks = chunk_text(page_text)
                index_chunks(chunks, filename, page_number)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDFs and index text chunks into Weaviate.")
    parser.add_argument('--source', default='data', help='Folder containing PDF files')
    args = parser.parse_args()
    main(args.source)
    query = "is Vale of White Horse District council working with external partners or other councils to seek to influence national governments on climate action, or to learn about and share best practice on council climate action?"
    search_results = search_query(query)
    print(search_results)
