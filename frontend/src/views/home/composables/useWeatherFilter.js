// 天气筛选 Composable
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useWeatherFilter() {
  const enable_weather = ref(false)
  const weather_clauses = ref([
    {
      start: 1,
      end: 28,
      min_count: 5
    }
  ])
  const weather_targets = ref(['Rain', 'Storm', 'Green Rain'])

  // 添加天气筛选条件
  function addWeatherClause() {
    if (weather_clauses.value.length >= 5) {
      ElMessage.error('最多只能添加5个天气筛选条件')
      return
    }
    weather_clauses.value.push({ start: 1, end: 28, min_count: 5 })
  }

  // 移除天气筛选条件
  function removeWeatherClause(index) {
    weather_clauses.value.splice(index, 1)
  }

  return {
    enable_weather,
    weather_clauses,
    weather_targets,
    addWeatherClause,
    removeWeatherClause
  }
}
