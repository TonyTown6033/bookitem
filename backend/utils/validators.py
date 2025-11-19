"""
数据验证器模块
集中管理所有数据验证逻辑
"""

from datetime import datetime
from fastapi import HTTPException

from utils.timezone import get_current_time


def validate_time_range(start_time: datetime, end_time: datetime) -> None:
    """
    验证时间范围
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        
    Raises:
        HTTPException: 时间范围无效时抛出
    """
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="开始时间必须早于结束时间"
        )


def validate_future_time(time: datetime) -> None:
    """
    验证时间是否在未来
    
    Args:
        time: 要验证的时间
        
    Raises:
        HTTPException: 时间在过去时抛出
    """
    if time < get_current_time():
        raise HTTPException(
            status_code=400,
            detail="不能预约过去的时间"
        )


def validate_positive_number(value: int, field_name: str = "值") -> None:
    """
    验证正整数
    
    Args:
        value: 要验证的值
        field_name: 字段名称（用于错误消息）
        
    Raises:
        HTTPException: 值不是正整数时抛出
    """
    if value <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"{field_name}必须是正整数"
        )


def validate_string_not_empty(value: str, field_name: str = "字段") -> None:
    """
    验证字符串非空
    
    Args:
        value: 要验证的字符串
        field_name: 字段名称（用于错误消息）
        
    Raises:
        HTTPException: 字符串为空时抛出
    """
    if not value or not value.strip():
        raise HTTPException(
            status_code=400,
            detail=f"{field_name}不能为空"
        )


def validate_email_format(email: str) -> None:
    """
    验证邮箱格式（简单验证）
    
    Args:
        email: 邮箱地址
        
    Raises:
        HTTPException: 邮箱格式无效时抛出
    """
    if not email or '@' not in email or '.' not in email.split('@')[1]:
        raise HTTPException(
            status_code=400,
            detail="邮箱格式无效"
        )

