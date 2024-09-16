from fastapi import FastAPI
from . import models
from blog.data_base import engine
from blog.router import blog, user, login

app = FastAPI()
models.Base.metadata.create_all(engine) 

app.include_router(login.router)
app.include_router(blog.router)
app.include_router(user.router)


