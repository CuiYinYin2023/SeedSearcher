<template>
  <div>
    <el-form-item label="天气筛选：">
      <el-switch :model-value="enable_weather" @update:model-value="$emit('update:enable_weather', $event)" />
      <el-button 
        text 
        type="primary" 
        @click="addWeatherClause" 
        v-if="enable_weather"
        class="mgl-8"
      >
        添加筛选条件
      </el-button>
    </el-form-item>
    
    <div v-if="enable_weather" class="filter-card weather-clauses">
      <el-form-item label="天气类型：">
        <el-checkbox-group :model-value="weather_targets" @update:model-value="$emit('update:weather_targets', $event)" class="weather-targets">
          <el-checkbox 
            v-for="option in weatherOptions" 
            :key="option.value" 
            :label="option.label"
            :value="option.value" 
          />
        </el-checkbox-group>
      </el-form-item>

      <div class="clauses-container">
        <div class="clause-item" v-for="(clause, index) in weather_clauses" :key="index">
          <div class="clause-header">
            <span class="clause-title">筛选条件 {{ index + 1 }}</span>
            <el-button 
              link 
              type="danger" 
              @click="removeWeatherClause(index)"
              v-if="weather_clauses.length > 1" 
              size="small"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>

          <div class="clause-content">
            <el-form-item label="开始日" class="clause-field">
              <el-input v-model="clause.start" style="width: 80px;" placeholder="1"></el-input>
            </el-form-item>
            <span class="clause-separator">至</span>
            <el-form-item label="结束日" class="clause-field">
              <el-input v-model="clause.end" style="width: 80px;" placeholder="28"></el-input>
            </el-form-item>
            <el-form-item label="最少天数" class="clause-field">
              <div class="input-with-suffix">
                <el-input v-model="clause.min_count" style="width: 80px;" placeholder="5"></el-input>
                <span class="field-suffix">天</span>
              </div>
            </el-form-item>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Delete } from '@element-plus/icons-vue'
import { weatherOptions } from '../constants/weatherConfig'

defineProps({
  enable_weather: Boolean,
  weather_clauses: Array,
  weather_targets: Array,
  addWeatherClause: Function,
  removeWeatherClause: Function
})

defineEmits(['update:enable_weather', 'update:weather_targets'])
</script>

<style scoped lang="scss">
.mgl-8 {
  margin-left: 8px;
}

.filter-card {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.weather-clauses {
  .weather-targets {
    .el-checkbox {
      margin-right: 16px;
      margin-bottom: 8px;
    }
  }

  .clauses-container {
    margin-top: 16px;
  }

  .clause-item {
    margin-bottom: 16px;
    padding: 16px;
    background-color: white;
    border-radius: 6px;
    border: 1px solid #dcdfe6;
    transition: all 0.3s ease;

    &:hover {
      border-color: #409eff;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
    }

    &:last-child {
      margin-bottom: 0;
    }

    .clause-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #f0f0f0;

      .clause-title {
        font-weight: 500;
        color: #303133;
        font-size: 14px;
      }

      .el-button {
        font-size: 12px;

        .el-icon {
          margin-right: 4px;
        }
      }
    }

    .clause-content {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;

      .clause-field {
        margin-bottom: 0;

        .input-with-suffix {
          display: flex;
          align-items: center;
          gap: 8px;

          .field-suffix {
            font-size: 14px;
            color: #909399;
            white-space: nowrap;
          }
        }
      }

      .clause-separator {
        font-size: 14px;
        color: #606266;
        margin: 0 4px;
      }
    }
  }
}
</style>
