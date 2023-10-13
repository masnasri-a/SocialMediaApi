
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