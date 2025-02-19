from fastapi import FastAPI, HTTPException
import uvicorn
import aiohttp
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from models import InferRequest
from db import save_inference, get_inferences, drop_inferences_collection, init_db

app = FastAPI()

# 🔹 Prometheus Metrics
REQUEST_COUNT = Counter(
    "infer_requests_total", "Total number of requests to /infer"
)

LATENCY_HISTOGRAM = Histogram(
    "infer_request_latency_seconds",
    "Latency of /infer requests in seconds",
    buckets=[0.01, 0.05, 0.075, 0.1, 0.5, 1, 5]  # Custom latency buckets
)

@app.on_event("startup")
async def startup_event():
    await init_db() 

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/infer")
async def infer(request: InferRequest):
    REQUEST_COUNT.inc()  # 🔹 Increase request count metric

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

    start_time = time.time()  # 🔹 Start timing

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()

                if "outputs" in result:
                    predicted_labels = result["outputs"][0]["data"]

                    # Save input and output to MongoDB
                    await save_inference(request.texts, predicted_labels)

                    return {"predictions": predicted_labels}
                else:
                    raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        latency = time.time() - start_time
        LATENCY_HISTOGRAM.observe(latency)  # 🔹 Record latency properly


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/dbshow")
async def get_all_inferences():
    try:
        inferences = await get_inferences()
        if inferences:
            return {"inferences": inferences}
        else:
            raise HTTPException(status_code=404, detail="No inferences found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/reset_inferences")
async def reset_inferences():
    try:
        await drop_inferences_collection()
        return {"status": "inferences collection dropped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
