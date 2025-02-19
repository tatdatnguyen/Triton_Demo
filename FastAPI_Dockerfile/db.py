from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

class Inference(Document):
    timestamp: datetime
    input_texts: list[str]
    predicted_labels: list[str]

    class Settings:
        collection = "inferences" 

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")  
    db = client["inference_db"]  
    await init_beanie(database=db, document_models=[Inference])

async def save_inference(input_texts, predicted_labels):
    inference_record = Inference(
        timestamp=datetime.utcnow(),
        input_texts=input_texts,
        predicted_labels=predicted_labels
    )
    await inference_record.insert()  

async def get_inferences():
    return await Inference.find_all().to_list()

async def drop_inferences_collection():
    await Inference.delete_all()

