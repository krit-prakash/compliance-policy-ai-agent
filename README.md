# 🏢 Enterprise Multi-Tenant Compliance AI Agent

<div align="center">

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflow-orange.svg?style=for-the-badge)](https://python.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deploy-Live_on_Render-success.svg?style=for-the-badge)](https://compliance-policy-ai-agent.onrender.com/docs)

**A secure, cloud-native Retrieval-Augmented Generation (RAG) system designed for multi-tenant document Q&A.**

[Live API](https://compliance-policy-ai-agent.onrender.com/docs) • [Architecture](#architecture) • [Tech Stack](#tech-stack) • [Local Setup](#local-setup)

</div>

---

## 📖 The Problem
Standard RAG applications are vulnerable to two major issues in enterprise environments:
1. **Data Leakage:** Without strict isolation, a user from Tenant A could retrieve data belonging to Tenant B.
2. **Hallucinations:** LLMs will confidently invent an answer if the retrieved context does not contain the truth.

## 💡 The Solution
This project implements an **Agentic RAG Architecture** using **LangGraph** to solve both problems. It forces the LLM to strictly adhere to the retrieved context and isolates data at the vector database level.

### Architecture Flow
```mermaid
graph TD
    User([User Query]) --> Filter[Tenant Filter]
    Filter -->|Strict Qdrant Filter| Retrieve[Retrieve Context]
    Retrieve -->|Cohere Embeddings| DB[(Qdrant Cloud DB)]
    Retrieve --> Generate[Generate Answer]
    Generate -->|Groq LLM| Evaluator{Faithfulness Evaluator}
    Evaluator -->|FAIL| Fallback[Safe Fallback Response]
    Evaluator -->|PASS| Answer([Deliver Final Answer])
    
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef security fill:#ffe6e6,stroke:#cc0000,stroke-width:2px;
    classDef ai fill:#e6f3ff,stroke:#0066cc,stroke-width:2px;
    class Evaluator security;
    class Generate,Retrieve ai;

🔑 Key Technical Decisions
Feature	Implementation	Business Impact
Multi-Tenancy	Every document chunk is tagged with a tenant_id. The retrieval node applies a strict Qdrant must filter.	Physically impossible for one tenant to search another's documents.
Hallucination Guard	LangGraph features a self-reflective loop. A secondary evaluation node verifies the answer against context.	Blocks LLM hallucinations and returns a safe fallback, ensuring compliance.
Cloud Optimization	Bypassed heavy PyTorch dependencies by utilizing Cohere API for embeddings.	Reduced container size to fit within 512MB RAM, enabling zero-cost cloud deployment.
🛠️ Tech Stack
<div align="center">
Category	Technology
Framework	FastAPI, Uvicorn
Agentic Engine	LangGraph
LLM Inference	Groq (openai/gpt-oss-120b)
Vector Database	Qdrant Cloud
Embeddings	Cohere (embed-english-light-v3.0)
Deployment	Docker, Render
</div>
🚀 Local Setup
Clone the repository

bash
git clone https://github.com/krit-prakash/compliance-policy-ai-agent.git
cd compliance-policy-ai-agent
Set up environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure Secrets
Create a .env file in the root directory:

env
GROQ_API_KEY=your_groq_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
COHERE_API_KEY=your_cohere_key
Ingest a Document

bash
python -c "from src.ingest import ingest_pdf; ingest_pdf('test_policy.pdf', tenant_id='acme_corp')"
Run the API

bash
uvicorn src.api:api --reload
Visit http://localhost:8000/docs to interact with the Swagger UI.

<div align="center"> <i>Built by <a href="https://github.com/krit-prakash">Krit Prakash</a></i> </div> ```
