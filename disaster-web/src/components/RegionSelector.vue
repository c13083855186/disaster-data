<template>
  <div class="region-selector">
    <el-cascader
      v-model="selectedRegions"
      :options="regionOptions"
      :props="{
        checkStrictly: true,
        label: 'label',
        value: 'value',
        children: 'children'
      }"
      placeholder="请选择地区"
      @change="handleChange"
      clearable
    />
  </div>
</template>

<script>
// 由于行政区划数据较大，建议单独放在一个文件中
import { regionData } from '../data/region-data'

export default {
  name: 'RegionSelector',
  data() {
    return {
      selectedRegions: [],
      regionOptions: regionData
    }
  },
  methods: {
    handleChange(value) {
      this.$emit('change', value)
    }
  }
}
</script>

<style scoped>
.region-selector {
  margin: 20px 0;
}
</style> 