from datetime import datetime, timedelta
import hashlib

from fastapi import HTTPException

from src.config.mongo import mongo_client
from src.util import validate_client


def create_client_sevice(body:dict):
    client_id = hashlib.sha256(str(body).encode()).hexdigest()
    created_at = datetime.now()
    role = "TRIAL"
    expired_at = datetime.now() + timedelta(days=7)
    client, collection = mongo_client()
    emails = body.get('email')
    if validate_client(None, emails):
        raise HTTPException(status_code=409, detail="Email Already Registered")
    bodies = {
        "_id":client_id,
        **body,
        "role":role,
        "created_at":created_at,
        "expired_at":expired_at
    }
    with client:
        collection.insert_one(bodies)
    raise HTTPException(status_code=201, detail="Account Successfully Created")