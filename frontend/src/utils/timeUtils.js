/**
 * 时间工具函数模块
 * 集中管理所有时间相关的工具函数
 */

// 常量配置
export const TIME_CONSTANTS = {
  MINUTES_PER_HOUR: 60,
  HOURS_PER_DAY: 24,
  MINUTES_PER_DAY: 24 * 60,
  MILLISECONDS_PER_MINUTE: 60 * 1000,
  MILLISECONDS_PER_HOUR: 60 * 60 * 1000,
  MILLISECONDS_PER_DAY: 24 * 60 * 60 * 1000,
  MIN_BOOKING_DURATION: 30, // 分钟
  TIME_SLOT_UNIT: 30, // 半小时为单位
  TOTAL_TIME_CELLS: 48 // 24小时 * 2（每小时两个格子）
}

/**
 * 格式化小时为 HH:00 格式
 * @param {number} hour - 小时数（0-23）
 * @returns {string} 格式化后的时间字符串
 */
export function formatHour(hour) {
  return `${String(hour).padStart(2, '0')}:00`
}

/**
 * 格式化时间为 HH:mm 格式
 * @param {Date} date - 日期对象
 * @returns {string} 格式化后的时间字符串
 */
export function formatTime(date) {
  if (!date) return ''
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

/**
 * 格式化日期时间为本地字符串
 * @param {string|Date} dateString - 日期字符串或日期对象
 * @returns {string} 格式化后的日期时间字符串
 */
export function formatDateTime(dateString) {
  return new Date(dateString).toLocaleString('zh-CN')
}

/**
 * 获取格子显示的时间（用于48格时间轴）
 * @param {number} cellIndex - 格子索引（1-48）
 * @returns {string} 格式化后的时间字符串
 */
export function getCellTime(cellIndex) {
  const totalMinutes = (cellIndex - 1) * TIME_CONSTANTS.TIME_SLOT_UNIT
  const hours = Math.floor(totalMinutes / TIME_CONSTANTS.MINUTES_PER_HOUR)
  const minutes = totalMinutes % TIME_CONSTANTS.MINUTES_PER_HOUR
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`
}

/**
 * 计算时长并格式化
 * @param {Date} startTime - 开始时间
 * @param {Date} endTime - 结束时间
 * @returns {string} 格式化后的时长字符串
 */
export function getTimeDuration(startTime, endTime) {
  if (!startTime || !endTime) return ''
  
  const minutes = (endTime - startTime) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE
  const hours = Math.floor(minutes / TIME_CONSTANTS.MINUTES_PER_HOUR)
  const mins = minutes % TIME_CONSTANTS.MINUTES_PER_HOUR
  
  if (hours > 0 && mins > 0) {
    return `${hours}小时${mins}分钟`
  } else if (hours > 0) {
    return `${hours}小时`
  } else {
    return `${mins}分钟`
  }
}

/**
 * 获取一天的开始时间
 * @param {Date} date - 日期
 * @returns {Date} 该日期的 00:00:00
 */
export function getDayStart(date) {
  const dayStart = new Date(date)
  dayStart.setHours(0, 0, 0, 0)
  return dayStart
}

/**
 * 获取一天的结束时间
 * @param {Date} date - 日期
 * @returns {Date} 该日期的 23:59:59.999
 */
export function getDayEnd(date) {
  const dayEnd = new Date(date)
  dayEnd.setHours(23, 59, 59, 999)
  return dayEnd
}

/**
 * 判断两个日期是否是同一天
 * @param {Date} date1 - 日期1
 * @param {Date} date2 - 日期2
 * @returns {boolean} 是否同一天
 */
export function isSameDay(date1, date2) {
  return date1.toDateString() === date2.toDateString()
}

/**
 * 禁用过去的日期（用于日期选择器）
 * @param {Date} time - 日期
 * @returns {boolean} 是否禁用
 */
export function disabledDate(time) {
  return time.getTime() < Date.now() - TIME_CONSTANTS.MILLISECONDS_PER_DAY
}

/**
 * 从位置计算时间（用于时间轴点击）
 * @param {number} x - 鼠标 x 坐标
 * @param {number} width - 时间轴宽度
 * @param {Date} selectedDate - 选中的日期
 * @returns {Date} 计算出的时间
 */
export function getTimeFromPosition(x, width, selectedDate) {
  const ratio = Math.max(0, Math.min(1, x / width))
  const minutes = Math.round(
    ratio * TIME_CONSTANTS.MINUTES_PER_DAY / TIME_CONSTANTS.TIME_SLOT_UNIT
  ) * TIME_CONSTANTS.TIME_SLOT_UNIT
  
  const date = new Date(selectedDate)
  date.setHours(0, 0, 0, 0)
  date.setMinutes(minutes)
  return date
}

/**
 * 计算时间在一天中的位置百分比
 * @param {Date} time - 时间
 * @param {Date} dayStart - 一天的开始时间
 * @returns {number} 百分比（0-100）
 */
export function getTimePosition(time, dayStart) {
  const timeMinutes = (time - dayStart) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE
  return (timeMinutes / TIME_CONSTANTS.MINUTES_PER_DAY) * 100
}

/**
 * 获取时间段样式（用于时间轴）
 * @param {Date} start - 开始时间
 * @param {Date} end - 结束时间
 * @param {Date} dayStart - 一天的开始时间
 * @returns {Object} 样式对象 { left, width }
 */
export function getSlotStyle(start, end, dayStart) {
  if (!start || !end) return {}
  
  const startMinutes = (start - dayStart) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE
  const endMinutes = (end - dayStart) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE
  
  const left = (startMinutes / TIME_CONSTANTS.MINUTES_PER_DAY) * 100
  const width = ((endMinutes - startMinutes) / TIME_CONSTANTS.MINUTES_PER_DAY) * 100
  
  return {
    left: `${left}%`,
    width: `${width}%`
  }
}

/**
 * 获取标记点样式（用于时间轴）
 * @param {Date} time - 时间
 * @param {Date} dayStart - 一天的开始时间
 * @returns {Object} 样式对象 { left }
 */
export function getMarkerStyle(time, dayStart) {
  if (!time) return {}
  
  const left = getTimePosition(time, dayStart)
  return { left: `${left}%` }
}

/**
 * 检查两个时间段是否重叠
 * @param {Date} start1 - 时间段1开始时间
 * @param {Date} end1 - 时间段1结束时间
 * @param {Date} start2 - 时间段2开始时间
 * @param {Date} end2 - 时间段2结束时间
 * @returns {boolean} 是否重叠
 */
export function isTimeOverlap(start1, end1, start2, end2) {
  return (
    (start1 >= start2 && start1 < end2) ||
    (end1 > start2 && end1 <= end2) ||
    (start1 <= start2 && end1 >= end2)
  )
}

/**
 * 格式化预约时间信息（用于对话框显示）
 * @param {Date} startTime - 开始时间
 * @param {Date} endTime - 结束时间
 * @returns {string} 格式化后的字符串
 */
export function formatBookingTime(startTime, endTime) {
  if (!startTime || !endTime) return ''
  
  const start = new Date(startTime)
  const end = new Date(endTime)
  
  const dateStr = start.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  })
  
  const timeStr = `${formatTime(start)} - ${formatTime(end)}`
  const duration = Math.round((end - start) / TIME_CONSTANTS.MILLISECONDS_PER_MINUTE)
  
  return `${dateStr} ${timeStr} (${duration}分钟)`
}

