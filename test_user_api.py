from requests import get, post, put, delete, HTTPError


def test_api():
    """
    copy version of https://github.com/mongodb-developer/mongodb-with-fastapi/blob/master/test_api.py
    """
    user_root = "http://localhost:8000/user/"

    initial_doc = {
            "email": "leelai12@gmail.com",
            "password": "LeeLai123",
            "firstName": "Lai",
            "lastName": "Lê Trần Đình",
            "userType": "Reader"
    }

    try:
        # Insert a student
        response = post(user_root, json=initial_doc)
        response.raise_for_status()
        doc = response.json()
        inserted_id = doc["id"]
        print(f"Inserted document with id: {inserted_id}")
        print(
            "If the test fails in the middle you may want to manually remove the document."
        )
        assert doc["email"] == "leelai12@gmail.com"
        assert doc["password"] == "LeeLai123"
        assert doc["firstName"] == "Lai"
        assert doc["lastName"] == "Lê Trần Đình"
        assert doc["userType"] == "Reader"

        # List users and ensure it's present
        response = get(user_root)
        response.raise_for_status()
        user_ids = {s["id"] for s in response.json()["users"]}
        assert inserted_id in user_ids

        # Get individual student doc
        response = get(user_root + inserted_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["email"] == "leelai12@gmail.com"
        assert doc["password"] == "LeeLai123"
        assert doc["firstName"] == "Lai"
        assert doc["lastName"] == "Lê Trần Đình"
        assert doc["userType"] == "Reader"

        # Update the user doc
        response = put(
            user_root + inserted_id,
            json={
                "password": "ledandinhlai123",
            },
        )
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["email"] == "leelai12@gmail.com"
        assert doc["password"] == "ledandinhlai123"
        assert doc["firstName"] == "Lai"
        assert doc["lastName"] == "Lê Trần Đình"
        assert doc["userType"] == "Reader"

        # Get the user doc and check for change
        response = get(user_root + inserted_id)
        response.raise_for_status()
        doc = response.json()
        assert doc["id"] == inserted_id
        assert doc["email"] == "leelai12@gmail.com"
        assert doc["password"] == "ledandinhlai123"
        assert doc["firstName"] == "Lai"
        assert doc["lastName"] == "Lê Trần Đình"
        assert doc["userType"] == "Reader"

        # Delete the doc
        response = delete(user_root + inserted_id)
        response.raise_for_status()

        # Get the doc and ensure it's been deleted
        response = get(user_root + inserted_id)
        assert response.status_code == 404
    except HTTPError as he:
        print(he.response.json())
        raise