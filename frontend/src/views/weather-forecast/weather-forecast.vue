<script setup>
import { ref } from 'vue'
import http from '@/utils/http.js'

// 简易表单参数
const seed = ref()
const start = ref(1)
const end = ref(28)
const minCount = ref(5)
// 逗号分隔的天气类型，默认 Rain,Storm；留空则使用后端默认集合（Rain, Storm, Green Rain）
const targetsText = ref('Rain,Storm')

const loading = ref(false)
const error = ref('')
const result = ref(null)

async function queryWeather() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const payload = {
      seed: Number(seed.value),
      clauses: [{ start: Number(start.value), end: Number(end.value), min_count: Number(minCount.value) }]
    }
    const t = targetsText.value.trim()
    if (t) {
      payload.targets = t.split(',').map(s => s.trim()).filter(Boolean)
    }
    const res = await http.post('/api/weather', payload)
    result.value = res
  } catch (e) {
    error.value = e?.response?.data?.message || e?.message || '请求失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>天气预测 Demo</h1>

    <p class="desc">
      输入一个种子与规则（日期区间 + 最少命中天数）。点击查询后端接口 <code>/api/weather</code>，返回是否满足（ok）以及命中的日期列表。
    </p>

    <div class="form">
      <label>
        种子（seed）：
        <input type="number" v-model.number="seed" />
      </label>
      <label>
        开始日（start）：
        <input type="number" v-model.number="start" />
      </label>
      <label>
        结束日（end）：
        <input type="number" v-model.number="end" />
      </label>
      <label>
        最少天数（min_count）：
        <input type="number" v-model.number="minCount" />
      </label>
      <label class="full">
        天气类型（targets，逗号分隔，可留空）：
        <input type="text" v-model="targetsText" placeholder="Rain,Storm 或留空用默认" />
      </label>

      <button :disabled="loading" @click="queryWeather">{{ loading ? '查询中…' : '查询天气' }}</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="result" class="result">
      <div class="summary">
        <span>是否满足规则（ok）：<strong :class="{ ok: result.ok, fail: !result.ok }">{{ result.ok ? '是' : '否'
            }}</strong></span>
        <span>命中天数：{{ (result.matched_days || []).length }}</span>
      </div>

      <table v-if="(result.matched_days || []).length" class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>绝对日</th>
            <th>季节</th>
            <th>日</th>
            <th>天气</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(d, i) in result.matched_days" :key="d.abs_day">
            <td>{{ i + 1 }}</td>
            <td>{{ d.abs_day }}</td>
            <td>{{ d.season }}</td>
            <td>{{ d.day }}</td>
            <td>{{ d.weather_zh }} ({{ d.weather }})</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

</template>

<style scoped lang="scss">
.page {
  max-width: 880px;
  margin: 24px auto;
  padding: 0 16px;
}

.desc {
  color: #666;
  margin-bottom: 16px;
}

.form {
  display: grid;
  grid-template-columns: repeat(2, minmax(240px, 1fr));
  gap: 12px 16px;
  margin-bottom: 16px;
}

.form label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form label.full {
  grid-column: 1 / -1;
}

.form input {
  flex: 1;
  padding: 6px 8px;
}

button {
  padding: 6px 12px;
  cursor: pointer;
}

.error {
  color: #c00;
  margin: 8px 0;
}

.summary {
  display: flex;
  gap: 16px;
  margin: 8px 0 12px;
}

.ok {
  color: #0a7f31;
}

.fail {
  color: #b40000;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 6px 8px;
  text-align: left;
}

.table thead {
  background: #f7f7f7;
}
</style>
