<template>
  <div>
    <el-form-item label="夜间事件：">
      <el-switch :model-value="enable_night_event" @update:model-value="$emit('update:enable_night_event', $event)" />
    </el-form-item>
    
    <div v-if="enable_night_event" class="filter-card night-event-clauses">
      <el-form-item label="检查日期">
        <el-input-number 
          :model-value="night_check_day" 
          @update:model-value="$emit('update:night_check_day', $event)"
          :min="1" 
          :max="28" 
          :step="1" 
          controls-position="right"
          style="width: 120px;" 
        />
      </el-form-item>
      <el-form-item label="温室是否解锁：">
        <el-switch :model-value="night_greenhouse_unlocked" @update:model-value="$emit('update:night_greenhouse_unlocked', $event)" />
      </el-form-item>
    </div>
  </div>
</template>

<script setup>
defineProps({
  enable_night_event: Boolean,
  night_check_day: Number,
  night_greenhouse_unlocked: Boolean
})

defineEmits(['update:enable_night_event', 'update:night_check_day', 'update:night_greenhouse_unlocked'])
</script>

<style scoped lang="scss">
.filter-card {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}
</style>
