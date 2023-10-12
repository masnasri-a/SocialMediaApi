from datetime import datetime, timedelta
import hashlib

from config.mongo import mongo_client


def create_client(body:dict):
    client_id = hashlib.sha256(str(body).encode()).hexdigest()
    created_at = datetime.now()
    role = "TRIAL"
    expired_at = datetime.now() + timedelta(days=1)
    client, collection = mongo_client()
    # with client:
    #     collection