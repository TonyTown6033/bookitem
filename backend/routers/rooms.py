from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Room
from schemas import RoomCreate, RoomResponse

router = APIRouter()

@router.post("/", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    # 检查会议室名称是否已存在
    db_room = db.query(Room).filter(Room.name == room.name).first()
    if db_room:
        raise HTTPException(status_code=400, detail="会议室名称已存在")
    
    # 创建新会议室
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

@router.get("/", response_model=List[RoomResponse])
def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = db.query(Room).offset(skip).limit(limit).all()
    return rooms

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="会议室不存在")
    return room

@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="会议室不存在")
    
    db_room.name = room.name
    db_room.location = room.location
    db_room.capacity = room.capacity
    db_room.description = room.description
    
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="会议室不存在")
    
    db.delete(room)
    db.commit()
    return {"message": "会议室已删除"}

