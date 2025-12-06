import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
load_dotenv()
# -----------------------------
# Step 1: Prepare documents
# -----------------------------
docs = [
    "Customer order number is 14 digits. It starts with 667517 and follows specific rules...",
    "Validation rules for order number: must be numeric, 14 characters long, and follow checksum rules.",
    "Examples of valid Customer order numbers: 66751710041004, 66751710581009, 66751710221007",
]

# -----------------------------
# Step 2: Split documents
# -----------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.create_documents(docs)

# -----------------------------
# Step 3: Embeddings
# -----------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# Step 4: Vector store
# -----------------------------
db = Chroma.from_documents(chunks, embedding=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 2})

# -----------------------------
# Step 5: Local Hugging Face LLM
# -----------------------------
# Use a text2text-generation pipeline locally
pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",  # lightweight local model
    tokenizer="google/flan-t5-small",
    device=-1  # CPU; use 0 for GPU
)

llm = HuggingFacePipeline(pipeline=pipe)

# -----------------------------
# Step 6: RAG chain
# -----------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
)

# -----------------------------
# Step 7: Ask questions
# -----------------------------
questions = [
    "What is the length of Customer order number?",
    "Give an example of a valid Customer order number.",
    "What are the validation rules for Customer order numbers?",
    "What does the first six digits of a Customer order number represent?",
]

for q in questions:
    response = qa_chain.invoke({"query": q})
    print("Q:", q)
    print("A:", response["result"])
    print("-" * 50)
