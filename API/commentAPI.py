from mongodb import mongodb
from pymongo import ReturnDocument
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from models.comment import *
from utils.utils import day_compare

router = APIRouter()

comment_collection = mongodb.create_connection('comments')
article_collection = mongodb.create_connection('article')

@router.post(
    "/",
    response_description="Add new comment",
    response_model=CommentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
async def create_comment(comment: CommentModel = Body(...)):
    """
        Thêm 1 comment, vì 1 comment có thể thêm nhiều comment (hoặc spam, cái này sẽ thêm comment time limit sau) nên sẽ không check comment tồn tại
    """
    comment_info = comment.model_dump(by_alias=True, exclude=["id"])
    articleId = comment_info['articleId']
    if (article:= article_collection.find_one({"_id": ObjectId(articleId)})) is None:
        raise HTTPException(status_code=404, detail=f"Article {articleId} not found")

    new_comment = comment_collection.insert_one(
        comment_info
    )
    created_comment = comment_collection.find_one(
        {"_id": new_comment.inserted_id}
    )
    return created_comment

@router.get(
    "/",
    response_description="List all comments of a article",
    response_model=CommentCollection,
    response_model_by_alias=False,
)
async def get_list_comments(articleId: str):
    """
        Liệt kê tất cả comment của 1 bài báo
    """
    comments = comment_collection.find({"articleId": articleId}).to_list(100)
    return CommentCollection(comments=comments)

@router.get(
    "/{id}",
    response_description="Get a single comment",
    response_model=CommentModel,
    response_model_by_alias=False,
)
async def show_comment(id: str):
    """
        Get the record for a specific comment, looked up by `id`.
    """
    if (
        comment := comment_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return comment

    raise HTTPException(status_code=404, detail=f"Comment {id} not found")

@router.put(
    "/{id}",
    response_description="Update a comment",
    response_model=CommentModel,
    response_model_by_alias=False
)
async def update_comment(id: str, comment: UpdateCommentModel = Body(...)):
    comment_update_detail = {
        k: v for k, v in comment.model_dump(by_alias=True).items() if v is not None
    }
    update_day = comment_update_detail['updateDay']
    comment_day = comment_update_detail['commentDay']
    
    if day_compare(update_day, comment_day) is False:
        raise HTTPException(status_code=422, detail=f"Update day must be greater than comment day")
    
    if len(comment_update_detail) >= 1:
        update_result = comment_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": comment_update_detail},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Comment {id} not found")
        
@router.delete("/{id}", response_description="Delete a comment")
async def delete_comment(id: str):
    """
    Remove a single comment record from the database.
    """
    delete_result = comment_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"comment {id} not found")

