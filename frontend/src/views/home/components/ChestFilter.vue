<template>
  <div>
    <el-form-item label="宝箱筛选：">
      <el-switch :model-value="enable_chests" @update:model-value="$emit('update:enable_chests', $event)" />
    </el-form-item>
    
    <div v-if="enable_chests" class="filter-card chests-clauses">
      <!-- 预设模板 -->
      <div class="preset-section">
        <div class="section-title">
          <span>快速选择预设</span>
          <el-tooltip content="点击应用预设配置" placement="top">
            <el-icon :size="16" style="margin-left: 4px; color: #909399; cursor: pointer;">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
        <div class="preset-list">
          <div v-for="(preset, index) in chestPresets" :key="index" class="preset-card"
            @click="applyChestPreset(preset)">
            <div class="preset-name">📦 {{ preset.name }}</div>
            <div class="preset-desc">{{ preset.description }}</div>
          </div>
        </div>
      </div>

      <el-divider />

      <!-- 自定义规则 -->
      <div class="custom-section">
        <div class="section-title">自定义规则</div>

        <el-form-item label="顶层模式：">
          <el-radio-group :model-value="chest_rules_mode" @update:model-value="$emit('update:chest_rules_mode', $event)">
            <el-radio :value="'ALL'">全部满足 (AND)</el-radio>
            <el-radio :value="'ANY'">满足任一 (OR)</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 规则列表 -->
        <div class="rules-container">
          <div v-for="(rule, ruleIndex) in chest_rules" :key="ruleIndex" class="rule-card">
            <div class="rule-header">
              <span class="rule-title">
                规则 {{ ruleIndex + 1 }}
                <el-tag :type="rule.type === 'atom' ? 'success' : 'warning'" size="small" style="margin-left: 8px;">
                  {{ rule.type === 'atom' ? '简单条件' : 'OR 组' }}
                </el-tag>
              </span>
              <el-button link type="danger" @click="removeChestRule(ruleIndex)" size="small">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>

            <!-- 简单条件 (atom) -->
            <div v-if="rule.type === 'atom'" class="rule-content">
              <el-form-item label="楼层" style="margin-bottom: 0;">
                <el-select v-model="rule.level" placeholder="选择楼层" style="width: 100px;"
                  @change="(newLevel) => handleLevelChange(rule, newLevel)">
                  <el-option v-for="level in chestLevels" :key="level" :label="`${level}层`" :value="level" />
                </el-select>
              </el-form-item>
              <span class="rule-separator">=</span>
              <el-form-item label="物品" style="margin-bottom: 0;">
                <el-select v-model="rule.item" placeholder="选择物品" style="width: 140px;">
                  <el-option v-for="item in getItemsByLevel(rule.level)" :key="item" :label="item" :value="item" />
                </el-select>
              </el-form-item>
            </div>

            <!-- OR 组 -->
            <div v-else-if="rule.type === 'or_group'" class="or-group-content">
              <div v-for="(subGroup, subIndex) in rule.items" :key="subIndex" class="and-subgroup">
                <div class="subgroup-header">
                  <span class="subgroup-title">AND 子组 {{ subIndex + 1 }}</span>
                  <el-button link type="danger" @click="removeAndSubGroup(rule, subIndex)"
                    v-if="rule.items.length > 1" size="small">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>

                <div class="subgroup-atoms">
                  <div v-for="(atom, atomIndex) in subGroup" :key="atomIndex" class="atom-item">
                    <el-select v-model="atom.level" placeholder="楼层" style="width: 100px;"
                      @change="(newLevel) => handleAtomLevelChange(atom, newLevel)">
                      <el-option v-for="level in chestLevels" :key="level" :label="`${level}层`" :value="level" />
                    </el-select>
                    <span class="atom-separator">=</span>
                    <el-select v-model="atom.item" placeholder="物品" style="width: 140px;">
                      <el-option v-for="item in getItemsByLevel(atom.level)" :key="item" :label="item"
                        :value="item" />
                    </el-select>
                    <el-button link type="danger" @click="removeAtomFromSubGroup(subGroup, atomIndex)"
                      v-if="subGroup.length > 1" size="small" style="margin-left: 8px;">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                  <el-button text type="primary" @click="addAtomToSubGroup(subGroup)" size="small"
                    style="margin-top: 8px;">
                    + 添加条件
                  </el-button>
                </div>
              </div>

              <el-button text type="primary" @click="addAndSubGroup(rule)" style="margin-top: 12px;">
                + 添加 AND 子组
              </el-button>
            </div>
          </div>
        </div>

        <!-- 添加规则按钮 -->
        <div class="add-rule-buttons">
          <el-button @click="addSimpleChestRule" type="primary" plain>
            + 添加简单条件
          </el-button>
          <el-button @click="addOrGroupChestRule" type="warning" plain>
            + 添加 OR 组
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Delete, QuestionFilled } from '@element-plus/icons-vue'
import { chestLevels, chestPresets } from '../constants/chestConfig'

defineProps({
  enable_chests: Boolean,
  chest_rules_mode: String,
  chest_rules: Array,
  addSimpleChestRule: Function,
  addOrGroupChestRule: Function,
  removeChestRule: Function,
  addAndSubGroup: Function,
  removeAndSubGroup: Function,
  addAtomToSubGroup: Function,
  removeAtomFromSubGroup: Function,
  applyChestPreset: Function,
  getItemsByLevel: Function,
  handleLevelChange: Function,
  handleAtomLevelChange: Function
})

defineEmits(['update:enable_chests', 'update:chest_rules_mode', 'update:chest_rules'])
</script>

<style scoped lang="scss">
.filter-card {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.chests-clauses {
  .preset-section {
    margin-bottom: 16px;

    .section-title {
      display: flex;
      align-items: center;
      font-weight: 500;
      font-size: 14px;
      color: #303133;
      margin-bottom: 12px;
    }

    .preset-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;

      .preset-card {
        padding: 12px 16px;
        background: #667eea;
        color: white;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .preset-name {
          font-size: 15px;
          font-weight: 600;
          margin-bottom: 6px;
        }

        .preset-desc {
          font-size: 12px;
          opacity: 0.9;
          line-height: 1.4;
        }
      }
    }
  }

  .custom-section {
    .section-title {
      font-weight: 500;
      font-size: 14px;
      color: #303133;
      margin-bottom: 12px;
    }

    .rules-container {
      margin-top: 16px;
      margin-bottom: 16px;

      .rule-card {
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

        .rule-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
          padding-bottom: 8px;
          border-bottom: 1px solid #f0f0f0;

          .rule-title {
            font-weight: 500;
            color: #303133;
            font-size: 14px;
            display: flex;
            align-items: center;
          }
        }

        .rule-content {
          display: flex;
          align-items: center;
          gap: 12px;

          .rule-separator {
            font-size: 16px;
            font-weight: 600;
            color: #409eff;
          }
        }

        .or-group-content {
          .and-subgroup {
            margin-bottom: 16px;
            padding: 12px;
            background-color: #fef9e7;
            border-radius: 6px;
            border: 1px solid #f9e79f;

            &:last-child {
              margin-bottom: 0;
            }

            .subgroup-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 10px;

              .subgroup-title {
                font-size: 13px;
                font-weight: 500;
                color: #856404;
              }
            }

            .subgroup-atoms {
              .atom-item {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 8px;

                &:last-child {
                  margin-bottom: 0;
                }

                .atom-separator {
                  font-size: 14px;
                  font-weight: 600;
                  color: #e67e22;
                }
              }
            }
          }
        }
      }
    }

    .add-rule-buttons {
      display: flex;
      gap: 12px;
      margin-top: 16px;
    }
  }
}
</style>
