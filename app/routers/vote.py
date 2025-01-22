from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, data_base, db_models as models, oauth2

#Created an Instance for the Router
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schema.Vote, db: Session = Depends(data_base.get_db), 
               current_user: int = Depends(oauth2.get_current_user)):
    
#When the post thus not exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote =   vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail=f"user {current_user.id} has already voted on post with an id {vote.post_id}"
)

            #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} 
                                 #has already voted on post with an id {vote.post_id}")
        #Creating a brand new post
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        
        #This will add the changes
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote!"}
    else:
        if not  found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist!")
        
        #If the Vote is found
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote!"}