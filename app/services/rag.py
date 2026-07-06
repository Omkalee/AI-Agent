import os
import fitz

from openai import OpenAI

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# -----------------------------
# Embedding Model
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Groq Client
# -----------------------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# Read PDF
# -----------------------------

def read_pdf(pdf_path: str):

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# -----------------------------
# Split into chunks
# -----------------------------

def split_text(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_text(text)


# -----------------------------
# Store in Chroma
# -----------------------------

def store_chunks(chunks):

    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory="app/chroma_db",
        collection_name="pdf_collection"
    )

    return len(chunks)


# -----------------------------
# Ask PDF
# -----------------------------

def search_pdf(question):

    vectordb = Chroma(
        persist_directory="app/chroma_db",
        embedding_function=embedding_model,
        collection_name="pdf_collection"
    )

    docs = vectordb.similarity_search(question, k=5)

    print("=" * 60)
    print("Retrieved Documents:", len(docs))
    print("=" * 60)

    for i, doc in enumerate(docs):
        print(f"\nChunk {i+1}\n")
        print(doc.page_content[:500])

    if len(docs) == 0:
        return "No information found in database."

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer does not exist, reply exactly:

I couldn't find this information in the uploaded PDF.

Context:

{context}

Question:

{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content