/**
 * 预约系统常量配置
 */

// 预约状态
export const BOOKING_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  CANCELLED: 'cancelled'
}

// 状态显示文本
export const STATUS_TEXT = {
  [BOOKING_STATUS.PENDING]: '待确认',
  [BOOKING_STATUS.CONFIRMED]: '已确认',
  [BOOKING_STATUS.CANCELLED]: '已取消'
}

// 状态对应的类型（用于Element Plus）
export const STATUS_TYPE = {
  [BOOKING_STATUS.PENDING]: 'info',
  [BOOKING_STATUS.CONFIRMED]: 'success',
  [BOOKING_STATUS.CANCELLED]: 'danger'
}

// 获取状态显示文本
export function getStatusText(status) {
  return STATUS_TEXT[status] || status
}

// 获取状态类型
export function getStatusType(status) {
  return STATUS_TYPE[status] || 'info'
}

// 时间轴配置
export const TIMELINE_CONFIG = {
  TOTAL_CELLS: 48, // 总格子数（24小时 * 2）
  CELL_UNIT: 30,   // 每格时长（分钟）
  TRACK_HEIGHT: 120 // 时间轴高度（px）
}

// UI 配置
export const UI_CONFIG = {
  // 颜色主题
  COLORS: {
    PRIMARY: '#667eea',
    PRIMARY_END: '#764ba2',
    SUCCESS: '#4299e1',
    SUCCESS_END: '#48bb78',
    DANGER: '#f56565',
    DANGER_END: '#e53e3e',
    GRAY: '#e8eaed',
    TEXT_PRIMARY: '#1a1a1a',
    TEXT_SECONDARY: '#5f6368'
  },
  
  // 圆角
  BORDER_RADIUS: {
    SMALL: '8px',
    MEDIUM: '12px',
    LARGE: '16px'
  },
  
  // 阴影
  SHADOWS: {
    LIGHT: '0 2px 8px rgba(0, 0, 0, 0.04)',
    MEDIUM: '0 4px 20px rgba(0, 0, 0, 0.08)',
    HEAVY: '0 12px 48px rgba(0, 0, 0, 0.15)',
    COLORED: '0 4px 12px rgba(102, 126, 234, 0.4)'
  }
}

