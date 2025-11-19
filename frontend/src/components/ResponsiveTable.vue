<template>
  <div class="responsive-table-wrapper">
    <!-- 桌面端表格 -->
    <div class="desktop-table">
      <slot name="desktop"></slot>
    </div>
    
    <!-- 移动端卡片列表 -->
    <div class="mobile-cards">
      <slot name="mobile"></slot>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.responsive-table-wrapper {
  width: 100%;
}

.desktop-table {
  display: block;
}

.mobile-cards {
  display: none;
}

@media (max-width: 768px) {
  .desktop-table {
    display: none;
  }
  
  .mobile-cards {
    display: block;
  }
}
</style>

