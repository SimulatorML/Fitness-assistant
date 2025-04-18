from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.database.models import User, Action
from sqlalchemy.exc import IntegrityError
from src.dependencies import DBSession
from src.schemas.action import ActionType
from src.schemas.user import UserDTO, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, db_session: DBSession) -> UserDTO:
    """Get user info from database
    
    Args:
        user_id (int): The Telegram ID of the user to retrieve.
        db_session (DBSession): The database session.

    Returns:
        UserDTO: The user object containing the details of the user.
    
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.model_validate(user)

@router.post("/create", response_model=UserDTO)
async def create_user(user: UserCreate, db_session: DBSession):
    """Create a new user in database
    
    Args:
        user (UserCreate): The user object containing the details of the new user.
        db_session (DBSession): The database session.

    Returns:
        UserDTO: The user object containing the details of the user.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    new_user = User(**user.model_dump())
    try:
        db_session.add(new_user)
        await db_session.flush()
        await db_session.refresh(new_user) # refresh the object to get the new ID
        action = Action(time=new_user.created_at, user_id=new_user.id, action_type=ActionType.REGISTRATION)
        db_session.add(action)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    return UserDTO.model_validate(new_user)

@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db_session: DBSession):
    """Update a user in database
    
    Args:
        user_id (int): The Telegram ID of the user to update.
        user (UserUpdate): The user object containing the details of the updated user.
        db_session (DBSession): The database session.

    Returns:
        UserDTO: The user object containing the details of the user.
        
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    try:
        await db_session.flush()
        await db_session.refresh(user)
        action = Action(time=user.updated_at, user_id=user.id, action_type=ActionType.UPDATE_PROFILE)
        db_session.add(action)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(status_code=400, detail=f"Problem with updating user information\nError: {e}")
    return UserDTO.model_validate(user)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db_session: DBSession):
    """Delete a user from database
    
    Args:
        user_id (int): The Telegram ID of the user to delete.
        db_session (DBSession): The database session.
        
    Raises:
        HTTPException: If the user is not found.
    """
    query = select(User).where(User.telegram_id == user_id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        await db_session.delete(user)
        await db_session.commit()
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
