import logging
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from os import environ
from os.path import exists 
from src.load_vector.doc_data import load_in_vector

# Load environment variables
load_dotenv()
genai_key = environ.get("genai_key")

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("posthog").setLevel(logging.CRITICAL)
# Constants
VECTOR_STORE_NAME = "simple-rag"
PERSIST_DIRECTORY = "./Data/vector_db"
DOC_PATH = "./Data/finance.txt"
MODEL ="gemini-2.0-flash"

def get_vector_db(persist_directory=PERSIST_DIRECTORY):
    """
    Open and return a connection to the Chroma vector database.
    """
    try:
        vector_db = Chroma(
            collection_name=VECTOR_STORE_NAME,
            persist_directory=persist_directory,
            embedding_function=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=genai_key)
        )
        logging.info(f"Connected to the vector database at {persist_directory}.")
        
        # Check the number of documents in the collection
        doc_count = vector_db._collection.count()  # Get the count of documents in the collection
        logging.info(f"Number of documents in the vector database: {doc_count}")
        
        return vector_db
    except Exception as e:
        logging.error(f"Failed to connect to the vector database: {e}")
        return None


def create_retriever(vector_db, llm):
    """
    Create a multi-query retriever using the given vector database and LLM.
    """
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from
a vector database. By generating multiple perspectives on the user question, your
goal is to help the user overcome some of the limitations of the distance-based
similarity search. Provide these alternative questions separated by newlines.
Original question: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
    )
    logging.info("Retriever created.")
    return retriever


def create_chain(retriever, llm):
    """
    Create the chain for retrieval-augmented generation (RAG).
    """
    template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logging.info("Chain created successfully.")
    return chain


def rag_query_resolver(query:str) -> str:

    """
    Main function to run the end-to-end pipeline.
    """
    if not genai_key:
        logging.error("API key for Google Generative AI not found. Exiting.")
        return
    if not exists(PERSIST_DIRECTORY) or get_vector_db()._collection.count() == 0:
        load_in_vector(DOC_PATH, PERSIST_DIRECTORY)
    # Initialize the Google Generative AI wrapper
    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=genai_key)

    # Load or connect to the vector database
    vector_db = get_vector_db()
    if not vector_db:
        logging.error("Vector database connection failed. Exiting.")
        return

    # Create the retriever
    retriever = create_retriever(vector_db, llm)

    # Create the chain
    chain = create_chain(retriever, llm)

    # Get the response
    try:
        res = chain.invoke(input=query)
        logging.info(f"Response:{res}")
        return res
    except Exception as e:
        logging.error(f"Error during chain invocation: {e}")


if __name__ == "__main__":
    query = "what is finance?"
    rag_query_resolver(query)
