import json
from fastapi import APIRouter, HTTPException, Request
from pydantic import Field

from src.service.instagram.profile import Instagram
from src.util.validator import validate_client, validator_expired
from src.util.counter import role_counter

app = APIRouter(prefix="/instagram")

@app.get("/profile")
def get_profile(username:str, client_id:str):
    try:
        role_counter(client_id)
        data = Instagram.scrap(username, None)
        if type(data) == str:
            data_loads = json.loads(data)
            del data_loads['edge_felix_video_timeline']
            del data_loads['edge_owner_to_timeline_media']
            del data_loads['edge_saved_media']
            return data_loads
    except HTTPException as http_e:
        raise http_e
    

@app.get("/posts")
def get_post_info(short_code:str, username:str, client_id:str):
    try:
        role_counter(client_id)
        data = Instagram.posts(short_code=short_code,username=username)
        if type(data) == str:
            return json.loads(data)
    except HTTPException as http_e:
        raise http_e
    