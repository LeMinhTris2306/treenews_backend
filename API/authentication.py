from mongodb import mongodb
from pymongo import ReturnDocument
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from models.user import *

router = APIRouter()
user_collection = mongodb.create_connection('users')

class AuthModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

@router.post(
    "/",
    response_model=UserModel,
    response_description="User authentication for login",
)
async def login(data: AuthModel):
    login_info = data.model_dump(by_alias=True)

    user = user_collection.find_one({"email": login_info['email'], "password": login_info['password']})
    if user is None:
        raise HTTPException(status_code=401, detail=f"User not found")
    
    return user

