from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from llm.workflow import process_fitness_query
from src.views.users import get_user
from src.dependencies import DBSession

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMRequest(BaseModel):
    query: str
    user_id: int 


@router.post("/request")
async def llm_request(data: LLMRequest, session: DBSession):
    """
    Endpoint to send a fitness-related query and user ID to the LLM.
    Retrieves user details from the database before querying.
    Temporary -> Uses mock user data if database is unavailable.
    """
    try:
        user_info = await get_user(data.user_id, session)
        
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_dict = user_info.model_dump()
    
    # use mock data (remove in future)
    except Exception:
        user_dict = {
            "id": data.user_id,
            "name": "Test User",
            "age": 30,
            "fitness_level": "Intermediate",
            "goal": "Gain muscle"
        }
  
    response = process_fitness_query(data.query, user_dict)
        
    return {"Status": "OK", "response": response}
