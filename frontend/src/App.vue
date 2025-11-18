<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header class="header">
        <div class="header-content">
          <h1 class="title">
            <el-icon><Calendar /></el-icon>
            会议室预约系统
          </h1>
          <el-menu
            :default-active="activeIndex"
            class="header-menu"
            mode="horizontal"
            @select="handleSelect"
            background-color="#409EFF"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/booking">会议室预约</el-menu-item>
            <el-menu-item index="/bookings">预约记录</el-menu-item>
            <el-menu-item index="/rooms">会议室管理</el-menu-item>
            <el-menu-item index="/users">用户管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Calendar } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const activeIndex = ref('/')

watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
}, { immediate: true })

const handleSelect = (key) => {
  router.push(key)
}
</script>

<style scoped>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  height: 100vh;
  margin: 0;
  padding: 0;
}

.layout-container {
  height: 100%;
}

.header {
  background-color: #409EFF;
  padding: 0;
  height: 60px !important;
  line-height: 60px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.title {
  color: white;
  margin: 0;
  font-size: 22px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-menu {
  border: none;
  background-color: transparent !important;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}
</style>

