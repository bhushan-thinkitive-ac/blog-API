from getpass import getuser
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail
from blog import data_base, models, schemas, oauth2, hashing
from sqlalchemy.orm import Session
from .. repository import user

router = APIRouter(
    prefix = "/user",
    tags = ['Users']
)
@router.post('/', status_code = status.HTTP_201_CREATED)
def create_user(items: schemas.User, db: Session = Depends(data_base.get_db)): 
    return user.create(items, db)
   
    

@router.get('/', status_code = status.HTTP_202_ACCEPTED, response_model = List[schemas.ShowUser])
def show_user(db: Session = Depends(data_base.get_db)):
    return user.showUser(db)  
    
@router.get('/{id}', status_code = status.HTTP_202_ACCEPTED, response_model = schemas.ShowUser)
def showUser(id:int, db: Session = Depends(data_base.get_db)):
    return user.userByid(id, db)
    
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user( id: int, db: Session = Depends(data_base.get_db)):
    return user.deleteUserById(id, db) 

