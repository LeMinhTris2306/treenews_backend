from requests import get, post, put, delete, HTTPError
from pathlib import Path
import json, os

def test_article_api():
    """
        Test both article` and its comments
    """
    article_root = "http://localhost:8000/article/"
    comment_root = "http://localhost:8000/comment/"
    server_path = r"D:\Python\server_storage"
    
    article_detail = [
        {
            "context": "ĐT Việt Nam cần đặc biệt dè chừng những cá nhân sắc bén của Thái Lan ở trận chung kết lượt về.",
            "img": {
                "imgName": "cailauthai.jpg",
                "imgTitle": "Suphanat là vũ khí cực nguy hiểm ở trận lượt về (Ảnh: FAT)"
            }
        }
    ]

    files = {
        'article': (None, '{"authorId":"674869091328903d9b56a0a9","categoryId":"6748701d1328903d9b56a0bb","detail":[{"context":"ĐT Việt Nam cần đặc biệt dè chừng những cá nhân sắc bén của Thái Lan ở trận chung kết lượt về.","img":{"imgName":"cailauthai.jpg","imgTitle":"Suphanat là vũ khí cực nguy hiểm ở trận lượt về (Ảnh: FAT)"}}],"displayName":"hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan","title":"HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái La4 n","uploadDay":"01/01/2025"}'),
        'files': ('D:/Python/treenews_backend/assets/images/cailauthai.jpg', open('D:/Python/treenews_backend/assets/images/cailauthai.jpg', 'rb'), 'image/jpeg'),
    }
    try:
        # Insert a article with img
        response = post(article_root, files=files, headers={'accept': 'application/json'})
        response.raise_for_status()
        doc = response.json()
        inserted_article_id = doc['Article']["id"]
        
        path = Path(os.path.join(server_path, "674869091328903d9b56a0a9", inserted_article_id))
        inserted_files = []
        for img_path in os.listdir(path):
            inserted_files.append(img_path)
        
        print(f"Inserted document with id: {inserted_article_id}")
        print(
            "If the test fails in the middle you may want to manually remove the document."
        )
        assert doc['Article']["authorId"] == "674869091328903d9b56a0a9"
        assert doc['Article']["categoryId"] == "6748701d1328903d9b56a0bb"
        assert doc['Article']["detail"] == article_detail
        assert doc['Article']["displayName"] == "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan"
        assert doc['Article']["title"] == "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái La4 n"
        assert doc['Article']["uploadDay"] == "01/01/2025"
        assert all(filename in doc['Filenames'] for filename in inserted_files)
        
        
        # List article and ensure it's present
        response = get(article_root, params={'n': "4"})
        response.raise_for_status()
        article_ids = {s["id"] for s in response.json()["articles"]}
        assert inserted_article_id in article_ids

        # Get individual article doc
        response = get(article_root + inserted_article_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["authorId"] == "674869091328903d9b56a0a9"
        assert doc["categoryId"] == "6748701d1328903d9b56a0bb"
        assert doc["detail"] == article_detail
        assert doc["displayName"] == "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan"
        assert doc["title"] == "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái La4 n"
        assert doc["uploadDay"] == "01/01/2025"
        
        # Update the article doc
        new_article_detail = [
            {
                "context": "Thailan ton luoi",
                "img": {
                    "imgName": "cailauthai.jpg",
                    "imgTitle": "Suphanat là vũ khí cực nguy hiểm ở trận lượt về (Ảnh: FAT)"
                }
            }
        ]
        new_files = {
            'article': (None, '{"authorId":"674869091328903d9b56a0a9","categoryId":"6748701d1328903d9b56a0bb","detail":[{"context":"Thailan ton luoi","img":{"imgName":"cailauthai.jpg","imgTitle":"Suphanat là vũ khí cực nguy hiểm ở trận lượt về (Ảnh: FAT)"}}],"displayName":"hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan","title":"HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái Lan","uploadDay":"31/12/2024"}'),
            'files': ('D:/Python/treenews_backend/assets/images/cailauthai.jpg', open('D:/Python/treenews_backend/assets/images/cailauthai.jpg', 'rb'), 'image/jpeg'),
        }
        response = put(
            article_root + inserted_article_id,
            files=new_files,
            params={"id": inserted_article_id}
        )
        response.raise_for_status()
        doc = response.json()
        assert doc['Article']["authorId"] == "674869091328903d9b56a0a9"
        assert doc['Article']["categoryId"] == "6748701d1328903d9b56a0bb"
        assert doc['Article']["detail"] == new_article_detail
        assert doc['Article']["displayName"] == "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan"
        assert doc['Article']["title"] == "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái Lan"
        assert doc['Article']["uploadDay"] == "31/12/2024"

        # Get the article doc and check for change
        response = get(article_root + inserted_article_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["authorId"] == "674869091328903d9b56a0a9"
        assert doc["categoryId"] == "6748701d1328903d9b56a0bb"
        assert doc["detail"] == new_article_detail
        assert doc["displayName"] == "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan"
        assert doc["title"] == "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái Lan"
        assert doc["uploadDay"] == "31/12/2024"

        #<=================== comment test =======================>
        #create comment for above article
        comment = {
            "articleId": inserted_article_id,
            "comment": "Tin chuẩn",
            "user": "6774a2d280abb73a62197ae4",
            "commentDay": "01/01/2025",
            "updateDay": ""
        }
        response = post(comment_root, json=comment)
        response.raise_for_status()
        doc = response.json()
        inserted_comment_id = doc["id"]
        print(f"Inserted document with id: {inserted_comment_id}")
        print(
            "If the test fails in the middle you may want to manually remove the document."
        )
        assert doc["articleId"] == inserted_article_id
        assert doc["comment"] == "Tin chuẩn"
        assert doc["user"] == "6774a2d280abb73a62197ae4"
        assert doc["commentDay"] == "01/01/2025"
        assert doc["updateDay"] == ""

        # List comments and ensure it's present
        response = get(comment_root, headers = {'accept': 'application/json'}, params={"articleId": inserted_article_id})
        response.raise_for_status()
        comment_ids = {s["id"] for s in response.json()["comments"]}
        assert inserted_comment_id in comment_ids

        # Get individual comment doc
        response = get(comment_root + inserted_comment_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_comment_id
        assert doc["articleId"] == inserted_article_id
        assert doc["comment"] == "Tin chuẩn"
        assert doc["user"] == "6774a2d280abb73a62197ae4"
        assert doc["commentDay"] == "01/01/2025"
        assert doc["updateDay"] == ""

        # Update the comment doc
        response = put(
            comment_root + inserted_comment_id,
            json={
                "comment": "Tin chuẩn chưa anh",
                "commentDay": "01/01/2025",
                "updateDay": "02/01/2025"
            },
        )
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_comment_id
        assert doc["articleId"] == inserted_article_id
        assert doc["comment"] == "Tin chuẩn chưa anh"
        assert doc["user"] == "6774a2d280abb73a62197ae4"
        assert doc["commentDay"] == "01/01/2025"
        assert doc["updateDay"] == "02/01/2025"

        # Get the comment and check for change
        response = get(comment_root + inserted_comment_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_comment_id
        assert doc["articleId"] == inserted_article_id
        assert doc["comment"] == "Tin chuẩn chưa anh"
        assert doc["user"] == "6774a2d280abb73a62197ae4"
        assert doc["commentDay"] == "01/01/2025"
        assert doc["updateDay"] == "02/01/2025"

        # Delete article
        response = delete(article_root + inserted_article_id)
        response.raise_for_status()

        # Get the doc and ensure it's been deleted
        response = get(article_root + inserted_comment_id)
        assert response.status_code == 404
        #Check if article's comments have been deleted
        response = get(comment_root + inserted_comment_id)
        assert response.status_code == 404
    except HTTPError as he:
        print(he.response.json())
        raise