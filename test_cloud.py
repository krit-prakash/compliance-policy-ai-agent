import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from qdrant_client import QdrantClient

load_dotenv()

print("Testing Qdrant...")
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
print("Qdrant connection successful!")

print("Testing Groq...")
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name=os.getenv("GROQ_MODEL"))
print("Groq says:", llm.invoke("Say 'Hello Krit'").content)