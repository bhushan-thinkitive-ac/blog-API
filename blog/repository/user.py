from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas, hashing
import json


def create(items: schemas.Item, db: Session):
    # Check if password is matching
    check_pass= items.validpass()
    print(check_pass)
    if items.password != items.confirm_password:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,  detail = "Password do not match")

    
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == items.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{items.email}' already exists.")
    
    new_user = models.User(name = items.name, email = items.email,test = items.test, password = hashing.Hash.hash_key(items.password))   #,phone_number = items.phone_number
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return_code = {"message" : f"{status.HTTP_201_CREATED} User created successfully"}
    json_data = json.dumps(return_code)  #return the success message only.
    return Response(json_data)

# def create_reset_code(items: schemas.ForgetPassword, email:str, reset_code:str, db: Session):
#     new_user = models.User(email = items.email, reset_code = items.reset_code)   #,phone_number = items.phone_number
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return_code = {"message" : f"{status.HTTP_201_CREATED} User created successfully"}
#     json_data = json.dumps(return_code)  #return the success message only.
#     return Response(json_data)


def showUser(db:Session):
    #print the id with the user details.
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    return user

def userByid(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    return user

def deleteUserById( id: int, db: Session):
    user_data =db.query(models.User).filter(models.User.id == id)
    if not user_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} is not found")
    user_data.delete(synchronize_session=False)
    db.commit()
    return {f"message": "User of id {id} is deleted"}
