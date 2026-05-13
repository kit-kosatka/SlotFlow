from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "client"

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

