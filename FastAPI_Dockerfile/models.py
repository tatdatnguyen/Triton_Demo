from pydantic import BaseModel

class InferRequest(BaseModel):
    texts: list[str]
