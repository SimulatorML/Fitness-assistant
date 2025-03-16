from fastapi import APIRouter
from pydantic import BaseModel
from llm.workflow import process_fitness_query
from src.dependencies import DBSession

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMRequest(BaseModel):
    query: str
    telegram_id: int 


@router.post("/request")
async def llm_request(data: LLMRequest, session: DBSession):
    """
    Endpoint to send a fitness-related query and user ID to the LLM.
    """
    response = await process_fitness_query(data.query, data.telegram_id, session)
        
    return {"Status": "OK", "response": response}
