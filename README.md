<div align="center">

# Enterprise Multi-Tenant Compliance AI Agent

### An Agentic RAG System for Secure, Context-Aware Compliance Policy Question Answering

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/LangGraph-Agentic_AI-1C3C3C?style=for-the-badge" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render"/>
</p>

<p>
  <a href="https://compliance-policy-ai-agent.onrender.com/docs">
    <img src="https://img.shields.io/badge/Live_API-Explore_Documentation-success?style=for-the-badge&logo=swagger&logoColor=white" alt="Live API Documentation"/>
  </a>
</p>

<p>
  <strong>Secure Multi-Tenant Retrieval-Augmented Generation | LangGraph Workflows | Hallucination Detection</strong>
</p>

</div>

---

## Overview

The **Enterprise Multi-Tenant Compliance AI Agent** is a cloud-deployed, agentic Retrieval-Augmented Generation (RAG) application designed to answer compliance-related questions using organization-specific policy documents.

The system combines **LangGraph, Groq LLMs, Cohere Embeddings, and Qdrant Cloud** to deliver context-aware responses while maintaining tenant-level data isolation.

Unlike a basic RAG pipeline that directly returns an LLM-generated response, this application incorporates an additional evaluation stage that verifies generated answers against retrieved document context.

If the generated answer fails the evaluation, the system returns a safe fallback rather than presenting an unsupported response.

### Key Highlights

- **Multi-Tenant Architecture:** Isolates organization-specific information using `tenant_id` metadata filtering in Qdrant.
- **Agentic Workflow:** Uses LangGraph StateGraph to orchestrate retrieval, answer generation, and evaluation.
- **Hallucination Guardrail:** Evaluates generated responses against retrieved context before returning an answer.
- **Cloud-Optimized Deployment:** Uses API-based embeddings instead of locally hosted PyTorch embedding models.
- **Production-Oriented API:** Built with FastAPI and deployed using Docker on Render.
- **Interactive API Documentation:** Provides an OpenAPI/Swagger interface for testing endpoints.

### Live Application

| Resource | Link |
|---|---|
| Live API | [Open Live Application](https://compliance-policy-ai-agent.onrender.com) |
| Swagger Documentation | [Explore API Endpoints](https://compliance-policy-ai-agent.onrender.com/docs) |
| OpenAPI Schema | [API Schema](https://compliance-policy-ai-agent.onrender.com/openapi.json) |

---

## Architecture Flow

The application follows an agentic RAG architecture in which each stage performs a specific responsibility.

```mermaid
flowchart TD
    A["User Query"] --> B["Tenant Filter"]
    B --> C["Qdrant Vector Search"]
    C --> D["Retrieve Relevant Context"]
    D --> E["LangGraph StateGraph"]
    E --> F["Groq LLM - Generate Answer"]
    F --> G["Evaluator Node"]
    G --> H{"Evaluation Result"}

    H -->|PASS| I["Return Verified Answer"]
    H -->|FAIL| J["Safe Fallback Response"]

    I --> K["API Response"]
    J --> K

    style A fill:#DCEEFF,stroke:#2563EB,color:#111827
    style B fill:#E0F2FE,stroke:#0284C7,color:#111827
    style C fill:#F3E8FF,stroke:#9333EA,color:#111827
    style F fill:#DCFCE7,stroke:#16A34A,color:#111827
    style G fill:#FEF3C7,stroke:#D97706,color:#111827
    style I fill:#DCFCE7,stroke:#16A34A,color:#111827
    style J fill:#FEE2E2,stroke:#DC2626,color:#111827
