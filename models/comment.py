from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]

class CommentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    articleId: str = Field(description="Id bài báo được comment")
    comment: str = Field(...)
    user: str = Field(description="Id người dùng đã comment")
    commentDay: str = Field(description="Ngày bình luận")
    updateDay: Optional[str] = Field(None, description="Ngày chỉnh sửa bình luận")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "articleId": "6777e2fdb12df6ecc4290d11",
                "comment": "Tin chuẩn",
                "user": "6774a2d280abb73a62197ae4",
                "commentDay": "01/01/2025",
                "updateDay": ""
            }
        },
    )

class UpdateCommentModel(BaseModel):
    articleId: Optional[str] = None
    comment: Optional[str] = None
    user: Optional[str] = None
    commentDay: Optional[str] = None
    updateDay: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "articleId": "6777e2fdb12df6ecc4290d11",
                "comment": "Tin không chuẩn",
                "user": "6774a2d280abb73a62197ae4",
                "commentDay": "01/01/2025",
                "updateDay": "02/01/2025"
            }
        },
    )

class CommentCollection(BaseModel):
    comments: List[CommentModel]