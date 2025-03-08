from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.database.models import User, Action
from sqlalchemy.exc import IntegrityError
from src.dependencies import DBSession
from src.schemas.action import ActionType
from src.schemas.user import UserDTO, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, session: DBSession) -> UserDTO:
    """Get user info from database
    
    Args:
        user_id (int): The Telegram ID of the user to retrieve.
        session (DBSession): The database session.

    Returns:
        UserDTO: The user object containing the details of the user.
    
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.model_validate(user)

@router.post("/create", response_model=UserDTO)
async def create_user(user: UserCreate, session: DBSession):
    """Create a new user in database
    
    Args:
        user (UserCreate): The user object containing the details of the new user.
        session (DBSession): The database session.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    new_user = User(**user.model_dump())
    try:
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user) # refresh the object to get the new ID
        action = Action(time=new_user.created_at, user_id=new_user.id, action_type=ActionType.REGISTRATION)
        session.add(action)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    return UserDTO.model_validate(new_user)

@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, session: DBSession):
    """Update a user in database
    
    Args:
        user_id (int): The Telegram ID of the user to update.
        user (UserUpdate): The user object containing the details of the updated user.
        session (DBSession): The database session.
        
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    try:
        await session.flush()
        await session.refresh(user)
        action = Action(time=user.updated_at, user_id=user.id, action_type=ActionType.UPDATE_PROFILE)
        session.add(action)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Problem with updating user information\nError: {e}")
    return UserDTO.model_validate(user)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: DBSession):
    """Delete a user from database
    
    Args:
        user_id (int): The Telegram ID of the user to delete.
        session (DBSession): The database session.
        
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        await session.delete(user)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
