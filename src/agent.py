from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from src.config import settings

# Define the State (the memory of the agent)
class AgentState(TypedDict):
    question: str
    tenant_id: str
    retrieved_docs: List[str]
    generation: str
    retry_count: int

# Initialize clients
llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name=settings.GROQ_MODEL)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

# Node 1: Retrieval
def retrieve_docs(state: AgentState):
    print("---RETRIEVING DOCS---")
    question = state["question"]
    tenant = state["tenant_id"]
    
    # Embed the question
    query_vector = embeddings.embed_query(question)
    
    # Search Qdrant (Strict tenant isolation!)
    search_result = qdrant.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=query_vector,
        query_filter={
            "must": [
                {"key": "tenant_id", "match": {"value": tenant}}
            ]
        },
        limit=3
    )
    
    docs = [hit.payload["text"] for hit in search_result.points]
    return {"retrieved_docs": docs}
        
# Node 2: Generation (with Guardrails)
def generate_answer(state: AgentState):
    print("---GENERATING ANSWER---")
    question = state["question"]
    docs = state["retrieved_docs"]
    retry = state.get("retry_count", 0)
    
    if not docs:
        return {"generation": "I cannot answer this based on the provided documents.", "retry_count": retry + 1}
        
    context = "\n\n".join(docs)
    
    prompt = f"""You are a compliance AI. Answer the question using ONLY the context below. 
    If you don't know, say "I don't know".
    
    Context: {context}
    Question: {question}
    Answer:"""
    
    response = llm.invoke(prompt)
    return {"generation": response.content, "retry_count": retry + 1}

# Node 3: Evaluate Faithfulness (The Hallucination Guard)
def evaluate_faithfulness(state: AgentState):
    print("---EVALUATING FAITHFULNESS---")
    generation = state["generation"]
    docs = state["retrieved_docs"]
    
    # If it couldn't find docs, don't evaluate, just end.
    if not docs:
        return {"generation": "I cannot answer this based on the provided documents."}
        
    context = "\n\n".join(docs)
    
    prompt = f"""Evaluate if the ANSWER is fully supported by the CONTEXT. 
    Reply ONLY with 'PASS' or 'FAIL'.
    
    Context: {context}
    Answer: {generation}
    """
    
    response = llm.invoke(prompt)
    
    if "FAIL" in response.content.upper():
        print("Hallucination detected! Overriding answer.")
        return {"generation": "I apologize, but I cannot verify the accuracy of this answer based on the current documents."}
    
    print("Answer passed evaluation.")
    return state

# Node 4: Conditional Logic
def should_retry(state: AgentState):
    if state.get("retry_count", 0) >= 1:
        return "end"
    return "end" # We keep it simple for now, could loop back to generate

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_docs)
workflow.add_node("generate", generate_answer)
workflow.add_node("evaluate", evaluate_faithfulness)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "evaluate")
workflow.add_conditional_edges("evaluate", should_retry, {"end": END})

app = workflow.compile()