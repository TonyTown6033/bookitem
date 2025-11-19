# 时区问题修复说明

## 问题描述

创建会议预约时出现错误：

```
TypeError: can't compare offset-naive and offset-aware datetimes
```

### 错误日志位置
```
File: backend/routers/bookings.py, line 48
Code: if booking.start_time < datetime.now():
```

## 问题原因

1. **前端发送的时间**：带有时区信息（ISO 8601格式）
   ```javascript
   // 前端 JavaScript
   new Date().toISOString()
   // 输出: "2025-11-19T14:00:00.000Z"  (带时区Z)
   ```

2. **后端比较的时间**：没有时区信息
   ```python
   # 后端 Python
   datetime.now()
   # 输出: 2025-11-19 14:00:00  (无时区信息)
   ```

3. **Python 限制**：无法比较带时区和不带时区的 datetime 对象

## 修复方案

### 修改文件：`backend/routers/bookings.py`

#### 1. 导入时区模块

```python
from datetime import datetime, timezone  # 添加 timezone
```

#### 2. 添加工具函数

```python
def make_aware(dt):
    """将 naive datetime 转换为 aware datetime (UTC)"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

def get_current_time():
    """获取当前时间（UTC，带时区信息）"""
    return datetime.now(timezone.utc)
```

#### 3. 修改预约创建逻辑

```python
# 修改前
if booking.start_time < datetime.now():
    raise HTTPException(status_code=400, detail="不能预约过去的时间")

# 修改后
# 处理时区问题
start_time = make_aware(booking.start_time) if booking.start_time.tzinfo is None else booking.start_time
end_time = make_aware(booking.end_time) if booking.end_time.tzinfo is None else booking.end_time

# 验证时间
if start_time < get_current_time():
    raise HTTPException(status_code=400, detail="不能预约过去的时间")

# 存储到数据库（移除时区信息）
db_booking = Booking(
    user_id=booking.user_id,
    room_id=booking.room_id,
    start_time=start_time.replace(tzinfo=None),
    end_time=end_time.replace(tzinfo=None),
    purpose=booking.purpose,
    status="confirmed"
)
```

## 技术细节

### Aware vs Naive DateTime

- **Naive DateTime**：不包含时区信息
  ```python
  datetime(2025, 11, 19, 14, 0, 0)  # 无时区
  ```

- **Aware DateTime**：包含时区信息
  ```python
  datetime(2025, 11, 19, 14, 0, 0, tzinfo=timezone.utc)  # UTC时区
  ```

### 时区处理流程

```
前端 (JavaScript)
    ↓ toISOString()
带时区的ISO字符串 ("2025-11-19T14:00:00Z")
    ↓ FastAPI/Pydantic 解析
Aware DateTime (带时区)
    ↓ make_aware() 确保有时区
统一的 Aware DateTime
    ↓ 业务逻辑处理
    ↓ replace(tzinfo=None)
Naive DateTime (存入数据库)
```

### 为什么数据库存储 Naive DateTime？

1. **SQLite 不原生支持时区**
2. **简化数据存储**
3. **UTC 作为标准时间**
4. **应用层处理时区转换**

## 测试验证

### 测试代码

```python
import requests
from datetime import datetime, timedelta, timezone

# 创建明天的预约
tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(hours=2)

booking_data = {
    "user_id": 1,
    "room_id": 1,
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
    "purpose": "测试预约"
}

response = requests.post('http://localhost:8000/api/bookings/', json=booking_data)
print(f"状态码: {response.status_code}")
print(f"结果: {response.json()}")
```

### 预期结果

```
✅ 状态码: 200
✅ 结果: {"id": 10, "user_id": 1, "room_id": 1, ...}
```

## 日志检查

### 修复前的错误日志

```
ERROR:    Exception in ASGI application
...
TypeError: can't compare offset-naive and offset-aware datetimes
```

### 修复后的正常日志

```
INFO:     127.0.0.1:58705 - "POST /api/bookings/ HTTP/1.1" 200 OK
```

## 最佳实践

### 1. 统一使用 UTC 时区

```python
# 推荐
datetime.now(timezone.utc)

# 不推荐
datetime.now()  # 系统本地时区，可能导致问题
```

### 2. API 时间格式

- **接收**：支持 ISO 8601 格式（带时区）
- **返回**：统一返回 ISO 8601 格式
- **存储**：数据库存储 UTC 时间（naive）

### 3. 前端时间处理

```javascript
// 发送时间到后端
const time = new Date(selectedTime).toISOString()

// 显示时间给用户
const localTime = new Date(booking.start_time).toLocaleString('zh-CN')
```

## 相关文件

- `backend/routers/bookings.py` - 预约路由（已修复）
- `frontend/src/components/TimelineSelector.vue` - 时间选择组件
- `frontend/src/views/RoomBooking.vue` - 预约页面

## 常见问题

### Q: 为什么不在数据库中存储时区？

A: 
1. SQLite 不原生支持时区
2. 统一存储 UTC 时间更简单
3. 时区转换在应用层处理更灵活

### Q: 如何处理不同时区的用户？

A: 
1. 后端统一使用 UTC
2. 前端根据用户浏览器时区显示
3. JavaScript 的 Date 对象会自动处理

### Q: 时间显示不正确怎么办？

A: 
1. 检查前端是否使用 `toLocaleString()`
2. 确认后端返回的是 UTC 时间
3. 验证浏览器时区设置

## 版本历史

- **v1.1.0** (2025-11-19) - 添加时区处理
- **v1.0.0** (2025-11-19) - 初始版本

## 测试检查清单

- [x] 创建预约成功
- [x] 时间比较正常
- [x] 不能预约过去时间
- [x] 时区转换正确
- [x] 数据库存储正确
- [x] 前端显示正确
- [x] 无错误日志

---

**修复完成时间**: 2025-11-19  
**修复状态**: ✅ 已完成并测试通过

