from fastapi import FastAPI
from .router import post,user
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)




    


