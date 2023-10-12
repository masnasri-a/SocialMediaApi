import hashlib
from pydantic import BaseModel, Field, EmailStr, validator

class ClientModel(BaseModel):
    full_name:str = Field(..., examples=["Nasri Adzlani"])
    email: EmailStr
    password:str = Field(..., examples=['rahasia'])
    
    @validator("password")
    def hash_password(cls, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password