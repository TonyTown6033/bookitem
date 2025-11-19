/**
 * 预约数据 Composable
 * 封装预约数据的计算逻辑
 */

import { computed } from 'vue'
import { getDayStart, getDayEnd, isSameDay } from '@/utils/timeUtils'

export function useBookingData(selectedDate, bookings) {
  // 计算过去的时间段
  const pastTimeSlot = computed(() => {
    if (!selectedDate.value) return null
    
    const now = new Date()
    const dateStart = getDayStart(selectedDate.value)
    const dateEnd = getDayEnd(selectedDate.value)
    
    // 如果选择的是今天，显示当前时间之前的部分
    if (isSameDay(dateStart, now)) {
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
    if (!selectedDate.value || !bookings.value) return []
    
    const dateStr = selectedDate.value.toDateString()
    return bookings.value
      .filter(booking => {
        if (booking.status === 'cancelled') return false
        const bookingDate = new Date(booking.start_time).toDateString()
        return bookingDate === dateStr
      })
      .map(booking => ({
        ...booking,
        start: new Date(booking.start_time),
        end: new Date(booking.end_time)
      }))
  })

  return {
    pastTimeSlot,
    bookedSlots
  }
}

