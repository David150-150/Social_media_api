from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter  # Import FastAPI modules
from sqlalchemy.orm import Session  # Import Session for database interactions

from .. import db_models as db_models  # Import database models
from .. import schema, oauth2  # Import schema and OAuth2 authentication module
from ..data_base import engine, get_db  # Import database dependencies
from typing import List, Optional  # Import type hints for response models
from sqlalchemy import func  # Import SQL functions for aggregations



# Create a router for post-related endpoints
router = APIRouter(
    prefix="/posts",  # Set the URL prefix for this router
    tags=["Posts"]  # Categorize endpoints under "Posts"
)

# GET all posts with vote counts
@router.get("/", response_model=List[schema.PostOut])  # Define GET endpoint with response model
async def get_all_posts(
    db: Session = Depends(get_db),  # Inject database session
    current_user: int = Depends(oauth2.get_current_user),  # Authenticate user
    limit: int = 10,  # Limit number of posts returned (default: 10)
    skip: int = 0,  # Number of posts to skip (pagination)
    search: Optional[str] = ""  # Optional search query (default: empty string)
):
    # Fetch posts and count votes using an outer join
    posts = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("votes")) \
        .outerjoin(db_models.Vote, db_models.Vote.post_id == db_models.Post.id) \
        .group_by(db_models.Post.id).all()

    # Return posts along with vote counts
    return [{"post": schema.Post.model_validate(post), "votes": votes} for post, votes in posts]  

# CREATE a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_posts(
    post: schema.PostCreate,  # Request body validation using schema
    db: Session = Depends(get_db),  # Inject database session
    current_user: int = Depends(oauth2.get_current_user)  # Authenticate user
):
    # Create a new post object with the current user's ID
    new_post = db_models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)  # Add post to database session
    db.commit()  # Commit transaction
    db.refresh(new_post)  # Refresh object with database data
    return new_post  # Return created post

# GET a specific post by ID
@router.get("/{id}", response_model=schema.PostOut)
async def get_post(
    id: int,  
    db: Session = Depends(get_db),  # Inject database session
    current_user: int = Depends(oauth2.get_current_user)  # Authenticate user
):
    # Fetch post and count votes using an outer join
    post = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("votes")) \
        .outerjoin(db_models.Vote, db_models.Vote.post_id == db_models.Post.id) \
        .filter(db_models.Post.id == id) \
        .group_by(db_models.Post.id) \
        .first()

    # If post not found, return 404 error
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    # Return the post with vote count
    return {"post": schema.Post.model_validate(post[0]), "votes": post[1]}

# DELETE a post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_post(
    id: int,  
    db: Session = Depends(get_db),  # Inject database session
    current_user: int = Depends(oauth2.get_current_user)  # Authenticate user
):
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)  # Query for post
    post = post_query.first()  # Retrieve post

    # If post does not exist, return 404 error
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # If user is not the owner, return 403 Forbidden error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    post_query.delete(synchronize_session=False)  # Delete post
    db.commit()  # Commit transaction
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Return empty response

# UPDATE a post by ID
@router.put("/{id}", response_model=schema.Post)
async def update_post(
    id: int,  
    updated_post: schema.PostCreate,  # Request body validation
    db: Session = Depends(get_db),  # Inject database session
    current_user: int = Depends(oauth2.get_current_user)  # Authenticate user
):
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)  # Query for post
    post = post_query.first()  # Retrieve post

    # If post does not exist, return 404 error
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # If user is not the owner, return 403 Forbidden error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post_query.update(updated_post.dict(), synchronize_session=False)  # Update post fields
    db.commit()  # Commit transaction
    return post_query.first()  # Return updated post





