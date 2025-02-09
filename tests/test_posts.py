import pytest
from typing import List
from app import schema


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schema.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = (list(posts_map))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    #assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorize_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorize_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")
    assert res.status_code == 404

# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     print(res.json())
#     post = schema.PostOut(**res.json())
#     assert post.Post.id == test_posts[0].id
#     assert post.Post.content == test_posts[0].content
#     assert post.Post.title == test_posts[0].title

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    #print(res.json())  # ✅ Debug API response

    post = schema.PostOut(**res.json())  # ✅ Ensure response matches schema

    assert post.post.id == test_posts[0].id  # ✅ Correct lowercase `post`
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, publish", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i like food", False),
    ("full house", "cute", True)
])

def test_create_post(authorized_client,test_user, test_posts, title, content, publish):
    #res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "publish": publish})
    #print(res.json())  # Debugging

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.publish == publish
    assert created_post.owner.id == test_user['id']
    
def test_create_post_default_published_true(authorized_client,test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "amaze"})
    #print(res.json())
    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "amaze"
    assert created_post.publish == True
    assert created_post.owner.id == test_user['id']

def test_unauthorize_user_create_posts(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "amaze"})
    #print(res.json())
    assert res.status_code == 401

def test_unauthorize_user_delete_posts(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    print(f"Deleting post with ID: {test_posts[0].id}")
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/30000")
    assert res.status_code == 404
   
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    #assert res.status_code == 404
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorize_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    #print(res.json())
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/30000", json=data)
    #print(res.json())
    assert res.status_code == 404



#     posts_list = (list(posts_map))
#     #print(res.json())
#     #posts = schema.PostOut(res.json())

#     assert len(res.json()) == len(test_posts)
#     assert len(res.json()) == len(test_posts)
#     assert res.status_code == 200
#     #assert posts_list[0].Post.id == test_posts[0].id

# def test_unauthorize_user_get_all_posts(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 404


# def test_unauthorize_user_get_one_posts(client, test_posts):
#     res = client.get("/posts/")
#     assert res.status_code == 404


# def test_get_one_post_not_exist(authorized_client, test_posts):
#      res = authorized_client.get("/posts/8888")
#      assert res.status_code == 404


# def test_get_one_post(authorized_client, test_posts):
#      res = authorized_client.get(f"/posts/{test_posts[0].id}")
#      #print(res.json())
#      post = schema.PostOut(**res.json())
#      assert post.Post.id == test_posts[0].id
#      assert post.Post.content == test_posts[0].content
#      assert post.Post.tittle == test_posts[0].tittle


# @pytest.mark.parametrize("tittle, content, published", [
#     ("awesome new tittle", "awesome new content", True),
#     ("favorite pizza", "i like food", False),
#     ("full house", "cute", True)
# ])


# def test_create_post(authorized_client,test_user, test_posts, tittle, content, published):
#     res = authorized_client.post("/posts/", json={"tittle": tittle, "content": content, "published": published})
#     created_post = schema.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.tittle == tittle
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner.id == test_user['id']


# def test_create_post_default_published_true(authorized_client,test_user, test_posts):
#     res = authorized_client.post("/posts/", json={"tittle": "arbitrary tittle", "content": "amaze"})
#     created_post = schema.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.tittle == "arbitrary tittle"
#     assert created_post.content == "amaze"
#     assert created_post.published == True
#     assert created_post.owner.id == test_user['id']


# def test_unauthorize_user_create_posts(client, test_users, test_posts):
#     res = client.post("/posts/", json={"tittle": "arbitrary tittle", "content": "amaze"})
#     assert res.status_code == 401


# def test_unauthorize_user_delete_posts(client, test_users, test_posts):
#     res = client.delete("/posts/{test_posts[0].id}")
#     assert res.status_code == 401


# def test_delete_post_success(authorized_client, test_users, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204


# def test_delete_post_non_exist(authorized_client, test_users, test_posts):
#     res = authorized_client.delete(f"/posts/30000")
#     assert res.status_code == 404


# def test_delete_other_user_post(authorized_client, test_users, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 404
#     assert res.status_code == 403


# def test_update_post(authorized_client, test_users, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[0].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
#     updated_post = schema.Post(**res.json)
#     assert res.status_code == 200
#     assert updated_post.tittle == data['tittle']
#     assert updated_post.content == data['content']

# def test_update_other_user_post(authorized_client, test_users, test_users2, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[3].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403


# def test_unauthorize_update_posts(client, test_users, test_posts):
#     res = client.put("/posts/{test_posts[0].id}")
#     assert res.status_code == 401


# def test_update_post_non_exist(authorized_client, test_users, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[3].id
#     }

#     res = authorized_client.put(f"/posts/30000", json=data)
#     assert res.status_code == 404





# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get("/posts/")
#     def validate(post):
#         return schema.PostOut(**post)
#     posts_map = map(validate, res.json())
#     posts_list = list(posts_map)

#     assert len(res.json()) == len(test_posts)
#     assert res.status_code == 200

# def test_unauthorize_user_get_all_posts(client, test_posts):
#     res = client.get("/posts/")
#     assert res.status_code == 401  # Fixed: Unauthorized access should return 401

# def test_unauthorize_user_get_one_posts(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401  # Fixed: Unauthorized access should return 401

# def test_get_one_post_not_exist(authorized_client, test_posts):
#     res = authorized_client.get("/posts/8888")
#     assert res.status_code == 404

# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     post = schema.PostOut(**res.json())
#     assert post.Post.id == test_posts[0].id
#     assert post.Post.content == test_posts[0].content
#     assert post.Post.tittle == test_posts[0].tittle

# @pytest.mark.parametrize("tittle, content, published", [
#     ("awesome new tittle", "awesome new content", True),
#     ("favorite pizza", "i like food", False),
#     ("full house", "cute", True)
# ])
# def test_create_post(authorized_client, test_user, test_posts, tittle, content, published):
#     res = authorized_client.post("/posts/", json={"tittle": tittle, "content": content, "published": published})
#     created_post = schema.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.tittle == tittle
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner.id == test_user['id']

# def test_create_post_default_published_true(authorized_client, test_user, test_posts):
#     res = authorized_client.post("/posts/", json={"tittle": "arbitrary tittle", "content": "amaze"})
#     created_post = schema.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.tittle == "arbitrary tittle"
#     assert created_post.content == "amaze"
#     assert created_post.published == True
#     assert created_post.owner.id == test_user['id']

# def test_unauthorize_user_create_posts(client, test_users, test_posts):
#     res = client.post("/posts/", json={"tittle": "arbitrary tittle", "content": "amaze"})
#     assert res.status_code == 401  # Fixed: Unauthorized access should return 401

# def test_unauthorize_user_delete_posts(client, test_users, test_posts):
#     res = client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401  # Fixed: Unauthorized access should return 401

# def test_delete_post_success(authorized_client, test_users, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204

# def test_delete_post_non_exist(authorized_client, test_users, test_posts):
#     res = authorized_client.delete("/posts/30000")
#     assert res.status_code == 404

# def test_delete_other_user_post(authorized_client, test_users, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403  # Fixed: Forbidden access for deleting another user's post

# def test_update_post(authorized_client, test_users, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[0].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
#     updated_post = schema.Post(**res.json())
#     assert res.status_code == 200
#     assert updated_post.tittle == data['tittle']
#     assert updated_post.content == data['content']

# def test_update_other_user_post(authorized_client, test_users, test_users2, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[3].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403  # Fixed: Forbidden access for updating another user's post

# def test_unauthorize_update_posts(client, test_users, test_posts):
#     res = client.put(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401  # Fixed: Unauthorized access should return 401

# def test_update_post_non_exist(authorized_client, test_users, test_posts):
#     data = {
#         "tittle": "updated tittle",
#         "content": "updated content",
#         "id": test_posts[3].id
#     }
#     res = authorized_client.put("/posts/30000", json=data)
#     assert res.status_code == 404
