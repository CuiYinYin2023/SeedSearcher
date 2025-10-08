// 夜间事件筛选 Composable
import { ref } from 'vue'

export function useNightEventFilter() {
  const enable_night_event = ref(false)
  const night_check_day = ref(1)
  const night_greenhouse_unlocked = ref(false)

  return {
    enable_night_event,
    night_check_day,
    night_greenhouse_unlocked
  }
}
