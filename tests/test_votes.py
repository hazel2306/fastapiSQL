import pytest
from app import models
from .conftest import nonexistent_post_id


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote=models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_successful_vote(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[2].id, "dir": 1})
    assert res.status_code == 409

def test_successful_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 201

def test_delete_nonexistent_vote(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404

def test_vote_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": nonexistent_post_id, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_vote(client, test_posts):
    res = client.post(
        "/vote/", json={"post_id": test_posts[1].id, "dir": 1})
    assert res.status_code == 401