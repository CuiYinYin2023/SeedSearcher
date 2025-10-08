// 矿井筛选 Composable
import { ref } from 'vue'

export function useMinesFilter() {
  const enable_mines = ref(false)
  const mines_start_day = ref(5)
  const mines_end_day = ref(5)
  const floor_start = ref(1)
  const floor_end = ref(85)
  const _require_no_infested = ref(1)
  const require_no_infested = ref(true)

  // 处理怪物层开关变更
  function handleNoInfestedChange(val) {
    require_no_infested.value = val === 1
  }

  return {
    enable_mines,
    mines_start_day,
    mines_end_day,
    floor_start,
    floor_end,
    _require_no_infested,
    require_no_infested,
    handleNoInfestedChange
  }
}
