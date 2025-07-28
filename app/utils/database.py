from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings

# engine = create_engine(DATABASE)
engine = create_async_engine(settings.database, echo=False) #change to True for debugging

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
