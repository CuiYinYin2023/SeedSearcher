<template>
  <div v-if="searchResult" class="search-result">
    <!-- 概览卡片 -->
    <el-card class="overview-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon>
              <Trophy />
            </el-icon>
            搜索结果概览
          </span>
          <el-tag :type="searchResult.hit_count > 0 ? 'success' : 'info'" size="large">
            找到 {{ searchResult.hit_count }} 个种子
          </el-tag>
        </div>
      </template>

      <div class="overview-stats">
        <div class="stat-item">
          <div class="stat-label">搜索范围</div>
          <div class="stat-value">{{ searchResult.seed_start }} - {{ searchResult.seed_range }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">检查总数</div>
          <div class="stat-value">{{ searchResult.total_checked.toLocaleString() }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">命中率</div>
          <div class="stat-value">{{ hitRate }}%</div>
        </div>
      </div>

      <!-- 启用的筛选条件 -->
      <el-divider />
      <div class="conditions-summary">
        <div class="conditions-title">
          <el-icon>
            <Filter />
          </el-icon>
          启用的筛选条件
        </div>
        <div class="conditions-tags">
          <el-tag v-if="searchResult.conditions.weather" type="primary" effect="plain">
            <el-icon>
              <Sunny />
            </el-icon> 天气筛选
          </el-tag>
          <el-tag v-if="searchResult.conditions.mines" type="warning" effect="plain">
            <el-icon>
              <Grid />
            </el-icon> 矿井筛选
          </el-tag>
          <el-tag v-if="searchResult.conditions.chests" type="success" effect="plain">
            <el-icon>
              <Box />
            </el-icon> 宝箱筛选
          </el-tag>
          <el-tag v-if="searchResult.conditions.desert" type="danger" effect="plain">
            <el-icon>
              <Sunny />
            </el-icon> 沙漠节筛选
          </el-tag>
          <el-tag v-if="searchResult.conditions.saloon" type="info" effect="plain">
            <el-icon>
              <ShoppingCart />
            </el-icon> 酒吧垃圾桶筛选
          </el-tag>
          <el-tag v-if="searchResult.conditions.night_event" effect="plain">
            <el-icon>
              <Moon />
            </el-icon> 夜间事件筛选
          </el-tag>
          <el-tag v-if="noConditions" type="info" effect="plain">
            未启用任何筛选条件
          </el-tag>
        </div>
      </div>
    </el-card>

    <!-- 种子列表 -->
    <el-card v-if="searchResult.hit_count > 0" class="seeds-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon>
              <List />
            </el-icon>
            符合条件的种子列表
          </span>
          <div class="header-actions">
            <el-button text @click="copyAllSeeds" :icon="CopyDocument">
              复制全部
            </el-button>
            <el-button text @click="exportSeeds" :icon="Download">
              导出
            </el-button>
          </div>
        </div>
      </template>

      <div class="seeds-grid">
        <div v-for="seed in paginatedSeeds" :key="seed" class="seed-item" @click="handleSeedClick(seed)">
          <div class="seed-value">{{ seed }}</div>
          <el-button link size="small" :icon="CopyDocument" @click.stop="copySeed(seed)" class="copy-btn">
            复制
          </el-button>
        </div>
      </div>

      <!-- 分页 -->
      <el-pagination v-if="searchResult.hit_count > pageSize" v-model:current-page="currentPage"
        v-model:page-size="pageSize" :page-sizes="[20, 50, 100, 200]" :total="searchResult.hit_count"
        layout="total, sizes, prev, pager, next, jumper" class="pagination" @current-change="handlePageChange"
        @size-change="handleSizeChange" />
    </el-card>

    <!-- 无结果提示 -->
    <el-empty v-else description="未找到符合条件的种子，请尝试调整筛选条件" :image-size="200">
      <el-button type="primary" @click="$emit('reset')">
        重新搜索
      </el-button>
    </el-empty>
  </div>

  <!-- 无搜索结果时的占位 -->
  <el-empty v-else description="点击左侧【搜索】按钮开始查找种子" :image-size="200" />
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  Trophy, Filter, Sunny, Grid, Box, ShoppingCart, Moon, List,
  CopyDocument, Download
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  searchResult: {
    type: Object,
    default: null
  }
})

defineEmits(['reset'])

// 分页
const currentPage = ref(1)
const pageSize = ref(50)

// 监听搜索结果变化，重置到第一页
watch(() => props.searchResult, (newResult) => {
  if (newResult) {
    currentPage.value = 1
  }
})

// 计算当前页显示的种子列表
const paginatedSeeds = computed(() => {
  if (!props.searchResult?.hit_seeds) return []
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return props.searchResult.hit_seeds.slice(start, end)
})

// 计算命中率
const hitRate = computed(() => {
  if (!props.searchResult || props.searchResult.total_checked === 0) return '0.00'
  return ((props.searchResult.hit_count / props.searchResult.total_checked) * 100).toFixed(2)
})

// 检查是否没有启用任何条件
const noConditions = computed(() => {
  if (!props.searchResult?.conditions) return true
  return !Object.values(props.searchResult.conditions).some(v => v === true)
})

// 复制单个种子
function copySeed(seed) {
  navigator.clipboard.writeText(seed.toString()).then(() => {
    ElMessage.success(`种子 ${seed} 已复制到剪贴板`)
  }).catch(() => {
    ElMessage.error('复制失败，请手动复制')
  })
}

// 复制所有种子
function copyAllSeeds() {
  const seedsText = props.searchResult.hit_seeds.join(', ')
  navigator.clipboard.writeText(seedsText).then(() => {
    ElMessage.success(`已复制 ${props.searchResult.hit_count} 个种子到剪贴板`)
  }).catch(() => {
    ElMessage.error('复制失败，请手动复制')
  })
}

// 导出种子
function exportSeeds() {
  const seedsText = props.searchResult.hit_seeds.join('\n')
  const blob = new Blob([seedsText], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `stardew-seeds-${Date.now()}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  ElMessage.success('导出成功')
}

// 点击种子（可以扩展为查看详情）
function handleSeedClick(seed) {
  console.log('点击种子:', seed)
  // 这里可以扩展为显示该种子的详细信息
}

function handlePageChange(page) {
  currentPage.value = page
}

function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1
}
</script>

<style scoped lang="scss">
.search-result {
  display: flex;
  flex-direction: column;
  gap: 20px;

  .overview-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #303133;
      }
    }

    .overview-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 16px;

      .stat-item {
        text-align: center;
        padding: 16px;
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        border-radius: 8px;

        .stat-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }

        .stat-value {
          font-size: 24px;
          font-weight: 700;
          color: #409eff;
        }
      }
    }

    .conditions-summary {
      .conditions-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        font-weight: 600;
        color: #606266;
        margin-bottom: 12px;
      }

      .conditions-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;

        .el-tag {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
    }
  }

  .seeds-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #303133;
      }

      .header-actions {
        display: flex;
        gap: 8px;
      }
    }

    .seeds-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 12px;
      margin-bottom: 20px;

      .seed-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 16px 12px;
        background: #667eea;
        color: white;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;

        &:hover {
          box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);

          .copy-btn {
            opacity: 1;
          }
        }

        .seed-value {
          font-size: 24px;
          font-weight: 700;
          margin-bottom: 8px;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .copy-btn {
          opacity: 0;
          transition: opacity 0.3s ease;
          color: white;
        }
      }
    }

    .pagination {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  }
}
</style>
