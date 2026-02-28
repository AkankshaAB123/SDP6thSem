from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_vector_store(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    # Fake embeddings (no external ML dependencies)
    embeddings = FakeEmbeddings(size=384)

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def retrieve_context(vectorstore, query):

    docs = vectorstore.similarity_search(query, k=5)

    return "\n\n".join([doc.page_content for doc in docs])