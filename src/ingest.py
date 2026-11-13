import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from src.config import settings

# Use Cohere for cloud embeddings (no PyTorch needed)
embeddings = CohereEmbeddings(
    cohere_api_key=settings.COHERE_API_KEY,
    model="embed-english-light-v3.0"
)

def ingest_pdf(file_path: str, tenant_id: str):
    print(f"Loading PDF: {file_path} for tenant: {tenant_id}")
    
    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # 2. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Connect to Qdrant
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    
    # 4. Create collection if it doesn't exist (Cohere light model uses size=1024)
    if not client.collection_exists(settings.COLLECTION_NAME):
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
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