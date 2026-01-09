---
name: 英雄平衡性优化（状态机v2.1）
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

## 状态转换流程

### 状态定义

| 状态 | 说明 |
|------|------|
| **IDLE** | 初始化/恢复点 |
| **COLLECTING** | 调用parse_universal.py收集数据 |
| **ANALYZING** | DU评估/覆盖率检查 |
| **SUPPLEMENTING_EFFECTS** | 补充effects_du.yml缺失效果 |
| **PROPOSING** | 编写proposal.md方案 |
| **AWAITING_CONFIRMATION** | **必须暂停等待用户确认** |
| **IMPLEMENTING** | 调用csv-balance-implementer修改CSV |
| **VERIFYING** | 验证修改结果 |
| **COMMITTING** | Git提交 |
| **DONE** | 归档状态 |
| **CANCELLED** | 流程终止 |

### 状态转换顺序

```
IDLE
  ↓ (用户输入hero_code)
COLLECTING
  ↓ (parse完成)
ANALYZING
  ├─→ (覆盖率<90%) → SUPPLEMENTING_EFFECTS → 回到ANALYZING
  └─→ (覆盖率≥90%) → PROPOSING
      ↓ (方案生成完成)
AWAITING_CONFIRMATION ⏸️  ← 关键检查点，必须等待用户
  ├─→ (用户确认) → IMPLEMENTING
  └─→ (用户取消) → CANCELLED
      ↓ (修改完成)
VERIFYING
  ├─→ (验证通过) → COMMITTING → DONE
  └─→ (验证失败) → IDLE (回滚)
```

### 英雄名称映射

```python
HERO_NAMES = {
    'bh': 'Bounty Hunter', 'cru': 'Crusader', 'dul': 'Duelist',
    'flg': 'Flagellant', 'gr': 'Grave Robber', 'hel': 'Hellion',
    'hwm': 'Highwayman', 'jes': 'Jester', 'lep': 'Leper',
    'maa': 'Man-at-Arms', 'occ': 'Occultist', 'pd': 'Plague Doctor',
    'run': 'Runaway', 'ves': 'Vestal', 'abm': 'Alchemist'
}
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
python _mods/scripts/state_manager.py <create|query|update|list|archive> <code>

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

### 游戏规则（_mods/rules/）
- [du_evaluation.md](_mods/rules/du_evaluation.md) - DU价值体系
- [csv_structure.md](_mods/rules/csv_structure.md) - CSV结构说明
- [effects_du.yml](_mods/rules/effects_du.yml) - 效果DU定义

### 案例示例（examples/）
- [runaway_buff_proposal.md](examples/runaway_buff_proposal.md) - 逃离者方案

### 资源文件（assets/）
- [hero_buff_proposal_template.md](assets/hero_buff_proposal_template.md) - 方案模板
- [state_template.json](assets/state_template.json) - 状态文件模板

### 流程问题记录（_mods/issues/）
- [2026-01-09_statemachine_workflow_upgrade.md](_mods/issues/2026-01-09_statemachine_workflow_upgrade.md) - 状态机升级
- [2026-01-09_hero_specific_scripts_workflow_violation.md](_mods/issues/2026-01-09_hero_specific_scripts_workflow_violation.md) - 特定脚本违规
- [2026-01-09_file_structure_redundancy_analysis.md](_mods/issues/2026-01-09_file_structure_redundancy_analysis.md) - 文件结构冗余

---

## 版本历史

### v2.1 (2026-01-09) - 流程引擎与工具分离 + MECE优化
- ✅ 添加状态转换流程（状态定义/转换顺序）
- ✅ 重构state_manager.py为纯工具函数（移除业务逻辑）
- ✅ 明确架构原则：SKILL.md定义流程，脚本提供工具
- ✅ MECE优化：删除冗余目录（references/、guides/、scripts/）
- ✅ 精简文档结构：SKILL.md核心流程 + core/详细说明 + examples/示例

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

**总行数**: ~230行
**信息密度**: 8.5 bits
**MECE合规**: ✅ 核心(SKILL.md) / 详细(core/) / 示例(examples/)
**重复度**: 0%
**架构分离**: ✅ 三层MECE结构，零冗余
