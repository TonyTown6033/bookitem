<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header class="header">
        <div class="header-content">
          <h1 class="title">
            <el-icon><Calendar /></el-icon>
            <span class="title-text">会议室预约系统</span>
          </h1>
          
          <!-- 桌面端菜单 -->
          <el-menu
            :default-active="activeIndex"
            class="header-menu desktop-menu"
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
          
          <!-- 移动端菜单按钮 -->
          <el-button 
            class="mobile-menu-button"
            :icon="Menu"
            circle
            @click="mobileMenuVisible = true"
          />
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
    
    <!-- 移动端抽屉菜单 -->
    <el-drawer
      v-model="mobileMenuVisible"
      title="导航菜单"
      direction="rtl"
      size="70%"
      :with-header="true"
    >
      <el-menu
        :default-active="activeIndex"
        class="mobile-menu"
        @select="handleMobileMenuSelect"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/booking">
          <el-icon><Calendar /></el-icon>
          <span>会议室预约</span>
        </el-menu-item>
        <el-menu-item index="/bookings">
          <el-icon><Tickets /></el-icon>
          <span>预约记录</span>
        </el-menu-item>
        <el-menu-item index="/rooms">
          <el-icon><OfficeBuilding /></el-icon>
          <span>会议室管理</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Calendar, Menu, HomeFilled, Tickets, OfficeBuilding, User } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const activeIndex = ref('/')
const mobileMenuVisible = ref(false)

watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
}, { immediate: true })

const handleSelect = (key) => {
  router.push(key)
}

const handleMobileMenuSelect = (key) => {
  router.push(key)
  mobileMenuVisible.value = false
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
  white-space: nowrap;
}

.title-text {
  display: inline;
}

.header-menu {
  border: none;
  background-color: transparent !important;
}

.desktop-menu {
  display: flex;
}

.mobile-menu-button {
  display: none;
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
}

.mobile-menu-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}

.mobile-menu {
  border: none;
}

.mobile-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
  font-size: 16px;
  padding-left: 20px;
}

.mobile-menu .el-icon {
  font-size: 20px;
  margin-right: 12px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .header {
    height: 56px !important;
    line-height: 56px;
  }
  
  .header-content {
    padding: 0 12px;
  }
  
  .title {
    font-size: 18px;
    gap: 6px;
  }
  
  .title-text {
    display: none;
  }
  
  .desktop-menu {
    display: none !important;
  }
  
  .mobile-menu-button {
    display: flex;
  }
  
  .main-content {
    padding: 12px;
  }
}

/* 平板适配 */
@media (max-width: 1024px) and (min-width: 769px) {
  .header-content {
    padding: 0 16px;
  }
  
  .title {
    font-size: 20px;
  }
  
  .header-menu .el-menu-item {
    padding: 0 12px;
    font-size: 14px;
  }
  
  .main-content {
    padding: 16px;
  }
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

