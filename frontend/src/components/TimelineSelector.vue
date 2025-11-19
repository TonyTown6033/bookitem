<template>
  <div class="timeline-selector">
    <div class="room-info">
      <h3>{{ room.name }}</h3>
      <p>{{ room.location }} | 容纳 {{ room.capacity }} 人</p>
    </div>

    <div class="date-selector">
      <el-date-picker
        v-model="selectedDate"
        type="date"
        placeholder="选择日期"
        :disabled-date="disabledDate"
        @change="loadBookings"
      />
    </div>

    <div class="timeline-container">
      <div class="time-labels">
        <div v-for="hour in 24" :key="hour" class="time-label">
          {{ formatHour(hour - 1) }}
        </div>
      </div>

      <div 
        class="timeline-track"
        @mousedown="startSelection"
        @mousemove="updateSelection"
        @mouseup="endSelection"
        @mouseleave="cancelSelection"
      >
        <!-- 过去的时间段（灰色，不可用） -->
        <div
          v-if="pastTimeSlot"
          class="past-time-slot"
          :style="getSlotStyle(pastTimeSlot.start, pastTimeSlot.end)"
          title="过去的时间不可预约"
        >
          <span class="past-time-info">已过期</span>
        </div>

        <!-- 已预约的时间段（深灰色） -->
        <div
          v-for="booking in bookedSlots"
          :key="booking.id"
          class="booked-slot"
          :style="getSlotStyle(booking.start, booking.end)"
          :title="`${booking.user.username} - ${booking.purpose || '会议'}`"
        >
          <span class="booking-info">
            {{ booking.user.username }}<br>
            {{ formatTime(booking.start) }} - {{ formatTime(booking.end) }}
          </span>
        </div>

        <!-- 当前选择的区间（蓝色半透明） -->
        <div
          v-if="selecting || selectedSlot"
          class="selected-slot"
          :class="{ invalid: !isValidSelection }"
          :style="getSlotStyle(selectionStart, selectionEnd)"
        >
          <span class="selection-time">
            {{ formatTime(selectionStart) }} - {{ formatTime(selectionEnd) }}
          </span>
        </div>

        <!-- 时间刻度线 -->
        <div class="time-grid">
          <div v-for="hour in 24" :key="hour" class="grid-line"></div>
        </div>
      </div>
    </div>

    <div class="selection-info" v-if="selectedSlot">
      <el-alert
        :title="isValidSelection ? '可以预约此时间段' : '此时间段有冲突，请重新选择'"
        :type="isValidSelection ? 'success' : 'error'"
        :closable="false"
      />
      <div class="action-buttons">
        <el-button @click="clearSelection">重新选择</el-button>
        <el-button 
          type="primary" 
          @click="confirmBooking"
          :disabled="!isValidSelection"
        >
          确认预约
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  room: {
    type: Object,
    required: true
  },
  bookings: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['create-booking', 'refresh'])

const selectedDate = ref(new Date())
const selecting = ref(false)
const selectedSlot = ref(null)
const selectionStart = ref(null)
const selectionEnd = ref(null)
const mouseDownTime = ref(null)

// 计算过去的时间段
const pastTimeSlot = computed(() => {
  if (!selectedDate.value) return null
  
  const now = new Date()
  const dateStart = new Date(selectedDate.value)
  dateStart.setHours(0, 0, 0, 0)
  
  const dateEnd = new Date(selectedDate.value)
  dateEnd.setHours(23, 59, 59, 999)
  
  // 如果选择的是今天，显示当前时间之前的部分
  if (dateStart.toDateString() === now.toDateString()) {
    return {
      start: dateStart,
      end: now
    }
  }
  
  // 如果选择的是过去的日期，整天都是灰色
  if (dateStart < now) {
    return {
      start: dateStart,
      end: dateEnd
    }
  }
  
  return null
})

// 过滤当前日期的预约
const bookedSlots = computed(() => {
  if (!selectedDate.value) return []
  
  const dateStr = selectedDate.value.toDateString()
  return props.bookings.filter(booking => {
    if (booking.status === 'cancelled') return false
    const bookingDate = new Date(booking.start_time).toDateString()
    return bookingDate === dateStr
  }).map(booking => ({
    ...booking,
    start: new Date(booking.start_time),
    end: new Date(booking.end_time)
  }))
})

// 检查选择是否有效（不与已有预约冲突，不在过去）
const isValidSelection = computed(() => {
  if (!selectionStart.value || !selectionEnd.value) return false
  if (selectionStart.value >= selectionEnd.value) return false
  
  // 检查是否在过去的时间
  const now = new Date()
  if (selectionStart.value < now) return false
  
  // 检查是否与过去的时间段重叠
  if (pastTimeSlot.value) {
    const pastStart = pastTimeSlot.value.start
    const pastEnd = pastTimeSlot.value.end
    
    if (
      (selectionStart.value >= pastStart && selectionStart.value < pastEnd) ||
      (selectionEnd.value > pastStart && selectionEnd.value <= pastEnd) ||
      (selectionStart.value <= pastStart && selectionEnd.value >= pastEnd)
    ) {
      return false
    }
  }
  
  // 检查是否与已有预约冲突
  return !bookedSlots.value.some(booking => {
    return (
      (selectionStart.value >= booking.start && selectionStart.value < booking.end) ||
      (selectionEnd.value > booking.start && selectionEnd.value <= booking.end) ||
      (selectionStart.value <= booking.start && selectionEnd.value >= booking.end)
    )
  })
})

// 禁用过去的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

// 开始选择时间段
const startSelection = (e) => {
  const rect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - rect.left
  const time = getTimeFromPosition(x, rect.width)
  
  mouseDownTime.value = time
  selectionStart.value = time
  selectionEnd.value = time
  selecting.value = true
  selectedSlot.value = null
}

// 更新选择
const updateSelection = (e) => {
  if (!selecting.value) return
  
  const rect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - rect.left
  const time = getTimeFromPosition(x, rect.width)
  
  if (time > mouseDownTime.value) {
    selectionStart.value = mouseDownTime.value
    selectionEnd.value = time
  } else {
    selectionStart.value = time
    selectionEnd.value = mouseDownTime.value
  }
}

// 结束选择
const endSelection = () => {
  if (!selecting.value) return
  
  selecting.value = false
  
  // 最小选择30分钟（半小时）
  const duration = (selectionEnd.value - selectionStart.value) / (1000 * 60)
  if (duration < 30) {
    ElMessage.warning('预约时长至少30分钟（半小时）')
    clearSelection()
    return
  }
  
  selectedSlot.value = {
    start: selectionStart.value,
    end: selectionEnd.value
  }
}

// 取消选择
const cancelSelection = () => {
  if (selecting.value) {
    selecting.value = false
    clearSelection()
  }
}

// 清除选择
const clearSelection = () => {
  selectedSlot.value = null
  selectionStart.value = null
  selectionEnd.value = null
}

// 确认预约
const confirmBooking = () => {
  if (!isValidSelection.value) return
  
  emit('create-booking', {
    room_id: props.room.id,
    start_time: selectionStart.value,
    end_time: selectionEnd.value
  })
}

// 从位置计算时间
const getTimeFromPosition = (x, width) => {
  const ratio = Math.max(0, Math.min(1, x / width))
  const date = new Date(selectedDate.value)
  const minutes = Math.round(ratio * 24 * 60 / 30) * 30 // 30分钟为单位（半小时）
  date.setHours(0, 0, 0, 0)
  date.setMinutes(minutes)
  return date
}

// 获取时间段样式
const getSlotStyle = (start, end) => {
  if (!start || !end) return {}
  
  const dayStart = new Date(selectedDate.value)
  dayStart.setHours(0, 0, 0, 0)
  
  const startMinutes = (start - dayStart) / (1000 * 60)
  const endMinutes = (end - dayStart) / (1000 * 60)
  
  const left = (startMinutes / (24 * 60)) * 100
  const width = ((endMinutes - startMinutes) / (24 * 60)) * 100
  
  return {
    left: `${left}%`,
    width: `${width}%`
  }
}

// 格式化小时
const formatHour = (hour) => {
  return `${hour.toString().padStart(2, '0')}:00`
}

// 格式化时间
const formatTime = (date) => {
  if (!date) return ''
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

// 加载预约数据
const loadBookings = () => {
  emit('refresh')
  clearSelection()
}

// 监听日期变化
watch(() => props.room, () => {
  clearSelection()
}, { deep: true })
</script>

<style scoped>
.timeline-selector {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.room-info {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e4e7ed;
}

.room-info h3 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 20px;
}

.room-info p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.date-selector {
  margin-bottom: 20px;
}

.timeline-container {
  position: relative;
  margin-bottom: 20px;
}

.time-labels {
  display: flex;
  margin-bottom: 8px;
  padding-left: 2px;
}

.time-label {
  flex: 1;
  font-size: 12px;
  color: #909399;
  text-align: left;
}

.timeline-track {
  position: relative;
  height: 80px;
  background: white;
  border: 2px solid #dcdfe6;
  border-radius: 4px;
  cursor: crosshair;
  user-select: none;
}

.time-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  pointer-events: none;
}

.grid-line {
  flex: 1;
  border-right: 1px solid #f0f0f0;
}

.grid-line:last-child {
  border-right: none;
}

.past-time-slot {
  position: absolute;
  top: 0;
  height: 100%;
  background: repeating-linear-gradient(
    45deg,
    #f5f5f5,
    #f5f5f5 10px,
    #e8e8e8 10px,
    #e8e8e8 20px
  );
  border-right: 2px solid #d0d0d0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 1;
  opacity: 0.8;
}

.past-time-info {
  font-size: 12px;
  color: #909399;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
}

.booked-slot {
  position: absolute;
  top: 0;
  height: 100%;
  background: linear-gradient(135deg, #d0d0d0 0%, #a0a0a0 100%);
  border-left: 2px solid #606266;
  border-right: 2px solid #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 2;
}

.booking-info {
  font-size: 11px;
  color: #303133;
  text-align: center;
  line-height: 1.4;
  padding: 0 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
}

.selected-slot {
  position: absolute;
  top: 0;
  height: 100%;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.3) 0%, rgba(64, 158, 255, 0.5) 100%);
  border: 2px solid #409EFF;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  animation: pulse 1s ease-in-out infinite;
}

.selected-slot.invalid {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.3) 0%, rgba(245, 108, 108, 0.5) 100%);
  border-color: #F56C6C;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.selection-time {
  font-size: 12px;
  font-weight: bold;
  color: #409EFF;
  background: white;
  padding: 2px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.selected-slot.invalid .selection-time {
  color: #F56C6C;
}

.selection-info {
  margin-top: 20px;
}

.action-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

