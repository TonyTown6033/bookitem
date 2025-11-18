#!/usr/bin/env python3
"""
简单的 API 测试脚本
确保后端服务在 http://localhost:8000 运行
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_connection():
    """测试连接"""
    print_section("1. 测试服务器连接")
    try:
        response = requests.get("http://localhost:8000")
        print(f"✅ 服务器连接成功")
        print(f"   响应: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("   请确保后端服务已启动: uvicorn main:app --reload")
        return False

def test_users():
    """测试用户 API"""
    print_section("2. 测试用户管理 API")
    
    # 获取用户列表
    print("\n📋 获取用户列表...")
    response = requests.get(f"{BASE_URL}/users")
    users = response.json()
    print(f"   状态码: {response.status_code}")
    print(f"   用户数量: {len(users)}")
    if users:
        print(f"   第一个用户: {users[0]['username']} ({users[0]['email']})")
    
    # 创建新用户
    print("\n➕ 创建新用户...")
    new_user = {
        "username": f"testuser_{datetime.now().timestamp()}",
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "phone": "13900139999",
        "password": "test123456"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    if response.status_code == 200:
        user = response.json()
        print(f"   ✅ 创建成功! ID: {user['id']}, 用户名: {user['username']}")
        return user['id']
    else:
        print(f"   ❌ 创建失败: {response.json()}")
        return None

def test_rooms():
    """测试会议室 API"""
    print_section("3. 测试会议室管理 API")
    
    # 获取会议室列表
    print("\n📋 获取会议室列表...")
    response = requests.get(f"{BASE_URL}/rooms")
    rooms = response.json()
    print(f"   状态码: {response.status_code}")
    print(f"   会议室数量: {len(rooms)}")
    if rooms:
        print(f"   第一个会议室: {rooms[0]['name']} - {rooms[0]['location']}")
        print(f"   容纳人数: {rooms[0]['capacity']} 人")
    
    # 创建新会议室
    print("\n➕ 创建新会议室...")
    new_room = {
        "name": f"测试会议室_{datetime.now().strftime('%H%M%S')}",
        "location": "测试楼层",
        "capacity": 10,
        "description": "这是一个通过API测试创建的会议室"
    }
    response = requests.post(f"{BASE_URL}/rooms", json=new_room)
    if response.status_code == 200:
        room = response.json()
        print(f"   ✅ 创建成功! ID: {room['id']}, 名称: {room['name']}")
        return room['id']
    else:
        print(f"   ❌ 创建失败: {response.json()}")
        return None

def test_bookings(user_id=None, room_id=None):
    """测试预约 API"""
    print_section("4. 测试预约管理 API")
    
    # 获取预约列表
    print("\n📋 获取预约列表...")
    response = requests.get(f"{BASE_URL}/bookings")
    bookings = response.json()
    print(f"   状态码: {response.status_code}")
    print(f"   预约数量: {len(bookings)}")
    if bookings:
        booking = bookings[0]
        print(f"   第一个预约:")
        print(f"     用户: {booking['user']['username']}")
        print(f"     会议室: {booking['room']['name']}")
        print(f"     时间: {booking['start_time']} ~ {booking['end_time']}")
        print(f"     状态: {booking['status']}")
    
    # 如果没有提供用户ID和会议室ID，使用默认值
    if not user_id or not room_id:
        # 获取第一个用户和会议室
        users = requests.get(f"{BASE_URL}/users").json()
        rooms = requests.get(f"{BASE_URL}/rooms").json()
        if users and rooms:
            user_id = users[0]['id']
            room_id = rooms[0]['id']
    
    if user_id and room_id:
        # 创建新预约
        print("\n➕ 创建新预约...")
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=2)
        
        new_booking = {
            "user_id": user_id,
            "room_id": room_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "purpose": "API 测试预约"
        }
        
        response = requests.post(f"{BASE_URL}/bookings", json=new_booking)
        if response.status_code == 200:
            booking = response.json()
            print(f"   ✅ 创建成功! ID: {booking['id']}")
            print(f"   开始时间: {booking['start_time']}")
            print(f"   结束时间: {booking['end_time']}")
            return booking['id']
        else:
            print(f"   ❌ 创建失败: {response.json()}")
            return None
    else:
        print("   ⚠️  没有可用的用户或会议室，跳过创建预约")
        return None

def test_conflict_detection():
    """测试时间冲突检测"""
    print_section("5. 测试时间冲突检测")
    
    # 获取第一个用户和会议室
    users = requests.get(f"{BASE_URL}/users").json()
    rooms = requests.get(f"{BASE_URL}/rooms").json()
    
    if not users or not rooms:
        print("   ⚠️  没有足够的数据进行测试")
        return
    
    user_id = users[0]['id']
    room_id = rooms[0]['id']
    
    # 创建第一个预约
    print("\n➕ 创建第一个预约...")
    future_date = datetime.now() + timedelta(days=7)
    start_time = future_date.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=2)
    
    booking1 = {
        "user_id": user_id,
        "room_id": room_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "purpose": "冲突检测测试 - 第一个预约"
    }
    
    response1 = requests.post(f"{BASE_URL}/bookings", json=booking1)
    if response1.status_code == 200:
        print(f"   ✅ 第一个预约创建成功")
        booking_id = response1.json()['id']
        
        # 尝试创建冲突的预约
        print("\n➕ 尝试创建冲突的预约...")
        conflict_start = start_time + timedelta(minutes=30)
        conflict_end = end_time + timedelta(minutes=30)
        
        booking2 = {
            "user_id": user_id,
            "room_id": room_id,
            "start_time": conflict_start.isoformat(),
            "end_time": conflict_end.isoformat(),
            "purpose": "冲突检测测试 - 冲突预约"
        }
        
        response2 = requests.post(f"{BASE_URL}/bookings", json=booking2)
        if response2.status_code == 400:
            print(f"   ✅ 冲突检测成功! 系统正确拒绝了冲突预约")
            print(f"   错误信息: {response2.json()['detail']}")
        else:
            print(f"   ❌ 冲突检测失败! 系统允许了冲突预约")
        
        # 清理：删除测试预约
        print("\n🗑️  清理测试数据...")
        requests.delete(f"{BASE_URL}/bookings/{booking_id}")
        print("   ✅ 测试数据清理完成")
    else:
        print(f"   ❌ 第一个预约创建失败: {response1.json()}")

def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("      会议室预约系统 - API 测试脚本")
    print("🚀" * 30)
    
    # 测试连接
    if not test_connection():
        return
    
    # 测试各个模块
    user_id = test_users()
    room_id = test_rooms()
    booking_id = test_bookings(user_id, room_id)
    test_conflict_detection()
    
    # 总结
    print_section("✅ 测试完成")
    print("\n所有基础功能测试完成！")
    print("\n📖 更多测试方法:")
    print("   1. 访问 Swagger UI: http://localhost:8000/docs")
    print("   2. 查看测试文档: API_TESTING.md")
    print("   3. 使用 Postman 或其他 API 测试工具")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

