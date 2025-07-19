from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

nonexistent_post_id = 17346897635876328576982376


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DTB_USERNAME}:{settings.DTB_PWD}@{settings.DTB_HOSTNAME}/{settings.DTB_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
# return the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
# return just the client response
    # run following code BEFORE running the test below
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # run any following code AFTER the test below

@pytest.fixture
def test_2nd_user(client):
    user_data = {"email": "secondtester2@g.com", 
                 "password": "pwd123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    print(res.json())

    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "tester@g.com", 
                 "password": "pwd123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    print(res.json())

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_2nd_user):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id" : test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id" : test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id" : test_2nd_user['id']
    }]

    def create_post_model(post_input):
        return models.Post(**post_input)
    
    post_map = map(create_post_model, posts_data)
    post_list = list(post_map)

    session.add_all(post_list)
    session.commit()

    posts = session.query(models.Post).all()
    return posts