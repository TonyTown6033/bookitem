from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Room schemas
class RoomBase(BaseModel):
    name: str
    location: str
    capacity: int
    description: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Booking schemas
class BookingBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None

class BookingCreate(BookingBase):
    user_id: int

class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingDetailResponse(BookingResponse):
    user: UserResponse
    room: RoomResponse
    
    class Config:
        from_attributes = True

