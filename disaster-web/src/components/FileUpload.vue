<template>
  <div class="upload-container">
    <region-selector @change="handleRegionChange" />
    
    <div class="upload-section">
      <el-upload
        class="upload-area"
        drag
        action="/api/upload"
        multiple
        :headers="uploadHeaders"
        :data="uploadData"
        :on-success="handleSuccess"
        :on-error="handleError"
        :before-upload="beforeUpload"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">
          只能上传xlsx/xls/csv文件，且不超过10MB
        </div>
      </el-upload>
    </div>
  </div>
</template>

<script>
import RegionSelector from './RegionSelector.vue'

export default {
  name: 'FileUpload',
  components: {
    RegionSelector
  },
  data() {
    return {
      selectedRegion: [],
      uploadHeaders: {
        // 如果需要认证token
        // 'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      uploadData: {
        region: ''
      }
    }
  },
  methods: {
    handleRegionChange(value) {
      this.uploadData.region = value.join(',')
    },
    beforeUpload(file) {
      const validTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv'
      ]
      const isValidType = validTypes.includes(file.type)
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isValidType) {
        this.$message.error('只能上传Excel/CSV文件！')
        return false
      }
      if (!isLt10M) {
        this.$message.error('文件大小不能超过10MB！')
        return false
      }
      if (!this.uploadData.region) {
        this.$message.error('请先选择地区！')
        return false
      }
      return true
    },
    handleSuccess(response) {
      this.$message.success('上传成功！')
    },
    handleError(err) {
      this.$message.error('上传失败：' + (err.message || '未知错误'))
    }
  }
}
</script>

<style scoped>
.upload-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.upload-section {
  margin-top: 20px;
}

.upload-area {
  width: 100%;
}
</style>