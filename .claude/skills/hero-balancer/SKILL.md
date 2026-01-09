---
name: 英雄平衡性优化（状态机版）
description: "暗黑地牢2英雄技能平衡性优化全流程。状态机模式：数据收集→方案制定→用户确认→实施修改→验证提交。支持中断恢复和人工审核。"
allowed-tools: [Task, Read, Write, Edit, Bash]
---

# 英雄平衡性优化技能（状态机v2.0）

## 核心目标

优化暗黑地牢2英雄技能平衡性，通过**状态机模式**完成：数据收集 → 方案制定 → **用户确认** → 实施修改 → 验证提交

**关键特性**:
- ✅ **状态持久化**: 支持中断后恢复
- ✅ **用户确认**: 方案实施前必须获得用户明确同意
- ✅ **上下文保存**: 每个状态保存完整工作上下文
- ✅ **安全机制**: 禁止绕过确认直接修改游戏文件

---

## 状态机设计

### 状态定义

```
┌─────────────────────────────────────────────────────────────┐
│                    英雄平衡性优化状态机                      │
└─────────────────────────────────────────────────────────────┘

  IDLE
   │
   ├─→ [用户输入: hero_code]
   ↓
  COLLECTING ──────┐
   │                │
   │ 调用            │ 调用
   │ game-mechanics- │ parse_universal.py
   │ researcher     │
   ↓                │
  ANALYZING ←───────┘
   │
   ├─→ [效果覆盖率 < 90%]
   │   ↓
   │  SUPPLEMENTING_EFFECTS (补充缺失效果)
   │   │
   │   └─→ [重新运行 parse_universal.py]
   │       ↓
   │     ANALYZING
   │
   ├─→ [覆盖率 ≥ 90%]
   ↓
  PROPOSING
   │  生成增强方案
   ↓
  AWAITING_CONFIRMATION ⏸️  [关键节点：必须等待用户确认]
   │
   ├─→ [用户: 取消/拒绝]
   │   ↓
   │  CANCELLED
   │   │ (保留方案文档，不修改游戏文件)
   │   ↓
   │  IDLE
   │
   └─→ [用户: 确认/同意]
       ↓
     IMPLEMENTING
      │ 调用 csv-balance-implementer
      ↓
     VERIFYING
      │ 验证修改结果
      ↓
     COMMITTING
      │ Git提交
      ↓
     DONE
       ↓
      IDLE
```

### 状态转换表

| 当前状态 | 触发条件 | 目标状态 | 动作 |
|---------|---------|---------|------|
| IDLE | 用户输入英雄代码 | COLLECTING | 初始化上下文，创建状态文件 |
| COLLECTING | 数据收集完成 | ANALYZING | 保存技能数据到上下文 |
| ANALYZING | 覆盖率 < 90% | SUPPLEMENTING_EFFECTS | 记录缺失效果到 MISSING_EFFECTS_TODO.md |
| SUPPLEMENTING_EFFECTS | 效果补充完成 | ANALYZING | 重新运行 parse_universal.py |
| ANALYZING | 覆盖率 ≥ 90% | PROPOSING | 生成增强方案文档 |
| PROPOSING | 方案生成完成 | AWAITING_CONFIRMATION | **暂停，显示方案摘要，等待用户确认** |
| AWAITING_CONFIRMATION | 用户确认 | IMPLEMENTING | 调用实施代理修改CSV |
| AWAITING_CONFIRMATION | 用户取消 | CANCELLED | 保留方案，结束流程 |
| IMPLEMENTING | 修改完成 | VERIFYING | 验证CSV格式和diff |
| VERIFYING | 验证通过 | COMMITTING | Git提交 |
| VERIFYING | 验证失败 | IDLE | 回滚修改，记录错误 |
| COMMITTING | 提交成功 | DONE | 清理状态文件 |
| DONE | 流程结束 | IDLE | 归档状态到历史记录 |

---

## 状态上下文存储

### 状态文件位置

```
_mods/state/
  ├── {hero_code}_balance_state.json  # 当前状态（运行时）
  └── history/
      └── {hero_code}_20260109_150430.json  # 历史记录（归档）
```

### 状态文件结构

```json
{
  "state_id": "bh_20260109_150430",
  "hero_code": "bh",
  "hero_name": "Bounty Hunter",
  "current_state": "AWAITING_CONFIRMATION",
  "start_time": "2026-01-09T15:04:30",
  "last_update": "2026-01-09T15:32:18",

  "context": {
    "skills_data": {
      "total_skills": 11,
      "weak_skills": ["bh_caltrops", "bh_hurlbat", "bh_staredown"],
      "effects_coverage": 73.5,
      "missing_effects": 9
    },
    "proposal_file": "_mods/bounty_hunter_buff_proposal.md",
    "target_csv": "expedition/hero_bh_data_export.Group.csv",
    "backup_path": "_mods/backups/hero_bh_data_export.Group.csv.bak"
  },

  "transitions": [
    {"from": "IDLE", "to": "COLLECTING", "timestamp": "2026-01-09T15:04:31"},
    {"from": "COLLECTING", "to": "ANALYZING", "timestamp": "2026-01-09T15:10:15"},
    {"from": "ANALYZING", "to": "PROPOSING", "timestamp": "2026-01-09T15:25:42"},
    {"from": "PROPOSING", "to": "AWAITING_CONFIRMATION", "timestamp": "2026-01-09T15:32:18"}
  ],

  "checkpoints": {
    "collecting_done": true,
    "analyzing_done": true,
    "proposing_done": true,
    "user_confirmed": false
  }
}
```

---

## 执行流程详解

### 状态1: IDLE（初始状态）

**入口**: 技能启动或流程完成
**职责**: 等待用户指定英雄

**检查项**:
- 是否存在未完成的流程？ → 恢复到之前状态
- 用户是否提供英雄代码？ → 进入 COLLECTING

**输出示例**:
```
📋 英雄平衡性优化技能已就绪

可用英雄:
  基础: flg, gr, hel, hwm, jes, lep, maa, occ, pd, run, ves
  DLC1: bh, cru, dul
  DLC2: abm

未完成流程:
  ✅ 无

请指定要优化的英雄代码: _
```

---

### 状态2: COLLECTING（数据收集中）

**入口**: 从 IDLE 接收英雄代码
**职责**: 收集英雄技能数据

**操作**:
1. 调用 `game-mechanics-researcher` 代理收集技能数据
2. 运行 `parse_universal.py <hero_code>` 生成技能评估
3. 检查效果覆盖率

**禁止事项**:
- ❌ 创建新的Python脚本
- ❌ 编写特定英雄代码
- ❌ 手动解析CSV

**允许工具**:
- ✅ Task(game-mechanics-researcher)
- ✅ Bash(parse_universal.py)
- ✅ Read(读取effects_du.yml)

**状态持久化**:
```json
{
  "current_state": "COLLECTING",
  "context": {
    "hero_code": "bh",
    "parse_output_file": "_mods/logs/bh_parse_20260109.txt"
  }
}
```

---

### 状态3: ANALYZING（分析数据中）

**入口**: COLLECTING 完成
**职责**: 分析技能数据，识别问题

**分析项**:
1. **效果覆盖率检查**:
   ```
   覆盖率 = 已定义效果数 / 唯一效果总数

   如果 覆盖率 < 90%:
     → 进入 SUPPLEMENTING_EFFECTS
     → 记录缺失效果到 MISSING_EFFECTS_TODO.md
     → 提示用户补充 effects_du.yml

   如果 覆盖率 ≥ 90%:
     → 继续 DU 分析
   ```

2. **弱势技能识别**:
   ```
   DU < 9:  ❌ 弱势
   DU 9-13: ⚠️ 可接受
   DU ≥ 14:  ✅ 优秀
   ```

3. **机制分析**:
   - 路径设计（三路径定位）
   - 连击协作
   - DoT机制

**⚠️ 调研铁律**:
- DU < 5 的技能必然存在**效果疏漏**或**解读错误**
- 必须检查所有效果字段（按优先级）:
  1. `target_effects` - 目标效果
  2. `performer_effects` - 施放者效果
  3. `performer_after_target_effects` - **施放者后续效果** ⚠️ 易遗漏
  4. `performer_team_others_effects` - 队友效果
  5. `target_buffs` - 目标buff
  6. `performer_buffs` - 施放buff

---

### 状态4: SUPPLEMENTING_EFFECTS（补充缺失效果）

**入口**: ANALYZING 发现覆盖率 < 90%
**职责**: 补充 effects_du.yml

**流程**:
1. 运行 `parse_universal.py <hero_code>` 获取缺失效果清单
2. 将缺失效果添加到 `_mods/rules/effects_du.yml`
3. 为每个效果定义 DU 价值
4. 重新运行 `parse_universal.py <hero_code>` 验证

**示例**:
```yaml
# _mods/rules/effects_du.yml

bh_caltrops_move_res_down_e:
  name: 移动抗性降低
  desc: 目标移动抗性-15%
  file: expedition/hero_bh_data_export.Group.csv
  line: 1234
  du: 2.0
```

**验证**:
```bash
cd _mods/scripts && python parse_universal.py bh
# 输出: 覆盖率 100% ✅
```

---

### 状态5: PROPOSING（方案制定中）

**入口**: ANALYZING 确认覆盖率 ≥ 90%
**职责**: 生成增强方案文档

**方案结构**:
```markdown
# {英雄名称} 增强方案

## 1. 弱势技能评估

### 技能名称 (skill_id)
- 当前DU: X.X
- 问题分析: ...
- 改进建议: ...

## 2. 机制流派设计

### 路径1: XXX
- 定位: ...
- 核心技能: ...

### 路径2: YYY
...

## 3. 技能改进列表

| 技能ID | 字段 | 原值 | 新值 | 理由 |
|--------|------|------|------|------|
| bh_caltrops | m_DamageMin | 2 | 3 | 提升基础伤害 |
```

**模板文件**: `.claude/skills/hero-balancer/assets/hero_buff_proposal_template.md`

**输出位置**: `_mods/{代码}_buff_proposal.md`

---

### 状态6: AWAITING_CONFIRMATION ⏸️（等待用户确认）

**入口**: PROPOSING 完成
**职责**: **暂停流程，显示方案摘要，等待用户明确确认**

**⚠️ 关键安全机制**:
- **禁止跳过此状态**
- **禁止自动确认**
- **禁止绕过用户直接实施修改**

**用户界面**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 增强方案已生成，请审阅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

英雄: Bounty Hunter (bh)
方案文件: _mods/bounty_hunter_buff_proposal.md

┌─ 弱势技能 (3个) ───────────────────────────────────┐
│ ✗ bh_caltrops    DU: 7.0   (铁蒺藜)               │
│ ✗ bh_hurlbat     DU: 8.0   (投掷矛)               │
│ ✗ bh_staredown   DU: 5.5   (对峙)                 │
└───────────────────────────────────────────────────┘

┌─ 预期改进 ────────────────────────────────────────┐
│ • bh_caltrops: 伤害 2-3 → 3-5 (+40%)             │
│ • bh_hurlbat:  添加眩晕效果 (DU+3)               │
│ • bh_staredown: 伤害 0-0 → 2-4 (基础伤害)        │
└───────────────────────────────────────────────────┘

📄 完整方案: _mods/bounty_hunter_buff_proposal.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  即将修改游戏文件，此操作不可撤销

请选择操作:
  [1] 确认实施 - 修改 hero_bh_data_export.Group.csv
  [2] 查看详情 - 显示完整方案文档
  [3] 取消流程 - 保留方案，不修改游戏文件

请输入选项 (1/2/3): _
```

**用户响应处理**:

| 输入 | 动作 | 目标状态 |
|------|------|---------|
| "1", "确认", "confirm" | 开始实施修改 | IMPLEMENTING |
| "2", "查看", "view" | 显示完整方案文档 | AWAITING_CONFIRMATION |
| "3", "取消", "cancel" | 保留方案，结束流程 | CANCELLED |

**安全检查**:
- ✅ 目标CSV文件存在
- ✅ 备份路径已创建
- ✅ 方案文档格式有效
- ✅ Git工作区干净（无未提交更改）

**状态持久化**:
```json
{
  "current_state": "AWAITING_CONFIRMATION",
  "context": {
    "proposal_summary": {
      "weak_skills_count": 3,
      "modifications_count": 5,
      "estimated_du_increase": "+8.5"
    }
  },
  "safety_checks": {
    "csv_exists": true,
    "backup_created": true,
    "git_clean": true
  }
}
```

---

### 状态7: IMPLEMENTING（实施修改中）

**入口**: 用户确认方案
**职责**: 修改游戏CSV文件

**操作**:
1. **创建备份**:
   ```bash
   cp expedition/hero_bh_data_export.Group.csv \
      _mods/backups/hero_bh_data_export.Group.csv.bak
   ```

2. **调用实施代理**: `csv-balance-implementer`
   - 输入: 方案文件 `_mods/bounty_hunter_buff_proposal.md`
   - 目标: `expedition/hero_bh_data_export.Group.csv`
   - 操作: 修改CSV字段值

3. **验证格式**:
   ```bash
   # 检查CSV格式
   python -c "import csv; csv.reader(open('expedition/hero_bh_data_export.Group.csv'))"
   ```

**禁止事项**:
- ❌ 手动编辑CSV
- ❌ 使用文本处理器批量替换
- ❌ 跳过备份步骤

**允许工具**:
- ✅ Task(csv-balance-implementer)
- ✅ Bash(cp, git)
- ✅ Read/Write(仅验证，不修改)

---

### 状态8: VERIFYING（验证修改中）

**入口**: IMPLEMENTING 完成
**职责**: 验证修改结果

**验证清单**:
```bash
# 1. CSV格式验证
cd _mods/scripts && python parse_universal.py bh
# 预期: 无错误，DU值已提升

# 2. Git差异检查
git diff expedition/hero_bh_data_export.Group.csv
# 预期: 仅包含预期修改的字段

# 3. 数量验证
echo "预期修改5个技能"
git diff --stat | grep "hero_bh_data_export.Group.csv"
```

**失败处理**:
```
如果验证失败:
  1. 停止流程
  2. 从备份恢复CSV
  3. 记录错误到 _mods/errors/{hero_code}_error.log
  4. 状态 → IDLE
```

---

### 状态9: COMMITTING（提交中）

**入口**: VERIFYING 通过
**职责**: Git提交

**提交信息格式**:
```
📊 balance(bh): enhance weak skills

Boost Bounty Hunter skills with low DU:
- bh_caltrops: damage 2-3 → 3-5 (+40%)
- bh_hurlbat: add stun effect (DU+3)
- bh_staredown: add base damage 2-4

Total DU increase: +8.5
Effects coverage: 73.5% → 100%

Refs: _mods/bounty_hunter_buff_proposal.md
```

**操作**:
```bash
git add expedition/hero_bh_data_export.Group.csv
git add _mods/bounty_hunter_buff_proposal.md
git commit -m "balance(bh): enhance weak skills"
```

---

### 状态10: DONE（完成）

**入口**: COMMITTING 成功
**职责**: 清理和归档

**操作**:
1. **归档状态文件**:
   ```bash
   mv _mods/state/bh_balance_state.json \
      _mods/state/history/bh_20260109_150430.json
   ```

2. **生成总结报告**:
   ```
   ✅ Bounty Hunter 平衡性优化完成

   修改技能: 3个
   总DU提升: +8.5
   提交哈希: a1b2c3d4

   方案文档: _mods/bounty_hunter_buff_proposal.md
   状态归档: _mods/state/history/bh_20260109_150430.json
   ```

3. **清理临时文件**:
   - 删除备份（可选）
   - 清理日志

---

## 恢复未完成流程

### 检测未完成流程

启动技能时检查 `_mods/state/` 目录：

```bash
# 查找未完成的状态文件
ls _mods/state/*_balance_state.json 2>/dev/null

# 输出示例:
# bh_balance_state.json
```

### 恢复流程

```
🔔 发现未完成流程

英雄: Bounty Hunter (bh)
当前状态: AWAITING_CONFIRMATION
开始时间: 2026-01-09 15:04
已耗时: 28分钟

方案文件: _mods/bounty_hunter_buff_proposal.md

选择操作:
  [1] 继续流程 - 从 AWAITING_CONFIRMATION 继续
  [2] 放弃流程 - 删除状态文件，重新开始
  [3] 查看详情 - 显示完整上下文

请输入选项 (1/2/3): _
```

---

## 代理路由

| 状态 | 代理 | 用途 |
|------|------|------|
| COLLECTING | game-mechanics-researcher | 收集客观数据 |
| IMPLEMENTING | csv-balance-implementer | 修改CSV提交 |

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
DLC1: bh - Bounty Hunter | cru - Crusader | dul - Duelist
DLC2: abm - Alchemist
```

---

## 文件路径规则

| 类型 | 路径格式 |
|------|----------|
| 基础英雄 | `hero_{代码}_data_export.Group.csv` |
| DLC1单独英雄 | `expedition/hero_{代码}_data_export.Group.csv` |
| DLC1双英雄 | `dlc_dul_cru/hero_{代码}_data_export.Group.csv` |
| DLC2英雄 | `dlc_catacombs/hero_{代码}_data_export.Group.csv` |

---

## 安全机制总结

### 三重确认机制

1. **效果覆盖度确认**:
   ```
   ANALYZING → 检查覆盖率
   如果 < 90% → 补充效果 → 重新验证
   如果 ≥ 90% → 继续
   ```

2. **用户方案确认**:
   ```
   PROPOSING → AWAITING_CONFIRMATION
   显示方案摘要 → 等待用户输入
   用户确认 → IMPLEMENTING
   用户取消 → CANCELLED
   ```

3. **修改结果验证**:
   ```
   IMPLEMENTING → VERIFYING
   CSV格式检查 → Git diff检查
   验证通过 → COMMITTING
   验证失败 → 回滚 → IDLE
   ```

### 禁止事项清单

❌ **绝对禁止**:
- 跳过 AWAITING_CONFIRMATION 状态
- 自动确认方案
- 绕过用户直接修改游戏文件
- 创建特定英雄的Python脚本
- 手动编辑CSV文件
- 跳过备份步骤

✅ **必须执行**:
- 每个状态持久化上下文
- 修改前创建备份
- 验证所有更改
- 获得用户明确确认

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

### 流程问题记录 (_mods/issues/)
- `2026-01-09_hero_specific_scripts_workflow_violation.md` - 特定脚本违规案例
- `2026-01-09_localization_temp_file_error.md` - 本地化文件错误案例
- `2026-01-08_effects_coverage_workflow.md` - 效果覆盖度流程问题

---

## 版本历史

### v2.0 (2026-01-09) - 状态机模式
- ✅ 新增状态机设计
- ✅ 新增用户确认机制
- ✅ 新增状态持久化
- ✅ 新增流程恢复功能
- ✅ 新增三重安全确认

### v1.0 (2026-01-08) - 初始版本
- 基础四阶段流程
- 代理协调机制
- 效果覆盖度检查
