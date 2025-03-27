# main.py
import os
import logging
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import pandas as pd
import posthog

# Disable PostHog telemetry
posthog.disabled = True

# Load environment variables
load_dotenv()
genai_key = os.getenv("genai_key")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
# DOC_PATH = os.path.join(BASE_DIR, "./Data/finance.txt")  # Ensure relative path handling
DOC_PATH = "./Data/finance.txt"
VECTOR_STORE_NAME = "simple-rag"
#PERSIST_DIRECTORY = os.path.join(BASE_DIR, "vector_db")
PERSIST_DIRECTORY = "./Data/vector_db"


def ingest_pdf(doc_path):
    """Load PDF documents if they exist."""
    try:
        if not os.path.exists(doc_path):
            logging.error(f"PDF file not found: {doc_path}")
            return None
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        logging.info(f"PDF loaded successfully: {doc_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading PDF: {e}")
        return None

def split_text_contents(text, chunk_size=1000, chunk_overlap=300):
    """Splits text into smaller chunks."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        documents = [Document(page_content=text)]
        chunks = text_splitter.split_documents(documents)
        logging.info(f"Text split into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logging.error(f"Error splitting text: {e}")
        return []

def split_documents(documents, chunk_size=1200, chunk_overlap=300):
    """Splits document-based content into smaller chunks."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        logging.info(f"Documents split into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logging.error(f"Error splitting documents: {e}")
        return []

def create_vector_db(chunks , PERSIST_DIRECTORY):
    """Creates and persists a vector database from document chunks."""
    try:
        if not chunks:
            logging.warning("No document chunks available for vector storage.")
            return None
        vector_db = Chroma.from_documents(
            documents=chunks,
            collection_name=VECTOR_STORE_NAME,
            persist_directory=PERSIST_DIRECTORY,
            embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=genai_key)
        )
        logging.info("Vector database created and persisted successfully.")
        return vector_db
    except Exception as e:
        logging.error(f"Error creating vector database: {e}")
        return None

def load_in_vector(DOC_PATH , PERSIST_DIRECTORY):
    """Main function to load, process, and store documents in a vector database."""
    if not os.path.exists(DOC_PATH):
        logging.error(f"Document not found: {DOC_PATH}")
        return

    try:
        if DOC_PATH.endswith(".txt"):
            logging.info(f"Loading text file: {DOC_PATH}")
            with open(DOC_PATH, 'r', encoding="utf-8") as file:
                data = file.read()
            doc_chunks = split_text_contents(data)
        elif DOC_PATH.endswith(".pdf"):
            logging.info(f"Loading PDF file: {DOC_PATH}")
            data = ingest_pdf(DOC_PATH)
            if data is None:
                return
            doc_chunks = split_documents(data)
            
        elif DOC_PATH.endswith(".docx"):
            logging.info(f"Loading DOCX file: {DOC_PATH}")
            loader = UnstructuredWordDocumentLoader(file_path=DOC_PATH)
            data = loader.load()
            doc_chunks = split_documents(data)
            
        elif DOC_PATH.endswith(".csv"):
            df = pd.read_csv(DOC_PATH)
            data = "\n".join(df.to_string(index=False).split("\n"))
            doc_chunks = split_text_contents(data)
            
        else:
            logging.error(f"Unsupported file type: {DOC_PATH}")
            return

        # Create and persist the vector database
        create_vector_db(doc_chunks , PERSIST_DIRECTORY)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    load_in_vector(DOC_PATH , PERSIST_DIRECTORY)
