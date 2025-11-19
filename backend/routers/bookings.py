from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from datetime import datetime, timezone
from database import get_db
from models import Booking, User, Room
from schemas import BookingCreate, BookingResponse, BookingDetailResponse

router = APIRouter()

def make_aware(dt):
    """将 naive datetime 转换为 aware datetime (UTC)"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

def get_current_time():
    """获取当前时间（UTC，带时区信息）"""
    return datetime.now(timezone.utc)

def check_time_conflict(db: Session, room_id: int, start_time: datetime, end_time: datetime, booking_id: int = None):
    """检查时间冲突"""
    query = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status != "cancelled",
        or_(
            and_(Booking.start_time <= start_time, Booking.end_time > start_time),
            and_(Booking.start_time < end_time, Booking.end_time >= end_time),
            and_(Booking.start_time >= start_time, Booking.end_time <= end_time)
        )
    )
    
    if booking_id:
        query = query.filter(Booking.id != booking_id)
    
    return query.first() is not None

@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # 验证用户存在
    user = db.query(User).filter(User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证会议室存在
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="会议室不存在")
    
    if not room.is_available:
        raise HTTPException(status_code=400, detail="会议室不可用")
    
    # 处理时区问题
    start_time = make_aware(booking.start_time) if booking.start_time.tzinfo is None else booking.start_time
    end_time = make_aware(booking.end_time) if booking.end_time.tzinfo is None else booking.end_time
    
    # 验证时间
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="开始时间必须早于结束时间")
    
    if start_time < get_current_time():
        raise HTTPException(status_code=400, detail="不能预约过去的时间")
    
    # 检查时间冲突
    if check_time_conflict(db, booking.room_id, start_time, end_time):
        raise HTTPException(status_code=400, detail="该时间段已被预约")
    
    # 创建预约（转换为 naive datetime 存储）
    db_booking = Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        start_time=start_time.replace(tzinfo=None),
        end_time=end_time.replace(tzinfo=None),
        purpose=booking.purpose,
        status="confirmed"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=List[BookingDetailResponse])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings

@router.get("/user/{user_id}", response_model=List[BookingDetailResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return bookings

@router.get("/room/{room_id}", response_model=List[BookingDetailResponse])
def get_room_bookings(room_id: int, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    return booking

@router.put("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="预约已取消")
    
    booking.status = "cancelled"
    db.commit()
    return {"message": "预约已取消"}

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    db.delete(booking)
    db.commit()
    return {"message": "预约已删除"}

