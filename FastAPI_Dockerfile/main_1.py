from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import requests

app = FastAPI()

class InferRequest(BaseModel):
    texts: list[str]    
    

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

# @app.post("/infer")
# def infer(request: InferRequest):
#     url = "http://localhost:8000/v2/models/bert/infer"
#     payload = {
#         "inputs": [
#             {
#                 "name": "text_input",
#                 "shape": [len(request.texts)],  # Dynamic batch size
#                 "datatype": "BYTES",
#                 "data": request.texts
#             }
#         ],
#         "outputs": [{"name": "output"}]
#     }
#     try:
#         response = requests.post(url, json=payload)
#         result = response.json()
        
#         if "outputs" in result:
#             predicted_labels = result["outputs"][0]["data"]
#             return {"predictions": predicted_labels}
#         else:
#             raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/infer")
async def infer(request: InferRequest):
    url = "http://localhost:8000/v2/models/bert/infer"
    payload = {
        "inputs": [
            {
                "name": "text_input",
                "shape": [len(request.texts)],  # Dynamic batch size
                "datatype": "BYTES",
                "data": request.texts
            }
        ],
        "outputs": [{"name": "output"}]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                
                if "outputs" in result:
                    predicted_labels = result["outputs"][0]["data"]
                    return {"predictions": predicted_labels}
                else:
                    raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
