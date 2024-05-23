from .database import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,MetaData
from sqlalchemy.sql.sqltypes import TIMESTAMP,VARCHAR,BIGINT
from sqlalchemy.sql.expression import text

class Posts(Base):
    __tablename__ = 'posts_sqlachemy'
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False,unique=True)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='true',nullable=False)
    created_at = Column(TIMESTAMP,nullable=False,server_default=text('now()'))
metadata = MetaData()

Base.metadata.create_all(bind=engine)