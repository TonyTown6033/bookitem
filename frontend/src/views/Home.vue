<template>
  <div class="home">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <el-icon size="24"><Calendar /></el-icon>
          <span>欢迎使用会议室预约系统</span>
        </div>
      </template>
      <div class="welcome-content">
        <p class="intro">本系统为您提供便捷的会议室预约服务</p>
        <el-row :gutter="20" class="stats-row">
          <el-col :span="8">
            <el-statistic title="会议室总数" :value="stats.totalRooms">
              <template #prefix>
                <el-icon><OfficeBuilding /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="8">
            <el-statistic title="今日预约" :value="stats.todayBookings">
              <template #prefix>
                <el-icon><Document /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="8">
            <el-statistic title="注册用户" :value="stats.totalUsers">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-statistic>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-row :gutter="20" class="feature-row">
      <el-col :span="6">
        <el-card shadow="hover" class="feature-card highlight" @click="$router.push('/booking')">
          <el-icon size="48" color="#409EFF"><Calendar /></el-icon>
          <h3>会议室预约</h3>
          <p>可视化时间轴，快速预约会议室</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/bookings')">
          <el-icon size="48" color="#67C23A"><Document /></el-icon>
          <h3>预约记录</h3>
          <p>查看和管理所有预约记录</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/rooms')">
          <el-icon size="48" color="#E6A23C"><OfficeBuilding /></el-icon>
          <h3>会议室管理</h3>
          <p>添加、编辑和管理会议室</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/users')">
          <el-icon size="48" color="#909399"><User /></el-icon>
          <h3>用户管理</h3>
          <p>管理系统用户信息</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Calendar, OfficeBuilding, Document, User } from '@element-plus/icons-vue'
import { roomAPI, bookingAPI, userAPI } from '@/api'

const stats = ref({
  totalRooms: 0,
  todayBookings: 0,
  totalUsers: 0
})

const loadStats = async () => {
  try {
    const [rooms, bookings, users] = await Promise.all([
      roomAPI.getRooms(),
      bookingAPI.getBookings(),
      userAPI.getUsers()
    ])
    
    stats.value.totalRooms = rooms.length
    stats.value.totalUsers = users.length
    
    // 计算今日预约
    const today = new Date().toDateString()
    stats.value.todayBookings = bookings.filter(booking => {
      const bookingDate = new Date(booking.start_time).toDateString()
      return bookingDate === today
    }).length
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
}

.welcome-content {
  text-align: center;
}

.intro {
  font-size: 16px;
  color: #606266;
  margin-bottom: 30px;
}

.stats-row {
  margin-top: 20px;
}

.feature-row {
  margin-top: 20px;
}

.feature-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  padding: 30px 20px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.feature-card.highlight {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2px solid #409EFF;
}

.feature-card.highlight:hover {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
}

.feature-card h3 {
  margin: 15px 0 10px;
  color: #303133;
}

.feature-card p {
  color: #909399;
  font-size: 14px;
}
</style>

