"""
会议室业务逻辑服务层
"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Room
from schemas import RoomCreate


class RoomService:
    """会议室服务类"""
    
    @staticmethod
    def check_room_name_exists(db: Session, name: str, exclude_id: int = None) -> bool:
        """
        检查会议室名称是否已存在
        
        Args:
            db: 数据库会话
            name: 会议室名称
            exclude_id: 排除的会议室ID（用于更新时）
            
        Returns:
            是否存在
        """
        query = db.query(Room).filter(Room.name == name)
        if exclude_id:
            query = query.filter(Room.id != exclude_id)
        return query.first() is not None
    
    @staticmethod
    def create_room(db: Session, room: RoomCreate) -> Room:
        """
        创建会议室
        
        Args:
            db: 数据库会话
            room: 会议室创建数据
            
        Returns:
            创建的会议室对象
            
        Raises:
            HTTPException: 会议室名称已存在时抛出
        """
        if RoomService.check_room_name_exists(db, room.name):
            raise HTTPException(status_code=400, detail="会议室名称已存在")
        
        db_room = Room(
            name=room.name,
            location=room.location,
            capacity=room.capacity,
            description=room.description
        )
        
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        
        return db_room
    
    @staticmethod
    def get_room_by_id(db: Session, room_id: int) -> Room:
        """
        根据ID获取会议室
        
        Args:
            db: 数据库会话
            room_id: 会议室ID
            
        Returns:
            会议室对象
            
        Raises:
            HTTPException: 会议室不存在时抛出
        """
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="会议室不存在")
        return room
    
    @staticmethod
    def get_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
        """
        获取会议室列表
        
        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            
        Returns:
            会议室列表
        """
        return db.query(Room).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_room(db: Session, room_id: int, room: RoomCreate) -> Room:
        """
        更新会议室
        
        Args:
            db: 数据库会话
            room_id: 会议室ID
            room: 会议室更新数据
            
        Returns:
            更新后的会议室对象
            
        Raises:
            HTTPException: 会议室不存在或名称冲突时抛出
        """
        db_room = RoomService.get_room_by_id(db, room_id)
        
        # 检查名称是否与其他会议室冲突
        if room.name != db_room.name:
            if RoomService.check_room_name_exists(db, room.name, room_id):
                raise HTTPException(status_code=400, detail="会议室名称已存在")
        
        db_room.name = room.name
        db_room.location = room.location
        db_room.capacity = room.capacity
        db_room.description = room.description
        
        db.commit()
        db.refresh(db_room)
        
        return db_room
    
    @staticmethod
    def delete_room(db: Session, room_id: int) -> dict:
        """
        删除会议室
        
        Args:
            db: 数据库会话
            room_id: 会议室ID
            
        Returns:
            操作结果消息
        """
        room = RoomService.get_room_by_id(db, room_id)
        db.delete(room)
        db.commit()
        return {"message": "会议室已删除"}

