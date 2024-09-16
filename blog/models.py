from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean # type: ignore
from blog.data_base import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'MyBlogs'
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    body = Column(String)
    # # description = Column(String)
    user_id = Column(Integer, ForeignKey('MyUsers.id'))
    creator = relationship('User', back_populates="blogs")

class User(Base):
    __tablename__ = 'MyUsers'

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    email = Column(String)
    # phone_number = Column(String)
    test = Column(Integer)
    password = Column(String)  
    is_two_factor_enabled = Column(Boolean, default=False) 
    two_factor_secret = Column(String, nullable=True) 

    blogs = relationship('Blog', back_populates="creator")


class Codes(Base):
    __tablename__ = 'MyCodes'

    id = Column(Integer, primary_key=True, index= True)
    email = Column(String)
    reset_code = Column(String)
    status = Column(String)
    expired_in = Column(DateTime)
