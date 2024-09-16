from fastapi import FastAPI #Importing FastAPI class from fastapi library
from typing import Optional
from pydantic import BaseModel
import datetime
app = FastAPI() #Creating the instance APP 


@app.get('/blog') #decorating the function with instance and appplying the REST operations on Path Parameters
def index(limit=10, published = bool):
    # return published
    return {'data': {f'{limit} Blogs are posted by Bhushan Chaudhari'}}

@app.get('/about')
def about():
    return {'data': {"About page"}}

@app.get('/blog/{id}')
def id(id:int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id:int):
    return {'data': {f"This is comment for id: {id}", f"This is another comment for id: {id}"}}


class Blog(BaseModel):
    title: str
    date: str
    body: Optional[str]

@app.post('/blog')
def post_blog(request: Blog):
    # return request
    return {'data': f'Blog is created with the title as {request.title} on {request.date}'}


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=9000)
