


import traceback
from fastapi import HTTPException
from src.config.mongo import mongo_client


def login_client_service(body:dict):
    try:
        client, collection = mongo_client()
        with client:
            data = collection.find_one(body)
            if data is None:
                return HTTPException(status_code=401, detail={
                    "msg": "Failed Authentication"
                })
            return data
    except:
        traceback.print_exc()