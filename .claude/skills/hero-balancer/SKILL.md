---
name: 英雄平衡性优化
description: "暗黑地牢2英雄技能平衡性优化全流程。协调调研代理收集数据，分析制定增强方案，协调实施代理修改CSV并提交Git。"
allowed-tools: [Task, Read, Write, Edit, Bash]
---

# 英雄平衡性优化技能

## 核心目标

优化暗黑地牢2英雄技能平衡性，通过标准化流程完成：数据收集 → 方案制定 → 实施修改 → 验证提交

## 工作流程

```
阶段1: 数据收集 → game-mechanics-researcher代理
阶段2: 方案制定 → 生成方案文档 (_mods/{代码}_buff_proposal.md)
阶段3: 实施修改 → csv-balance-implementer代理
阶段4: 验证提交 → Git提交
```

---

## 执行步骤

### 阶段1：数据收集

**调用代理**: `game-mechanics-researcher`

**任务**: 收集英雄技能数据 (伤害/位置/效果/连击/DoT)

**输出**: 技能数据表格、DU计算、机制说明

### 阶段2：方案制定

**模板**: `assets/hero_buff_proposal_template.md`
**输出**: `../../_mods/{代码}_buff_proposal.md`

**参考案例**:
- `references/jester_buff_proposal.md`
- `references/runaway_buff_proposal.md`

**方案结构**:
1. 弱势技能评估 (DU < 10)
2. 机制流派设计 (三路径定位)
3. 技能改进列表 (字段修改)

### 阶段3：实施修改

**调用代理**: `csv-balance-implementer`

**输入**:
- 方案文件: `_mods/{代码}_buff_proposal.md`
- 目标文件: `hero_{代码}_data_export.Group.csv`

### 阶段4：验证提交

**验证清单**:
- [ ] 所有DU < 10的技能已增强
- [ ] CSV格式有效
- [ ] Git diff仅含预期变更
- [ ] 提交信息清晰

---

## 代理路由

| 阶段 | 代理 | 用途 |
|------|------|------|
| 数据收集 | game-mechanics-researcher | 收集客观数据 |
| 实施修改 | csv-balance-implementer | 修改CSV提交 |

---

## 英雄代码索引

### 基础英雄
```
flg - Flagellant | gr - Grave Robber | hel - Hellion
hwm - Highwayman | jes - Jester       | lep - Leper
maa - Man-at-Arms | occ - Occultist   | pd - Plague Doctor
run - Runaway     | ves - Vestal
```

### DLC英雄
```
DLC1: cru - Crusader | dul - Duelist
DLC2: abm - Alchemist
```

---

## 文件路径规则

| 类型 | 路径格式 |
|------|----------|
| 基础英雄 | `hero_{代码}_data_export.Group.csv` |
| DLC1英雄 | `dlc_dul_cru/hero_{代码}_data_export.Group.csv` |
| DLC2英雄 | `dlc_catacombs/hero_{代码}_data_export.Group.csv` |

---

## 技能命名规则

| 类型 | 格式 | 示例 |
|-----|------|------|
| 基础 | `{代码}_{名称}` | `run_ransack` |
| 升级 | `{代码}_{名称}_u` | `run_ransack_u` |
| 路径 | `{代码}_{名称}_p{1/2/3}` | `run_ransack_p2` |
| 路径升级 | `{代码}_{名称}_p{数字}_u` | `run_ransack_p2_u` |

---

## 参考文档索引

### 游戏规则与数据 (references/)
- `rules.md` - DU评估标准、铁律、文件路径
- `hero_file_rules.md` - CSV结构说明
- `available_effects.md` - 效果DU价值完整表

### 方案案例 (references/)
- `jester_buff_proposal.md` - 小丑增强方案
- `runaway_buff_proposal.md` - 逃离者增强方案

### 模板 (assets/)
- `hero_buff_proposal_template.md` - 方案文档模板
