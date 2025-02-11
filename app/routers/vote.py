
# Import necessary FastAPI modules for API creation and error handling
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
# Import SQLAlchemy's Session to interact with the database
from sqlalchemy.orm import Session
# Import database models, schemas, database connection, and authentication utilities
from .. import db_models as db_models, schema, data_base, oauth2

# Create an instance of APIRouter to define voting-related endpoints
router = APIRouter(
    prefix="/vote",  # Prefix for all routes in this router (e.g., "/vote")
    tags=['Vote']  # Grouping this route under the 'Vote' tag for documentation
)

# Define a POST endpoint to handle voting logic
@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schema.Vote,  # Expecting a request body matching the Vote schema
    db: Session = Depends(data_base.get_db),  # Dependency to get database session
    current_user: int = Depends(oauth2.get_current_user)  # Dependency to get the authenticated user
):
    
    # Query the database to check if the post exists
    post = db.query(db_models.Post).filter(db_models.Post.id == vote.post_id).first()
    # If the post does not exist, return a 404 error
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP 404 error for "Not Found"
            detail=f"Post with id {vote.post_id} does not exist"  # Error message
        )
    
    # Query to check if the user has already voted on this post
    vote_query = db.query(db_models.Vote).filter(
        db_models.Vote.post_id == vote.post_id,  # Filtering by post ID
        db_models.Vote.user_id == current_user.id  # Filtering by user ID
    )
    found_vote = vote_query.first()  # Fetch the first matching vote (if exists)

    # If the vote direction is 1 (upvote)
    if vote.dir == 1:
        # Check if the user has already voted on this post
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,  # HTTP 409 error for "Conflict"
                detail=f"User {current_user.id} has already voted on post with id {vote.post_id}"  # Error message
            )
        
        # Create a new vote entry in the database
        new_vote = db_models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)  # Add the new vote to the database session
        db.commit()  # Commit changes to the database
        return {"message": "Successfully added vote!"}  # Return success response
    
    # If the vote direction is -1 (downvote/removal)
    elif vote.dir == -1:
        # If no vote exists, return an error since there's nothing to remove
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,  # HTTP 404 error for "Not Found"
                detail=f"Vote does not exist for user {current_user.id} on post {vote.post_id}"  # Error message
            )
        
        # Remove the existing vote from the database
        vote_query.delete(synchronize_session=False)  # Delete the found vote
        db.commit()  # Commit the deletion to the database
        return {"message": "Successfully deleted vote!"}  # Return success response
    
    # If the vote direction is invalid (not 1 or -1)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # HTTP 400 error for "Bad Request"
            detail="Invalid vote direction"  # Error message
        )
