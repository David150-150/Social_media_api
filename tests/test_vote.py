import pytest
from app import db_models as models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit






def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    print(res.json())
    assert res.status_code == 201

# def test_vote_twice_post(authorized_client, test_posts, test_vote):
#     res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 1})
#     print(res.json())
#     assert res.status_code == 409
    

def test_vote_twice_on_post(authorized_client, test_posts):
    post_id = test_posts[3].id

    # First vote should pass
    res1 = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert res1.status_code == 201

    # Second vote should fail
    res2 = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    print(res2.json())
    assert res2.status_code == 409  # Expecting 409 Conflict
   
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 0})
    print(res.json())
    assert res.status_code == 400

def test_delete_vote_on_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 0})
    print(res.json())
    assert res.status_code == 400
   
    
def test_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote", json={"post_id": 8000, "dir": -1})
    print(res.json())
    assert res.status_code == 404

def test_vote_on_unauthorized_user(client, test_posts):
    res = client.post("/vote", json={"post_id": test_posts[3].id, "dir": 1})
    print(res.json())
    assert res.status_code == 401
















# 

