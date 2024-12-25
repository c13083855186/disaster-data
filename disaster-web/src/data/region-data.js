// 从后端 API 获取地区数据
export const loadRegionData = async (provinceCode) => {
  try {
    let url = '';
    if (!provinceCode) {
      url = '/api/regions/provinces';
      console.log('正在请求省份数据:', url);
    } else if (provinceCode.length === 2) {
      url = `/api/regions/cities/${provinceCode}`;
      console.log('正在请求城市数据:', url);
    } else if (provinceCode.length === 4) {
      url = `/api/regions/counties/${provinceCode}`;
      console.log('正在请求区县数据:', url);
    } else if (provinceCode.length === 6) {
      url = `/api/regions/towns/${provinceCode}`;
      console.log('正在请求街道数据:', url);
    } else if (provinceCode.length === 9) {
      url = `/api/regions/villages/${provinceCode}`;
      console.log('正在请求村数据:', url);
    }

    const response = await fetch(url);
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('API 返回数据:', data);
    return data;
  } catch (error) {
    console.error('加载地区数据失败:', error);
    console.error('详细错误信息:', error.message);
    return [];
  }
}

// 初始化时加载省份列表
export const initProvinceList = async () => {
  try {
    return await loadRegionData()
  } catch (error) {
    console.error('加载省份列表失败:', error)
    return []
  }
}

export const regionData = {
  loadRegionData,
  initProvinceList
}
