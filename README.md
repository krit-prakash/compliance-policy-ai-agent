# 🏢 Enterprise Multi-Tenant Compliance AI Agent

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflow-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)
![Render](https://img.shields.io/badge/Deploy-Render_Live-success?style=flat-square)

A secure, cloud-native Retrieval-Augmented Generation (RAG) system designed for multi-tenant document Q&A. Built to demonstrate strict data isolation, hallucination prevention, and lightweight cloud deployment.

🔗 **[Try the Live API](https://compliance-policy-ai-agent.onrender.com/docs)**

---

## 📖 The Problem
Standard RAG applications are vulnerable to two major issues in enterprise environments:
1. **Data Leakage:** Without strict isolation, a user from Tenant A could retrieve data belonging to Tenant B.
2. **Hallucinations:** LLMs will confidently invent an answer if the retrieved context doesn't contain the truth.

## 💡 The Solution
This project implements an **Agentic RAG Architecture** using **LangGraph** to solve both problems.

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
[ Generate Answer ] ──(Groq / Llama-3)
      │
      ▼
[ 🛡️ Faithfulness Evaluator ] ──(LangGraph Node)
      │
      ├─► (FAIL) ──> [ Safe Fallback Response ]
      │
      └─► (PASS) ──> [ Deliver Final Answer ]
