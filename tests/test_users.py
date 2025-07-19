import pytest
import jwt
from app import schemas
from app.config import settings
# from .database import client, session

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hi new user in docker bind mount'
#     assert res.status_code == 200 

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "tester@g.com", "password": "pwd123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "tester@g.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'

@pytest.mark.parametrize("data, status_code", [
    ({"username": "wrongemail@gm.com", "password": "password123"}, 403),
    ({"username": "tester@g.com", "password": "wrongpwd"}, 403),
    ({"username": "wrongemail@gm.com", "password": "wrongpwd"}, 403),
    ({"password": "password123"}, 422),  # username missing
    ({"username": "tester@g.com"}, 422),  # password missing
])
def test_incorrect_login(test_user, client, data, status_code):
    res = client.post("/login", data=data)
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"