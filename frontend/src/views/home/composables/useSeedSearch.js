// 种子搜索主逻辑 Composable
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import http from '@/utils/http.js'

export function useSeedSearch() {
  const seedForm = ref(null)
  const loading = ref(false)
  
  // 种子范围
  const use_legacy = ref(true)
  const seed_start = ref(0)
  const seed_range = ref(1000)

  // 表单验证规则
  const rules = ref({
    seed_start: [
      { required: true, message: '请输入种子开始值', trigger: 'blur' },
      {
        validator: (rule, value, callback) => {
          if (value === '' || value === null || value === undefined) {
            callback(new Error('种子开始值不能为空'))
            return
          }
          const num = Number(value)
          if (isNaN(num) || !Number.isInteger(num)) {
            callback(new Error('种子开始值必须是整数'))
            return
          }
          const endValue = Number(seed_range.value)
          if (!isNaN(endValue) && num >= endValue) {
            callback(new Error('种子开始值必须小于结束值'))
            return
          }
          if (!isNaN(endValue) && (endValue - num) > 5000) {
            callback(new Error('种子范围不能超过5000'))
            return
          }
          callback()
        },
        trigger: 'blur'
      }
    ],
    seed_range: [
      { required: true, message: '请输入种子结束值', trigger: 'blur' },
      {
        validator: (rule, value, callback) => {
          if (value === '' || value === null || value === undefined) {
            callback(new Error('种子结束值不能为空'))
            return
          }
          const num = Number(value)
          if (isNaN(num) || !Number.isInteger(num)) {
            callback(new Error('种子结束值必须是整数'))
            return
          }
          const startValue = Number(seed_start.value)
          if (!isNaN(startValue) && num <= startValue) {
            callback(new Error('种子结束值必须大于开始值'))
            return
          }
          if (!isNaN(startValue) && (num - startValue) > 5000) {
            callback(new Error('种子范围不能超过5000'))
            return
          }
          callback()
        },
        trigger: 'blur'
      }
    ]
  })

  // 种子范围失焦处理
  function handleSeedRangeBlur() {
    const form = seedForm.value
    if (form) {
      form.validateField('seed_start')
      form.validateField('seed_range')
    }
  }

  // 搜索种子
  async function searchSeeds(allFiltersData, validateChestRulesFn, formatChestRulesFn) {
    const form = seedForm.value
    if (!form) return
    
    const valid = await form.validate().catch(() => false)
    if (!valid) return

    // 验证宝箱规则
    if (!validateChestRulesFn()) return

    try {
      // 准备请求数据
      const requestData = {
        use_legacy: use_legacy.value,
        seed_start: +seed_start.value,
        seed_range: +seed_range.value,
        ...allFiltersData
      }

      // 格式化天气筛选数据
      if (requestData.enable_weather && requestData.weather_clauses.length) {
        requestData.weather_clauses.forEach(item => {
          item.start = Number(item.start)
          item.end = Number(item.end)
          item.min_count = Number(item.min_count)
        })
      }

      // 格式化宝箱筛选数据
      if (requestData.enable_chests && requestData.chest_rules.length) {
        requestData.chest_rules = formatChestRulesFn(requestData.chest_rules)
      }

      loading.value = true
      const res = await http.post('/api/search', requestData)
      return res
    } catch (error) {
      const errorMsg = error?.response?.data?.message || error?.message || '搜索失败'
      ElMessage.error(errorMsg)
      console.error('搜索错误：', error)
    } finally {
      loading.value = false
    }
  }

  return {
    seedForm,
    loading,
    use_legacy,
    seed_start,
    seed_range,
    rules,
    handleSeedRangeBlur,
    searchSeeds
  }
}
