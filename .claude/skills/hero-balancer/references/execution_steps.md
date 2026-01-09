# 执行流程详解

本文档详细说明状态机各阶段的执行步骤和注意事项。

---

## 1. COLLECTING - 数据收集

### 操作步骤
```bash
cd _mods/scripts && python parse_universal.py <hero_code>
```

### 输出内容
- 技能评估表（伤害/范围/DU/状态）
- 效果覆盖度统计
- 弱势技能列表

### ⚠️ 调研铁律
- **DU < 5 必然存在效果疏漏**
- 必须检查6个效果字段（优先级排序）:
  1. target_effects
  2. performer_effects
  3. performer_after_target_effects ⚠️
  4. performer_team_others_effects
  5. target_buffs
  6. performer_buffs

### 禁止事项
- ❌ 创建新Python脚本
- ❌ 编写特定英雄代码
- ❌ 手动解析CSV

---

## 2. ANALYZING - 数据分析

### 效果覆盖率检查
```
覆盖率 = 已定义效果数 / 唯一效果总数

if 覆盖率 < 90%:
    进入 SUPPLEMENTING_EFFECTS
    补充 _mods/effects/{英雄代码}_effects.md
    重新运行 parse_universal.py

if 覆盖率 ≥ 90%:
    继续 DU 分析
```

### 弱势技能识别
```
DU < 9:  ❌ 弱势（必须增强）
DU 9-13: ⚠️ 可接受
DU ≥ 14:  ✅ 优秀
```

---

## 3. PROPOSING - 方案制定

### 方案结构
```markdown
# {英雄名称} 增强方案

## 1. 弱势技能评估
## 2. 机制流派设计（三路径）
## 3. 技能改进列表（字段修改）
```

### 资源文件
- **模板**: `assets/hero_buff_proposal_template.md`
- **案例**: `examples/runaway_buff_proposal.md`
- **输出位置**: `_mods/{代码}_buff_proposal.md`

---

## 4. AWAITING_CONFIRMATION - 等待用户确认

### 关键安全机制
- ⚠️ **禁止跳过此状态**
- ⚠️ **禁止自动确认**
- ⚠️ **禁止绕过用户直接修改**

### 用户界面
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

### 安全检查
- ✅ 目标CSV存在
- ✅ 备份路径已创建
- ✅ Git工作区干净

---

## 5. IMPLEMENTING - 实施修改

### 操作步骤
1. 创建备份
2. 调用csv-balance-implementer代理
3. 验证CSV格式

### 禁止事项
- ❌ 手动编辑CSV
- ❌ 跳过备份

---

## 6. VERIFYING - 验证修改

### 验证清单
```bash
# 1. 格式验证
cd _mods/scripts && python parse_universal.py <hero_code>

# 2. 差异检查
git diff hero_*_data_export.Group.csv

# 3. 数量验证
git diff --stat | grep "hero_*"
```

### 失败处理
从备份恢复 → 记录错误 → 回到IDLE

---

## 7. COMMITTING - Git提交

### 提交信息格式
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

**相关文档**:
- [SKILL.md](../SKILL.md) - 核心流程
- [data_collection.md](data_collection.md) - 数据收集详解
- [proposal_creation.md](proposal_creation.md) - 方案制定详解
- [safety_mechanisms.md](safety_mechanisms.md) - 安全机制详解
