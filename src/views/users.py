from fastapi import APIRouter
from src.database.models import User
from src.dependencies import DBSession
from src.schemas.user import UserDTO, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create")
def create_user(user: UserCreate):
    """Create a new user in database
    
    Args:
        user (UserCreate): The user object containing the details of the new user.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    return {"Status": "OK"}

@router.get("/{user_id}")
def get_user(user_id: int, session: DBSession) -> UserDTO:
    """Get user info from database
    
    Args:
        user_id (int): The ID of the user to retrieve.
        session (DBSession): The database session.

    Returns:
        UserDTO: The user object containing the details of the user.
    
    Raises:
        HTTPException: If the user is not found.
    """
    user = session.get(User, user_id)
    return UserDTO.model_validate(user)

@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    return {"Status": "OK", "user_id": user.user_id}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"Status": "OK"}
