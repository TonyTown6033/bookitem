<template>
  <div class="rooms-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>会议室管理</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加会议室
          </el-button>
        </div>
      </template>

      <el-table :data="rooms" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="会议室名称" />
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="capacity" label="容纳人数" width="120" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="is_available" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_available ? 'success' : 'danger'">
              {{ row.is_available ? '可用' : '不可用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="showEditDialog(row)"
              :icon="Edit"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="deleteRoom(row.id)"
              :icon="Delete"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑会议室对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑会议室' : '添加会议室'" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="会议室名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入会议室名称" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入位置" />
        </el-form-item>
        <el-form-item label="容纳人数" prop="capacity">
          <el-input-number v-model="form.capacity" :min="1" :max="500" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述"
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { roomAPI } from '@/api'

const rooms = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = ref({
  id: null,
  name: '',
  location: '',
  capacity: 10,
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入会议室名称', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入位置', trigger: 'blur' }
  ],
  capacity: [
    { required: true, message: '请输入容纳人数', trigger: 'blur' }
  ]
}

const loadRooms = async () => {
  try {
    rooms.value = await roomAPI.getRooms()
  } catch (error) {
    ElMessage.error('加载会议室列表失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  form.value = {
    id: null,
    name: '',
    location: '',
    capacity: 10,
    description: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (room) => {
  isEdit.value = true
  form.value = { ...room }
  dialogVisible.value = true
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    if (isEdit.value) {
      await roomAPI.updateRoom(form.value.id, form.value)
      ElMessage.success('更新会议室成功')
    } else {
      await roomAPI.createRoom(form.value)
      ElMessage.success('添加会议室成功')
    }
    dialogVisible.value = false
    loadRooms()
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
    }
  }
}

const deleteRoom = (id) => {
  ElMessageBox.confirm('确定要删除此会议室吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await roomAPI.deleteRoom(id)
      ElMessage.success('删除成功')
      loadRooms()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  loadRooms()
})
</script>

<style scoped>
.rooms-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

