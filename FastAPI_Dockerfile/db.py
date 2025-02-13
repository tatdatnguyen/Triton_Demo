from pymongo import MongoClient
from datetime import datetime

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017")  
db = client["inference_db"]  
collection = db["inferences"]  

def save_inference(input_texts, predicted_labels):
    inference_record = {
        "timestamp": datetime.utcnow(),
        "input_texts": input_texts,
        "predicted_labels": predicted_labels
    }
    collection.insert_one(inference_record)  # Save to MongoDB

def get_inferences():
    # Retrieve inferences from the database
    return list(collection.find({}, {"_id": 0}))  
def drop_inferences_collection():
    # Drop the entire collection (documents + collection itself)
    collection.drop()
