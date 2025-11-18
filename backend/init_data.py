"""
初始化示例数据脚本
运行此脚本将创建测试用户、会议室和预约数据
"""
from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models import User, Room, Booking
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database():
    """初始化数据库"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")

def clear_data(db):
    """清除现有数据"""
    print("清除现有数据...")
    db.query(Booking).delete()
    db.query(User).delete()
    db.query(Room).delete()
    db.commit()
    print("✅ 数据清除完成")

def create_users(db):
    """创建测试用户"""
    print("\n创建测试用户...")
    users = [
        User(
            username="admin",
            email="admin@example.com",
            phone="13800138000",
            hashed_password=pwd_context.hash("admin123"),
            is_active=True
        ),
        User(
            username="zhangsan",
            email="zhangsan@example.com",
            phone="13800138001",
            hashed_password=pwd_context.hash("123456"),
            is_active=True
        ),
        User(
            username="lisi",
            email="lisi@example.com",
            phone="13800138002",
            hashed_password=pwd_context.hash("123456"),
            is_active=True
        ),
        User(
            username="wangwu",
            email="wangwu@example.com",
            phone="13800138003",
            hashed_password=pwd_context.hash("123456"),
            is_active=True
        )
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    print(f"✅ 成功创建 {len(users)} 个用户")
    return users

def create_rooms(db):
    """创建测试会议室"""
    print("\n创建测试会议室...")
    rooms = [
        Room(
            name="大会议室",
            location="1楼101室",
            capacity=20,
            description="配备投影仪、白板、音响系统，适合大型会议和培训",
            is_available=True
        ),
        Room(
            name="小会议室A",
            location="2楼201室",
            capacity=8,
            description="配备电视屏幕、白板，适合小组讨论",
            is_available=True
        ),
        Room(
            name="小会议室B",
            location="2楼202室",
            capacity=8,
            description="配备电视屏幕、白板，适合小组讨论",
            is_available=True
        ),
        Room(
            name="视频会议室",
            location="3楼301室",
            capacity=12,
            description="配备专业视频会议设备，支持远程会议",
            is_available=True
        ),
        Room(
            name="培训室",
            location="3楼302室",
            capacity=30,
            description="配备投影仪、音响、话筒，适合培训和讲座",
            is_available=True
        ),
        Room(
            name="头脑风暴室",
            location="4楼401室",
            capacity=6,
            description="轻松舒适的环境，配备白板和便签，适合创意讨论",
            is_available=True
        )
    ]
    
    for room in rooms:
        db.add(room)
    
    db.commit()
    print(f"✅ 成功创建 {len(rooms)} 个会议室")
    return rooms

def create_bookings(db, users, rooms):
    """创建测试预约"""
    print("\n创建测试预约...")
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    bookings = [
        # 今天的预约
        Booking(
            user_id=users[0].id,
            room_id=rooms[0].id,
            start_time=today + timedelta(hours=9),
            end_time=today + timedelta(hours=11),
            purpose="项目启动会议",
            status="confirmed"
        ),
        Booking(
            user_id=users[1].id,
            room_id=rooms[1].id,
            start_time=today + timedelta(hours=10),
            end_time=today + timedelta(hours=11),
            purpose="团队周会",
            status="confirmed"
        ),
        Booking(
            user_id=users[2].id,
            room_id=rooms[0].id,
            start_time=today + timedelta(hours=14),
            end_time=today + timedelta(hours=16),
            purpose="客户需求评审",
            status="confirmed"
        ),
        
        # 明天的预约
        Booking(
            user_id=users[0].id,
            room_id=rooms[3].id,
            start_time=today + timedelta(days=1, hours=9),
            end_time=today + timedelta(days=1, hours=10),
            purpose="远程会议",
            status="confirmed"
        ),
        Booking(
            user_id=users[1].id,
            room_id=rooms[2].id,
            start_time=today + timedelta(days=1, hours=13),
            end_time=today + timedelta(days=1, hours=15),
            purpose="技术分享会",
            status="confirmed"
        ),
        
        # 后天的预约
        Booking(
            user_id=users[2].id,
            room_id=rooms[4].id,
            start_time=today + timedelta(days=2, hours=9),
            end_time=today + timedelta(days=2, hours=12),
            purpose="新员工培训",
            status="confirmed"
        ),
        Booking(
            user_id=users[3].id,
            room_id=rooms[5].id,
            start_time=today + timedelta(days=2, hours=14),
            end_time=today + timedelta(days=2, hours=16),
            purpose="产品创意讨论",
            status="confirmed"
        ),
        
        # 一个取消的预约
        Booking(
            user_id=users[1].id,
            room_id=rooms[1].id,
            start_time=today + timedelta(days=3, hours=10),
            end_time=today + timedelta(days=3, hours=11),
            purpose="临时会议（已取消）",
            status="cancelled"
        )
    ]
    
    for booking in bookings:
        db.add(booking)
    
    db.commit()
    print(f"✅ 成功创建 {len(bookings)} 条预约记录")
    return bookings

def main():
    """主函数"""
    print("=" * 50)
    print("会议室预约系统 - 示例数据初始化")
    print("=" * 50)
    
    # 初始化数据库
    init_database()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 清除现有数据
        clear_data(db)
        
        # 创建测试数据
        users = create_users(db)
        rooms = create_rooms(db)
        bookings = create_bookings(db, users, rooms)
        
        print("\n" + "=" * 50)
        print("🎉 示例数据初始化完成！")
        print("=" * 50)
        print("\n测试账号信息：")
        print("-" * 50)
        print("用户名: admin     | 密码: admin123")
        print("用户名: zhangsan  | 密码: 123456")
        print("用户名: lisi      | 密码: 123456")
        print("用户名: wangwu    | 密码: 123456")
        print("-" * 50)
        print(f"\n📊 数据统计：")
        print(f"   - 用户数量: {len(users)}")
        print(f"   - 会议室数量: {len(rooms)}")
        print(f"   - 预约数量: {len(bookings)}")
        print("\n现在可以启动系统进行测试了！")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

