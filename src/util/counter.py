from datetime import datetime, timedelta
import traceback
from fastapi import HTTPException
from redis.exceptions import ConnectionError
from src.model.client import RoleEnum
from src.config import redis_client
from src.util.validator import validator_expired

def get_midnight_timedelta():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
    return (midnight - now).total_seconds()

def time_by_role(role:str):
    if role == RoleEnum.TRIAL: return 10
    if role == RoleEnum.BASIC: return 100
    if role == RoleEnum.PREMIUM: return 1000
    return 10**100

def role_counter(client_id:str):
    try:
        role = validator_expired(client_id=client_id)
        counter_id = f'client-counter:{client_id}'
        red = redis_client(db=1)
        with red:
            count = red.get(counter_id)
            if count is None:
                red.setex(counter_id,int(get_midnight_timedelta()),1)
            else:
                current_count = int(count)
                if current_count >= time_by_role(role=role):
                    raise HTTPException(status_code=429, detail="Request has been limited")
                else:
                    current_count += 1
                    red.setex(counter_id,int(get_midnight_timedelta()), current_count)
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail="Redis has broken")

        