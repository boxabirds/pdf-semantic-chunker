import argparse
import PyPDF2
from semantic_split import SimilarSentenceSplitter, SentenceTransformersSimilarity, SpacySentenceSplitter

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
    return text

def split_text_semantically(text):
    model = SentenceTransformersSimilarity()
    sentence_splitter = SpacySentenceSplitter()
    splitter = SimilarSentenceSplitter(model, sentence_splitter)
    return splitter.split(text)

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF and split it semantically.")
    parser.add_argument("--file", type=str, required=True, help="Path to the PDF file.")
    args = parser.parse_args()

    pdf_text = extract_text_from_pdf(args.file)
    semantic_chunks = split_text_semantically(pdf_text)
    
    for chunk in semantic_chunks:
        print("Chunk:")
        for sentence in chunk:
            print(sentence)
        print("\n---\n")

if __name__ == "__main__":
    main()
