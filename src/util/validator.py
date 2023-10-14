
from datetime import datetime
from fastapi import HTTPException
from src.config.mongo import mongo_client


def validate_client(client_id:str = None, email:str = None):
    client, collection = mongo_client()
    with client:
        temp = {}
        if client_id != None:
            print('client_id',client_id)
            temp['client_id'] = client_id
        elif email != None:
            print('email',email)
            temp['email'] = email
        print(temp)
        result = collection.find_one(temp)

        if result:
            return True
    return False

def validator_expired(client_id):
    client, collection = mongo_client()
    with client:
        data = collection.find_one({'_id':client_id})
        if data is None:
            raise HTTPException(status_code=400, detail="invalid client id")
        role = data.get('role')
        if 'TRIAL' in role:
            date_obj = data.get('expired_at')
            if date_obj < datetime.now():
                raise HTTPException(status_code=403, detail="Client Id Has Expired")
        return role
