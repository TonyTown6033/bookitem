<template>
  <div class="bookings-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>预约管理</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            创建预约
          </el-button>
        </div>
      </template>

      <el-table :data="bookings" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户" width="150">
          <template #default="{ row }">
            {{ row.user.username }}
          </template>
        </el-table-column>
        <el-table-column label="会议室" width="150">
          <template #default="{ row }">
            {{ row.room.name }}
          </template>
        </el-table-column>
        <el-table-column label="开始时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column label="结束时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="purpose" label="预约目的" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'confirmed'"
              type="warning"
              size="small"
              @click="cancelBooking(row.id)"
            >
              取消
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="deleteBooking(row.id)"
              :icon="Delete"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建预约对话框 -->
    <el-dialog v-model="dialogVisible" title="创建预约" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户" prop="user_id">
          <el-select v-model="form.user_id" placeholder="请选择用户" style="width: 100%">
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="会议室" prop="room_id">
          <el-select v-model="form.room_id" placeholder="请选择会议室" style="width: 100%">
            <el-option
              v-for="room in availableRooms"
              :key="room.id"
              :label="`${room.name} (${room.location})`"
              :value="room.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            style="width: 100%"
            :disabled-date="disabledDate"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            style="width: 100%"
            :disabled-date="disabledDate"
          />
        </el-form-item>
        <el-form-item label="预约目的" prop="purpose">
          <el-input
            v-model="form.purpose"
            type="textarea"
            :rows="3"
            placeholder="请输入预约目的"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import { bookingAPI, userAPI, roomAPI } from '@/api'

const bookings = ref([])
const users = ref([])
const rooms = ref([])
const dialogVisible = ref(false)
const formRef = ref(null)

const form = ref({
  user_id: null,
  room_id: null,
  start_time: null,
  end_time: null,
  purpose: ''
})

const rules = {
  user_id: [
    { required: true, message: '请选择用户', trigger: 'change' }
  ],
  room_id: [
    { required: true, message: '请选择会议室', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ]
}

const availableRooms = computed(() => {
  return rooms.value.filter(room => room.is_available)
})

const loadData = async () => {
  try {
    const [bookingsData, usersData, roomsData] = await Promise.all([
      bookingAPI.getBookings(),
      userAPI.getUsers(),
      roomAPI.getRooms()
    ])
    bookings.value = bookingsData
    users.value = usersData
    rooms.value = roomsData
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

const showAddDialog = () => {
  form.value = {
    user_id: null,
    room_id: null,
    start_time: null,
    end_time: null,
    purpose: ''
  }
  dialogVisible.value = true
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    
    const bookingData = {
      user_id: form.value.user_id,
      room_id: form.value.room_id,
      start_time: form.value.start_time.toISOString(),
      end_time: form.value.end_time.toISOString(),
      purpose: form.value.purpose
    }
    
    await bookingAPI.createBooking(bookingData)
    ElMessage.success('创建预约成功')
    dialogVisible.value = false
    loadData()
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('创建预约失败')
    }
  }
}

const cancelBooking = (id) => {
  ElMessageBox.confirm('确定要取消此预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await bookingAPI.cancelBooking(id)
      ElMessage.success('取消预约成功')
      loadData()
    } catch (error) {
      ElMessage.error('取消预约失败')
    }
  }).catch(() => {})
}

const deleteBooking = (id) => {
  ElMessageBox.confirm('确定要删除此预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await bookingAPI.deleteBooking(id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7 // 禁用过去的日期
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const getStatusType = (status) => {
  const types = {
    pending: 'info',
    confirmed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待确认',
    confirmed: '已确认',
    cancelled: '已取消'
  }
  return texts[status] || status
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.bookings-page {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

