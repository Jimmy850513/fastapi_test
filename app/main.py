from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from SQL_achemy_db_folder.schemas import Post,PostResponse,User,UserResponse
from typing import Optional,List
from SQL_achemy_db_folder import models
from SQL_achemy_db_folder.database import engine,SessionLocal
from sqlalchemy.orm import Session
from . import utils
app = FastAPI()



def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get('/sqlachemy/posts',response_model=List[PostResponse])
def get_posts(db:Session = Depends(get_db)):
    #SELECT * FROM posts
    data = db.query(models.Posts).all()
    query = db.query(models.Posts)
    return data



@app.post('/sqlachemy/posts_created/',response_model=PostResponse)
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
    

@app.get('/sqlachemy/posts_find/',status_code=status.HTTP_302_FOUND,response_model=PostResponse)
def find_posts_by_id(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()      
    if post:
        return post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#delete 
@app.delete("/sqlachemy/posts_delete/",status_code=status.HTTP_202_ACCEPTED)
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
@app.patch("/sqlachemy/posts_patch/",status_code=status.HTTP_202_ACCEPTED,response_model=PostResponse)
def patch_post_by_id(id:int,data:dict=Body(...),db:Session = Depends(get_db)):
    posts = db.query(models.Posts).filter(models.Posts.id == id).first()
    if posts:
        post = db.query(models.Posts).filter(models.Posts.id == id).update({**data})
        post_return = db.query(models.Posts).filter(models.Posts.id == id).first()
        db.commit()
        return post_return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='can not find the post to update')
    
#user create
@app.post("/sqlachemy/user_create/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user_input:User,db:Session = Depends(get_db)):
    #hash user password
    hashed_password = utils.hash(user_input.password)
    user_input.password = hashed_password
    user_account = models.User(**user_input.dict())
    if user_account:
        db.add(user_account)
        db.commit()
        db.refresh(user_account)
        return user_account
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="user has been used before")

