import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.config import settings

# We use a free, local embedding model (runs on your laptop CPU)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_pdf(file_path: str, tenant_id: str):
    print(f"Loading PDF: {file_path} for tenant: {tenant_id}")
    
    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # 2. Chunk the text (1000 chars with 150 overlap)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Connect to Qdrant
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    
    # 4. Create collection if it doesn't exist
    if not client.collection_exists(settings.COLLECTION_NAME):
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
       
        client.create_payload_index(
            collection_name=settings.COLLECTION_NAME,
            field_name="tenant_id",
            field_schema="keyword",
        )    
    # 5. Embed and upload chunks
    points = []
    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk.page_content)
        
        # We attach tenant_id and page number to the metadata!
        payload = {
            "tenant_id": tenant_id,
            "text": chunk.page_content,
            "page": chunk.metadata.get("page", 0)
        }
        
        points.append(PointStruct(id=i, vector=vector, payload=payload))
        
    client.upsert(collection_name=settings.COLLECTION_NAME, points=points)
    print(f"Successfully ingested {len(points)} chunks into Qdrant.")

if __name__ == "__main__":
    print("Ingestion module loaded successfully.")