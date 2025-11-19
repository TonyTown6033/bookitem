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
      <p class="intro">
        <span class="intro-desktop">选择会议室，然后在时间轴上拖动选择时间段进行预约</span>
        <span class="intro-mobile">点击会议室选择时间</span>
      </p>
    </el-card>

    <!-- 会议室列表 -->
    <div class="rooms-grid">
      <template v-for="room in availableRooms" :key="room.id">
        <!-- 会议室卡片 -->
        <div class="room-item">
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
        </div>
        
        <!-- 时间轴选择器（展开在当前会议室下方） -->
        <transition name="timeline-expand">
          <div 
            v-if="selectedRoom?.id === room.id" 
            class="timeline-wrapper"
          >
            <el-card class="timeline-card">
              <template #header>
                <div class="timeline-header">
                  <span>选择预约时间</span>
                  <el-button 
                    text 
                    @click.stop="closeTimeline"
                    :icon="Close"
                  >
                    关闭
                  </el-button>
                </div>
              </template>
              <TimelineSelector
                :room="selectedRoom"
                :bookings="roomBookings"
                @create-booking="showBookingDialog"
                @refresh="loadRoomBookings"
              />
            </el-card>
          </div>
        </transition>
      </template>
    </div>

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
import { OfficeBuilding, Location, User, List, Close } from '@element-plus/icons-vue'
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
  
  // 如果点击的是同一个会议室，则关闭时间轴
  if (selectedRoom.value?.id === room.id) {
    selectedRoom.value = null
    return
  }
  
  selectedRoom.value = room
  await loadRoomBookings()
}

const closeTimeline = () => {
  selectedRoom.value = null
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
    
    // 刷新预约列表（这会触发 TimelineSelector 更新）
    await loadRoomBookings()
    
    // 显示成功消息
    ElMessage.success('预约成功！')
    
    // 关闭对话框
    dialogVisible.value = false
    
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
  max-width: 1600px;
  margin: 0 auto;
  padding: 32px;
  background: linear-gradient(to bottom, #f7f9fc 0%, #ffffff 100%);
  min-height: 100vh;
}

.header-card {
  margin-bottom: 32px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header-card :deep(.el-card__header) {
  background: transparent;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  padding: 28px 32px;
}

.header-card :deep(.el-card__body) {
  padding: 24px 32px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  color: white;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.intro {
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  font-size: 16px;
  letter-spacing: 0.5px;
}

.intro-mobile {
  display: none;
}

.intro-desktop {
  display: inline;
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 28px;
}

.room-item {
  /* 会议室卡片容器 */
}

.room-card {
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  border: 3px solid #e8eaed;
  background: linear-gradient(to bottom, #ffffff, #f9fafb);
}

.room-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.2);
  border-color: #b8c5f0;
}

.room-card.selected {
  border-color: #667eea;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.35);
  background: linear-gradient(135deg, #f0f3ff 0%, #ffffff 100%);
}

.room-card.selected .room-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 16px;
  margin: -1px -1px 15px -1px;
}

.room-card.selected .room-header h3 {
  color: white;
}

.room-card.selected .room-header .el-icon {
  color: white;
}

.room-header {
  text-align: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e8eaed;
  transition: all 0.3s ease;
}

.room-header .el-icon {
  font-size: 42px;
  color: #667eea;
}

.room-header h3 {
  margin: 12px 0 0 0;
  color: #1a1a1a;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.room-details {
  margin-bottom: 16px;
  padding: 0 16px;
}

.room-details p {
  margin: 10px 0;
  color: #4a5568;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.room-details .el-icon {
  color: #667eea;
  font-size: 18px;
}

.room-details .description {
  color: #718096;
  font-size: 14px;
  line-height: 1.6;
  display: block;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 2px solid #f0f2f4;
  font-weight: 400;
}

.room-footer {
  display: flex;
  justify-content: center;
  padding: 0 16px 12px 16px;
}

.room-footer .el-button {
  border-radius: 10px;
  padding: 10px 28px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.room-card.selected .room-footer .el-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.room-card.selected .room-footer .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

/* 时间轴包装器 - 占据整行 */
.timeline-wrapper {
  grid-column: 1 / -1;
  margin: -12px 0 12px 0;
  animation: timeline-slide-down 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
  border: 3px solid #667eea;
  background: linear-gradient(to bottom, #ffffff, #fafbfc);
}

.timeline-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-weight: 600;
  font-size: 18px;
  padding: 20px 28px;
  letter-spacing: 0.5px;
  color: white;
  border-bottom: none;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.timeline-header .el-button {
  color: white;
  font-weight: 600;
}

.timeline-header .el-button:hover {
  color: #ffd04b;
}

/* 展开动画 */
.timeline-expand-enter-active {
  animation: timeline-expand-in 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-expand-leave-active {
  animation: timeline-expand-out 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes timeline-expand-in {
  from {
    opacity: 0;
    transform: translateY(-20px) scaleY(0.8);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0) scaleY(1);
    max-height: 1000px;
  }
}

@keyframes timeline-expand-out {
  from {
    opacity: 1;
    transform: translateY(0) scaleY(1);
    max-height: 1000px;
  }
  to {
    opacity: 0;
    transform: translateY(-20px) scaleY(0.8);
    max-height: 0;
  }
}

@keyframes timeline-slide-down {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.capacity-hint {
  margin-left: 12px;
  color: #718096;
  font-size: 15px;
  font-weight: 500;
}

/* 优化弹窗样式 */
:deep(.el-dialog) {
  border-radius: 16px;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px 32px;
  border-radius: 16px 16px 0 0;
}

:deep(.el-dialog__title) {
  color: white;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 24px;
}

:deep(.el-dialog__body) {
  padding: 32px;
  background: linear-gradient(to bottom, #fafbfc, #ffffff);
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #2d3748;
  font-size: 15px;
  letter-spacing: 0.3px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 2px solid #e8eaed;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #b8c5f0;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

:deep(.el-textarea__inner) {
  border-radius: 10px;
  border: 2px solid #e8eaed;
  transition: all 0.3s ease;
}

:deep(.el-textarea__inner:hover) {
  border-color: #b8c5f0;
}

:deep(.el-textarea__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-button) {
  border-radius: 10px;
  padding: 12px 32px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

:deep(.el-alert) {
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .room-booking-page {
    padding: 12px;
    background: #f5f7fa;
  }
  
  .header-card {
    margin-bottom: 16px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
  
  .header-card :deep(.el-card__header) {
    padding: 12px 16px;
  }
  
  .header-card :deep(.el-card__body) {
    padding: 12px 16px;
  }
  
  .card-header {
    flex-direction: row;
    gap: 8px;
    align-items: center;
    font-size: 16px;
  }
  
  .card-header span {
    flex: 1;
    font-size: 16px;
  }
  
  .card-header .el-button {
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .card-header .el-button .el-icon {
    font-size: 14px;
  }
  
  .intro {
    font-size: 13px;
    line-height: 1.5;
  }
  
  .intro-mobile {
    display: inline;
  }
  
  .intro-desktop {
    display: none;
  }
  
  .rooms-grid {
    grid-template-columns: 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .room-item {
    width: 100%;
    max-width: 100%;
  }
  
  .room-card {
    border-radius: 10px;
    border-width: 2px;
    padding: 0;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }
  
  .room-card :deep(.el-card__body) {
    padding: 12px;
    width: 100%;
    box-sizing: border-box;
  }
  
  .room-card:hover {
    transform: none;
  }
  
  .room-card.selected {
    width: 100%;
    max-width: 100%;
  }
  
  .room-card.selected:hover {
    transform: none;
  }
  
  .room-header {
    margin-bottom: 10px;
    padding-bottom: 10px;
    flex-direction: row;
    display: flex;
    align-items: center;
    gap: 10px;
    text-align: left;
  }
  
  .room-header .el-icon {
    font-size: 24px !important;
    flex-shrink: 0;
  }
  
  .room-header h3 {
    font-size: 15px;
    margin: 0;
  }
  
  .room-card.selected .room-header {
    margin: -12px -12px 10px -12px;
    padding: 10px 12px;
  }
  
  .room-details {
    padding: 0;
  }
  
  .room-details p {
    font-size: 12px;
    margin: 6px 0;
  }
  
  .room-details .el-icon {
    font-size: 14px;
  }
  
  .room-details .description {
    font-size: 12px;
    margin-top: 8px;
    padding-top: 8px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .room-footer {
    padding: 8px 0 0 0;
    justify-content: flex-start;
  }
  
  .room-footer .el-tag {
    font-size: 11px;
    padding: 2px 8px;
    height: auto;
  }
  
  .timeline-wrapper {
    margin: 0 0 12px 0;
  }
  
  .timeline-card {
    border-radius: 10px;
    border-width: 2px;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.12);
  }
  
  .timeline-card :deep(.el-card__header) {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .timeline-card :deep(.el-card__body) {
    padding: 0;
  }
  
  .timeline-header {
    font-size: 14px;
  }
  
  .timeline-header .el-button {
    padding: 6px 12px;
    font-size: 12px;
  }
  
  :deep(.el-dialog__header) {
    padding: 16px 20px 12px;
  }
  
  :deep(.el-dialog__title) {
    font-size: 18px;
  }
  
  :deep(.el-dialog__body) {
    padding: 16px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 16px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 13px;
    padding-bottom: 4px;
  }
  
  :deep(.el-button) {
    padding: 10px 20px;
    font-size: 14px;
  }
}

/* 平板适配 */
@media (max-width: 1024px) and (min-width: 769px) {
  .rooms-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 大屏幕适配 */
@media (min-width: 1400px) {
  .rooms-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>

