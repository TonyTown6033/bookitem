<template>
  <div class="room-booking-page">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>会议室预约</span>
          <el-button @click="$router.push('/bookings')">
            <el-icon><List /></el-icon>
            查看所有预约
          </el-button>
        </div>
      </template>
      <p class="intro">选择会议室，然后在时间轴上拖动选择时间段进行预约</p>
    </el-card>

    <!-- 会议室列表 -->
    <el-row :gutter="20" class="rooms-row">
      <el-col 
        v-for="room in availableRooms" 
        :key="room.id" 
        :xs="24" 
        :sm="12" 
        :md="8" 
        :lg="6"
      >
        <el-card 
          class="room-card" 
          :class="{ selected: selectedRoom?.id === room.id }"
          shadow="hover"
          @click="selectRoom(room)"
        >
          <div class="room-header">
            <el-icon size="32" color="#409EFF"><OfficeBuilding /></el-icon>
            <h3>{{ room.name }}</h3>
          </div>
          <div class="room-details">
            <p><el-icon><Location /></el-icon> {{ room.location }}</p>
            <p><el-icon><User /></el-icon> {{ room.capacity }} 人</p>
            <p class="description">{{ room.description }}</p>
          </div>
          <div class="room-footer">
            <el-tag v-if="room.is_available" type="success" size="small">可用</el-tag>
            <el-tag v-else type="danger" size="small">不可用</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 时间轴选择器 -->
    <el-card v-if="selectedRoom" class="timeline-card">
      <TimelineSelector
        :room="selectedRoom"
        :bookings="roomBookings"
        @create-booking="showBookingDialog"
        @refresh="loadRoomBookings"
      />
    </el-card>

    <!-- 创建预约对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="确认预约信息" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="bookingForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="会议室">
          <el-input :value="selectedRoom?.name" disabled />
        </el-form-item>
        
        <el-form-item label="预约时间">
          <el-input 
            :value="formatBookingTime()" 
            disabled 
          />
        </el-form-item>
        
        <el-form-item label="预约人" prop="user_id">
          <el-select 
            v-model="bookingForm.user_id" 
            placeholder="请选择预约人" 
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="`${user.username} (${user.email})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="会议主题" prop="purpose">
          <el-input
            v-model="bookingForm.purpose"
            placeholder="请输入会议主题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="会议描述">
          <el-input
            v-model="bookingForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入会议描述、议程等信息（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="参与人数">
          <el-input-number 
            v-model="bookingForm.attendees" 
            :min="1" 
            :max="selectedRoom?.capacity || 100"
          />
          <span class="capacity-hint">
            / {{ selectedRoom?.capacity }} 人
          </span>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBooking" :loading="submitting">
          确认预约
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { OfficeBuilding, Location, User, List } from '@element-plus/icons-vue'
import TimelineSelector from '@/components/TimelineSelector.vue'
import { roomAPI, bookingAPI, userAPI } from '@/api'

const rooms = ref([])
const users = ref([])
const selectedRoom = ref(null)
const roomBookings = ref([])
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const bookingForm = ref({
  user_id: null,
  room_id: null,
  start_time: null,
  end_time: null,
  purpose: '',
  description: '',
  attendees: 1
})

const rules = {
  user_id: [
    { required: true, message: '请选择预约人', trigger: 'change' }
  ],
  purpose: [
    { required: true, message: '请输入会议主题', trigger: 'blur' }
  ]
}

const availableRooms = computed(() => {
  return rooms.value.filter(room => room.is_available)
})

const loadRooms = async () => {
  try {
    rooms.value = await roomAPI.getRooms()
  } catch (error) {
    ElMessage.error('加载会议室列表失败')
  }
}

const loadUsers = async () => {
  try {
    users.value = await userAPI.getUsers()
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  }
}

const selectRoom = async (room) => {
  if (!room.is_available) {
    ElMessage.warning('该会议室当前不可用')
    return
  }
  
  selectedRoom.value = room
  await loadRoomBookings()
}

const loadRoomBookings = async () => {
  if (!selectedRoom.value) return
  
  try {
    roomBookings.value = await bookingAPI.getRoomBookings(selectedRoom.value.id)
  } catch (error) {
    ElMessage.error('加载预约信息失败')
  }
}

const showBookingDialog = (timeSlot) => {
  bookingForm.value = {
    user_id: null,
    room_id: selectedRoom.value.id,
    start_time: timeSlot.start_time,
    end_time: timeSlot.end_time,
    purpose: '',
    description: '',
    attendees: 1
  }
  dialogVisible.value = true
}

const formatBookingTime = () => {
  if (!bookingForm.value.start_time || !bookingForm.value.end_time) return ''
  
  const start = new Date(bookingForm.value.start_time)
  const end = new Date(bookingForm.value.end_time)
  
  const dateStr = start.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  })
  
  const timeStr = `${start.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })} - ${end.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })}`
  
  const duration = Math.round((end - start) / (1000 * 60))
  
  return `${dateStr} ${timeStr} (${duration}分钟)`
}

const submitBooking = async () => {
  try {
    await formRef.value.validate()
    
    submitting.value = true
    
    const data = {
      user_id: bookingForm.value.user_id,
      room_id: bookingForm.value.room_id,
      start_time: bookingForm.value.start_time.toISOString(),
      end_time: bookingForm.value.end_time.toISOString(),
      purpose: bookingForm.value.purpose
    }
    
    await bookingAPI.createBooking(data)
    
    ElMessage.success('预约成功！')
    dialogVisible.value = false
    
    // 刷新预约列表
    await loadRoomBookings()
    
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else if (error instanceof Error && !error.message.includes('validation')) {
      ElMessage.error('创建预约失败')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadRooms()
  loadUsers()
})
</script>

<style scoped>
.room-booking-page {
  max-width: 1400px;
  margin: 0 auto;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.intro {
  color: #606266;
  margin: 0;
  font-size: 14px;
}

.rooms-row {
  margin-bottom: 20px;
}

.room-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  margin-bottom: 20px;
}

.room-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.room-card.selected {
  border: 2px solid #409EFF;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.room-header {
  text-align: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.room-header h3 {
  margin: 10px 0 0 0;
  color: #303133;
  font-size: 18px;
}

.room-details {
  margin-bottom: 15px;
}

.room-details p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.room-details .description {
  color: #909399;
  font-size: 13px;
  line-height: 1.5;
  display: block;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.room-footer {
  display: flex;
  justify-content: center;
}

.timeline-card {
  margin-top: 20px;
}

.capacity-hint {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}
</style>

