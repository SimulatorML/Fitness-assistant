from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/request/{query}")
def test_llm(query: str):
    return {"Status": "OK", "response": "llm response here"}
