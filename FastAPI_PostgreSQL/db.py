from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, String, ARRAY
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://sqldemo:abc123@localhost/inference_db"

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Inference(Base):
    __tablename__ = "inferences"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_texts = Column(ARRAY(String))
    predicted_labels = Column(ARRAY(String))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_inference(input_texts: List[str], predicted_labels: List[str]):
    async with AsyncSessionLocal() as session:
        inference_record = Inference(
            input_texts=input_texts,
            predicted_labels=predicted_labels
        )
        session.add(inference_record)
        await session.commit()



async def get_inferences():
    async with AsyncSessionLocal() as session:
        # Use text() to wrap the SQL query
        result = await session.execute(text("SELECT * FROM inferences"))
        return result.fetchall()


async def get_all_inferences():
    try:
        inferences = await get_inferences()
        if inferences:
            # Check what type the rows are before accessing _mapping
            return {"inferences": [row._asdict() for row in inferences]}
        else:
            raise HTTPException(status_code=404, detail="No inferences found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def drop_inferences_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)