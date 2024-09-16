from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas


def get_all(db: Session ):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = "Blog list is empty, Please create one!!")
    return blogs

def create(items:schemas.Item, db: Session):
    new_blog = models.Blog(title = items.title, body = items.body, user_id = None)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id: int, db: Session):
    blog_data =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} is not found")
    blog_data.delete(synchronize_session=False)
    db.commit()
    return 'Deleted Successfully'

def update(id:int, items:schemas.Item, db: Session):
    items_data=items.model_dump()
    blog_data=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} is not found")

    blog_data.update(items_data, synchronize_session=False)
    db.commit()
    return 'Blog Updated Successfully'

def show_blog(id, db: Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    return blogs
