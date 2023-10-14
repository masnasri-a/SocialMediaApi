from enum import Enum
import hashlib
from pydantic import BaseModel, Field, EmailStr, validator

class RoleEnum(Enum):
    TRIAL = "TRIAL"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"

    SUPER_ADMIN = "SUPER_ADMIN"

class ClientModel(BaseModel):
    username:str = Field(..., examples=["nasri"])
    full_name:str = Field(..., examples=["Nasri Adzlani"])
    email: EmailStr
    password:str = Field(..., examples=['rahasia'])

    @validator("password")
    def hash_password(cls, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
class LoginClientModel(BaseModel):
    username: str = Field(..., examples=["nasri"])
    password:str = Field(..., examples=['rahasia'])

    @validator("password")
    def hash_password(cls, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password