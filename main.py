#tutorial: https://github.com/mongodb-developer/mongodb-with-fastapi/blob/master/app.py
#fastapi import
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

#routers import
from API import *

import os, shutil
from typing import List, Optional

from pydantic import BaseModel, model_validator, Field
from pydantic.functional_validators import BeforeValidator
import json
from typing_extensions import Annotated

app = FastAPI()

UPLOAD_FOLDER = './assets/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc bạn có thể chỉ định các nguồn (URLs) được phép
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(category_router, prefix="/category", tags=["categories"])
app.include_router(article_router, prefix="/article", tags=["articles"])
app.include_router(comment_router, prefix="/comment", tags=["comments"])

PyObjectId = Annotated[str, BeforeValidator(str)]

class Base(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    point: Optional[float] = None
    is_accepted: Optional[bool] = False

# Tạo route cho trang chủ
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post(
    "/upload", 
    response_model=Base,
)
async def upload_files(data: Base = Body(...), files: List[UploadFile] = File(...)):
    return {"JSON Payload": data, "Filenames": [file.filename for file in files]}