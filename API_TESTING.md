# API 测试指南

本文档提供了使用 curl 命令测试 API 接口的示例。

## 前提条件

- 后端服务已启动（http://localhost:8000）
- 已运行 `python backend/init_data.py` 初始化测试数据

## 用户管理 API

### 1. 获取所有用户

```bash
curl -X GET "http://localhost:8000/api/users"
```

### 2. 获取指定用户

```bash
curl -X GET "http://localhost:8000/api/users/1"
```

### 3. 创建新用户

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "phone": "13900139000",
    "password": "test123456"
  }'
```

### 4. 删除用户

```bash
curl -X DELETE "http://localhost:8000/api/users/5"
```

## 会议室管理 API

### 1. 获取所有会议室

```bash
curl -X GET "http://localhost:8000/api/rooms"
```

### 2. 获取指定会议室

```bash
curl -X GET "http://localhost:8000/api/rooms/1"
```

### 3. 创建新会议室

```bash
curl -X POST "http://localhost:8000/api/rooms" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试会议室",
    "location": "5楼501室",
    "capacity": 15,
    "description": "用于测试的会议室"
  }'
```

### 4. 更新会议室

```bash
curl -X PUT "http://localhost:8000/api/rooms/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "大会议室（已更新）",
    "location": "1楼101室",
    "capacity": 25,
    "description": "更新后的描述"
  }'
```

### 5. 删除会议室

```bash
curl -X DELETE "http://localhost:8000/api/rooms/7"
```

## 预约管理 API

### 1. 获取所有预约

```bash
curl -X GET "http://localhost:8000/api/bookings"
```

### 2. 获取指定预约

```bash
curl -X GET "http://localhost:8000/api/bookings/1"
```

### 3. 获取用户的预约

```bash
curl -X GET "http://localhost:8000/api/bookings/user/1"
```

### 4. 获取会议室的预约

```bash
curl -X GET "http://localhost:8000/api/bookings/room/1"
```

### 5. 创建新预约

```bash
# 获取明天的日期时间（示例）
TOMORROW=$(date -v+1d '+%Y-%m-%dT10:00:00')
END_TIME=$(date -v+1d '+%Y-%m-%dT12:00:00')

curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": 1,
    \"room_id\": 2,
    \"start_time\": \"${TOMORROW}\",
    \"end_time\": \"${END_TIME}\",
    \"purpose\": \"测试预约\"
  }"
```

或者使用固定时间：

```bash
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "room_id": 2,
    "start_time": "2025-12-01T10:00:00",
    "end_time": "2025-12-01T12:00:00",
    "purpose": "测试预约"
  }'
```

### 6. 取消预约

```bash
curl -X PUT "http://localhost:8000/api/bookings/1/cancel"
```

### 7. 删除预约

```bash
curl -X DELETE "http://localhost:8000/api/bookings/9"
```

## 测试场景

### 场景1：时间冲突检测

```bash
# 第一步：创建一个预约
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "room_id": 1,
    "start_time": "2025-12-15T10:00:00",
    "end_time": "2025-12-15T12:00:00",
    "purpose": "第一个预约"
  }'

# 第二步：尝试创建冲突的预约（应该失败）
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "room_id": 1,
    "start_time": "2025-12-15T11:00:00",
    "end_time": "2025-12-15T13:00:00",
    "purpose": "冲突的预约"
  }'
```

预期结果：第二个请求应该返回 400 错误，提示时间冲突。

### 场景2：验证数据有效性

```bash
# 尝试创建用户名重复的用户（应该失败）
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "newadmin@example.com",
    "password": "123456"
  }'
```

预期结果：返回 400 错误，提示用户名已存在。

### 场景3：创建过去时间的预约

```bash
# 尝试预约过去的时间（应该失败）
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "room_id": 1,
    "start_time": "2020-01-01T10:00:00",
    "end_time": "2020-01-01T12:00:00",
    "purpose": "过去的预约"
  }'
```

预期结果：返回 400 错误，提示不能预约过去的时间。

## 使用 Swagger UI 测试

访问 http://localhost:8000/docs 可以使用交互式 API 文档进行测试。

### Swagger UI 优势

1. **可视化界面**：友好的图形界面
2. **自动验证**：自动进行请求验证
3. **在线测试**：直接在浏览器中测试
4. **查看响应**：实时查看响应结果
5. **模型展示**：清晰展示数据模型

## Python 测试脚本示例

创建一个 `test_api.py` 文件：

```python
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def test_create_user():
    """测试创建用户"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13900139000",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/users", json=data)
    print(f"创建用户: {response.status_code}")
    print(response.json())

def test_get_rooms():
    """测试获取会议室列表"""
    response = requests.get(f"{BASE_URL}/rooms")
    print(f"获取会议室: {response.status_code}")
    rooms = response.json()
    print(f"共有 {len(rooms)} 个会议室")

def test_create_booking():
    """测试创建预约"""
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=14, minute=0, second=0)
    end_time = start_time + timedelta(hours=2)
    
    data = {
        "user_id": 1,
        "room_id": 1,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "purpose": "Python脚本测试预约"
    }
    
    response = requests.post(f"{BASE_URL}/bookings", json=data)
    print(f"创建预约: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    test_get_rooms()
    test_create_user()
    test_create_booking()
```

运行测试：

```bash
python test_api.py
```

## JavaScript 测试示例

```javascript
// 使用 fetch API
async function testAPI() {
  // 获取会议室列表
  const rooms = await fetch('http://localhost:8000/api/rooms')
    .then(res => res.json());
  console.log('会议室列表:', rooms);
  
  // 创建用户
  const user = await fetch('http://localhost:8000/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'jstest',
      email: 'jstest@example.com',
      password: 'test123'
    })
  }).then(res => res.json());
  console.log('创建用户:', user);
  
  // 创建预约
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(15, 0, 0, 0);
  
  const endTime = new Date(tomorrow);
  endTime.setHours(17, 0, 0, 0);
  
  const booking = await fetch('http://localhost:8000/api/bookings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 1,
      room_id: 1,
      start_time: tomorrow.toISOString(),
      end_time: endTime.toISOString(),
      purpose: 'JavaScript测试预约'
    })
  }).then(res => res.json());
  console.log('创建预约:', booking);
}

testAPI();
```

## 常见响应代码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |

## 错误处理示例

所有错误响应都包含 `detail` 字段：

```json
{
  "detail": "用户名已存在"
}
```

或

```json
{
  "detail": "该时间段已被预约"
}
```

## 性能测试

使用 Apache Bench 进行简单的性能测试：

```bash
# 测试获取会议室列表的性能（100次请求，10个并发）
ab -n 100 -c 10 http://localhost:8000/api/rooms
```

## 自动化测试建议

1. 使用 pytest 编写单元测试
2. 使用 pytest-asyncio 测试异步代码
3. 使用 httpx 作为测试客户端
4. 使用测试数据库（避免污染生产数据）
5. 测试覆盖率目标：80%+

## 总结

- ✅ 使用 Swagger UI 进行快速交互式测试
- ✅ 使用 curl 进行命令行测试
- ✅ 使用编程语言编写自动化测试脚本
- ✅ 关注边界条件和异常情况测试
- ✅ 进行性能测试确保系统稳定性

