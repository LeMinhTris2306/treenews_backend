from mongodb import mongodb
from pymongo import ReturnDocument
from fastapi import APIRouter, Body, HTTPException, status, UploadFile, File
from fastapi.responses import Response
from models.article import *

import os, shutil

router = APIRouter()
cat_collection = mongodb.create_connection('categories')
user_collection = mongodb.create_connection('user')
article_collection = mongodb.create_connection('article')
comment_collection = mongodb.create_connection('comments')

server_storage_path = r"D:\Python\server_storage"

class ResponseModel(BaseModel):
    Article: ArticleModel = Field(...)
    Filenames: Optional[List[str]] = Field(None)

@router.post(
    "/",
    response_description="Add new article",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False
)
async def create_article(article: ArticleModel = Body(...), files: List[UploadFile] = File(None, description="Thông tin hình ảnh đi kèm")):
    """
        hàm này sẽ lưu thông tin bài báo trước, sau đó lấy objID để tạo thư mục với tên objID và lưu ảnh vào đấy
    """
    article_info = article.model_dump(by_alias=True, exclude=["id"])
    authorId = article_info['authorId']

    if (article := article_collection.find_one({"title": article_info.get('title')})) is not None:
        raise HTTPException(status_code=409, detail=f"Tựa đề {article_info.get('title')} đã được dùng")

    new_article = article_collection.insert_one(article_info)

    article_assets_path = os.path.join(server_storage_path, authorId, str(new_article.inserted_id))
    os.makedirs(article_assets_path, exist_ok=True)
    
    try:
        for file in files:
            file_location = os.path.join(article_assets_path, file.filename)
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Có lỗi khi upload ảnh, lỗi: {e}")
    
    inserted_article = article_collection.find_one({
        "_id": new_article.inserted_id
    })
    
    return {
        "Article": inserted_article,
        "Filenames": [file.filename for file in files]
    }

@router.get(
    "/",
    response_description="get a list number of articles",
    response_model=ArticleCollection,
    response_model_by_alias=False,
)
async def get_list_articles(n: int):
    """
    Tìm n số bài báo
    """
    articles = article_collection.find().to_list(n)
    return ArticleCollection(articles=articles)

@router.get(
    "/{id}",
    response_description="Get a single article",
    response_model=ArticleModel,
    response_model_by_alias=False,
)
async def show_article(id: str):
    """
    tìm 1 bài báo cụ thể theo id của bài báo
    """
    if (
        article := article_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return article

    raise HTTPException(status_code=404, detail=f"Không tìm thấy bài báo {id}")


@router.put(
    "/{id}",
    response_description="Update a category",
    response_model=ResponseModel,
    response_model_by_alias=False
)
async def update_article(id: str, article: UpdateArticleModel = Body(...), files: Optional[List[UploadFile]] = File(None, description="Thông tin hình ảnh đi kèm")):
    article = {
        k: v for k, v in article.model_dump(by_alias=True).items() if v is not None
    }
    
    if len(article) >= 1:
        article_title = article['title']
        if (existed_article := article_collection.find_one({"title": article_title})) is not None:
            raise HTTPException(status_code=409, detail=f"Tựa đề {article_title} đã được dùng")
        update_result = article_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": article},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            article_assets_path = os.path.join(server_storage_path, update_result["authorId"], id)
            if files is not None:
                #Xóa tất cả các file trước khi cập nhật
                try:
                    for filename in os.listdir(article_assets_path):
                        file_path = os.path.join(article_assets_path, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    #Cập nhật file mới
                    for file in files:
                        file_location = os.path.join(article_assets_path, file.filename)
                        with open(file_location, "wb") as buffer:
                            shutil.copyfileobj(file.file, buffer)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"error: {e}")
            
            return {"Article": update_result, "Filenames": [file.filename for file in files]}
        else:
            raise HTTPException(status_code=404, detail=f"Article {id} not found")
        
    

        
@router.delete("/{id}", response_description="Delete a article")
async def delete_article(id: str):
    """
        Xóa 1 bài báo bằng id, bao gồm comment và thư mục chứa file
    """
    article = article_collection.find_one({"_id": ObjectId(id)})

    if article is not None:
        article_collection.delete_one({"_id": ObjectId(id)})
        comment_collection.delete_many({"articleId": id})
        try:
            shutil.rmtree(os.path.join(server_storage_path, article["authorId"], id))
        except:
            pass
        return Response(status_code=status.HTTP_204_NO_CONTENT)        

    raise HTTPException(status_code=404, detail=f"category {id} not found")