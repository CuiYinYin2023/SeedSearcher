<template>
  <div>
    <el-form-item label="矿井筛选：">
      <el-switch :model-value="enable_mines" @update:model-value="$emit('update:enable_mines', $event)" />
    </el-form-item>
    
    <div v-if="enable_mines" class="filter-card mines-clauses">
      <el-checkbox 
        :model-value="_require_no_infested" 
        @update:model-value="handleNoInfestedChange($event)"
        label="要求'完全没有怪物/史莱姆层'" 
        :true-value="1" 
        :false-value="0"
      />
      <div class="flex-c align-base">
        <el-form-item label="开始日" style="margin-bottom: 0;">
          <el-input :model-value="mines_start_day" @update:model-value="$emit('update:mines_start_day', $event)" style="width: 80px;" placeholder="开始日"></el-input>
        </el-form-item>
        <span class="connectors">至</span>
        <el-form-item label="结束日" style="margin-bottom: 0;">
          <el-input :model-value="mines_end_day" @update:model-value="$emit('update:mines_end_day', $event)" style="width: 80px;" placeholder="结束日"></el-input>
        </el-form-item>
        <el-form-item label="起始层" style="margin-bottom: 0;" class="mgl-8">
          <el-input :model-value="floor_start" @update:model-value="$emit('update:floor_start', $event)" style="width: 80px;" placeholder="起始层"></el-input>
        </el-form-item>
        <span class="connectors">至</span>
        <el-form-item label="结束层" style="margin-bottom: 0;">
          <el-input :model-value="floor_end" @update:model-value="$emit('update:floor_end', $event)" style="width: 80px;" placeholder="结束层"></el-input>
        </el-form-item>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  enable_mines: Boolean,
  mines_start_day: Number,
  mines_end_day: Number,
  floor_start: Number,
  floor_end: Number,
  _require_no_infested: Number,
  handleNoInfestedChange: Function
})

defineEmits(['update:enable_mines', 'update:mines_start_day', 'update:mines_end_day', 'update:floor_start', 'update:floor_end', 'update:_require_no_infested'])
</script>

<style scoped lang="scss">
.flex-c {
  display: flex;
  gap: 8px;

  &.align-base {
    align-items: baseline;
  }
}

.mgl-8 {
  margin-left: 8px;
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
</style>
