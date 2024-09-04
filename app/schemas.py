from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
import enum

# Enum definitions
class UserRole(str, enum.Enum):
    Farmer = "Farmer"
    Client = "Client"
    Admin = "Admin"

class UserStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Suspended = "Suspended"

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    status: Optional[UserStatus] = UserStatus.Active

class User(UserBase):
    user_id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True  # Updated for Pydantic V2

class UserResponse(BaseModel):
    message: str
    user: User

# Farmer schemas
class FarmerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class FarmerOut(BaseModel):
    farmer_id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    registration_date: date

    class Config:
        from_attributes = True  # Updated for Pydantic V2

# Cattle schemas
class CattleCreate(BaseModel):
    name: str
    breed: str
    birth_date: date
    gender: str
    quality_score: float
    status: str

class CattleOut(BaseModel):
    cattle_id: int
    name: str
    breed: str
    birth_date: date
    gender: str
    quality_score: float
    status: str

    class Config:
        from_attributes = True  # Updated for Pydantic V2

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
