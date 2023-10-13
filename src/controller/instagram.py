import json
from fastapi import APIRouter, HTTPException

from src.service.instagram.profile import Instagram
from src.util.validator import validate_client

app = APIRouter(prefix="/instagram")

@app.get("/profile")
def get_profile(username:str, client_id:str):
    try:
        if validate_client(client_id) is False:
            raise HTTPException(status_code=403, detail={"client id not valid"})
        data = Instagram.scrap(username, None)
        if type(data) == str:
            return json.loads(data)
    except HTTPException as http_e:
        raise http_e