from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
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

class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"

class CattleStatusEnum(str, enum.Enum):
    Available = "Available"
    Sold = "Sold"
    NotAvailable = "Not Available"

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str
    phone: Optional[Annotated[str, Field(min_length=10, max_length=20)]] = None
    address: Optional[str] = None  # Optional address field

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    user_id: int
    created_at: datetime
    status: UserStatus
    role: str
    phone: Optional[Annotated[str, Field(min_length=10, max_length=20)]] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True  # Updated for Pydantic V2

class UserResponse(BaseModel):
    message: str
    user: User

# Location schemas
class LocationBase(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    climate_zone: Optional[str]
    updated_at: Optional[date]

class LocationCreate(LocationBase):
    farmer_id: Optional[int]

class LocationOut(LocationBase):
    location_id: int
    farmer_id: Optional[int]

    class Config:
        orm_mode = True  # Updated for Pydantic V2

# Farmer schemas
class FarmerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class FarmerCreate(FarmerBase):
    pass

class FarmerOut(FarmerBase):
    farmer_id: int
    registration_date: date

    class Config:
        orm_mode = True  # Updated for Pydantic V2

# Cattle schemas
class CattleBase(BaseModel):
    name: str
    breed: Optional[str] = None
    birth_date: date
    gender: GenderEnum
    quality_score: Optional[float] = None
    status: CattleStatusEnum

class CattleCreate(CattleBase):
    pass

class CattleOut(CattleBase):
    cattle_id: int

    class Config:
        orm_mode = True  # Updated for Pydantic V2

# Cattle Image schemas
class CattleImageBase(BaseModel):
    cattle_id: int
    image_url: str

class CattleImageCreate(CattleImageBase):
    pass

class CattleImageOut(CattleImageBase):
    image_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True  # Updated for Pydantic V2
