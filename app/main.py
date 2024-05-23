from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from SQL_achemy_db_folder import models
from SQL_achemy_db_folder.database import engine,SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True


def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get('/sqlachemy/posts')
def get_posts(db:Session = Depends(get_db)):
    #SELECT * FROM posts
    data = db.query(models.Posts).all()
    query = db.query(models.Posts)
    print(query)
    print(data)
    return {"data":data}


@app.post('/sqlachemy/posts_created/')
def create_posts(post:dict=Body(...),db:Session = Depends(get_db)):
    new_post = models.Posts(title=post['title'],content=post['content'],
                            published=post['published'] if post.get('published') else True)
    if new_post:
        db.add(new_post)
        db.commit()
        return {"data":"true","message":"created successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"message":"created not successfully"})
    
        