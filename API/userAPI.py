from mongodb import mongodb
from pymongo import ReturnDocument
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from models.user import *

router = APIRouter()
user_collection = mongodb.create_connection('users')

@router.post(
    "/",
    response_description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
async def create_user(user: UserModel = Body(...)):
    user_info = user.model_dump(by_alias=True, exclude=["id"])

    user_exists = user_collection.find_one({"email": user_info['email']})
    if user_exists is not None:
        raise HTTPException(status_code=409, detail=f"Email {user_info['email']} exists")
    
    new_user = user_collection.insert_one(
        user_info
    )
    created_user = user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.get(
    "/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def get_list_users():
    users = user_collection.find().to_list(100)
    return UserCollection(users=users)

@router.get(
    "/{id}",
    response_description="Get a single user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (
        user := user_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"user {id} not found")

@router.put(
    "/{id}",
    response_description="Update a user",
    response_model=UserModel,
    response_model_by_alias=False
)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    try:
        user.pop('email', None)
    except:
        pass
    
    if len(user) >= 1:
        update_result = user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")
        
@router.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    """
    Remove a single user record from the database.
    """
    delete_result = user_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
