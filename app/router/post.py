
from SQL_achemy_db_folder import models
from .. import utils
from SQL_achemy_db_folder.database import SessionLocal
from fastapi import status,HTTPException,Depends,APIRouter,Body
from SQL_achemy_db_folder.schemas import Post,PostResponse
from typing import List
from sqlalchemy.orm import Session
from SQL_achemy_db_folder.database import get_db

router = APIRouter(
    prefix='/sqlachemy',
    tags=['Post_API']
)




@router.get('/posts/',response_model=List[PostResponse])
def get_posts(db:Session = Depends(get_db)):
    #SELECT * FROM posts
    data = db.query(models.Posts).all()
    query = db.query(models.Posts)
    return data



@router.post('/posts_created/',response_model=PostResponse)
def create_posts(post:Post,db:Session = Depends(get_db)):
    data = post.dict()
    new_post = models.Posts(**data)
    if new_post:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"message":"created not successfully"})
    

@router.get('/posts_find/',status_code=status.HTTP_302_FOUND,response_model=PostResponse)
def find_posts_by_id(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()      
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#delete 
@router.delete("/posts_delete/",status_code=status.HTTP_202_ACCEPTED)
def delete_post_by_id(id:int,db:Session = Depends(get_db)):
    posts = db.query(models.Posts).filter(models.Posts.id == id).first()
    if posts:
        post = db.query(models.Posts).filter(models.Posts.id == id)
        post.delete()
        db.commit()
        return {"data":"successfully delete"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='can not find the post to delete')
    
#update post
@router.patch("/posts_patch/",status_code=status.HTTP_202_ACCEPTED,response_model=PostResponse)
def patch_post_by_id(id:int,data:dict=Body(...),db:Session = Depends(get_db)):
    posts = db.query(models.Posts).filter(models.Posts.id == id).first()
    if posts:
        post = db.query(models.Posts).filter(models.Posts.id == id).update({**data})
        post_return = db.query(models.Posts).filter(models.Posts.id == id).first()
        db.commit()
        return post_return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='can not find the post to update')