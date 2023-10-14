import hashlib
import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.service.client.manage_role import manage_role
from src.model.client import LoginClientModel, RoleEnum
from src.service.client.login_client import login_client_service
from src.service.client import create_client_sevice
from src.model import ClientModel
from src.util import create_access_token
from src.util.security import create_refresh_token, oauth2_scheme, validate_token

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
            raise HTTPException(401, "Unatuhorize")
        del data['password']
        del data['created_at']
        del data['expired_at']
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        return {
            "access_token":access_token,
            "refresh_token":refresh_token,
            "client_id":data.get('_id')
        }
    except HTTPException as http_exception:
        raise http_exception
    except:
        traceback.print_exc()
        return None

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    password = hashlib.sha256(form_data.password.encode()).hexdigest()
    print(password)
    data = login_client_service({"username":form_data.username, "password":password})
    print(data)
    if type(data) != dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    del data['password']
    del data['created_at']
    del data['expired_at']
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {
        "access_token":access_token,
        "token_type":"bearer",
        "refresh_token":refresh_token,
        "client_id":data.get('_id')
    }
    # return {"access_token": access_token, "token_type": "bearer"}


@app.put("/manage_role")
def manage_roles(client_id:str,role:RoleEnum,token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload:dict = validate_token(token)
        # client_id = payload.get("_id")
        if 'SUPER_ADMIN' not in payload.get('role'):
            raise HTTPException(403, "Only Super Admin can change a user role")
        manage_role(client_id=client_id,role=role.value)
        return {
            "message":"Success"
        }        
        # validate_token(token)
    except HTTPException as e:
        raise e