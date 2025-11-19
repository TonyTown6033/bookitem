"""
用户业务逻辑服务层
"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

from models import User
from schemas import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """用户服务类"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        哈希密码
        
        Args:
            password: 明文密码
            
        Returns:
            哈希后的密码
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 哈希密码
            
        Returns:
            密码是否匹配
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def check_username_exists(db: Session, username: str) -> bool:
        """
        检查用户名是否已存在
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            是否存在
        """
        return db.query(User).filter(User.username == username).first() is not None
    
    @staticmethod
    def check_email_exists(db: Session, email: str) -> bool:
        """
        检查邮箱是否已存在
        
        Args:
            db: 数据库会话
            email: 邮箱
            
        Returns:
            是否存在
        """
        return db.query(User).filter(User.email == email).first() is not None
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        创建用户
        
        Args:
            db: 数据库会话
            user: 用户创建数据
            
        Returns:
            创建的用户对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在时抛出
        """
        # 检查用户名
        if UserService.check_username_exists(db, user.username):
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱
        if UserService.check_email_exists(db, user.email):
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        
        # 创建用户
        hashed_password = UserService.hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        根据ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            用户对象
            
        Raises:
            HTTPException: 用户不存在时抛出
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        获取用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量
            
        Returns:
            用户列表
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        """
        删除用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            操作结果消息
        """
        user = UserService.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return {"message": "用户已删除"}

