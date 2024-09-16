from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from ..  import schemas, data_base, models, oauth2
from sqlalchemy.orm import Session
from .. repository import blog

router = APIRouter(
    prefix = "/myblog",
    tags =['Blogs']
)

@router.get('/', status_code = status.HTTP_202_ACCEPTED, response_model=List[schemas.ShowItem])
def get_all_blog(db: Session = Depends(data_base.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_blog( items: schemas.Item,  db: Session = Depends(data_base.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)): # type: ignore
    return blog.create(items, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(data_base.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_blog(id: int, items:schemas.Item, db: Session = Depends(data_base.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, items, db)


@router.get('/{id}', status_code = 200, response_model= schemas.ShowItem)
def show(id: int, db: Session = Depends(data_base.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show_blog(id, db)

