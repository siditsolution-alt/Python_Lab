import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# -----------------------------
# Step 1: Prepare your documents
# -----------------------------
docs = [
    "Customer order number is 14 digits. It starts with 667517 and follows specific rules...",
    "Validation rules for order number: must be numeric, 14 characters long, and follow checksum rules.",
    "Examples of valid Customer order numbers: 66751710041004, 66751710581009, 66751710221007",
]
# -----------------------------
# Step 2: Split documents into smaller chunks
# -----------------------------
# RecursiveCharacterTextSplitter splits large text into chunks suitable for embedding
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.create_documents(docs)

# -----------------------------
# Step 3: Create embeddings for chunks
# -----------------------------
# OpenAIEmbeddings converts text into vector representations
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# -----------------------------
# Step 4: Create a vector store (Chroma)
# -----------------------------
# Stores embeddings and enables semantic search
db = Chroma.from_documents(chunks, embedding=embeddings)

# -----------------------------
# Step 5: Create a retriever
# -----------------------------
# Wrap vector store as a retriever to fetch relevant documents
retriever = db.as_retriever(search_kwargs={"k": 2})  # fetch top 2 relevant chunks

# -----------------------------
# Step 6: Create the LLM
# -----------------------------
# ChatOpenAI is the language model that generates answers
llm = ChatOpenAI(model="gpt-4o", temperature=0)  # temperature=0 for deterministic answers

# -----------------------------
# Step 7: Create the RetrievalQA (RAG) chain
# -----------------------------
# Combines retriever and LLM to answer questions using relevant docs
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",  # "stuff" combines all retrieved docs into one prompt
)

# -----------------------------
# Step 8: Ask a question
# -----------------------------
questions = [
    "What is the length of Customer order number?",
    "Give an example of a valid Customer order number.",
    "What are the validation rules for Customer order numbers?",
    "What does the first six digits of an Customer order number represent?",
]

# Loop through questions and get answers
for q in questions:
    response = qa_chain.invoke({"query": q})
    print("Q:", q)
    print("A:", response["result"])
    print("-" * 50)