# tests/test_onboarding.py

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from datetime import datetime


@pytest.mark.asyncio
async def test_create_and_delete_user(db_session: AsyncSession):
    """Test onboarding with mock ID - create and delete user."""
    telegram_id = 1234567890 

    user = User(
        telegram_id=telegram_id,
        name="Test User",
        height=180,
        weight=75.0,
        birth_date=datetime(1990, 1, 1),
        gender="male",
        activity_level="moderate",
        goal="health",
        health_restrictions="none",
        preferred_activities="swimming",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.telegram_id == telegram_id

    # Cleanup
    await db_session.delete(user)
    await db_session.commit()

    deleted = await db_session.get(User, user.id)
    assert deleted is None
