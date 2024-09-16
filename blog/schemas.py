from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)




class Item(BaseModel):
    title:str
    # description: str
    body: str

    class Config():
        from_attributes = True



class User(BaseModel):
    name: str 
    email: EmailStr
    # phone_number: Optional[str] = None
    test: int 
    password: str
    confirm_password: str
    class Config():
        from_attributes = True


 
    def validpass(self):
        if self.password != self.confirm_password:
            return False

class ShowUser(BaseModel):
    name: str 
    email: EmailStr
    # password: str 
    # blogs : List[str]

    class Config():
        from_attributes = True

class ShowItem(Item):
    title: str
    body: str
    # creator: ShowUser

    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str 

    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class ForgetPassword(BaseModel):
    email:str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class EnableTwoFactor(BaseModel):
    email: str
    password: str

class VerifyTwoFactor(BaseModel):
    email: str
    code: str