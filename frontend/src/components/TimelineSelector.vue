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
      <!-- 桌面端：单排时间轴 -->
      <div class="timeline-desktop">
        <!-- 时间标签（每小时，从8点到24点） -->
        <div class="time-labels">
          <div v-for="hour in TIME_CONSTANTS.WORKING_HOURS" :key="hour" class="time-label">
            {{ formatHour(TIME_CONSTANTS.START_HOUR + hour - 1) }}
          </div>
        </div>

        <div 
          class="timeline-track"
          @click="handleTimelineClick"
          @mousemove="handleTimelineMove"
          @mouseleave="clearPreview"
        >
        <!-- 时间格子背景（48个半小时格子） -->
        <div class="time-cells">
          <div 
            v-for="cell in TIME_CONSTANTS.TOTAL_TIME_CELLS" 
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
          :style="getSlotStyleWrapper(pastTimeSlot.start, pastTimeSlot.end)"
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
          :style="getSlotStyleWrapper(booking.start, booking.end)"
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
          :style="getMarkerStyleWrapper(firstClickPoint)"
        >
          <div class="marker-dot"></div>
          <div class="marker-time">{{ formatTime(firstClickPoint) }}</div>
        </div>

        <!-- 预览选择区间（第一次点击后鼠标移动） -->
        <div
          v-if="firstClickPoint && previewEnd && !selectedSlot"
          class="preview-slot"
          :class="{ invalid: !isValidSelection }"
          :style="getSlotStyleWrapper(selectionStart, selectionEnd)"
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
          :style="getSlotStyleWrapper(selectionStart, selectionEnd)"
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
      
      <!-- 移动端：均匀分两排 -->
      <div class="timeline-mobile">
        <!-- 第一排时间轴 (8:00-16:00) -->
        <div class="timeline-period">
          <div class="period-title">08:00 - 16:00</div>
          <div class="time-labels-mobile">
            <div v-for="hour in 8" :key="`row1-${hour}`" class="time-label-mobile">
              {{ formatHour(8 + hour - 1) }}
            </div>
          </div>
          <div 
            class="timeline-track-mobile row1-track"
            @click="(e) => handleTimelineClickMobile(e, 'row1')"
            @touchstart="(e) => handleTouchStart(e, 'row1')"
            @touchend="(e) => handleTouchEnd(e, 'row1')"
          >
            <!-- 时间格子 -->
            <div class="time-cells">
              <div 
                v-for="cell in 16" 
                :key="`row1-cell-${cell}`" 
                class="time-cell"
                :class="{ 
                  'cell-hour': cell % 2 === 1,
                  'cell-half': cell % 2 === 0
                }"
              ></div>
            </div>
            
            <!-- 过去时间 -->
            <div
              v-if="pastTimeSlotRow1"
              class="past-time-slot"
              :style="getSlotStyleMobile(pastTimeSlotRow1.start, pastTimeSlotRow1.end, 'row1')"
            ></div>
            
            <!-- 预约 -->
            <div
              v-for="booking in row1Bookings"
              :key="`row1-${booking.id}`"
              class="booked-slot-mobile"
              :style="getSlotStyleMobile(booking.start, booking.end, 'row1')"
            >
              <span class="booking-text">{{ booking.user.username }}</span>
            </div>
            
            <!-- 第一次点击标记（充能动画） -->
            <div
              v-if="firstClickInRow === 'row1' && firstClickPoint"
              class="first-click-marker-mobile"
              :style="getMarkerStyleMobile(firstClickPoint, 'row1')"
            >
              <div class="charging-circle"></div>
              <div class="charging-pulse"></div>
            </div>
          </div>
        </div>
        
        <!-- 第二排时间轴 (16:00-24:00) -->
        <div class="timeline-period">
          <div class="period-title">16:00 - 24:00</div>
          <div class="time-labels-mobile">
            <div v-for="hour in 8" :key="`row2-${hour}`" class="time-label-mobile">
              {{ formatHour(16 + hour - 1) }}
            </div>
          </div>
          <div 
            class="timeline-track-mobile row2-track"
            @click="(e) => handleTimelineClickMobile(e, 'row2')"
            @touchstart="(e) => handleTouchStart(e, 'row2')"
            @touchend="(e) => handleTouchEnd(e, 'row2')"
          >
            <!-- 时间格子 -->
            <div class="time-cells">
              <div 
                v-for="cell in 16" 
                :key="`row2-cell-${cell}`" 
                class="time-cell"
                :class="{ 
                  'cell-hour': cell % 2 === 1,
                  'cell-half': cell % 2 === 0
                }"
              ></div>
            </div>
            
            <!-- 过去时间 -->
            <div
              v-if="pastTimeSlotRow2"
              class="past-time-slot"
              :style="getSlotStyleMobile(pastTimeSlotRow2.start, pastTimeSlotRow2.end, 'row2')"
            ></div>
            
            <!-- 预约 -->
            <div
              v-for="booking in row2Bookings"
              :key="`row2-${booking.id}`"
              class="booked-slot-mobile"
              :style="getSlotStyleMobile(booking.start, booking.end, 'row2')"
            >
              <span class="booking-text">{{ booking.user.username }}</span>
            </div>
            
            <!-- 第一次点击标记（充能动画） -->
            <div
              v-if="firstClickInRow === 'row2' && firstClickPoint"
              class="first-click-marker-mobile"
              :style="getMarkerStyleMobile(firstClickPoint, 'row2')"
            >
              <div class="charging-circle"></div>
              <div class="charging-pulse"></div>
            </div>
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
import { Clock, UserFilled, Calendar, InfoFilled } from '@element-plus/icons-vue'

// Composables
import { useBookingData } from '@/composables/useBookingData'
import { useTimelineSelection } from '@/composables/useTimelineSelection'

// Utils
import {
  TIME_CONSTANTS,
  formatHour,
  formatTime,
  getCellTime,
  getTimeDuration,
  getDayStart,
  getSlotStyle,
  getMarkerStyle,
  disabledDate
} from '@/utils/timeUtils'

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

// 基础状态
const selectedDate = ref(new Date())

// 使用预约数据 Composable
const { pastTimeSlot, bookedSlots } = useBookingData(selectedDate, computed(() => props.bookings))

// 使用时间轴选择 Composable
const {
  selecting,
  selectedSlot,
  selectionStart,
  selectionEnd,
  firstClickPoint,
  previewEnd,
  isValidSelection,
  handleTimelineClick,
  handleTimelineMove,
  clearPreview,
  clearSelection
} = useTimelineSelection(selectedDate, bookedSlots, pastTimeSlot)

// 包装样式函数，传入 dayStart
const getSlotStyleWrapper = (start, end) => {
  const dayStart = getDayStart(selectedDate.value)
  return getSlotStyle(start, end, dayStart)
}

const getMarkerStyleWrapper = (time) => {
  const dayStart = getDayStart(selectedDate.value)
  return getMarkerStyle(time, dayStart)
}

// 获取选择的时长
const getSelectionDuration = () => {
  return getTimeDuration(selectionStart.value, selectionEnd.value)
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

// 加载预约数据
const loadBookings = () => {
  emit('refresh')
  clearSelection()
}

// 清除选择（包括移动端状态）
const clearSelectionAll = () => {
  clearSelection()
  firstClickInRow.value = null
}

// 监听日期变化
watch(() => props.room, () => {
  clearSelectionAll()
}, { deep: true })

// 移动端：两排预约数据
const row1Bookings = computed(() => {
  return bookedSlots.value.filter(booking => {
    const hour = booking.start.getHours()
    return hour >= 8 && hour < 16
  })
})

const row2Bookings = computed(() => {
  return bookedSlots.value.filter(booking => {
    const hour = booking.start.getHours()
    return hour >= 16
  })
})

// 移动端：两排过去时间段
const pastTimeSlotRow1 = computed(() => {
  if (!pastTimeSlot.value) return null
  const slot = pastTimeSlot.value
  const row1Start = new Date(slot.start)
  row1Start.setHours(8, 0, 0, 0)
  const row1End = new Date(slot.start)
  row1End.setHours(16, 0, 0, 0)
  
  if (slot.end <= row1Start) return null
  if (slot.start >= row1End) return null
  
  return {
    start: slot.start < row1Start ? row1Start : slot.start,
    end: slot.end > row1End ? row1End : slot.end
  }
})

const pastTimeSlotRow2 = computed(() => {
  if (!pastTimeSlot.value) return null
  const slot = pastTimeSlot.value
  const row2Start = new Date(slot.start)
  row2Start.setHours(16, 0, 0, 0)
  const row2End = new Date(slot.start)
  row2End.setHours(24, 0, 0, 0)
  
  if (slot.end <= row2Start) return null
  if (slot.start >= row2End) return null
  
  return {
    start: slot.start < row2Start ? row2Start : slot.start,
    end: slot.end > row2End ? row2End : slot.end
  }
})

// 记录第一次点击在哪一排
const firstClickInRow = ref(null)

// 移动端：计算时间段样式
const getSlotStyleMobile = (start, end, row) => {
  if (!start || !end) return {}
  
  const periodStart = new Date(selectedDate.value)
  const periodMinutes = 8 * 60 // 每排8小时
  
  if (row === 'row1') {
    periodStart.setHours(8, 0, 0, 0)
  } else {
    periodStart.setHours(16, 0, 0, 0)
  }
  
  const startMinutes = Math.max(0, (start - periodStart) / (60 * 1000))
  const endMinutes = Math.min(periodMinutes, (end - periodStart) / (60 * 1000))
  
  const left = (startMinutes / periodMinutes) * 100
  const width = ((endMinutes - startMinutes) / periodMinutes) * 100
  
  return {
    left: `${left}%`,
    width: `${width}%`
  }
}

// 移动端：计算标记点样式
const getMarkerStyleMobile = (time, row) => {
  if (!time) return {}
  
  const periodStart = new Date(selectedDate.value)
  const periodMinutes = 8 * 60
  
  if (row === 'row1') {
    periodStart.setHours(8, 0, 0, 0)
  } else {
    periodStart.setHours(16, 0, 0, 0)
  }
  
  const minutes = (time - periodStart) / (60 * 1000)
  const left = (minutes / periodMinutes) * 100
  
  return { left: `${left}%` }
}

// 移动端：处理点击事件
const handleTimelineClickMobile = (event, row) => {
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const ratio = x / rect.width
  
  const periodStart = new Date(selectedDate.value)
  
  if (row === 'row1') {
    periodStart.setHours(8, 0, 0, 0)
  } else {
    periodStart.setHours(16, 0, 0, 0)
  }
  
  const minutes = Math.round(ratio * 8 * 60 / 30) * 30 // 8小时
  const clickTime = new Date(periodStart.getTime() + minutes * 60 * 1000)
  
  // 如果是第一次点击
  if (!firstClickPoint.value) {
    firstClickPoint.value = clickTime
    firstClickInRow.value = row
  } else {
    // 第二次点击
    const start = firstClickPoint.value < clickTime ? firstClickPoint.value : clickTime
    const end = firstClickPoint.value < clickTime ? clickTime : firstClickPoint.value
    
    selectionStart.value = start
    selectionEnd.value = end
    selectedSlot.value = true
    firstClickInRow.value = null
  }
}

// 触摸事件处理
const handleTouchStart = (event, row) => {
  event.preventDefault()
}

const handleTouchEnd = (event, row) => {
  event.preventDefault()
  const touch = event.changedTouches[0]
  const rect = event.currentTarget.getBoundingClientRect()
  const x = touch.clientX - rect.left
  const ratio = x / rect.width
  
  const periodStart = new Date(selectedDate.value)
  
  if (row === 'row1') {
    periodStart.setHours(8, 0, 0, 0)
  } else {
    periodStart.setHours(16, 0, 0, 0)
  }
  
  const minutes = Math.round(ratio * 8 * 60 / 30) * 30
  const clickTime = new Date(periodStart.getTime() + minutes * 60 * 1000)
  
  if (!firstClickPoint.value) {
    firstClickPoint.value = clickTime
    firstClickInRow.value = row
  } else {
    const start = firstClickPoint.value < clickTime ? firstClickPoint.value : clickTime
    const end = firstClickPoint.value < clickTime ? clickTime : firstClickPoint.value
    
    selectionStart.value = start
    selectionEnd.value = end
    selectedSlot.value = true
    firstClickInRow.value = null
  }
}
</script>

<style scoped>
.timeline-selector {
  background: linear-gradient(to bottom, #ffffff, #fafbfc);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .timeline-selector {
    padding: 16px;
    border-radius: 12px;
  }
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

/* 桌面端时间轴 */
.timeline-desktop {
  display: block;
}

/* 移动端时间轴 */
.timeline-mobile {
  display: none;
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

/* 移动端时间轴样式 */
.timeline-period {
  margin-bottom: 16px;
}

.period-title {
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 8px;
  padding-left: 4px;
}

.time-labels-mobile {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 0 4px;
}

.time-label-mobile {
  font-size: 11px;
  color: #5f6368;
  font-weight: 500;
}

.timeline-track-mobile {
  position: relative;
  height: 60px;
  background: linear-gradient(to bottom, #ffffff, #f8f9fa);
  border: 2px solid #e8eaed;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
}

.booked-slot-mobile {
  position: absolute;
  top: 2px;
  height: calc(100% - 4px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
}

.booking-text {
  color: white;
  font-size: 10px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 4px;
}

/* 移动端：第一次点击标记（充能动画） */
.first-click-marker-mobile {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  width: 40px;
  height: 40px;
  pointer-events: none;
}

.charging-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
  animation: charging-pulse 1.5s ease-out infinite;
}

.charging-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 3px solid #667eea;
  border-radius: 50%;
  animation: charging-expand 1.5s ease-out infinite;
}

@keyframes charging-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
  }
}

@keyframes charging-expand {
  0% {
    width: 20px;
    height: 20px;
    opacity: 1;
    border-width: 3px;
  }
  50% {
    width: 40px;
    height: 40px;
    opacity: 0.5;
    border-width: 2px;
  }
  100% {
    width: 50px;
    height: 50px;
    opacity: 0;
    border-width: 1px;
  }
}

/* 移动端样式优化 */
@media (max-width: 768px) {
  /* 隐藏桌面端时间轴 */
  .timeline-desktop {
    display: none;
  }
  
  /* 显示移动端时间轴 */
  .timeline-mobile {
    display: block;
  }
  
  .room-info {
    margin-bottom: 16px;
    padding: 16px 12px;
  }
  
  .room-info h3 {
    font-size: 18px;
    margin-bottom: 8px;
  }
  
  .room-info p {
    font-size: 13px;
  }
  
  .date-selector {
    margin-bottom: 16px;
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .date-selector :deep(.el-date-editor) {
    width: 100% !important;
  }
  
  .usage-hint {
    padding: 10px 12px;
    font-size: 12px;
    text-align: center;
  }
  
  .usage-hint .el-icon {
    font-size: 14px;
  }
  
  .timeline-container {
    margin-bottom: 16px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .time-labels {
    min-width: 100%;
    padding: 0 2px;
  }
  
  .time-label {
    font-size: 11px;
    min-width: 40px;
  }
  
  .timeline-track {
    min-width: 100%;
    height: 100px;
    touch-action: none;
  }
  
  .time-cell {
    min-width: 20px;
  }
  
  .cell-time {
    font-size: 9px;
    bottom: 2px;
  }
  
  /* 预约块在移动端的优化 */
  .booked-slot {
    top: 2px;
    height: calc(100% - 4px);
    border-radius: 6px;
  }
  
  .booking-content {
    padding: 6px 8px;
  }
  
  .booking-header {
    font-size: 11px;
    gap: 4px;
  }
  
  .booking-time {
    font-size: 9px;
  }
  
  .booking-purpose {
    font-size: 9px;
  }
  
  /* 选择区域在移动端的优化 */
  .selected-slot,
  .preview-slot {
    top: 2px;
    height: calc(100% - 4px);
    border-radius: 6px;
    border-width: 2px;
  }
  
  .selection-content,
  .preview-content {
    padding: 8px 10px;
    gap: 4px;
  }
  
  .selection-icon {
    font-size: 16px;
  }
  
  .selection-time,
  .preview-time {
    font-size: 11px;
  }
  
  .selection-duration,
  .preview-duration {
    font-size: 9px;
  }
  
  /* 第一次点击标记 */
  .marker-dot {
    width: 16px;
    height: 16px;
  }
  
  .marker-time {
    top: -28px;
    font-size: 11px;
    padding: 3px 8px;
  }
  
  /* 过去时间段 */
  .past-time-slot {
    border-right-width: 2px;
  }
  
  .slot-icon {
    font-size: 20px;
  }
  
  .slot-text {
    font-size: 11px;
  }
  
  /* 选择信息区域 */
  .selection-info {
    margin-top: 16px;
    padding: 16px 12px;
  }
  
  .action-buttons {
    margin-top: 12px;
    flex-direction: column;
    gap: 8px;
  }
  
  .action-buttons .el-button {
    width: 100%;
    padding: 14px 20px;
    font-size: 15px;
  }
}

/* 平板适配 */
@media (max-width: 1024px) and (min-width: 769px) {
  .timeline-selector {
    padding: 24px;
  }
  
  .room-info h3 {
    font-size: 20px;
  }
  
  .timeline-track {
    height: 110px;
  }
  
  .time-label {
    font-size: 12px;
  }
}

/* 横屏适配 */
@media (max-width: 768px) and (orientation: landscape) {
  .timeline-track {
    height: 80px;
  }
  
  .usage-hint {
    font-size: 11px;
    padding: 6px 10px;
  }
}
</style>

