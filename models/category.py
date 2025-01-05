from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]

class CategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    categoryName: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "categoryName": "Thể thao trong nước"
            }
        },
    )
    
class UpdateCategoryModel(BaseModel):
    categoryName: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "categoryName": "Thể thao trong nước"
            }
        },
    )

class CategoryCollection(BaseModel):
    categories: List[CategoryModel]