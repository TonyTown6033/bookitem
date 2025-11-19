<template>
  <div class="debug-page">
    <el-card class="debug-card">
      <template #header>
        <div class="card-header">
          <h2>🔍 网络诊断工具</h2>
        </div>
      </template>

      <div class="info-section">
        <h3>📍 当前网络信息</h3>
        <div class="info-item">
          <label>当前页面地址：</label>
          <code>{{ currentURL }}</code>
        </div>
        <div class="info-item">
          <label>主机名 (Hostname)：</label>
          <code>{{ hostname }}</code>
        </div>
        <div class="info-item">
          <label>前端端口：</label>
          <code>{{ frontendPort }}</code>
        </div>
        <div class="info-item">
          <label>API 地址：</label>
          <code>{{ apiBaseURL }}</code>
        </div>
        <div class="info-item">
          <label>环境：</label>
          <el-tag :type="isProd ? 'success' : 'warning'">
            {{ isProd ? '生产环境' : '开发环境' }}
          </el-tag>
        </div>
      </div>

      <el-divider />

      <div class="test-section">
        <h3>🧪 连接测试</h3>
        
        <el-button 
          type="primary" 
          @click="testBackendConnection"
          :loading="testing"
          style="margin-bottom: 20px;"
        >
          测试后端连接
        </el-button>

        <div v-if="testResult" class="test-result">
          <el-alert
            :title="testResult.success ? '✅ 连接成功！' : '❌ 连接失败'"
            :type="testResult.success ? 'success' : 'error'"
            :description="testResult.message"
            show-icon
            :closable="false"
          />
          
          <div v-if="testResult.details" class="details">
            <h4>详细信息：</h4>
            <pre>{{ JSON.stringify(testResult.details, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <el-divider />

      <div class="tips-section">
        <h3>💡 故障排查步骤</h3>
        <ol>
          <li>
            <strong>检查后端服务：</strong>
            确保后端服务正在运行（应该在 8000 端口）
            <el-tag type="info" size="small" style="margin-left: 10px;">
              运行 ./start.sh
            </el-tag>
          </li>
          <li>
            <strong>检查网络：</strong>
            手机和电脑必须在同一个 WiFi 网络下
          </li>
          <li>
            <strong>检查防火墙：</strong>
            确保防火墙允许 8000 端口的连接
          </li>
          <li>
            <strong>获取电脑 IP：</strong>
            <el-tag type="warning" size="small" style="margin-left: 10px;">
              macOS: ifconfig | grep "inet "
            </el-tag>
            <el-tag type="warning" size="small" style="margin-left: 10px;">
              Windows: ipconfig
            </el-tag>
          </li>
          <li>
            <strong>手机访问地址：</strong>
            <code>http://电脑IP:5173</code>
            <br>
            例如：<code style="color: #409eff;">http://192.168.1.100:5173</code>
          </li>
        </ol>
      </div>

      <el-divider />

      <div class="command-section">
        <h3>⚙️ 有用的命令</h3>
        <div class="command-item">
          <label>查看本机 IP (macOS/Linux)：</label>
          <el-input 
            readonly 
            value="ifconfig | grep 'inet ' | grep -v 127.0.0.1"
            style="font-family: monospace;"
          >
            <template #append>
              <el-button @click="copyToClipboard('ifconfig | grep \'inet \' | grep -v 127.0.0.1')">
                复制
              </el-button>
            </template>
          </el-input>
        </div>
        
        <div class="command-item">
          <label>测试后端端口 (macOS/Linux)：</label>
          <el-input 
            readonly 
            :value="`curl http://${hostname}:8000/`"
            style="font-family: monospace;"
          >
            <template #append>
              <el-button @click="copyToClipboard(`curl http://${hostname}:8000/`)">
                复制
              </el-button>
            </template>
          </el-input>
        </div>

        <div class="command-item">
          <label>允许防火墙端口 (macOS)：</label>
          <el-input 
            readonly 
            value="sudo pfctl -d"
            style="font-family: monospace;"
          >
            <template #append>
              <el-button @click="copyToClipboard('sudo pfctl -d')">
                复制
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const currentURL = ref(window.location.href)
const hostname = ref(window.location.hostname)
const frontendPort = ref(window.location.port)
const isProd = ref(import.meta.env.PROD)

const apiBaseURL = computed(() => {
  if (import.meta.env.PROD) {
    return '/api'
  }
  return `http://${hostname.value}:8000/api`
})

const testing = ref(false)
const testResult = ref(null)

const testBackendConnection = async () => {
  testing.value = true
  testResult.value = null

  try {
    const testURL = `http://${hostname.value}:8000/`
    console.log('测试连接到:', testURL)
    
    const response = await axios.get(testURL, { timeout: 5000 })
    
    testResult.value = {
      success: true,
      message: '后端服务连接成功！',
      details: {
        url: testURL,
        status: response.status,
        data: response.data
      }
    }
    
    ElMessage.success('后端连接正常！')
  } catch (error) {
    console.error('连接测试失败:', error)
    
    let message = '无法连接到后端服务'
    let details = {}
    
    if (error.code === 'ECONNABORTED') {
      message = '连接超时，后端服务可能未启动或网络不通'
    } else if (error.response) {
      message = `服务器返回错误: ${error.response.status}`
      details = {
        status: error.response.status,
        data: error.response.data
      }
    } else if (error.request) {
      message = '请求已发送但未收到响应，可能原因：'
      details = {
        reasons: [
          '1. 后端服务未启动',
          '2. 防火墙阻止了连接',
          '3. 手机和电脑不在同一网络',
          `4. IP地址 ${hostname.value} 不正确`
        ]
      }
    }
    
    testResult.value = {
      success: false,
      message,
      details
    }
    
    ElMessage.error('后端连接失败，请查看详细信息')
  } finally {
    testing.value = false
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}

onMounted(() => {
  console.log('=== 网络诊断信息 ===')
  console.log('当前URL:', currentURL.value)
  console.log('Hostname:', hostname.value)
  console.log('API地址:', apiBaseURL.value)
  console.log('环境:', isProd.value ? '生产' : '开发')
})
</script>

<style scoped>
.debug-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.debug-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.info-section,
.test-section,
.tips-section,
.command-section {
  margin-bottom: 20px;
}

h3 {
  font-size: 18px;
  color: #409eff;
  margin-bottom: 15px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  min-width: 150px;
  color: #606266;
}

.info-item code {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Monaco', 'Courier New', monospace;
  color: #e6a23c;
}

.test-result {
  margin-top: 20px;
}

.details {
  margin-top: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.details h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #606266;
}

.details pre {
  background: #ffffff;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  overflow-x: auto;
  font-size: 12px;
  color: #303133;
}

.tips-section ol {
  padding-left: 20px;
}

.tips-section li {
  margin-bottom: 15px;
  line-height: 1.8;
  color: #606266;
}

.tips-section strong {
  color: #303133;
}

.command-section .command-item {
  margin-bottom: 20px;
}

.command-section label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #606266;
}

@media (max-width: 768px) {
  .debug-page {
    padding: 10px;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-item label {
    margin-bottom: 5px;
  }
}
</style>

