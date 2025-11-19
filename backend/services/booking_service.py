"""
预约业务逻辑服务层
将业务逻辑从路由中分离，提高可维护性和可测试性
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException

from models import Booking, User, Room
from schemas import BookingCreate
from utils.timezone import make_aware, make_naive, get_current_time
from utils.validators import validate_time_range, validate_future_time


class BookingService:
    """预约服务类"""
    
    @staticmethod
    def check_time_conflict(
        db: Session,
        room_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_booking_id: Optional[int] = None
    ) -> bool:
        """
        检查时间冲突
        
        Args:
            db: 数据库会话
            room_id: 会议室ID
            start_time: 开始时间
            end_time: 结束时间
            exclude_booking_id: 排除的预约ID（用于更新时）
            
        Returns:
            是否存在冲突
        """
        # 转换为 naive datetime 以便与数据库比较
        check_start = make_naive(start_time)
        check_end = make_naive(end_time)
        
        query = db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.status != "cancelled",
            or_(
                and_(Booking.start_time <= check_start, Booking.end_time > check_start),
                and_(Booking.start_time < check_end, Booking.end_time >= check_end),
                and_(Booking.start_time >= check_start, Booking.end_time <= check_end)
            )
        )
        
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        
        conflicting_booking = query.first()
        return conflicting_booking is not None
    
    @staticmethod
    def validate_booking_data(
        db: Session,
        booking: BookingCreate,
        start_time: datetime,
        end_time: datetime
    ) -> tuple[User, Room]:
        """
        验证预约数据
        
        Args:
            db: 数据库会话
            booking: 预约创建数据
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            (用户对象, 会议室对象)
            
        Raises:
            HTTPException: 验证失败时抛出
        """
        # 验证用户存在
        user = db.query(User).filter(User.id == booking.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 验证会议室存在
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="会议室不存在")
        
        # 验证会议室可用
        if not room.is_available:
            raise HTTPException(status_code=400, detail="会议室不可用")
        
        # 验证时间范围
        validate_time_range(start_time, end_time)
        
        # 验证不能预约过去的时间
        validate_future_time(start_time)
        
        # 检查时间冲突
        if BookingService.check_time_conflict(db, booking.room_id, start_time, end_time):
            raise HTTPException(status_code=400, detail="该时间段已被预约")
        
        return user, room
    
    @staticmethod
    def create_booking(
        db: Session,
        booking: BookingCreate
    ) -> Booking:
        """
        创建预约
        
        Args:
            db: 数据库会话
            booking: 预约创建数据
            
        Returns:
            创建的预约对象
        """
        # 处理时区
        start_time = make_aware(booking.start_time)
        end_time = make_aware(booking.end_time)
        
        # 验证数据
        BookingService.validate_booking_data(db, booking, start_time, end_time)
        
        # 创建预约（存储为 naive datetime）
        db_booking = Booking(
            user_id=booking.user_id,
            room_id=booking.room_id,
            start_time=make_naive(start_time),
            end_time=make_naive(end_time),
            purpose=booking.purpose,
            status="confirmed"
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        
        return db_booking
    
    @staticmethod
    def get_booking_by_id(
        db: Session,
        booking_id: int
    ) -> Booking:
        """
        根据ID获取预约
        
        Args:
            db: 数据库会话
            booking_id: 预约ID
            
        Returns:
            预约对象
            
        Raises:
            HTTPException: 预约不存在时抛出
        """
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="预约不存在")
        return booking
    
    @staticmethod
    def get_bookings(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        """
        获取预约列表
        
        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            
        Returns:
            预约列表
        """
        return db.query(Booking).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_bookings(
        db: Session,
        user_id: int
    ) -> List[Booking]:
        """
        获取用户的预约列表
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            预约列表
        """
        return db.query(Booking).filter(Booking.user_id == user_id).all()
    
    @staticmethod
    def get_room_bookings(
        db: Session,
        room_id: int
    ) -> List[Booking]:
        """
        获取会议室的预约列表
        
        Args:
            db: 数据库会话
            room_id: 会议室ID
            
        Returns:
            预约列表
        """
        return db.query(Booking).filter(Booking.room_id == room_id).all()
    
    @staticmethod
    def cancel_booking(
        db: Session,
        booking_id: int
    ) -> dict:
        """
        取消预约
        
        Args:
            db: 数据库会话
            booking_id: 预约ID
            
        Returns:
            操作结果消息
            
        Raises:
            HTTPException: 预约不存在或已取消时抛出
        """
        booking = BookingService.get_booking_by_id(db, booking_id)
        
        if booking.status == "cancelled":
            raise HTTPException(status_code=400, detail="预约已取消")
        
        booking.status = "cancelled"
        db.commit()
        
        return {"message": "预约已取消"}
    
    @staticmethod
    def delete_booking(
        db: Session,
        booking_id: int
    ) -> dict:
        """
        删除预约
        
        Args:
            db: 数据库会话
            booking_id: 预约ID
            
        Returns:
            操作结果消息
        """
        booking = BookingService.get_booking_by_id(db, booking_id)
        
        db.delete(booking)
        db.commit()
        
        return {"message": "预约已删除"}

