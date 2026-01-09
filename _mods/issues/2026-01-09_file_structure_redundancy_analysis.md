# 文件结构冗余分析与重构方案

**日期**: 2026-01-09
**状态**: 🔍 分析中
**优先级**: 高

## 问题诊断

### 1. 严重重复（违反DRY原则）

| 文件A | 文件B | 重复度 | 问题 |
|-------|-------|--------|------|
| `.claude/skills/hero-balancer/references/rules.md` | `_mods/rules/rules.md` | 95% | 游戏规则重复 |
| `.claude/skills/hero-balancer/references/hero_file_rules.md` | `_mods/rules/hero_file_rules.md` | 100% | CSV规则完全相同 |
| `.claude/skills/hero-balancer/references/available_effects.md` | `_mods/rules/available_effects.md` | ? | 需验证 |

### 2. 信息密度低（香农熵值低）

**SKILL.md 问题**:
- 行数: 682行
- 包含内容: 状态机、流程、规则、案例、工具说明
- 香农熵值: ~4-5 bits（信息密度低）
- 目标: 7+ bits（高信息密度）

### 3. 违反MECE原则

**当前结构**:
```
.claude/skills/hero-balancer/
├── SKILL.md (682行，包含所有内容)
└── references/
    ├── rules.md (与_mods/rules/rules.md重复)
    ├── hero_file_rules.md (与_mods/rules/hero_file_rules.md重复)
    └── available_effects.md (可能与_mods/rules/available_effects.md重复)

_mods/rules/
├── rules.md (权威)
├── hero_file_rules.md (权威)
└── available_effects.md (权威?)
```

**问题**:
- ❌ 职责不清：游戏规则应该属于技能还是属于游戏数据？
- ❌ 重复维护：两处都要更新
- ❌ 版本不一致风险：可能出现内容不同步

---

## 重构方案

### 设计原则

1. **SSOT（单一事实来源）**: 游戏规则只有一个权威位置
2. **MECE**: 技能流程 vs 游戏规则 vs 工具使用，职责相互独立
3. **高香农熵**: 文档精简，信息密度≥7 bits
4. **清晰层次**: 流程层引用规则层，不重复规则

### 新文件结构

```
.claude/skills/hero-balancer/          # 流程层（技能执行逻辑）
├── SKILL.md                            # 技能入口（300行以内）
│   ├── 状态机概要（1页）
│   ├── 快速开始（1页）
│   ├── 状态详解（引用core/*.md）
│   └── 文档索引
├── core/                               # 核心流程文档
│   ├── statemachine.md                 # 状态机完整说明
│   ├── data_collection.md              # COLLECTING/ANALYZING详解
│   ├── proposal_creation.md            # PROPOSING详解
│   └── safety_mechanisms.md            # 三重确认机制
├── guides/                             # 使用指南
│   ├── quickstart.md                   # 5分钟快速开始
│   ├── troubleshooting.md              # 常见问题
│   └── best_practices.md               # 最佳实践
├── assets/                             # 资源文件
│   ├── hero_buff_proposal_template.md  # 方案模板
│   └── state_template.json             # 状态文件模板
└── examples/                           # 案例示例
    ├── bounty_hunter_workflow.md       # BH完整流程案例
    └── jester_buff_proposal.md         # 优秀方案示例

_mods/rules/                            # 规则层（游戏数据和机制）
├── du_evaluation.md                    # DU价值体系（合并rules.md）
├── csv_structure.md                    # CSV结构说明（合并hero_file_rules.md）
├── effects_du.yml                      # 效果DU定义（数据文件）
├── hero_index.md                       # 英雄代码索引
└── skills_index.yml                    # 技能元数据

_mods/scripts/                          # 工具层
├── parse_universal.py                  # 通用解析器
├── apply_universal.py                  # 通用应用器
├── state_manager.py                    # 状态管理工具
└── po_manager.py                       # 本地化管理工具
```

### 职责划分（MECE）

| 层级 | 职责 | 示例内容 |
|------|------|----------|
| **流程层** (技能) | 如何执行平衡性优化 | 状态机、步骤、验证、确认 |
| **规则层** (_mods/rules) | 游戏机制和计算标准 | DU价值、CSV结构、效果定义 |
| **工具层** (_mods/scripts) | 具体实现脚本 | Python工具、数据解析 |

### 引用关系

```
SKILL.md
  ├── 引用 → core/statemachine.md（状态机详解）
  ├── 引用 → guides/quickstart.md（快速开始）
  └── 外部引用 → _mods/rules/du_evaluation.md（DU规则）
      ├── 外部引用 → _mods/rules/csv_structure.md（CSV结构）
      └── 外部引用 → _mods/rules/effects_du.yml（效果DU）
```

**原则**: 流程层引用规则层，不重复规则内容

---

## 具体操作

### 阶段1: 清理重复文件

#### 删除技能references中的重复文件
```bash
# 这些文件与_mods/rules/重复
rm .claude/skills/hero-balancer/references/rules.md
rm .claude/skills/hero-balancer/references/hero_file_rules.md

# available_effects.md需要检查是否重复
diff .claude/skills/hero-balancer/references/available_effects.md \
     _mods/rules/available_effects.md
```

### 阶段2: 重构SKILL.md

#### 当前SKILL.md结构（682行）
```markdown
1. 核心目标 (10行)
2. 状态机设计 (80行)
3. 状态上下文存储 (50行)
4. 执行流程详解 (400行) ← 太长，需要拆分
5. 恢复未完成流程 (40行)
6. 代理路由 (10行)
7. 英雄代码索引 (20行)
8. 文件路径规则 (20行)
9. 安全机制总结 (30行)
10. 参考文档索引 (10行)
11. 版本历史 (10行)
```

#### 新SKILL.md结构（目标250行）
```markdown
# 英雄平衡性优化技能（状态机v2.0）

## 快速开始 (30行)
5分钟完成第一个英雄优化

## 状态机概要 (40行)
- 状态图
- 转换表
- 关键状态

## 执行流程 (80行)
- 每个状态1-2句话说明
- 详细内容链接到 core/*.md

## 安全机制 (30行)
三重确认机制概要

## 快速参考 (50行)
- 英雄代码表
- 文件路径规则
- 常用命令

## 文档索引 (20行)
链接到详细文档
```

**拆分策略**:
- `执行流程详解` (400行) → 拆分为 `core/statemachine.md`
- 调研铁律、效果字段等 → `core/data_collection.md`
- 方案制定细节 → `core/proposal_creation.md`
- 安全检查详情 → `core/safety_mechanisms.md`

### 阶段3: 创建新的核心文档

#### core/statemachine.md（200行）
```markdown
# 状态机完整说明

## 状态定义
## 状态转换表
## 状态持久化
## 每个状态的详细说明
## 错误处理
```

#### core/data_collection.md（150行）
```markdown
# 数据收集流程

## COLLECTING状态
## ANALYZING状态
## SUPPLEMENTING_EFFECTS状态
## 调研铁律详解
## 效果字段优先级
## 覆盖率检查
```

#### core/proposal_creation.md（100行）
```markdown
# 方案制定流程

## PROPOSING状态
## 方案结构
## DU计算规则
## 技能改进建议
```

#### core/safety_mechanisms.md（80行）
```markdown
# 安全机制详解

## 三重确认
## 备份策略
## 验证清单
## 回滚机制
```

### 阶段4: 优化规则层文件

#### 合并重复规则文件
```bash
# _mods/rules/

当前:
├── rules.md          # DU评估 + 英雄代码
└── hero_file_rules.md # CSV结构

优化后:
├── du_evaluation.md       # DU价值体系 + 评估标准（合并rules.md内容）
├── csv_structure.md       # CSV结构说明（保持hero_file_rules.md）
├── effects_du.yml         # 效果DU定义（数据文件，保持）
├── hero_index.md          # 英雄代码索引（从rules.md提取）
└── skills_index.yml       # 技能元数据（保持，需要补全）
```

---

## 预期效果

### 信息密度提升

| 文件 | 原行数 | 新行数 | 熵值提升 |
|------|--------|--------|----------|
| SKILL.md | 682 | 250 | 4→7 bits |
| rules.md | 150 | (合并) | - |
| hero_file_rules.md | 200 | (保持) | - |

### MECE合规度

| 维度 | 当前 | 目标 |
|------|------|------|
| 职责独立 | ❌ 流程和规则混在一起 | ✅ 流程/规则/工具分离 |
| 完全穷尽 | ⚠️ 部分内容缺失 | ✅ 核心+guides覆盖全场景 |
| 单一来源 | ❌ 规则重复2次 | ✅ 规则只在_mods/rules |

### 维护成本

| 指标 | 当前 | 目标 | 改进 |
|------|------|------|------|
| 规则更新位置 | 2处 | 1处 | -50% |
| 文档总行数 | ~1200 | ~1000 | -17% |
| 平均文件长度 | 400行 | 150行 | -63% |

---

## 实施计划

### 立即执行（高优先级）
1. ✅ 分析文件重复度
2. ✅ 设计新结构
3. ⏳ 删除重复文件
4. ⏳ 重构SKILL.md

### 后续优化（中优先级）
5. 创建core/目录和文档
6. 创建guides/目录
7. 优化_mods/rules/结构

### 长期维护（低优先级）
8. 补全skills_index.yml
9. 添加更多案例
10. 建立文档审查机制

---

## 风险评估

### 低风险
- 删除重复文件：内容在_mods/rules/有备份
- 重构SKILL.md：内容保留，只是重新组织

### 中风险
- 外部引用链接可能失效
- 需要更新所有引用旧路径的文档

### 缓解措施
- 使用相对路径
- 建立重定向映射
- 分阶段迁移，保留旧文件作为过渡

---

## 结论

**状态**: 🔍 设计完成，待执行

当前文件结构存在严重重复和信息密度低的问题。

**重构目标**:
- 消除所有重复文件
- SKILL.md精简到250行（熵值7+ bits）
- 建立清晰的流程/规则/工具三层结构
- 符合MECE原则

**优先级**: 高（影响文档维护和可读性）

**下一步**: 开始执行阶段1-3，验证效果后再进行阶段4
