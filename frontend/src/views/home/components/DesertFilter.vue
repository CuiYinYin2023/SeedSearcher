<template>
  <div>
    <el-form-item label="沙漠节筛选：">
      <el-switch :model-value="enable_desert" @update:model-value="$emit('update:enable_desert', $event)" />
    </el-form-item>
    
    <div v-if="enable_desert" class="filter-card desert-clauses">
      <el-checkbox :model-value="require_leah" @update:model-value="$emit('update:require_leah', $event)" label='需要"莉亚"' />
      <el-checkbox :model-value="require_jas" @update:model-value="$emit('update:require_jas', $event)" label='需要"贾斯"' />
    </div>
  </div>
</template>

<script setup>
defineProps({
  enable_desert: Boolean,
  require_leah: Boolean,
  require_jas: Boolean
})

defineEmits(['update:enable_desert', 'update:require_leah', 'update:require_jas'])
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
