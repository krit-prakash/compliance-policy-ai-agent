from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import app as agent_app

api = FastAPI(title="Compliance AI Agent API", version="1.0")

class ChatRequest(BaseModel):
    question: str
    tenant_id: str

class ChatResponse(BaseModel):
    answer: str
    tenant_id: str
    status: str

@api.get("/health")
def health_check():
    return {"status": "healthy", "service": "compliance-agent"}

@api.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        inputs = {
            "question": request.question,
            "tenant_id": request.tenant_id,
            "retry_count": 0
        }
        
        final_answer = ""
        for output in agent_app.stream(inputs):
            for key, value in output.items():
                if "generation" in value:
                    final_answer = value["generation"]
                    
        if not final_answer:
            raise HTTPException(status_code=500, detail="Agent failed to generate an answer.")
            
        return ChatResponse(
            answer=final_answer,
            tenant_id=request.tenant_id,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))