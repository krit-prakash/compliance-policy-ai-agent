\# Enterprise Multi-Tenant Compliance AI Agent



A cloud-native RAG application built for secure document Q\&A. It uses LangGraph for agentic workflows, Groq for LLM inference, and Qdrant for vector storage. 



\*\*Live API Endpoint:\*\* https://compliance-policy-ai-agent.onrender.com/docs



\## Architecture

\- \*\*FastAPI:\*\* Serves the REST API endpoints.

\- \*\*LangGraph:\*\* Manages the agent state and conditional routing.

\- \*\*Groq (openai/gpt-oss-120b):\*\* Handles generation and evaluation tasks.

\- \*\*Qdrant Cloud:\*\* Stores document embeddings with strict tenant isolation.

\- \*\*Cohere:\*\* Generates embeddings for document chunks and user queries.

\- \*\*Docker:\*\* Containerized for deployment on Render.



\## Implementation Details

\- \*\*Multi-Tenancy:\*\* Data isolation is enforced at the database level. Every chunk is tagged with a `tenant\_id`, and retrieval queries always filter by this ID. A tenant cannot access another tenant's data.

\- \*\*Hallucination Guardrail:\*\* The LangGraph workflow includes an evaluation node. After the LLM generates an answer, a second prompt verifies if the answer is actually supported by the retrieved context. If it detects a hallucination, it overrides the answer with a safe fallback.

\- \*\*Cloud Deployment Constraints:\*\* Handled the 512MB memory limit on Render's free tier by moving away from local HuggingFace/PyTorch embeddings to Cohere's API, reducing the container size and memory footprint significantly.



\## Local Setup

1\. Clone the repository.

2\. Create a virtual environment and install dependencies: `pip install -r requirements.txt`

3\. Add your API keys to a `.env` file (`GROQ\_API\_KEY`, `QDRANT\_URL`, `QDRANT\_API\_KEY`, `COHERE\_API\_KEY`).

4\. Run the ingestion script to load a PDF: `python -c "from src.ingest import ingest\_pdf; ingest\_pdf('test\_policy.pdf', tenant\_id='acme\_corp')"`

5\. Start the server: `uvicorn src.api:api --reload`

