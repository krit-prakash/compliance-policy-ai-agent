# Enterprise Multi-Tenant Compliance AI Agent

A secure, cloud-native Retrieval-Augmented Generation (RAG) system designed for multi-tenant document Q&A.

**[Try the Live API](https://compliance-policy-ai-agent.onrender.com/docs)**

## The Problem
Standard RAG applications are vulnerable to two major issues in enterprise environments:
1. **Data Leakage:** Without strict isolation, a user from Tenant A could retrieve data belonging to Tenant B.
2. **Hallucinations:** LLMs will confidently invent an answer if the retrieved context doesn't contain the truth.

## The Solution
This project implements an Agentic RAG Architecture using LangGraph to solve both problems.

```text
[ User Query ] 
      │
      ▼
[ Tenant Filter ] ──(Strict Qdrant Metadata Isolation)──┐
      │                                                 │
      ▼                                                 ▼
[ Retrieve Context ] ──(Cohere Embeddings)──> [ Qdrant Cloud DB ]
      │
      ▼
[ Generate Answer ] ──(Groq)
      │
      ▼
[ Faithfulness Evaluator ] ──(LangGraph Node)
      │
      ├─► (FAIL) ──> [ Safe Fallback Response ]
      │
      └─► (PASS) ──> [ Deliver Final Answer ]

Key Technical Decisions
Multi-Tenancy: Every document chunk is tagged with a tenant_id. The retrieval node applies a strict Qdrant must filter, making it physically impossible for one tenant to search another's documents.

Hallucination Guardrail: The LangGraph workflow features a self-reflective loop. The generated answer is passed to a secondary evaluation node. If it detects that the LLM hallucinated, it blocks the output and returns a safe fallback.

Cloud-Native Optimization: To bypass the memory limitations of serverless free tiers, the system avoids heavy local PyTorch dependencies. Instead, it utilizes the Cohere API for lightweight, highly scalable embeddings.

Tech Stack
Framework: FastAPI, Uvicorn

Agentic Engine: LangGraph

LLM Inference: Groq

Vector Database: Qdrant Cloud

Embeddings: Cohere

Deployment: Docker, Render

Local Setup
Clone the repository: git clone https://github.com/krit-prakash/compliance-policy-ai-agent.git

Set up environment: python -m venv venv and pip install -r requirements.txt

Configure Secrets in .env (GROQ_API_KEY, QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY)

Ingest a Document: python -c "from src.ingest import ingest_pdf; ingest_pdf('test_policy.pdf', tenant_id='acme_corp')"

Run the API: uvicorn src.api:api --reload

Built by Krit Prakash