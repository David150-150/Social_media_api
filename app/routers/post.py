from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import db_models as models, schema, oauth2
from ..data_base import engine, get_db
from typing import  List, Optional
from sqlalchemy import func

 #This a Router object
router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)




# Path Operation
#Getting all posts
@router.get("/", response_model=List[schema.Post])
#async def get_posts():
async def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                        Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(search)
   
    posts = db.query(models.Post).filter(models.post.owner_id == current_user.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results



#Path operation for creating a post
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    
    #this will reload to give you back the data if updated
    new_post = models.Post(owner_id = current_user.id, **post.dict()) 

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
                             
    
    



#GETTING JUST A POST
@router.get("/{id}", response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #print(post)
    if not post:
    
        raise HTTPException(status_code=404, detail=(f"post with id: {id} was not found"))
    
    #if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorize to perform the requires action")

    return post

   


#Deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorize to perform the requires action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Updating Post
@router.put("/{id}", response_model=schema.Post)
async def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =  post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorize to perform the requires action")



    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
   

   

   

