/**
 * 时间轴选择 Composable
 * 封装时间轴选择的所有逻辑
 */

import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  TIME_CONSTANTS, 
  getTimeFromPosition, 
  isTimeOverlap,
  getDayStart 
} from '@/utils/timeUtils'

export function useTimelineSelection(selectedDate, bookedSlots, pastTimeSlot) {
  // 状态
  const selecting = ref(false)
  const selectedSlot = ref(null)
  const selectionStart = ref(null)
  const selectionEnd = ref(null)
  const firstClickPoint = ref(null)
  const previewEnd = ref(null)

  // 检查选择是否有效
  const isValidSelection = computed(() => {
    if (!selectionStart.value || !selectionEnd.value) return false
    if (selectionStart.value >= selectionEnd.value) return false
    
    // 检查是否在过去
    const now = new Date()
    if (selectionStart.value < now) return false
    
    // 检查是否与过去的时间段重叠
    if (pastTimeSlot.value) {
      if (isTimeOverlap(
        selectionStart.value,
        selectionEnd.value,
        pastTimeSlot.value.start,
        pastTimeSlot.value.end
      )) {
        return false
      }
    }
    
    // 检查是否与已有预约冲突
    return !bookedSlots.value.some(booking => 
      isTimeOverlap(
        selectionStart.value,
        selectionEnd.value,
        booking.start,
        booking.end
      )
    )
  })

  // 处理时间轴点击
  const handleTimelineClick = (e) => {
    if (!selectedDate.value) return
    
    const timelineRect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - timelineRect.left
    const time = getTimeFromPosition(x, timelineRect.width, selectedDate.value)
    
    if (!firstClickPoint.value) {
      // 第一次点击
      firstClickPoint.value = time
      selectionStart.value = time
      selectionEnd.value = time
      selecting.value = true
      selectedSlot.value = null
      ElMessage.info('请点击第二个位置确定时间区间', { duration: 2000 })
    } else {
      // 第二次点击
      let start = firstClickPoint.value
      let end = time
      
      // 确保开始时间小于结束时间
      if (start > end) {
        [start, end] = [end, start]
      }
      
      // 检查最小时长
      const duration = (end - start) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE
      if (duration < TIME_CONSTANTS.MIN_BOOKING_DURATION) {
        ElMessage.warning(`预约时长至少为${TIME_CONSTANTS.MIN_BOOKING_DURATION}分钟`)
        clearSelection()
        return
      }
      
      selectionStart.value = start
      selectionEnd.value = end
      
      if (isValidSelection.value) {
        selectedSlot.value = { start, end }
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
    const time = getTimeFromPosition(x, timelineRect.width, selectedDate.value)
    
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

  // 清除预览
  const clearPreview = () => {
    previewEnd.value = null
  }

  // 取消选择
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

  return {
    // 状态
    selecting,
    selectedSlot,
    selectionStart,
    selectionEnd,
    firstClickPoint,
    previewEnd,
    
    // 计算属性
    isValidSelection,
    
    // 方法
    handleTimelineClick,
    handleTimelineMove,
    clearPreview,
    cancelSelection,
    clearSelection
  }
}

