---
name: 英雄平衡性优化
description: "暗黑地牢2英雄技能平衡性优化全流程。协调调研代理收集数据，分析制定增强方案，协调实施代理修改CSV并提交Git。"
allowed-tools: [Task, Read, Write, Edit, Bash]
---

# 英雄平衡性优化技能

## 使用场景

当需要优化暗黑地牢2英雄技能平衡性时，使用此技能完成标准化流程。

## 工作流程

```
阶段1: 数据收集 → game-mechanics-researcher
阶段2: 方案制定 → 生成方案文档
阶段3: 实施修改 → csv-balance-implementer
阶段4: 验证提交 → Git提交
```

## 标准流程

### 阶段1：数据收集

调用 `game-mechanics-researcher` 代理：

```
英雄代码: {代码}
任务: 收集技能数据、效果标记、DU价值、机制关系
```

**输出**：技能数据表格、DU计算、机制说明

### 阶段2：方案制定

基于调研数据生成方案：

```
模板: assets/hero_buff_proposal_template.md
输出: ../../_mods/{代码}_buff_proposal.md
```

**参考案例**：
- `references/jester_buff_proposal.md`
- `references/runaway_buff_proposal.md`

**DU评估**：
- 优秀 (>15 DU): 不修改
- 可接受 (10-15 DU): 可选
- 弱势 (<10 DU): 必须增强

### 阶段3：实施修改

调用 `csv-balance-implementer` 代理：

```
方案: ../../_mods/{代码}_buff_proposal.md
目标: 修改 ../../hero_{代码}_data_export.Group.csv
```

### 阶段4：验证提交

```
验证CSV格式 → Git提交 → 完成确认
```

## 依赖关系

### 内部文件 (skill目录内)
- `references/hero_file_rules.md` - CSV结构说明
- `references/available_effects.md` - 效果DU价值表
- `references/rules.md` - 工作规则
- `references/jester_buff_proposal.md` - 小丑案例
- `references/runaway_buff_proposal.md` - 逃离者案例
- `assets/hero_buff_proposal_template.md` - 方案模板

### 外部依赖 (工作目录)
- `../../_mods/{代码}_buff_proposal.md` - 输出方案文档
- `../../hero_{代码}_data_export.Group.csv` - 修改目标
- `.claude/agents/game-mechanics-researcher` - 调研代理
- `.claude/agents/csv-balance-implementer` - 实施代理

## 英雄代码

```
基础: flg/gr/hel/hwm/jes/lep/maa/occ/pd/run/ves
DLC: cru/dul/abm
```

## 代理路由

| 阶段 | 代理 | 用途 |
|------|------|------|
| 数据收集 | game-mechanics-researcher | 收集客观数据 |
| 实施修改 | csv-balance-implementer | 修改CSV提交 |
