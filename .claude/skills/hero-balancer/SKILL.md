---
name: 英雄平衡性优化（状态机v2.0）
description: "暗黑地牢2英雄技能平衡性优化。状态机：数据收集→方案制定→用户确认→实施修改→验证提交。支持中断恢复和人工审核。"
allowed-tools: [Task, Read, Write, Edit, Bash]
---

# 英雄平衡性优化技能

## 核心目标

优化暗黑地牢2英雄技能平衡性，通过**状态机模式**完成：数据收集 → 方案制定 → **用户确认** → 实施修改 → 验证提交

**关键特性**:
- ✅ **状态持久化**: 支持中断后恢复
- ✅ **用户确认**: 方案实施前必须获得用户明确同意
- ✅ **上下文保存**: 每个状态保存完整工作上下文
- ✅ **安全机制**: 三重确认（覆盖率/用户/验证）

---

## 快速开始（5分钟）

```bash
# 1. 选择英雄
# 基础: flg/gr/hel/hwm/jes/lep/maa/occ/pd/run/ves
# DLC1: bh/cru/dul
# DLC2: abm

# 2. 数据收集
cd _mods/scripts && python parse_universal.py <hero_code>

# 3. 检查覆盖率（必须≥90%）
# 如果<90%，补充缺失效果到 _mods/rules/effects_du.yml

# 4. 生成方案
# 基于数据手动创建 _mods/<hero_code>_buff_proposal.md

# 5. 用户确认
# 查看方案摘要，确认后实施

# 6. 实施修改
# 调用csv-balance-implementer代理修改CSV

# 7. 验证提交
git add . && git commit -m "balance(<code>): enhance weak skills"
```

---

## 状态机概要

### 状态转换图

```
IDLE → COLLECTING → ANALYZING → PROPOSING →
AWAITING_CONFIRMATION ⏸️ → IMPLEMENTING → VERIFYING →
COMMITTING → DONE
```

### 状态速查表

| 状态 | 职责 | 输出 | 关键点 |
|------|------|------|--------|
| **IDLE** | 初始化 | 状态文件 | 检测未完成流程 |
| **COLLECTING** | 数据收集 | 技能评估表 | 使用parse_universal.py |
| **ANALYZING** | 分析数据 | 弱势技能列表 | 覆盖率≥90%才能继续 |
| **SUPPLEMENTING** | 补充效果 | effects_du.yml | 循环回到ANALYZING |
| **PROPOSING** | 生成方案 | proposal.md | 遵循模板结构 |
| **AWAITING** ⏸️ | 等待确认 | 用户输入 | **必须暂停等待** |
| **IMPLEMENTING** | 实施修改 | CSV备份 | 使用csv-balance-implementer |
| **VERIFYING** | 验证结果 | 验证报告 | 失败则回滚 |
| **COMMITTING** | Git提交 | commit hash | 规范化提交信息 |
| **DONE** | 完成 | 归档状态 | 清理临时文件 |

### 状态转换规则

```markdown
当前状态          → 触发条件              → 目标状态
──────────────────────────────────────────────────
IDLE              → 用户输入hero_code     → COLLECTING
COLLECTING        → parse完成            → ANALYZING
ANALYZING         → 覆盖率<90%           → SUPPLEMENTING
ANALYZING         → 覆盖率≥90%           → PROPOSING
SUPPLEMENTING     → 效果补充完成         → ANALYZING
PROPOSING         → 方案生成完成         → AWAITING_CONFIRMATION
AWAITING_CONFIRM  → 用户确认             → IMPLEMENTING
AWAITING_CONFIRM  → 用户取消             → CANCELLED
IMPLEMENTING      → 修改完成             → VERIFYING
VERIFYING         → 验证通过             → COMMITTING
VERIFYING         → 验证失败             → IDLE (回滚)
COMMITTING        → 提交成功             → DONE
DONE              → 流程结束             → IDLE
```

**详细信息**: [core/statemachine.md](core/statemachine.md)

---

## 执行流程（简版）

### 1. COLLECTING - 数据收集

**操作**:
```bash
cd _mods/scripts && python parse_universal.py <hero_code>
```

**输出**:
- 技能评估表（伤害/范围/DU/状态）
- 效果覆盖度统计
- 弱势技能列表

**⚠️ 调研铁律**:
- DU < 5 必然存在效果疏漏
- 必须检查6个效果字段（优先级排序）:
  1. target_effects
  2. performer_effects
  3. performer_after_target_effects ⚠️
  4. performer_team_others_effects
  5. target_buffs
  6. performer_buffs

**禁止事项**:
- ❌ 创建新Python脚本
- ❌ 编写特定英雄代码
- ❌ 手动解析CSV

**详细信息**: [core/data_collection.md](core/data_collection.md)

---

### 2. ANALYZING - 数据分析

**关键检查**:

#### 效果覆盖率检查
```
覆盖率 = 已定义效果数 / 唯一效果总数

if 覆盖率 < 90%:
    进入 SUPPLEMENTING_EFFECTS
    补充 _mods/rules/effects_du.yml
    重新运行 parse_universal.py

if 覆盖率 ≥ 90%:
    继续 DU 分析
```

#### 弱势技能识别
```
DU < 9:  ❌ 弱势（必须增强）
DU 9-13: ⚠️ 可接受
DU ≥ 14:  ✅ 优秀
```

**详细信息**: [core/data_collection.md](core/data_collection.md)

---

### 3. PROPOSING - 方案制定

**方案结构**:
```markdown
# {英雄名称} 增强方案

## 1. 弱势技能评估
## 2. 机制流派设计（三路径）
## 3. 技能改进列表（字段修改）
```

**模板**: [assets/hero_buff_proposal_template.md](assets/hero_buff_proposal_template.md)
**案例**: [examples/runaway_buff_proposal.md](examples/runaway_buff_proposal.md)
**输出位置**: `_mods/{代码}_buff_proposal.md`

**详细信息**: [core/proposal_creation.md](core/proposal_creation.md)

---

### 4. AWAITING_CONFIRMATION ⏸️ - 等待用户确认

**关键安全机制**:
- ⚠️ **禁止跳过此状态**
- ⚠️ **禁止自动确认**
- ⚠️ **禁止绕过用户直接修改**

**用户界面**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 增强方案已生成，请审阅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

英雄: Bounty Hunter (bh)
方案文件: _mods/bounty_hunter_buff_proposal.md

┌─ 弱势技能 (3个) ─────────────────────┐
│ ✗ bh_caltrops    DU: 7.0            │
│ ✗ bh_hurlbat     DU: 8.0            │
│ ✗ bh_staredown   DU: 5.5            │
└──────────────────────────────────────┘

请选择:
  [1] 确认实施
  [2] 查看详情
  [3] 取消流程
```

**安全检查**:
- ✅ 目标CSV存在
- ✅ 备份路径已创建
- ✅ Git工作区干净

**详细信息**: [core/safety_mechanisms.md](core/safety_mechanisms.md)

---

### 5. IMPLEMENTING - 实施修改

**操作**:
1. 创建备份
2. 调用csv-balance-implementer代理
3. 验证CSV格式

**禁止**:
- ❌ 手动编辑CSV
- ❌ 跳过备份

**详细信息**: [core/safety_mechanisms.md](core/safety_mechanisms.md)

---

### 6. VERIFYING - 验证修改

**验证清单**:
```bash
# 1. 格式验证
cd _mods/scripts && python parse_universal.py <hero_code>

# 2. 差异检查
git diff hero_*_data_export.Group.csv

# 3. 数量验证
git diff --stat | grep "hero_*"
```

**失败处理**: 从备份恢复 → 记录错误 → 回到IDLE

---

### 7. COMMITTING - Git提交

**提交信息格式**:
```
balance(code): enhance weak skills

Boost {Hero} skills with low DU:
- skill1: modification1
- skill2: modification2

Total DU increase: +X.X
Effects coverage: X% → 100%

Refs: _mods/code_buff_proposal.md
```

---

## 安全机制（三重确认）

### 1. 效果覆盖度确认
```
ANALYZING → 检查覆盖率
如果 < 90% → 补充效果 → 重新验证
如果 ≥ 90% → 继续
```

### 2. 用户方案确认
```
PROPOSING → AWAITING_CONFIRMATION
显示方案摘要 → 等待用户输入
用户确认 → IMPLEMENTING
用户取消 → CANCELLED
```

### 3. 修改结果验证
```
IMPLEMENTING → VERIFYING
CSV格式检查 → Git diff检查
验证通过 → COMMITTING
验证失败 → 回滚 → IDLE
```

**详细信息**: [core/safety_mechanisms.md](core/safety_mechanisms.md)

---

## 状态持久化

### 状态文件结构
```json
{
  "state_id": "bh_20260109_150430",
  "hero_code": "bh",
  "current_state": "AWAITING_CONFIRMATION",
  "start_time": "2026-01-09T15:04:30",
  "context": {...},
  "transitions": [...],
  "checkpoints": {...}
}
```

### 状态管理
```bash
# 初始化
python _mods/scripts/state_manager.py init <hero_code>

# 更新状态
python _mods/scripts/state_manager.py update <hero_code> <state>

# 查看状态
python _mods/scripts/state_manager.py get <hero_code>

# 列出未完成
python _mods/scripts/state_manager.py list

# 归档状态
python _mods/scripts/state_manager.py archive <hero_code>
```

**详细信息**: [core/statemachine.md](core/statemachine.md)

---

## 恢复未完成流程

### 检测未完成流程
```bash
# 启动技能时自动检测
ls _mods/state/*_balance_state.json

# 输出未完成流程列表
python _mods/scripts/state_manager.py list
```

### 恢复流程
```
🔔 发现未完成流程

英雄: Bounty Hunter (bh)
当前状态: AWAITING_CONFIRMATION
开始时间: 2026-01-09 15:04

选择操作:
  [1] 继续流程
  [2] 放弃流程
  [3] 查看详情
```

---

## 快速参考

### 英雄代码索引

| 代码 | 英雄 | 类型 |
|------|------|------|
| flg | Flagellant | 基础 |
| gr | Grave Robber | 基础 |
| hel | Hellion | 基础 |
| hwm | Highwayman | 基础 |
| jes | Jester | 基础 |
| lep | Leper | 基础 |
| maa | Man-at-Arms | 基础 |
| occ | Occultist | 基础 |
| pd | Plague Doctor | 基础 |
| run | Runaway | 基础 |
| ves | Vestal | 基础 |
| bh | Bounty Hunter | DLC1单独 |
| cru | Crusader | DLC1 |
| dul | Duelist | DLC1 |
| abm | Alchemist | DLC2 |

### 文件路径规则

| 类型 | 路径格式 |
|------|----------|
| 基础英雄 | `hero_{代码}_data_export.Group.csv` |
| DLC1单独 | `expedition/hero_{代码}_data_export.Group.csv` |
| DLC1双英雄 | `dlc_dul_cru/hero_{代码}_data_export.Group.csv` |
| DLC2英雄 | `dlc_catacombs/hero_{代码}_data_export.Group.csv` |

### 常用命令

```bash
# 数据收集
cd _mods/scripts && python parse_universal.py <code>

# 状态管理
python _mods/scripts/state_manager.py <init|update|get|list> <code>

# Git操作
git diff hero_*_data_export.Group.csv
git add . && git commit -m "balance(code): message"
```

---

## 文档索引

### 核心流程（core/）
- [statemachine.md](core/statemachine.md) - 状态机完整说明
- [data_collection.md](core/data_collection.md) - 数据收集详解
- [proposal_creation.md](core/proposal_creation.md) - 方案制定详解
- [safety_mechanisms.md](core/safety_mechanisms.md) - 安全机制详解

### 使用指南（guides/）
- [quickstart.md](guides/quickstart.md) - 5分钟快速开始
- [troubleshooting.md](guides/troubleshooting.md) - 故障排除
- [best_practices.md](guides/best_practices.md) - 最佳实践

### 游戏规则（_mods/rules/）
- [du_evaluation.md](_mods/rules/du_evaluation.md) - DU价值体系
- [csv_structure.md](_mods/rules/csv_structure.md) - CSV结构说明
- [effects_du.yml](_mods/rules/effects_du.yml) - 效果DU定义

### 案例示例（examples/）
- [runaway_buff_proposal.md](examples/runaway_buff_proposal.md) - 逃离者方案
- [bounty_hunter_workflow.md](examples/bounty_hunter_workflow.md) - BH完整流程

### 资源文件（assets/）
- [hero_buff_proposal_template.md](assets/hero_buff_proposal_template.md) - 方案模板
- [state_template.json](assets/state_template.json) - 状态文件模板

### 流程问题记录（_mods/issues/）
- [2026-01-09_statemachine_workflow_upgrade.md](_mods/issues/2026-01-09_statemachine_workflow_upgrade.md) - 状态机升级
- [2026-01-09_hero_specific_scripts_workflow_violation.md](_mods/issues/2026-01-09_hero_specific_scripts_workflow_violation.md) - 特定脚本违规
- [2026-01-09_file_structure_redundancy_analysis.md](_mods/issues/2026-01-09_file_structure_redundancy_analysis.md) - 文件结构冗余

---

## 版本历史

### v2.0 (2026-01-09) - 状态机模式 + 文件结构优化
- ✅ 状态机设计（10状态）
- ✅ 用户确认机制
- ✅ 状态持久化
- ✅ 三重安全确认
- ✅ 消除文件重复（熵值提升到7bits）
- ✅ MECE原则重构（流程/规则/工具分离）

### v1.0 (2026-01-08) - 初始版本
- 基础四阶段流程
- 代理协调机制
- 效果覆盖度检查

---

## 代理路由

| 状态 | 代理 | 用途 |
|------|------|------|
| COLLECTING | game-mechanics-researcher | 收集客观数据 |
| IMPLEMENTING | csv-balance-implementer | 修改CSV提交 |

---

**总行数**: 273行
**信息密度**: 7 bits
**MECE合规**: ✅ 流程/规则/工具分离
**重复度**: 0%
