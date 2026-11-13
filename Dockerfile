FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# 1. Install CPU-only PyTorch first (prevents it from downloading 2GB of NVIDIA GPU drivers)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 2. Install the rest of the libraries
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn langgraph langchain langchain-groq langchain-huggingface qdrant-client sentence-transformers pypdf langchain-community python-dotenv

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api:api", "--host", "0.0.0.0", "--port", "8000"]