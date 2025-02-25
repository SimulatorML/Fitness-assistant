import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(os.environ.get('DATABASE_URL'))
session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
