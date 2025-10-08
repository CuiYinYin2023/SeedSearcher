<script setup>
// 导入组件
import { ref } from 'vue'
import WeatherFilter from './components/WeatherFilter.vue'
import MinesFilter from './components/MinesFilter.vue'
import ChestFilter from './components/ChestFilter.vue'
import DesertFilter from './components/DesertFilter.vue'
import SaloonFilter from './components/SaloonFilter.vue'
import NightEventFilter from './components/NightEventFilter.vue'
import SearchResult from './components/SearchResult.vue'

// 导入 composables
import { useSeedSearch } from './composables/useSeedSearch'
import { useWeatherFilter } from './composables/useWeatherFilter'
import { useMinesFilter } from './composables/useMinesFilter'
import { useChestFilter } from './composables/useChestFilter'
import { useDesertFilter } from './composables/useDesertFilter'
import { useSaloonFilter } from './composables/useSaloonFilter'
import { useNightEventFilter } from './composables/useNightEventFilter'

// 主搜索逻辑
const {
  seedForm,
  loading,
  use_legacy,
  seed_start,
  seed_range,
  rules,
  handleSeedRangeBlur,
  searchSeeds
} = useSeedSearch()

// 天气筛选
const weatherFilter = useWeatherFilter()

// 矿井筛选
const minesFilter = useMinesFilter()

// 宝箱筛选
const chestFilter = useChestFilter()

// 沙漠节筛选
const desertFilter = useDesertFilter()

// 酒吧筛选
const saloonFilter = useSaloonFilter()

// 夜间事件筛选
const nightEventFilter = useNightEventFilter()

// 搜索结果
const searchResult = ref(null)

// 搜索按钮处理
async function handleSearch() {
  // 收集所有筛选器数据
  const allFiltersData = {
    // 天气筛选
    enable_weather: weatherFilter.enable_weather.value,
    weather_clauses: weatherFilter.weather_clauses.value,
    weather_targets: weatherFilter.weather_targets.value,

    // 矿井筛选
    enable_mines: minesFilter.enable_mines.value,
    mines_start_day: minesFilter.mines_start_day.value,
    mines_end_day: minesFilter.mines_end_day.value,
    floor_start: minesFilter.floor_start.value,
    floor_end: minesFilter.floor_end.value,
    _require_no_infested: minesFilter._require_no_infested.value,
    require_no_infested: minesFilter.require_no_infested.value,

    // 宝箱筛选
    enable_chests: chestFilter.enable_chests.value,
    chest_rules_mode: chestFilter.chest_rules_mode.value,
    chest_rules: chestFilter.chest_rules.value,

    // 沙漠节筛选
    enable_desert: desertFilter.enable_desert.value,
    require_leah: desertFilter.require_leah.value,
    require_jas: desertFilter.require_jas.value,

    // 酒吧筛选
    enable_saloon: saloonFilter.enable_saloon.value,
    saloon_start_day: saloonFilter.saloon_start_day.value,
    saloon_end_day: saloonFilter.saloon_end_day.value,
    saloon_daily_luck: saloonFilter.saloon_daily_luck.value,
    saloon_has_book: saloonFilter.saloon_has_book.value,
    saloon_require_min_hit: saloonFilter.saloon_require_min_hit.value,

    // 夜间事件筛选
    enable_night_event: nightEventFilter.enable_night_event.value,
    night_check_day: nightEventFilter.night_check_day.value,
    night_greenhouse_unlocked: nightEventFilter.night_greenhouse_unlocked.value,
  }

  const result = await searchSeeds(
    allFiltersData,
    chestFilter.validateChestRules,
    chestFilter.formatChestRulesForBackend
  )
  
  // 保存搜索结果
  searchResult.value = result
}

// 重置搜索结果
function handleReset() {
  searchResult.value = null
}
</script>

<template>
  <el-container>
    <el-aside width="600px">
      <el-form :model="{ seed_start, seed_range }" :rules="rules" ref="seedForm">
        <!-- 种子范围 -->
        <el-form-item label="是否启用旧随机：">
          <el-switch v-model="use_legacy" disabled />
        </el-form-item>

        <el-form-item label="种子范围：">
          <div class="flex-c">
            <el-form-item prop="seed_start" style="margin-bottom: 0;">
              <el-input v-model="seed_start" style="width: 150px;" placeholder="开始值" @blur="handleSeedRangeBlur" />
            </el-form-item>
            <span class="connectors">至</span>
            <el-form-item prop="seed_range" style="margin-bottom: 0;">
              <el-input v-model="seed_range" style="width: 150px;" placeholder="结束值" @blur="handleSeedRangeBlur" />
            </el-form-item>
          </div>
        </el-form-item>

        <!-- 天气筛选组件 -->
        <WeatherFilter v-model:enable_weather="weatherFilter.enable_weather.value"
          v-model:weather_clauses="weatherFilter.weather_clauses.value"
          v-model:weather_targets="weatherFilter.weather_targets.value"
          :addWeatherClause="weatherFilter.addWeatherClause" :removeWeatherClause="weatherFilter.removeWeatherClause" />

        <!-- 矿井筛选组件 -->
        <MinesFilter v-model:enable_mines="minesFilter.enable_mines.value"
          v-model:mines_start_day="minesFilter.mines_start_day.value"
          v-model:mines_end_day="minesFilter.mines_end_day.value" v-model:floor_start="minesFilter.floor_start.value"
          v-model:floor_end="minesFilter.floor_end.value"
          v-model:_require_no_infested="minesFilter._require_no_infested.value"
          :handleNoInfestedChange="minesFilter.handleNoInfestedChange" />

        <!-- 宝箱筛选组件 -->
        <ChestFilter v-model:enable_chests="chestFilter.enable_chests.value"
          v-model:chest_rules_mode="chestFilter.chest_rules_mode.value"
          v-model:chest_rules="chestFilter.chest_rules.value" :addSimpleChestRule="chestFilter.addSimpleChestRule"
          :addOrGroupChestRule="chestFilter.addOrGroupChestRule" :removeChestRule="chestFilter.removeChestRule"
          :addAndSubGroup="chestFilter.addAndSubGroup" :removeAndSubGroup="chestFilter.removeAndSubGroup"
          :addAtomToSubGroup="chestFilter.addAtomToSubGroup"
          :removeAtomFromSubGroup="chestFilter.removeAtomFromSubGroup" :applyChestPreset="chestFilter.applyChestPreset"
          :getItemsByLevel="chestFilter.getItemsByLevel" :handleLevelChange="chestFilter.handleLevelChange"
          :handleAtomLevelChange="chestFilter.handleAtomLevelChange" />

        <!-- 沙漠节筛选组件 -->
        <DesertFilter v-model:enable_desert="desertFilter.enable_desert.value"
          v-model:require_leah="desertFilter.require_leah.value" v-model:require_jas="desertFilter.require_jas.value" />

        <!-- 酒吧筛选组件 -->
        <SaloonFilter v-model:enable_saloon="saloonFilter.enable_saloon.value"
          v-model:saloon_start_day="saloonFilter.saloon_start_day.value"
          v-model:saloon_end_day="saloonFilter.saloon_end_day.value"
          v-model:saloon_daily_luck="saloonFilter.saloon_daily_luck.value"
          v-model:saloon_has_book="saloonFilter.saloon_has_book.value"
          v-model:saloon_require_min_hit="saloonFilter.saloon_require_min_hit.value" />

        <!-- 夜间事件筛选组件 -->
        <NightEventFilter v-model:enable_night_event="nightEventFilter.enable_night_event.value"
          v-model:night_check_day="nightEventFilter.night_check_day.value"
          v-model:night_greenhouse_unlocked="nightEventFilter.night_greenhouse_unlocked.value" />

        <!-- 搜索按钮 -->
        <el-form-item class="mgt-16">
          <el-button type="primary" @click="handleSearch" :loading="loading">搜索</el-button>
          <el-button @click="handleReset" :disabled="!searchResult">重置</el-button>
        </el-form-item>
      </el-form>
    </el-aside>

    <el-main style="padding-top: 0; padding-bottom: 0;">
      <!-- 搜索结果区域 -->
      <SearchResult :searchResult="searchResult" @reset="handleReset" />
    </el-main>
  </el-container>
</template>

<style scoped lang="scss">
.flex-c {
  display: flex;
  gap: 8px;
}

.connectors {
  font-size: 14px;
  color: #606266;
}

.mgt-16 {
  margin-top: 16px;
}
</style>
