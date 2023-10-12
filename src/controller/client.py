from fastapi import APIRouter
from src.model import ClientModel
app = APIRouter(prefix="/client")

@app.post("/")
def create(body: ClientModel):
    return body.model_dump()