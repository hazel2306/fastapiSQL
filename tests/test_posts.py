import pytest 
from app import schemas
from .conftest import nonexistent_post_id

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(posts):
        return schemas.PostOut(**posts)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id

def test_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    # def validate(posts):
    #     return schemas.PostOut(**posts)
    
    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)

    # assert len(res.json()) == len(test_posts)
    # assert res.status_code == 200

def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{nonexistent_post_id}")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("first ever title", "very informative content", True),
    ("2nd ever title", "more informative content", False),
    ("still a title", "still so cool content", False),
    ("still a title", "very informative content", True),
])

def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts", json={"title": "title", "content": "content"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "title", "content": "content"})
    assert res.status_code == 401

def test_unathorized_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_successful_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_nonexistent_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{nonexistent_post_id}")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    new_post = {
        "title": "new title",
        "content": "new content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}",
                                json = new_post)

    assert res.status_code == 200
    updated_post = schemas.Post(**res.json())

    assert updated_post.title == new_post['title']
    assert updated_post.content == new_post['content']

def test_update_other_user_post(authorized_client, test_user, test_2nd_user, test_posts):
    new_post = {
        "title": "new title",
        "content": "new content",
        "id" : test_posts[2].id
    }
    res = authorized_client.put(f"/posts/{test_posts[2].id}",
                                json = new_post)
    assert res.status_code == 403

def test_unathorized_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_nonexistent_post(authorized_client, test_user, test_posts):
    new_post = {
        "title": "new title",
        "content": "new content",
        "id" : test_posts[2].id
    }
    res = authorized_client.put(
        f"/posts/{nonexistent_post_id}", json=new_post)
    assert res.status_code == 404