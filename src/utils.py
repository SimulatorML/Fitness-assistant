from datetime import datetime
from sqlalchemy import select
from src.database.models.user import User
from sqlalchemy.orm import Session

def calculate_age(birth_date: datetime) -> int:
    """Calculate the age based on the birth date.
    
    Args:
        birth_date (datetime): The birth date of the user.
    
    Returns:
        int: The age of the user.
    """
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

async def get_user(telegram_id: int, db_session: Session) -> User | None:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db_session.execute(query)
    return result.scalar_one_or_none()
