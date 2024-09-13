from pydantic import BaseModel, EmailStr, Field, ValidationError
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
    role: UserRole  # Use enum directly

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: UserRole
    phone: Optional[Annotated[str, Field(min_length=10, max_length=20)]] = None
    address: Optional[str] = None
    last_login: Optional[datetime] = None

    class Config:
        use_enum_values = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None
    address: Optional[str] = None
    last_login: Optional[datetime] = None

class User(UserBase):
    user_id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    status: UserStatus
    phone: Optional[Annotated[str, Field(min_length=10, max_length=20)]] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    status: UserStatus
    phone: Optional[Annotated[str, Field(min_length=10, max_length=20)]] = None
    address: Optional[str] = None
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


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
        from_attributes = True

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
        from_attributes = True

# Cattle schemas
class CattleBase(BaseModel):
    name: str
    breed: Optional[str] = None
    birth_date: date
    gender: GenderEnum
    quality_score: Optional[float] = None
    status: CattleStatusEnum

class CattleCreate(CattleBase):
    user_id: Optional[int] = None

class CattleUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[GenderEnum] = None
    quality_score: Optional[float] = None
    status: Optional[CattleStatusEnum] = None

class CattleOut(CattleBase):
    cattle_id: int

    class Config:
        from_attributes = True

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
        from_attributes = True

class CattleImageResponse(CattleImageBase):
    image_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# WhatsApp Message schemas
class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    message_content: str
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Calving schemas
class CalvingBase(BaseModel):
    cattle_id: Optional[int] = None
    calving_date: Optional[date] = None
    calf_gender: Optional[GenderEnum] = None
    calf_health_status: Optional[str] = None

class CalvingCreate(CalvingBase):
    pass

class CalvingOut(CalvingBase):
    calving_id: int

    class Config:
        from_attributes = True

# Insemination schemas
class InseminationBase(BaseModel):
    cattle_id: int
    insemination_date: date
    insemination_method: Optional[str] = None
    bull_id: Optional[int] = None

class InseminationCreate(InseminationBase):
    pass

class InseminationOut(InseminationBase):
    insemination_id: int

    class Config:
        from_attributes = True

# Milk Production schemas
class MilkProductionBase(BaseModel):
    cattle_id: int
    production_date: date
    volume: float

class MilkProductionCreate(MilkProductionBase):
    pass

class MilkProductionOut(MilkProductionBase):
    production_id: int

    class Config:
        from_attributes = True

# Pedigree schemas
class PedigreeBase(BaseModel):
    cattle_id: int
    dam_id: Optional[int] = None
    sire_id: Optional[int] = None

class PedigreeCreate(PedigreeBase):
    pass

class PedigreeOut(PedigreeBase):
    id: int

    class Config:
        from_attributes = True

# Cattle Ownership History schemas
class CattleOwnershipHistoryBase(BaseModel):
    cattle_id: Optional[int] = None
    previous_owner_id: Optional[int] = None
    new_owner_id: Optional[int] = None
    ownership_change_date: Optional[date] = None

class CattleOwnershipHistoryCreate(CattleOwnershipHistoryBase):
    cattle_id: Optional[int] = None
    previous_owner_id: Optional[int] = None
    new_owner_id: Optional[int] = None
    ownership_change_date: Optional[date] = None

class CattleOwnershipHistoryOut(CattleOwnershipHistoryBase):
    ownership_id: int

    class Config:
        from_attributes = True

# Favorite schemas
class FavoriteBase(BaseModel):
    client_id: Optional[int] = None
    cattle_id: Optional[int] = None
    created_at: Optional[datetime] = None

class FavoriteCreate(FavoriteBase):
    client_id: Optional[int] = None
    cattle_id: Optional[int] = None
    created_at: Optional[datetime] = None

class FavoriteOut(FavoriteBase):
    client_id: Optional[int] = None
    cattle_id: Optional[int] = None
    created_at: Optional[datetime] = None
    favorite_id: int

    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    user_id: int
    message: str
    created_at: Optional[datetime] = None
    read_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(NotificationBase):
    notification_id: int

    class Config:
        from_attributes = True

# Trade schemas
class TradeBase(BaseModel):
    seller_id: int
    buyer_id: int
    cattle_id: int
    trade_date: Optional[datetime] = None
    price: float

class TradeOut(TradeBase):
    seller_id: int
    buyer_id: int
    cattle_id: int
    trade_date: Optional[datetime] = None
    price: float
    trade_id: int

    class Config:
        from_attributes = True

# Weight Record schemas
class WeightRecordBase(BaseModel):
    cattle_id: int
    weight_date: date
    weight: float

class WeightRecordCreate(WeightRecordBase):
    pass

class WeightRecordOut(WeightRecordBase):
    weight_id: int

    class Config:
        from_attributes = True