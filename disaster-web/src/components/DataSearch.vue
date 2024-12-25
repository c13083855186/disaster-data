<template>
  <div class="data-search">
    <h2>数据查询</h2>
    
    <div class="search-container">
      <region-selector @change="handleRegionChange" />
      
      <div class="search-actions">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <!-- 数据列表 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        style="width: 100%; margin-top: 20px;">
        <el-table-column prop="integrated_code" label="一体化编码" width="300">
          <template #default="scope">
            <el-tooltip :content="getCodeExplanation(scope.row.integrated_code)" placement="top">
              <span>{{ scope.row.integrated_code }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="earthquake_code" label="地震编码" width="200" />
        <el-table-column prop="source_code" label="信息来源" width="100">
          <template #default="scope">
            <span>{{ getSourceName(scope.row.source_code) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="carrier_code" label="载体类型" width="100">
          <template #default="scope">
            <span>{{ getCarrierName(scope.row.carrier_code) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="灾情分类" />
        <el-table-column prop="subCategory" label="灾情子类" />
        <el-table-column prop="indicator" label="灾情指标" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="text" size="small" @click="handleDownload(scope.row)">下载</el-button>
            <el-button type="text" size="small" @click="handlePreview(scope.row)">预览</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next"
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import RegionSelector from './RegionSelector.vue'
import axios from 'axios'

export default {
  name: 'DataSearch',
  components: {
    RegionSelector
  },
  data() {
    return {
      loading: false,
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      searchParams: {
        region: '',
        category: '',
        subCategory: '',
        indicator: '',
        startTime: '',
        endTime: ''
      }
    }
  },
  methods: {
    // 处理地区选择变化
    handleRegionChange(data) {
      console.log('数据查询 - 接收到region变更:', data)
      
      try {
        // 获取最后一级选择的值作为region
        const getSelectedRegion = () => {
          if (data.village?.value) return data.village.value
          if (data.town?.value) return data.town.value
          if (data.county?.value) return data.county.value
          if (data.city?.value) return data.city.value
          if (data.province?.value) return data.province.value
          return ''
        }

        this.searchParams = {
          ...this.searchParams,
          region: getSelectedRegion(),
          category: data.category?.value || '',
          subCategory: data.subCategory?.value || '',
          indicator: data.indicator?.value || ''
        }

        console.log('数据查询 - 更新后的搜索参数:', this.searchParams)
      } catch (error) {
        console.error('数据查询 - 处理地区选择变化时出错:', error)
        this.$message.error('处理地区选择时出错：' + error.message)
      }
    },

    // 执行搜索
    async handleSearch() {
      console.log('数据查询 - 开始搜索，参数:', {
        ...this.searchParams,
        page: this.currentPage,
        pageSize: this.pageSize
      })

      this.loading = true
      try {
        const response = await axios.get('/api/data/search', {
          params: {
            ...this.searchParams,
            page: this.currentPage,
            pageSize: this.pageSize
          }
        })

        console.log('数据查询 - 搜索结果:', response.data)
        this.tableData = response.data.items
        this.total = response.data.total
      } catch (error) {
        console.error('数据查询 - 搜索请求失败:', error)
        console.error('数据查询 - 错误详情:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        })
        this.$message.error('查询失败：' + (error.response?.data?.message || error.message))
      } finally {
        this.loading = false
      }
    },

    // 重置搜索
    handleReset() {
      console.log('数据查询 - 重置搜索条件')
      this.searchParams = {
        region: '',
        category: '',
        subCategory: '',
        indicator: '',
        startTime: '',
        endTime: ''
      }
      this.currentPage = 1
      // 触发RegionSelector组件的重置
      this.$emit('reset')
    },

    // 处理分页大小变化
    handleSizeChange(val) {
      console.log('数据查询 - 每页显示数量变更:', val)
      this.pageSize = val
      this.handleSearch()
    },

    // 处理页码变化
    handleCurrentChange(val) {
      console.log('数据查询 - 当前页码变更:', val)
      this.currentPage = val
      this.handleSearch()
    },

    // 处理文件下载
    async handleDownload(row) {
      console.log('数据查询 - 开始下载文件:', row)
      try {
        const response = await axios.get(`/api/data/download/${row.integrated_code}`, {
          responseType: 'blob'
        })
        
        // 从响应头中获取文件名
        const contentDisposition = response.headers['content-disposition']
        let filename = row.integrated_code
        if (contentDisposition) {
          const matches = contentDisposition.match(/filename\*=UTF-8''(.+)/)
          if (matches && matches[1]) {
            filename = decodeURIComponent(matches[1])
          }
        }
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error('数据查询 - 下载文件失败:', error)
        this.$message.error('下载失败：' + (error.response?.data?.message || error.message))
      }
    },

    // 处理文件预览
    async handlePreview(row) {
      console.log('数据查询 - 预览文件:', row)
      try {
        const response = await axios.get(`/api/data/preview/${row.integrated_code}`)
        console.log('数据查询 - 预览数据:', response.data)
        // 这里可以添加预览逻辑，比如打开一个对话框显示数据
      } catch (error) {
        console.error('数据查询 - 预览文件失败:', error)
        this.$message.error('预览失败：' + (error.response?.data?.message || error.message))
      }
    },

    // 获取一体化编码说明
    getCodeExplanation(code) {
      if (!code) return '编码格式错误'
      try {
        const region = code.slice(0, 12)
        const time = code.slice(12, 26)
        const source = code.slice(26, 29)
        const carrier = code.slice(29, 30)
        const disaster = code.slice(30, 36)
        
        return `地区码: ${region}\n时间码: ${time}\n来源码: ${source}\n载体类型: ${carrier}\n灾情码: ${disaster}`
      } catch (error) {
        console.error('数据查询 - 解析一体化编码失败:', error)
        return '编码格式错误'
      }
    },

    // 获取信息来源名称
    getSourceName(code) {
      const sourceMap = {
        '300': '系统录入'
        // 可以添加更多来源类型
      }
      return sourceMap[code] || code
    },

    // 获取载体类型名称
    getCarrierName(code) {
      const carrierMap = {
        '0': '文字',
        '1': '图像',
        '2': '音频',
        '3': '视频',
        '4': '其他'
      }
      return carrierMap[code] || code
    },

    // 获取文件扩展名
    getFileExtension(carrierCode) {
      const extensionMap = {
        '0': 'xlsx',
        '1': 'jpg',
        '2': 'mp3',
        '3': 'mp4',
        '4': 'dat'
      }
      return extensionMap[carrierCode] || 'dat'
    }
  },
  mounted() {
    console.log('数据查询组件已加载')
    this.handleSearch()
  }
}
</script>

<style scoped>
.data-search {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.search-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.search-actions {
  margin: 20px 0;
  text-align: right;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 