<template>
  <div>
    <el-form-item label="酒吧垃圾桶筛选：">
      <el-switch :model-value="enable_saloon" @update:model-value="$emit('update:enable_saloon', $event)" />
    </el-form-item>
    
    <div v-if="enable_saloon" class="filter-card saloon-clauses">
      <el-form-item label="检查日期范围：">
        <div class="flex-c align-base">
          <el-form-item label="开始" style="margin-bottom: 0;">
            <el-input-number 
              :model-value="saloon_start_day" 
              @update:model-value="$emit('update:saloon_start_day', $event)"
              :min="1" 
              :max="112" 
              :step="1"
              controls-position="right" 
              style="width: 120px;" 
            />
          </el-form-item>
          <span class="connectors">至</span>
          <el-form-item label="结束" style="margin-bottom: 0;">
            <el-input-number 
              :model-value="saloon_end_day" 
              @update:model-value="$emit('update:saloon_end_day', $event)"
              :min="1" 
              :max="112" 
              :step="1" 
              controls-position="right"
              style="width: 120px;" 
            />
          </el-form-item>
          <el-tooltip placement="top" effect="dark">
            <template #content>
              1-28 = 春季<br />
              29-56 = 夏季<br />
              57-84 = 秋季<br />
              85-112 = 冬季
            </template>
            <el-icon :size="16" style="margin-left: 8px; color: #909399; cursor: help;">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
      </el-form-item>

      <el-form-item label="运势值：">
        <div class="flex-c align-base">
          <el-slider 
            :model-value="saloon_daily_luck" 
            @update:model-value="$emit('update:saloon_daily_luck', $event)"
            :min="-0.1" 
            :max="0.1" 
            :step="0.01"
            :format-tooltip="(val) => val.toFixed(2)" 
            style="width: 200px;" 
          />
          <span class="value-display">{{ saloon_daily_luck.toFixed(2) }}</span>
          <el-tooltip placement="top" effect="dark">
            <template #content>
              运势影响命中概率：<br />
              -0.1（最低）→ 10% 基础概率<br />
              0.0（中等）→ 20% 基础概率<br />
              +0.1（最高）→ 30% 基础概率
            </template>
            <el-icon :size="16" style="margin-left: 8px; color: #909399; cursor: help;">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
      </el-form-item>

      <el-form-item label="垃圾之书：">
        <el-switch :model-value="saloon_has_book" @update:model-value="$emit('update:saloon_has_book', $event)" />
        <span class="field-tip">（已读书可使命中概率 +20%）</span>
      </el-form-item>

      <el-form-item label="至少命中天数：">
        <div class="flex-c align-base">
          <el-input-number 
            :model-value="saloon_require_min_hit" 
            @update:model-value="$emit('update:saloon_require_min_hit', $event)"
            :min="1" 
            :max="28" 
            controls-position="right"
            style="width: 120px;" 
          />
          <span class="field-unit">天</span>
          <el-tooltip placement="top" effect="dark">
            <template #content>
              在指定日期范围内，至少几天能从<br />
              酒吧垃圾桶获得"今日特供"才算合格
            </template>
            <el-icon :size="16" style="margin-left: 8px; color: #909399; cursor: help;">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
      </el-form-item>

      <div class="info-card">
        <div class="info-title">💡 功能说明</div>
        <div class="info-content">
          • <strong>筛选目标</strong>：只统计"今日特供 (Dish of the Day)"，其他物品不计入<br />
          • <strong>概率机制</strong>：基础 20% + 运势值 + (垃圾书 20%)<br />
          • <strong>日期范围</strong>：1-112 对应游戏内春夏秋冬四季（每季28天）<br />
          • <strong>推荐配置</strong>：春季前7天，运势 -0.1，已读书，至少命中 2 天
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { QuestionFilled } from '@element-plus/icons-vue'

defineProps({
  enable_saloon: Boolean,
  saloon_start_day: Number,
  saloon_end_day: Number,
  saloon_daily_luck: Number,
  saloon_has_book: Boolean,
  saloon_require_min_hit: Number
})

defineEmits([
  'update:enable_saloon', 
  'update:saloon_start_day', 
  'update:saloon_end_day', 
  'update:saloon_daily_luck', 
  'update:saloon_has_book', 
  'update:saloon_require_min_hit'
])
</script>

<style scoped lang="scss">
.flex-c {
  display: flex;
  gap: 8px;

  &.align-base {
    align-items: baseline;
  }
}

.connectors {
  font-size: 14px;
  color: #606266;
}

.filter-card {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.saloon-clauses {
  .value-display {
    min-width: 50px;
    text-align: center;
    font-weight: 500;
    color: #409eff;
    margin-left: 12px;
  }

  .field-tip {
    font-size: 13px;
    color: #909399;
    margin-left: 12px;
  }

  .field-unit {
    font-size: 14px;
    color: #606266;
    margin-left: 8px;
  }

  .info-card {
    margin-top: 16px;
    padding: 12px 16px;
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    border-radius: 8px;
    border-left: 4px solid #4caf50;

    .info-title {
      font-size: 14px;
      font-weight: 600;
      color: #2e7d32;
      margin-bottom: 8px;
    }

    .info-content {
      font-size: 13px;
      line-height: 1.8;
      color: #424242;

      strong {
        color: #1b5e20;
      }
    }
  }

  .el-slider {
    margin-right: 0;
  }
}
</style>
