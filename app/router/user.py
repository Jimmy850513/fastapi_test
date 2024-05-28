
from SQL_achemy_db_folder import models
from .. import utils
from SQL_achemy_db_folder.database import SessionLocal
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from SQL_achemy_db_folder.schemas import User,UserResponse
from sqlalchemy.orm import Session
from SQL_achemy_db_folder.database import get_db

router = APIRouter(
    prefix='/sqlachemy',
    tags=['Users_API']
)


#user create
@router.post("/user_create/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
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

#user find
@router.get('/find_user/',status_code=status.HTTP_302_FOUND,response_model=UserResponse)
def find_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    return user