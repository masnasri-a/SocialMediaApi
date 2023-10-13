import traceback
from fastapi import APIRouter, HTTPException
from src.model.client import LoginClientModel
from src.service.client.login_client import login_client_service
from src.service.client import create_client_sevice
from src.model import ClientModel

app = APIRouter(prefix="/client")

@app.post("/register")
def create(body: ClientModel):
    try:
        create_client_sevice(body.model_dump())
        raise HTTPException(status_code=201, detail="Account has been created!!")
    except HTTPException as http_exception:
        raise http_exception
    
@app.post("/login")
def get(body: LoginClientModel):
    try:
        data = login_client_service(body.model_dump())
        if type(data) != dict:
            raise data
        del data['password']
        return data
    except HTTPException as http_exception:
        raise http_exception
    except:
        traceback.print_exc()
        print()

