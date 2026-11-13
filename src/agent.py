from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_cohere import CohereEmbeddings
from qdrant_client import QdrantClient
from src.config import settings

class AgentState(TypedDict):
    question: str
    tenant_id: str
    retrieved_docs: List[str]
    generation: str
    retry_count: int

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name=settings.GROQ_MODEL)
embeddings = CohereEmbeddings(
    cohere_api_key=settings.COHERE_API_KEY,
    model="embed-english-light-v3.0"
)
qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

def retrieve_docs(state: AgentState):
    print("---RETRIEVING DOCS---")
    question = state["question"]
    tenant = state["tenant_id"]
    
    query_vector = embeddings.embed_query(question)
    
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

def evaluate_faithfulness(state: AgentState):
    print("---EVALUATING FAITHFULNESS---")
    generation = state["generation"]
    docs = state["retrieved_docs"]
    
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

def should_retry(state: AgentState):
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_docs)
workflow.add_node("generate", generate_answer)
workflow.add_node("evaluate", evaluate_faithfulness)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "evaluate")
workflow.add_conditional_edges("evaluate", should_retry, {"end": END})

app = workflow.compile()