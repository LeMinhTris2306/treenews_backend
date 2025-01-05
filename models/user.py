from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

import json
from pydantic import model_validator
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr = Field(...)
    password: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    userType: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "leelai@gmail.com",
                "password": "LeeLai123",
                "firstName": "Lai",
                "lastName": "Lê Trần Đình",
                "userType": "Reader",
            }
        },
    )
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UpdateUserModel(BaseModel):
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    userType: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "password": "LeeLai123",
                "firstName": "Lai",
                "lastName": "Lê Trần Đình",
                "userType": "Reader"
            }
        },
    )

class UserCollection(BaseModel):
    users: List[UserModel]