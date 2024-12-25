<template>
  <div class="selector-container">
    <div class="region-selector">
      <!-- 省份选择 -->
      <el-select
        v-model="selectedProvince"
        placeholder="请选择省份"
        @change="handleProvinceChange"
        :loading="loadingProvinces"
        clearable
      >
        <el-option
          v-for="item in provinceOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        />
      </el-select>

      <!-- 城市选择 -->
      <el-select
        v-model="selectedCity"
        placeholder="请选择城市"
        @change="handleCityChange"
        :loading="loadingCities"
        :disabled="!selectedProvince"
        clearable
      >
        <el-option
          v-for="item in cityOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        />
      </el-select>

      <!-- 区县选择 -->
      <el-select
        v-model="selectedCounty"
        placeholder="请选择区县"
        @change="handleCountyChange"
        :disabled="!selectedCity"
        clearable
      >
        <el-option
          v-for="item in countyOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        />
      </el-select>

      <!-- 街道/镇选择 -->
      <el-select
        v-model="selectedTown"
        placeholder="请选择街道/镇"
        @change="handleTownChange"
        :disabled="!selectedCounty"
        clearable
      >
        <el-option
          v-for="item in townOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        />
      </el-select>

      <!-- 村/社区选择 -->
      <el-select
        v-model="selectedVillage"
        placeholder="请选择村/社区"
        @change="handleVillageChange"
        :disabled="!selectedTown"
        clearable
      >
        <el-option
          v-for="item in villageOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        />
      </el-select>
    </div>

    <div class="disaster-selector">
      <!-- 灾情大类选择 -->
      <el-select
        v-model="selectedCategory"
        placeholder="请选择灾情大类"
        @change="handleCategoryChange"
        clearable
      >
        <el-option
          v-for="item in categoryOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        >
          <span>{{ item.code }} - {{ item.label }}</span>
        </el-option>
      </el-select>

      <!-- 灾情子类选择 -->
      <el-select
        v-model="selectedSubCategory"
        placeholder="请选择灾情子类"
        @change="handleSubCategoryChange"
        :disabled="!selectedCategory"
        clearable
      >
        <el-option
          v-for="item in subCategoryOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        >
          <span>{{ item.code }} - {{ item.label }}</span>
        </el-option>
      </el-select>

      <!-- 灾情指标选择 -->
      <el-select
        v-model="selectedIndicator"
        placeholder="请选择灾情指标"
        :disabled="!selectedCategory"
        clearable
      >
        <el-option
          v-for="item in indicatorOptions"
          :key="item.value"
          :label="item.label"
          :value="item"
        >
          <span>{{ item.code }} - {{ item.label }}</span>
        </el-option>
      </el-select>

      <!-- 添加指标值输入框 -->
      <el-input
        v-model="indicatorValue"
        :placeholder="getIndicatorPlaceholder"
        :disabled="!selectedIndicator"
        clearable
      >
        <template #append v-if="selectedIndicator?.unit">
          {{ selectedIndicator.unit }}
        </template>
      </el-input>
    </div>

    <div v-if="selectedPath" class="selected-path">
      已选择: {{ selectedPath }}
    </div>
  </div>
</template>

<script>
import { regionData } from '../data/region-data'

export default {
  name: 'RegionSelector',
  data() {
    return {
      provinceOptions: [],
      cityOptions: [],
      countyOptions: [],
      townOptions: [],
      villageOptions: [],

      selectedProvince: null,
      selectedCity: null,
      selectedCounty: null,
      selectedTown: null,
      selectedVillage: null,

      loadingProvinces: false,
      loadingCities: false,
      loadingCounties: false,
      loadingTowns: false,
      loadingVillages: false,

      selectedPath: '',

      categoryOptions: [
        { value: '1', code: '1', label: '地震事件信息' },
        { value: '2', code: '2', label: '人员伤亡及失踪信息' },
        { value: '3', code: '3', label: '房屋破坏信息' },
        { value: '4', code: '4', label: '生命线工程灾情信息' },
        { value: '5', code: '5', label: '次生灾害信息' }
      ],
      subCategoryMap: {
        '1': [{ value: '01', code: '01', label: '震情信息' }],
        '2': [
          { value: '01', code: '01', label: '死亡' },
          { value: '02', code: '02', label: '受伤' },
          { value: '03', code: '03', label: '失踪' }
        ],
        '3': [
          { value: '01', code: '01', label: '土木' },
          { value: '02', code: '02', label: '砖木' },
          { value: '03', code: '03', label: '砖混' },
          { value: '04', code: '04', label: '框架' },
          { value: '05', code: '05', label: '其他' }
        ],
        '4': [
          { value: '01', code: '01', label: '交通' },
          { value: '02', code: '02', label: '供水' },
          { value: '03', code: '03', label: '输油' },
          { value: '04', code: '04', label: '燃气' },
          { value: '05', code: '05', label: '电力' },
          { value: '06', code: '06', label: '通信' },
          { value: '07', code: '07', label: '水利' }
        ],
        '5': [
          { value: '01', code: '01', label: '崩塌' },
          { value: '02', code: '02', label: '滑坡' },
          { value: '03', code: '03', label: '泥石流' },
          { value: '04', code: '04', label: '岩溶塌陷' },
          { value: '05', code: '05', label: '地裂缝' },
          { value: '06', code: '06', label: '地面沉降' },
          { value: '07', code: '07', label: '其他(沙土液化、火灾、毒气泄露、爆炸、环境污染、瘟疫、海啸等)' }
        ]
      },
      indicatorMap: {
        '1': [
          { value: '001', code: '001', label: '地理位置' },
          { value: '002', code: '002', label: '时间' },
          { value: '003', code: '003', label: '震级' },
          { value: '004', code: '004', label: '震源深度' },
          { value: '005', code: '005', label: '烈度' }
        ],
        '2': [
          { value: '001', code: '001', label: '受灾人数' },
          { value: '002', code: '002', label: '受灾程度' }
        ],
        '3': [
          { value: '001', code: '001', label: '一般损坏面积' },
          { value: '002', code: '002', label: '严重损坏面积' },
          { value: '003', code: '003', label: '受灾程度' }
        ],
        '4': [
          { value: '001', code: '001', label: '受灾设施数' },
          { value: '002', code: '002', label: '受灾范围' },
          { value: '003', code: '003', label: '受灾程度' }
        ],
        '5': [
          { value: '001', code: '001', label: '灾害损失' },
          { value: '002', code: '002', label: '灾害范围' },
          { value: '003', code: '003', label: '受灾程度' }
        ]
      },
      selectedCategory: null,
      selectedSubCategory: null,
      selectedIndicator: null,
      subCategoryOptions: [],
      indicatorOptions: [],
      indicatorValue: ''
    }
  },
  async created() {
    await this.loadProvinces()
  },
  computed: {
    getIndicatorPlaceholder() {
      return this.selectedIndicator 
        ? `请输入${this.selectedIndicator.label}` 
        : '请先选择指标'
    }
  },
  methods: {
    async loadProvinces() {
      try {
        this.loadingProvinces = true
        const data = await regionData.initProvinceList()
        if (Array.isArray(data) && data.length > 0) {
          this.provinceOptions = data
        }
      } catch (error) {
        console.error('加载省份列表失败:', error)
      } finally {
        this.loadingProvinces = false
      }
    },

    async handleProvinceChange(province) {
      this.resetCityAndBelow()
      
      if (province) {
        await this.loadCities(province.value)
      }
      this.updatePath()
    },

    async loadCities(provinceCode) {
      try {
        this.loadingCities = true
        const data = await regionData.loadRegionData(provinceCode)
        if (Array.isArray(data)) {
          this.cityOptions = data
        }
      } catch (error) {
        console.error('加载城市数据失败:', error)
      } finally {
        this.loadingCities = false
      }
    },

    resetCityAndBelow() {
      this.selectedCity = null
      this.selectedCounty = null
      this.selectedTown = null
      this.selectedVillage = null
      this.cityOptions = []
      this.countyOptions = []
      this.townOptions = []
      this.villageOptions = []
    },

    resetCountyAndBelow() {
      this.selectedCounty = null
      this.selectedTown = null
      this.selectedVillage = null
      this.countyOptions = []
      this.townOptions = []
      this.villageOptions = []
    },

    async handleCityChange(city) {
      this.resetCountyAndBelow()
      
      if (city) {
        await this.loadCounties(city.value)
      }
      this.updatePath()
    },

    async loadCounties(countyCode) {
      try {
        this.loadingCounties = true
        const data = await regionData.loadRegionData(countyCode)
        if (Array.isArray(data)) {
          this.countyOptions = data
        }
      } catch (error) {
        console.error('加载区县数据失败:', error)
      } finally {
        this.loadingCounties = false
      }
    },

    async handleCountyChange(county) {
      this.selectedTown = null
      this.selectedVillage = null
      this.townOptions = []
      this.villageOptions = []

      if (county) {
        this.townOptions = await regionData.loadRegionData(county.value)
      }
      this.updatePath()
    },

    async handleTownChange(town) {
      this.selectedVillage = null
      this.villageOptions = []

      if (town) {
        this.villageOptions = await regionData.loadRegionData(town.value)
      }
      this.updatePath()
    },

    handleVillageChange() {
      this.updatePath()
    },

    handleCategoryChange(category) {
      this.selectedSubCategory = null;
      this.selectedIndicator = null;
      if (category) {
        this.subCategoryOptions = this.subCategoryMap[category.value] || [];
        this.indicatorOptions = this.indicatorMap[category.value] || [];
      } else {
        this.subCategoryOptions = [];
        this.indicatorOptions = [];
      }
      this.updatePath();
    },

    handleSubCategoryChange() {
      this.updatePath();
    },

    updatePath() {
      const selections = [
        this.selectedProvince,
        this.selectedCity,
        this.selectedCounty,
        this.selectedTown,
        this.selectedVillage,
        this.selectedCategory,
        this.selectedSubCategory,
        this.selectedIndicator
      ].filter(Boolean);

      this.selectedPath = selections.length > 0
        ? selections.map(item => item.label).join(' / ') + 
          (this.indicatorValue ? `: ${this.indicatorValue}` : '')
        : '';

      this.$emit('change', {
        province: this.selectedProvince,
        city: this.selectedCity,
        county: this.selectedCounty,
        town: this.selectedTown,
        village: this.selectedVillage,
        category: this.selectedCategory,
        subCategory: this.selectedSubCategory,
        indicator: this.selectedIndicator,
        indicatorValue: this.indicatorValue,
        path: this.selectedPath
      });
    }
  },
  watch: {
    indicatorValue() {
      this.updatePath();
    }
  }
}
</script>

<style scoped>
.selector-container {
  margin: 20px 0;
}

.region-selector, .disaster-selector {
  display: flex;
  gap: 10px;
  flex-wrap: nowrap;
  margin-bottom: 10px;
}

.el-select {
  width: 160px;
  flex-shrink: 0;
}

.el-input {
  width: 160px;
  flex-shrink: 0;
}

.selected-path {
  width: 100%;
  margin-top: 10px;
  color: #409EFF;
  font-size: 14px;
  flex-basis: 100%;
}
</style> 