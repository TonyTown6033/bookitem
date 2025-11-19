"""
数据初始化脚本 - 创建测试数据
"""
from datetime import datetime, timedelta
from database import SessionLocal
from models import User, Room, Booking

def clear_all_data():
    """清空所有数据"""
    db = SessionLocal()
    try:
        print("🗑️  清空现有数据...")
        db.query(Booking).delete()
        db.query(Room).delete()
        db.query(User).delete()
        db.commit()
        print("✅ 数据已清空")
    except Exception as e:
        print(f"❌ 清空数据失败: {e}")
        db.rollback()
    finally:
        db.close()

def seed_users():
    """创建测试用户"""
    db = SessionLocal()
    try:
        print("\n👥 创建测试用户...")
        # 简单的密码哈希（生产环境应该使用 bcrypt）
        fake_password = "hashed_password_123"
        
        users = [
            User(username="张三", email="zhangsan@example.com", phone="13800138001", hashed_password=fake_password),
            User(username="李四", email="lisi@example.com", phone="13800138002", hashed_password=fake_password),
            User(username="王五", email="wangwu@example.com", phone="13800138003", hashed_password=fake_password),
            User(username="赵六", email="zhaoliu@example.com", phone="13800138004", hashed_password=fake_password),
            User(username="钱七", email="qianqi@example.com", phone="13800138005", hashed_password=fake_password),
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print(f"✅ 成功创建 {len(users)} 个用户")
        
        # 返回用户ID列表
        db.refresh(users[0])
        return [u.id for u in users]
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        db.rollback()
        return []
    finally:
        db.close()

def seed_rooms():
    """创建测试会议室"""
    db = SessionLocal()
    try:
        print("\n🏢 创建测试会议室...")
        rooms = [
            Room(
                name="大会议室",
                location="1楼101室",
                capacity=20,
                description="配备投影仪、白板、音响系统，适合大型会议和培训"
            ),
            Room(
                name="小会议室",
                location="2楼201室",
                capacity=6,
                description="配备电视、白板，适合小组讨论和一对一面谈"
            ),
            Room(
                name="视频会议室",
                location="3楼301室",
                capacity=10,
                description="配备高清摄像头、麦克风、大屏幕，适合远程视频会议"
            ),
            Room(
                name="培训室",
                location="2楼202室",
                capacity=30,
                description="配备投影仪、音响、可移动桌椅，适合培训和讲座"
            ),
            Room(
                name="讨论室A",
                location="3楼302室",
                capacity=4,
                description="安静的小型讨论空间，适合头脑风暴和快速会议"
            ),
            Room(
                name="讨论室B",
                location="3楼303室",
                capacity=4,
                description="安静的小型讨论空间，适合头脑风暴和快速会议"
            ),
        ]
        
        for room in rooms:
            db.add(room)
        
        db.commit()
        print(f"✅ 成功创建 {len(rooms)} 个会议室")
        
        # 返回会议室ID列表
        db.refresh(rooms[0])
        return [r.id for r in rooms]
    except Exception as e:
        print(f"❌ 创建会议室失败: {e}")
        db.rollback()
        return []
    finally:
        db.close()

def seed_bookings(user_ids, room_ids):
    """创建测试预约"""
    db = SessionLocal()
    try:
        print("\n📅 创建测试预约...")
        
        # 获取今天和未来几天的日期
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        bookings = []
        
        # 今天的预约
        bookings.extend([
            Booking(
                user_id=user_ids[0],
                room_id=room_ids[0],
                start_time=today.replace(hour=9, minute=0),
                end_time=today.replace(hour=11, minute=0),
                purpose="项目启动会 - 新项目启动会议，讨论项目目标和时间表",
                status="confirmed"
            ),
            Booking(
                user_id=user_ids[1],
                room_id=room_ids[1],
                start_time=today.replace(hour=14, minute=0),
                end_time=today.replace(hour=15, minute=30),
                purpose="产品评审 - 新版本产品功能评审",
                status="confirmed"
            ),
            Booking(
                user_id=user_ids[2],
                room_id=room_ids[2],
                start_time=today.replace(hour=10, minute=0),
                end_time=today.replace(hour=11, minute=0),
                purpose="设计评审会 - UI/UX设计方案评审",
                status="confirmed"
            ),
        ])
        
        # 明天的预约
        tomorrow = today + timedelta(days=1)
        bookings.extend([
            Booking(
                user_id=user_ids[3],
                room_id=room_ids[0],
                start_time=tomorrow.replace(hour=10, minute=0),
                end_time=tomorrow.replace(hour=12, minute=0),
                purpose="市场推广计划 - 下季度市场推广策略讨论",
                status="confirmed"
            ),
            Booking(
                user_id=user_ids[4],
                room_id=room_ids[3],
                start_time=tomorrow.replace(hour=14, minute=0),
                end_time=tomorrow.replace(hour=16, minute=0),
                purpose="新员工培训 - 新员工入职培训",
                status="confirmed"
            ),
        ])
        
        # 后天的预约
        day_after = today + timedelta(days=2)
        bookings.extend([
            Booking(
                user_id=user_ids[0],
                room_id=room_ids[1],
                start_time=day_after.replace(hour=13, minute=0),
                end_time=day_after.replace(hour=14, minute=0),
                purpose="一对一面谈 - 团队成员一对一沟通",
                status="confirmed"
            ),
            Booking(
                user_id=user_ids[1],
                room_id=room_ids[4],
                start_time=day_after.replace(hour=15, minute=0),
                end_time=day_after.replace(hour=16, minute=0),
                purpose="头脑风暴 - 产品创新想法讨论",
                status="confirmed"
            ),
        ])
        
        for booking in bookings:
            db.add(booking)
        
        db.commit()
        print(f"✅ 成功创建 {len(bookings)} 个预约")
    except Exception as e:
        print(f"❌ 创建预约失败: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 开始初始化数据...")
    print("=" * 60)
    
    # 清空现有数据
    clear_all_data()
    
    # 创建测试数据
    user_ids = seed_users()
    if not user_ids:
        print("❌ 用户创建失败，停止初始化")
        return
    
    room_ids = seed_rooms()
    if not room_ids:
        print("❌ 会议室创建失败，停止初始化")
        return
    
    seed_bookings(user_ids, room_ids)
    
    print("\n" + "=" * 60)
    print("✅ 数据初始化完成！")
    print("=" * 60)
    print(f"\n📊 数据统计:")
    print(f"   • 用户: {len(user_ids)} 个")
    print(f"   • 会议室: {len(room_ids)} 个")
    print(f"   • 预约: 已创建多个测试预约")
    print("\n💡 提示:")
    print("   • 访问 http://localhost:5173 查看前端")
    print("   • 访问 http://localhost:8000/docs 查看API文档")
    print("\n")

if __name__ == "__main__":
    main()

