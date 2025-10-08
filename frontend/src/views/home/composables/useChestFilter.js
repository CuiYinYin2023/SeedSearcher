// 宝箱筛选 Composable
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { chestItems } from '../constants/chestConfig'

export function useChestFilter() {
  const enable_chests = ref(false)
  const chest_rules_mode = ref('ALL') // ALL / ANY
  const chest_rules = ref([])

  // 添加简单宝箱规则
  function addSimpleChestRule() {
    chest_rules.value.push({
      type: 'atom',
      level: 20,
      item: '磁铁戒指'
    })
  }

  // 添加 OR 组宝箱规则
  function addOrGroupChestRule() {
    chest_rules.value.push({
      type: 'or_group',
      items: [
        [{ level: 80, item: '长柄锤' }]
      ]
    })
  }

  // 移除宝箱规则
  function removeChestRule(index) {
    chest_rules.value.splice(index, 1)
  }

  // 添加 AND 子组
  function addAndSubGroup(rule) {
    if (rule.type === 'or_group') {
      rule.items.push([{ level: 80, item: '长柄锤' }])
    }
  }

  // 移除 AND 子组
  function removeAndSubGroup(rule, subIndex) {
    if (rule.type === 'or_group' && rule.items.length > 1) {
      rule.items.splice(subIndex, 1)
    }
  }

  // 添加原子条件到子组
  function addAtomToSubGroup(subGroup) {
    subGroup.push({ level: 80, item: '长柄锤' })
  }

  // 从子组移除原子条件
  function removeAtomFromSubGroup(subGroup, atomIndex) {
    if (subGroup.length > 1) {
      subGroup.splice(atomIndex, 1)
    }
  }

  // 应用预设模板
  function applyChestPreset(preset) {
    chest_rules_mode.value = preset.mode
    chest_rules.value = JSON.parse(JSON.stringify(preset.rules))
    ElMessage.success(`已应用预设：${preset.name}`)
  }

  // 根据楼层获取物品列表
  function getItemsByLevel(level) {
    return chestItems[level] || []
  }

  // 楼层变更处理 - 简单条件
  function handleLevelChange(rule, newLevel) {
    if (rule.item) {
      const newItems = getItemsByLevel(newLevel)
      if (!newItems.includes(rule.item)) {
        rule.item = ''
        ElMessage.info('楼层已变更，请重新选择物品')
      }
    }
  }

  // 楼层变更处理 - 原子条件
  function handleAtomLevelChange(atom, newLevel) {
    if (atom.item) {
      const newItems = getItemsByLevel(newLevel)
      if (!newItems.includes(atom.item)) {
        atom.item = ''
        ElMessage.info('楼层已变更，请重新选择物品')
      }
    }
  }

  // 验证宝箱规则
  function validateChestRules() {
    if (!enable_chests.value) return true

    if (chest_rules.value.length === 0) {
      ElMessage.error('请至少添加一个宝箱规则')
      return false
    }

    for (const rule of chest_rules.value) {
      if (rule.type === 'atom') {
        if (!rule.level || !rule.item) {
          ElMessage.error('简单条件必须选择楼层和物品')
          return false
        }
      } else if (rule.type === 'or_group') {
        if (!rule.items || rule.items.length === 0) {
          ElMessage.error('OR 组至少需要一个 AND 子组')
          return false
        }
        for (const subGroup of rule.items) {
          if (subGroup.length === 0) {
            ElMessage.error('AND 子组至少需要一个条件')
            return false
          }
          for (const atom of subGroup) {
            if (!atom.level || !atom.item) {
              ElMessage.error('所有条件必须选择楼层和物品')
              return false
            }
          }
        }
      }
    }

    return true
  }

  // 转换前端数据格式为后端格式
  function formatChestRulesForBackend(rules) {
    return rules.map(rule => {
      if (rule.type === 'atom') {
        return [rule.level, rule.item]
      } else if (rule.type === 'or_group') {
        return rule.items.map(subGroup =>
          subGroup.map(atom => [atom.level, atom.item])
        )
      }
      return rule
    })
  }

  return {
    enable_chests,
    chest_rules_mode,
    chest_rules,
    addSimpleChestRule,
    addOrGroupChestRule,
    removeChestRule,
    addAndSubGroup,
    removeAndSubGroup,
    addAtomToSubGroup,
    removeAtomFromSubGroup,
    applyChestPreset,
    getItemsByLevel,
    handleLevelChange,
    handleAtomLevelChange,
    validateChestRules,
    formatChestRulesForBackend
  }
}
