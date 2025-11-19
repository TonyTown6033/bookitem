"""
时区处理工具模块
统一管理所有时区相关的操作
"""

from datetime import datetime, timezone
from typing import Optional, List, TypeVar

T = TypeVar('T')


def make_aware(dt: datetime) -> datetime:
    """
    将 naive datetime 转换为 aware datetime (UTC)
    
    Args:
        dt: 日期时间对象
        
    Returns:
        带时区信息的 datetime (UTC)
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def make_naive(dt: datetime) -> datetime:
    """
    将 aware datetime 转换为 naive datetime
    用于存储到数据库
    
    Args:
        dt: 日期时间对象
        
    Returns:
        不带时区信息的 datetime
    """
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def get_current_time() -> datetime:
    """
    获取当前时间（UTC，带时区信息）
    
    Returns:
        当前 UTC 时间
    """
    return datetime.now(timezone.utc)


def add_timezone_to_object(obj, *fields: str):
    """
    为对象的指定字段添加 UTC 时区信息
    
    Args:
        obj: 数据对象
        fields: 需要添加时区的字段名
    """
    for field in fields:
        if hasattr(obj, field):
            value = getattr(obj, field)
            if value and isinstance(value, datetime) and value.tzinfo is None:
                setattr(obj, field, value.replace(tzinfo=timezone.utc))
    return obj


def add_timezone_to_list(objects: List[T], *fields: str) -> List[T]:
    """
    批量为对象列表的指定字段添加 UTC 时区信息
    
    Args:
        objects: 对象列表
        fields: 需要添加时区的字段名
        
    Returns:
        处理后的对象列表
    """
    for obj in objects:
        add_timezone_to_object(obj, *fields)
    return objects


# 预定义的常用字段组合
BOOKING_DATETIME_FIELDS = ('start_time', 'end_time', 'created_at')
STANDARD_DATETIME_FIELDS = ('created_at', 'updated_at')

