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
      <div class="usage-hint">
        <el-icon><InfoFilled /></el-icon>
        <span>点击时间轴两次选择时间区间（第一次确定起点，第二次确定终点）</span>
      </div>
    </div>

    <div class="timeline-container">
      <!-- 时间标签（每小时） -->
      <div class="time-labels">
        <div v-for="hour in 24" :key="hour" class="time-label">
          {{ formatHour(hour - 1) }}
        </div>
      </div>

      <div 
        class="timeline-track"
        @click="handleTimelineClick"
        @mousemove="handleTimelineMove"
        @mouseleave="previewEnd = null"
      >
        <!-- 时间格子背景（48个半小时格子） -->
        <div class="time-cells">
          <div 
            v-for="cell in 48" 
            :key="cell" 
            class="time-cell"
            :class="{ 
              'cell-hour': cell % 2 === 1,
              'cell-half': cell % 2 === 0
            }"
          >
            <span class="cell-time">{{ getCellTime(cell) }}</span>
          </div>
        </div>

        <!-- 过去的时间段（优雅灰色） -->
        <div
          v-if="pastTimeSlot"
          class="past-time-slot"
          :style="getSlotStyle(pastTimeSlot.start, pastTimeSlot.end)"
          title="过去的时间不可预约"
        >
          <div class="slot-overlay">
            <el-icon class="slot-icon"><Clock /></el-icon>
            <span class="slot-text">已过期</span>
          </div>
        </div>

        <!-- 已预约的时间段（深色优雅渐变） -->
        <div
          v-for="booking in bookedSlots"
          :key="booking.id"
          class="booked-slot"
          :style="getSlotStyle(booking.start, booking.end)"
          :title="`${booking.user.username} - ${booking.purpose || '会议'}`"
        >
          <div class="booking-content">
            <div class="booking-header">
              <el-icon><UserFilled /></el-icon>
              <span class="booking-user">{{ booking.user.username }}</span>
            </div>
            <div class="booking-time">
              {{ formatTime(booking.start) }} - {{ formatTime(booking.end) }}
            </div>
            <div class="booking-purpose" v-if="booking.purpose">
              {{ booking.purpose }}
            </div>
          </div>
        </div>

        <!-- 第一次点击的标记点 -->
        <div
          v-if="firstClickPoint && !selectedSlot"
          class="first-click-marker"
          :style="getMarkerStyle(firstClickPoint)"
        >
          <div class="marker-dot"></div>
          <div class="marker-time">{{ formatTime(firstClickPoint) }}</div>
        </div>

        <!-- 预览选择区间（第一次点击后鼠标移动） -->
        <div
          v-if="firstClickPoint && previewEnd && !selectedSlot"
          class="preview-slot"
          :class="{ invalid: !isValidSelection }"
          :style="getSlotStyle(selectionStart, selectionEnd)"
        >
          <div class="preview-content">
            <span class="preview-time">
              {{ formatTime(selectionStart) }} - {{ formatTime(selectionEnd) }}
            </span>
            <span class="preview-duration">
              {{ getSelectionDuration() }}
            </span>
          </div>
        </div>

        <!-- 最终选择的区间 -->
        <div
          v-if="selectedSlot"
          class="selected-slot"
          :class="{ invalid: !isValidSelection }"
          :style="getSlotStyle(selectionStart, selectionEnd)"
        >
          <div class="selection-content">
            <el-icon class="selection-icon"><Calendar /></el-icon>
            <span class="selection-time">
              {{ formatTime(selectionStart) }} - {{ formatTime(selectionEnd) }}
            </span>
            <span class="selection-duration">
              {{ getSelectionDuration() }}
            </span>
          </div>
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
import { Clock, UserFilled, Calendar, InfoFilled } from '@element-plus/icons-vue'

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
const firstClickPoint = ref(null) // 第一次点击的点
const previewEnd = ref(null) // 鼠标移动时的预览终点

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

// 处理时间轴点击
const handleTimelineClick = (e) => {
  if (!selectedDate.value) return
  
  const timelineRect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - timelineRect.left
  const time = getTimeFromPosition(x, timelineRect.width)
  
  // 如果是第一次点击
  if (!firstClickPoint.value) {
    firstClickPoint.value = time
    selectionStart.value = time
    selectionEnd.value = time
    selecting.value = true
    selectedSlot.value = null
    ElMessage.info('请点击第二个位置确定时间区间', { duration: 2000 })
  } else {
    // 第二次点击，确定区间
    let start = firstClickPoint.value
    let end = time
    
    // 确保开始时间小于结束时间
    if (start > end) {
      [start, end] = [end, start]
    }
    
    // 检查最小时长（30分钟）
    const minDuration = 30 * 60 * 1000 // 30分钟
    if (end - start < minDuration) {
      ElMessage.warning('预约时长至少为30分钟')
      clearSelection()
      return
    }
    
    selectionStart.value = start
    selectionEnd.value = end
    
    if (isValidSelection.value) {
      selectedSlot.value = {
        start: start,
        end: end
      }
      // 完成选择后清除第一次点击的状态
      firstClickPoint.value = null
      previewEnd.value = null
      selecting.value = false
    } else {
      ElMessage.warning('所选时间段有冲突，请重新选择')
      clearSelection()
    }
  }
}

// 处理鼠标移动（显示预览）
const handleTimelineMove = (e) => {
  if (!firstClickPoint.value || !selectedDate.value) return
  
  const timelineRect = e.currentTarget.getBoundingClientRect()
  const x = e.clientX - timelineRect.left
  const time = getTimeFromPosition(x, timelineRect.width)
  
  previewEnd.value = time
  
  // 更新预览区间
  let start = firstClickPoint.value
  let end = time
  
  if (start > end) {
    [start, end] = [end, start]
  }
  
  selectionStart.value = start
  selectionEnd.value = end
}

// 取消选择（点击外部或ESC键）
const cancelSelection = () => {
  firstClickPoint.value = null
  previewEnd.value = null
  selecting.value = false
  selectionStart.value = null
  selectionEnd.value = null
  selectedSlot.value = null
}

// 清除选择
const clearSelection = () => {
  selectedSlot.value = null
  selectionStart.value = null
  selectionEnd.value = null
  firstClickPoint.value = null
  previewEnd.value = null
  selecting.value = false
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

// 计算标记点样式
const getMarkerStyle = (time) => {
  if (!time || !selectedDate.value) return {}
  
  const dayStart = new Date(selectedDate.value)
  dayStart.setHours(0, 0, 0, 0)
  
  const timeMinutes = (time - dayStart) / (1000 * 60)
  const left = (timeMinutes / (24 * 60)) * 100
  
  return {
    left: `${left}%`
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

// 获取格子显示的时间
const getCellTime = (cellIndex) => {
  const totalMinutes = (cellIndex - 1) * 30
  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
}

// 获取选择的时长
const getSelectionDuration = () => {
  if (!selectionStart.value || !selectionEnd.value) return ''
  const minutes = (selectionEnd.value - selectionStart.value) / (1000 * 60)
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours > 0 && mins > 0) {
    return `${hours}小时${mins}分钟`
  } else if (hours > 0) {
    return `${hours}小时`
  } else {
    return `${mins}分钟`
  }
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
  background: linear-gradient(to bottom, #ffffff, #fafbfc);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.room-info {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e8eaed;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  padding: 20px;
  border-radius: 12px;
}

.room-info h3 {
  margin: 0 0 10px 0;
  color: #1a1a1a;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.room-info p {
  margin: 0;
  color: #5f6368;
  font-size: 15px;
}

.date-selector {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.usage-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #e6f2ff 0%, #f0f7ff 100%);
  border-radius: 8px;
  border: 1px solid #b8d4f1;
  color: #4a7ba7;
  font-size: 13px;
  font-weight: 500;
}

.usage-hint .el-icon {
  font-size: 16px;
  color: #667eea;
}

.timeline-container {
  position: relative;
  margin-bottom: 24px;
}

.time-labels {
  display: flex;
  margin-bottom: 12px;
  padding: 0 4px;
}

.time-label {
  flex: 1;
  font-size: 13px;
  color: #5f6368;
  text-align: left;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.timeline-track {
  position: relative;
  height: 120px;
  background: linear-gradient(to bottom, #ffffff, #f8f9fa);
  border: 2px solid #e8eaed;
  border-radius: 12px;
  cursor: crosshair;
  user-select: none;
  overflow: hidden;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.04);
}

.time-cells {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  pointer-events: none;
  z-index: 0;
}

.time-cell {
  flex: 1;
  border-right: 1px solid #f0f2f4;
  position: relative;
  transition: background-color 0.2s ease;
}

.time-cell:hover {
  background-color: rgba(64, 158, 255, 0.03);
}

.time-cell.cell-hour {
  border-right: 2px solid #e0e3e6;
}

.time-cell:last-child {
  border-right: none;
}

.cell-time {
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  color: #c0c4c8;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.time-cell:hover .cell-time {
  opacity: 1;
}

.past-time-slot {
  position: absolute;
  top: 0;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(220, 220, 220, 0.3) 0%,
    rgba(200, 200, 200, 0.4) 100%
  );
  backdrop-filter: blur(2px);
  border-right: 3px solid rgba(160, 160, 160, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 1;
}

.slot-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  backdrop-filter: blur(4px);
}

.slot-icon {
  font-size: 24px;
  color: #909399;
}

.slot-text {
  font-size: 13px;
  color: #606266;
  font-weight: 600;
  letter-spacing: 1px;
}

.booked-slot {
  position: absolute;
  top: 4px;
  height: calc(100% - 8px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-left: 3px solid #5a67d8;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 2;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.booked-slot:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

.booking-content {
  padding: 8px 12px;
  color: white;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.booking-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  font-size: 13px;
}

.booking-user {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.booking-time {
  font-size: 11px;
  opacity: 0.9;
  font-weight: 500;
}

.booking-purpose {
  font-size: 10px;
  opacity: 0.8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-style: italic;
}

.selected-slot {
  position: absolute;
  top: 4px;
  height: calc(100% - 8px);
  background: linear-gradient(135deg, rgba(66, 153, 225, 0.25) 0%, rgba(72, 187, 120, 0.25) 100%);
  border: 3px solid #4299e1;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  animation: selectionGlow 2s ease-in-out infinite;
  backdrop-filter: blur(2px);
  box-shadow: 0 4px 16px rgba(66, 153, 225, 0.3);
}

.selected-slot.invalid {
  background: linear-gradient(135deg, rgba(245, 101, 101, 0.25) 0%, rgba(229, 62, 62, 0.25) 100%);
  border-color: #f56565;
  box-shadow: 0 4px 16px rgba(245, 101, 101, 0.3);
}

@keyframes selectionGlow {
  0%, 100% { 
    opacity: 1;
    box-shadow: 0 4px 16px rgba(66, 153, 225, 0.3);
  }
  50% { 
    opacity: 0.9;
    box-shadow: 0 6px 20px rgba(66, 153, 225, 0.5);
  }
}

.selection-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.selection-icon {
  font-size: 20px;
  color: #4299e1;
}

.selected-slot.invalid .selection-icon {
  color: #f56565;
}

.selection-time {
  font-size: 13px;
  font-weight: 600;
  color: #2c5282;
  letter-spacing: 0.3px;
}

.selected-slot.invalid .selection-time {
  color: #c53030;
}

.selection-duration {
  font-size: 11px;
  color: #718096;
  font-weight: 500;
}

/* 第一次点击标记点 */
.first-click-marker {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: markerPulse 1.5s ease-in-out infinite;
}

.marker-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.3),
              0 0 0 8px rgba(102, 126, 234, 0.15);
  animation: dotPulse 1.5s ease-in-out infinite;
}

.marker-time {
  position: absolute;
  top: -32px;
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
  background: white;
  padding: 4px 10px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  letter-spacing: 0.5px;
}

@keyframes markerPulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
}

@keyframes dotPulse {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.3),
                0 0 0 8px rgba(102, 126, 234, 0.15);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(102, 126, 234, 0.4),
                0 0 0 12px rgba(102, 126, 234, 0.2);
  }
}

/* 预览选择区间 */
.preview-slot {
  position: absolute;
  top: 4px;
  height: calc(100% - 8px);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  border: 2px dashed #667eea;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  pointer-events: none;
  animation: previewBlink 1s ease-in-out infinite;
}

.preview-slot.invalid {
  background: linear-gradient(135deg, rgba(245, 101, 101, 0.15) 0%, rgba(229, 62, 62, 0.15) 100%);
  border-color: #f56565;
  border-style: dashed;
}

@keyframes previewBlink {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

.preview-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preview-time {
  font-size: 12px;
  font-weight: 600;
  color: #667eea;
  letter-spacing: 0.3px;
}

.preview-slot.invalid .preview-time {
  color: #f56565;
}

.preview-duration {
  font-size: 10px;
  color: #718096;
  font-weight: 500;
}

.selection-info {
  margin-top: 24px;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
}

.action-buttons {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.action-buttons .el-button {
  font-weight: 500;
  letter-spacing: 0.5px;
  padding: 12px 24px;
  border-radius: 8px;
}
</style>

