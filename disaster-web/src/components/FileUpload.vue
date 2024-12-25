<template>
  <div class="upload-container">
    <region-selector @change="handleRegionChange" />
    
    <div class="upload-section">
      <el-upload
        class="upload-area"
        drag
        action="/api/data/upload/"
        multiple
        :auto-upload="false"
        :headers="uploadHeaders"
        :data="uploadData"
        :on-success="handleSuccess"
        :on-error="handleError"
        :before-upload="beforeUpload"
        ref="upload"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击选择</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持上传文字(Excel/CSV)、图像、音频、视频等文件，且不超过10MB
          </div>
        </template>
      </el-upload>
      
      <div class="upload-button-container">
        <el-button type="primary" @click="submitUpload">开始上传</el-button>
      </div>
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
      uploadHeaders: {
        // 如果需要认证token
        // 'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      uploadData: {
        integrated_code: '',
        earthquake_code: '',
        source_code: '300',  // 默认信息来源编码
        carrier_code: '',
        disaster_code: '4',  // 默认灾情编码
        data_type: '',
        category: '',
        subCategory: '',
        indicator: ''
      }
    }
  },
  methods: {
    submitUpload() {
      // 从localStorage获取region信息
      const regionInfo = localStorage.getItem('selectedRegion')
      console.log('当前region信息:', regionInfo)

      // 验证所有选择框是否都已选择
      if (!regionInfo) {
        this.$message.error('请先选择地区！')
        console.log('region验证失败：未找到region信息')
        return
      }

      const regionData = JSON.parse(regionInfo)
      console.log('解析后的region数据:', regionData)

      // 检查fullData中的选择情况
      const { fullData } = regionData
      console.log('检查fullData:', fullData)

      if (!fullData?.category?.value) {
        this.$message.error('请先选择灾情分类！')
        console.log('验证失败：未选择灾情分类')
        return
      }
      if (!fullData?.subCategory?.value) {
        this.$message.error('请先选择灾情子类！')
        console.log('验证失败：未选择灾情子类')
        return
      }
      if (!fullData?.indicator?.value) {
        this.$message.error('请先选择灾情指标！')
        console.log('验证失败：未选择灾情指标')
        return
      }

      // 验证通过，开始上传
      console.log('验证通过，准备上传文件')
      this.$refs.upload.submit()
    },
    handleRegionChange(data) {
      console.log('接收到region变更:', data)

      // 检查数据有效性
      if (!data || (!data.province && !data.category && !data.subCategory && !data.indicator)) {
        console.log('收到无效的region数据，跳过更新')
        return
      }

      // 从localStorage获取现有数据
      const existingData = localStorage.getItem('selectedRegion')
      if (existingData) {
        const parsedData = JSON.parse(existingData)
        // 如果新数据是空的，保留现有数据
        if (!data.province && parsedData.fullData.province) {
          console.log('保留现有region数据')
          return
        }
      }

      // 获取最后一级选择的值作为region
      const getSelectedRegion = () => {
        if (data.village?.value) return data.village.value
        if (data.town?.value) return data.town.value
        if (data.county?.value) return data.county.value
        if (data.city?.value) return data.city.value
        if (data.province?.value) return data.province.value
        return ''
      }

      // 获取12位地区码（使用最后一级选择的值）
      const getRegionCode = () => {
        if (data.village?.value) return data.village.value
        if (data.town?.value) return data.town.value
        if (data.county?.value) return data.county.value
        if (data.city?.value) return data.city.value
        if (data.province?.value) return data.province.value
        return ''
      }

      // 生成14位时间码
      const generateTimeCode = () => {
        const now = new Date()
        return now.getFullYear().toString() +
          (now.getMonth() + 1).toString().padStart(2, '0') +
          now.getDate().toString().padStart(2, '0') +
          now.getHours().toString().padStart(2, '0') +
          now.getMinutes().toString().padStart(2, '0') +
          now.getSeconds().toString().padStart(2, '0')
      }

      // 生成一体化编码：12位地区码 + 14位时间码 + 300(信息来源) + 1位文件类型 + 6位灾情编码
      const generateIntegratedCode = () => {
        const regionCode = getRegionCode().padEnd(12, '0')
        const timeCode = generateTimeCode()
        const sourceCode = '300'  // 信息来源编码
        const fileType = this.uploadData.carrier_code || '0'  // 文件类型编码
        const disasterCode = generateDisasterCode().padStart(6, '0')  // 灾情编码，确保6位
        return regionCode + timeCode + sourceCode + fileType + disasterCode
      }
      const generateEarthquakeCode = () => {
        const regionCode = getRegionCode().padEnd(12, '0')
        const timeCode = generateTimeCode()
        return regionCode + timeCode
      }
      // 生成灾情编码：大类编码 + 子类编码 + 指标编码
      const generateDisasterCode = () => {
        const categoryCode = data.category?.code || ''
        const subCategoryCode = data.subCategory?.code || ''
        const indicatorCode = data.indicator?.code || ''
        return categoryCode + subCategoryCode + indicatorCode
      }

      const selectedRegion = getSelectedRegion()
      console.log('获取到的region值:', selectedRegion)

      // 更新上传数据
      this.uploadData = {
        ...this.uploadData,
        integrated_code: generateIntegratedCode(),
        earthquake_code: generateEarthquakeCode(),  // 使用相同的生成逻辑
        disaster_code: generateDisasterCode() || '4',  // 灾情分类代码，默认为4
        category: data.category?.value || '',
        subCategory: data.subCategory?.value || '',
        indicator: data.indicator?.value || ''
      }

      // 构建要存储的数据结构
      const storageData = {
        region: selectedRegion,
        category: data.category?.value || '',
        subCategory: data.subCategory?.value || '',
        indicator: data.indicator?.value || '',
        fullData: {
          province: data.province || null,
          city: data.city || null,
          county: data.county || null,
          town: data.town || null,
          village: data.village || null,
          category: data.category || null,
          subCategory: data.subCategory || null,
          indicator: data.indicator || null
        }
      }

      // 将region信息存储到localStorage
      localStorage.setItem('selectedRegion', JSON.stringify(storageData))
      console.log('存储到localStorage的数据:', storageData)
    },
    beforeUpload(file) {
      const validTypes = {
        // 文字类型
        text: [
          'application/vnd.ms-excel',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'text/csv'
        ],
        // 图像类型
        image: [
          'image/jpeg',
          'image/png',
          'image/gif',
          'image/bmp',
          'image/webp'
        ],
        // 音频类型
        audio: [
          'audio/mpeg',
          'audio/wav',
          'audio/ogg',
          'audio/mp3',
          'audio/aac'
        ],
        // 视频类型
        video: [
          'video/mp4',
          'video/mpeg',
          'video/quicktime',
          'video/x-msvideo',
          'video/webm'
        ]
      }

      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isLt10M) {
        this.$message.error('文件大小不能超过10MB！')
        return false
      }

      // 根据文件类型设置载体编码
      let carrier_code = '4' // 默认其他
      
      // 检查文件类型
      if (validTypes.text.includes(file.type)) {
        carrier_code = '0' // 文字
      } else if (validTypes.image.includes(file.type)) {
        carrier_code = '1' // 图像
      } else if (validTypes.audio.includes(file.type)) {
        carrier_code = '2' // 音频
      } else if (validTypes.video.includes(file.type)) {
        carrier_code = '3' // 视频
      }
      
      this.uploadData.carrier_code = carrier_code
      this.uploadData.data_type = carrier_code

      return true
    },
    handleSuccess(/* response */) {
      this.$message.success('上传成功！')
    },
    async handleError(err) {
      console.error('上传错误:', err)
      let errorMessage = '上传失败'
      
      try {
        // 尝试解析错误响应
        if (err.response) {
          const errorData = await err.response.json()
          console.log('后端返回的错误数据:', errorData)
          
          if (errorData.detail) {
            if (Array.isArray(errorData.detail)) {
              // 处理多个错误信息
              errorMessage = errorData.detail.map(error => {
                return `${error.msg} (${error.loc.join('.')})`
              }).join('\n')
            } else {
              // 处理单个错误信息
              errorMessage = errorData.detail
            }
          }
        } else if (err.message) {
          errorMessage = err.message
        }
      } catch (parseError) {
        console.error('解析错误响应失败:', parseError)
        errorMessage = '解析错误响应失败'
      }

      // 使用 Element UI 的 Notification 组件显示详细错误
      this.$notify.error({
        title: '上传失败',
        message: errorMessage,
        duration: 0,  // 不自动关闭
        dangerouslyUseHTMLString: true
      })
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

.upload-button-container {
  margin-top: 20px;
  text-align: center;
}
</style>