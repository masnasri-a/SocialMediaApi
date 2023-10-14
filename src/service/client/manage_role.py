from fastapi import HTTPException
from src.config.mongo import mongo_client


def manage_role(client_id, role):
    try:
        client, collection = mongo_client()
        with client:
            newvalues = { "$set": { "role": role } }
            collection.update_one({"_id":client_id},newvalues)
    except Exception:
        raise HTTPException(500, "Manage Role Database has broken")