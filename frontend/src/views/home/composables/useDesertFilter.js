// 沙漠节筛选 Composable
import { ref } from 'vue'

export function useDesertFilter() {
  const enable_desert = ref(false)
  const require_leah = ref(true)
  const require_jas = ref(true)

  return {
    enable_desert,
    require_leah,
    require_jas
  }
}
