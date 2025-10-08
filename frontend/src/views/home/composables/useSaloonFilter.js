// 酒吧垃圾桶筛选 Composable
import { ref } from 'vue'

export function useSaloonFilter() {
  const enable_saloon = ref(false)
  const saloon_start_day = ref(1)
  const saloon_end_day = ref(7)
  const saloon_daily_luck = ref(-0.1)
  const saloon_has_book = ref(false)
  const saloon_require_min_hit = ref(1)

  return {
    enable_saloon,
    saloon_start_day,
    saloon_end_day,
    saloon_daily_luck,
    saloon_has_book,
    saloon_require_min_hit
  }
}
