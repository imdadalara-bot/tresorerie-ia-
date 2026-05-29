from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    name: str
    password: str
    sector: str = "commercant"
    currency: str = "XOF"


class UserLogin(BaseModel):
    email: str | None = None
    phone: str | None = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str | None
    phone: str | None
    name: str
    sector: str
    currency: str

    model_config = {"from_attributes": True}
