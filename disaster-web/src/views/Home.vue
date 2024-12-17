<template>
  <div class="home">
    <el-container>
      <el-header>
        <h1>数据管理系统</h1>
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          @select="handleSelect"
        >
          <el-menu-item index="upload">上传数据</el-menu-item>
          <el-menu-item index="search">数据查询</el-menu-item>
        </el-menu>
      </el-header>
      
      <el-main>
        <div v-if="activeMenu === 'upload'">
          <file-upload></file-upload>
        </div>
        <div v-else-if="activeMenu === 'search'">
          <!-- 数据查询组件将在这里 -->
          <data-search></data-search>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue'
import DataSearch from '@/components/DataSearch.vue'

export default {
  name: 'HomePage',
  components: {
    FileUpload,
    DataSearch
  },
  data() {
    return {
      activeMenu: '',
    }
  },
  methods: {
    handleSelect(key) {
      this.activeMenu = key
    }
  }
}
</script>

<style scoped>
.home {
  height: 100vh;
}
.el-header {
  background-color: #f5f7fa;
  padding: 20px;
}
h1 {
  color: #333;
  margin: 0 0 20px 0;
}
.el-main {
  padding: 20px;
}
</style>