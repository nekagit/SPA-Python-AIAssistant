from utils import config
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import main


# Initialize async SQLAlchemy
engine = create_async_engine(config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


# Dependency to get the async session for each request
async def get_db():
    async with SessionLocal() as session:
        yield session
