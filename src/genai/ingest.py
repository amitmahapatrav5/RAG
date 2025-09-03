import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()


# # Loading Data
loader = DirectoryLoader(
    path = Path(os.environ.get('DATA_DIRECTORY_ABSOLUTE_PATH')),
    loader_cls=UnstructuredMarkdownLoader

)
docs = loader.lazy_load()



# def load_data_in_vector_db(file):
#     pass


# Splitting Data into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents( [doc for doc in docs] )


# Adding Chunks to Vector DB
embedding_model = HuggingFaceEmbeddings(
    model_name=os.environ.get('EMBEDDING_MODEL_REPO_ID')
)

db = Chroma(
    persist_directory=Path(os.environ.get('VECTOR_DB_PERSISTENT_ABSOLUTE_PATH')),
    embedding_function=embedding_model,
    collection_name=os.environ.get('VECTOR_DB_NAME')
)
db.add_documents(chunks)

# Created By Amit Mahapatra