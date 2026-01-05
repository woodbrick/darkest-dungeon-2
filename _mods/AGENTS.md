# 英雄技能修改指南

## 概述

本文档说明如何修改暗黑地牢2的英雄技能数据，包括伤害、效果、冷却等属性的调整。

---

## 一、文件结构

### 1.1 英雄数据文件

**路径**: `hero_{英雄代码}_data_export.Group.csv`

**DLC英雄**:
- DLC1: `dlc_dul_cru/hero_{英雄代码}_data_export.Group.csv`
- DLC2: `dlc_catacombs/hero_{英雄代码}_data_export.Group.csv`

### 1.2 CSV格式

```
element_start,{元素ID},{元素类型}
{字段名1},{值1},{值2},...
{字段名2},{值1},{值2},...
element_end
```

---

## 二、元素类型

### 2.1 ActorDataStats - 属性数据

定义英雄的基础属性

**元素ID**: 英雄的内部名称（如 `hellion`, `flagellant`, `abomination`）

**常用字段**:
- `add_stats` - 属性值列表
- `key_map` - 属性键映射（定义add_stats中每个位置的含义）

**示例**:
```csv
element_start,hellion,ActorDataStats
add_stats,33,3,10,0.3,0.3,0.2,0.1,0.4,0.3,0.2,0.6
key_map,health,max_stress,deathblow_resistance,stun,resist_blight,resist_bleed,resist_burn,resist_disease,resist_move,resist_debuff,resist_death
element_end
```

### 2.2 ActorDataSkill - 技能数据

定义技能的基本信息和效果

**元素ID**: `{英雄代码}_{技能名称}`

**常用字段**:

**基础信息**:
- `m_IsFriendly` - 是否友方技能 (True/False)
- `launch_ranks` - 施放位置 (如: 1,2 表示从位置1或2施放)
- `target_ranks` - 目标位置 (如: 1,2,3,4 表示可攻击所有位置)
- `m_IsMultiHit` - 是否群体攻击 (True=群体, False=单体)
- `m_Cooldown` - 冷却回合数
- `m_CanBeRiposted` - 可被反击 (True/False)
- `m_Tags` - 技能标签

**伤害数据**:
- `key_map` - 定义伤害类型
- `add_stats` - 伤害数值
  - 格式: `基础伤害,随机伤害,暴击率`
  - 实际伤害 = 基础伤害 ~ (基础伤害 + 随机伤害)

**效果字段**:
- `performer_effects` - 施放者自身效果
- `target_effects` - 目标效果
- `performer_after_target_effects` - 攻击后施放者效果
- `on_hit_as_performer_to_performer_effects` - 命中时施放者获得效果
- `on_crit_as_performer_to_target_effects` - 暴击时目标效果
- `performer_buffs` - 施放者获得Buff

**示例**:
```csv
element_start,hel_wicked_hack,ActorDataSkill
m_IsFriendly,False
launch_ranks,1,2
target_ranks,1,2
m_IsMultiHit,True
m_Cooldown,0
m_CanBeRiposted,True
key_map,health_damage,health_damage_range,crit_chance
add_stats,5,3,0.05
performer_effects,move_forward_1
target_effects,add_1_vulnerable
element_end
```

---

## 三、伤害计算

### 3.1 伤害公式

**CSV格式**: `add_stats,基础伤害,随机伤害,暴击率`

| add_stats | 实际伤害 | 平均 |
|-----------|---------|------|
| `5,5,0.05` | 5-10 | 7.5 |
| `8,8,0.1` | 8-16 | 12 |
| `3,2,0.05` | 3-5 | 4 |

### 3.2 修改伤害

**原伤害**: `add_stats,5,3,0.05` = 5-8伤害

**提升伤害**: `add_stats,6,4,0.05` = 6-10伤害

**操作步骤**:
1. 找到技能的 `element_start` 行
2. 定位 `add_stats` 字段
3. 修改数值（第一位是基础伤害，第二位是随机伤害）

---

## 四、效果修改

### 4.1 效果字段位置

| 字段 | 作用 | 示例 |
|------|------|------|
| `performer_effects` | 施放者获得效果 | `add_1_strength` |
| `target_effects` | 目标获得效果 | `add_1_vulnerable` |
| `performer_after_target_effects` | 攻击后施放者效果 | `stress_damage_1` |
| `performer_buffs` | 施放者获得Buff | `combo_crit_50pct` |

### 4.2 添加效果

**示例: 给技能添加力量效果**

原文件:
```csv
performer_effects,move_forward_1
```

修改后:
```csv
performer_effects,move_forward_1,add_1_strength
```

### 4.3 移除效果

**示例: 移除压力伤害**

原文件:
```csv
performer_after_target_effects,stress_damage_1
```

修改后:
```csv
performer_after_target_effects,
```
或直接删除该行

---

## 五、常见修改场景

### 5.1 增加技能伤害

**找到**:
```csv
key_map,health_damage,health_damage_range,crit_chance
add_stats,5,3,0.05
```

**修改为** (增加2点基础伤害):
```csv
add_stats,7,3,0.05
```

### 5.2 修改攻击类型（单体→群体）

**找到**:
```csv
m_IsMultiHit,False
target_ranks,1,2,3,4
```

**修改为**:
```csv
m_IsMultiHit,True
target_ranks,1,2,3,4
```

**说明**: `m_IsMultiHit=False` 时需要逐个选择目标，`m_IsMultiHit=True` 时一次性攻击所有目标

### 5.3 添加连击配合

**在攻击技能中添加Buff**:
```csv
performer_buffs,combo_crit_50pct
```

**配合控制技能添加连击标记**:
```csv
target_effects,prime_combo
```

### 5.4 移除负面效果

**原文件**:
```csv
performer_after_target_effects,stress_damage_1
```

**修改为** (清空该字段):
```csv
performer_after_target_effects,
```

---

## 六、效果标记参考

详细的效果标记列表请参考: [available_effects.md](available_effects.md)

### 常用效果速查

**增益**:
- `add_1_strength` / `add_2_strength` - 力量
- `add_1_crit` / `add_2_crit` - 暴击标记
- `add_1_guard` / `add_2_guard` - 护卫

**减益**:
- `add_1_vulnerable` / `add_2_vulnerable` - 脆弱
- `add_1_weak` - 虚弱
- `add_1_daze` - 眩晕

**移除**:
- `remove_all_block` - 移除格挡
- `remove_all_guard` - 移除护卫
- `remove_all_dodge` - 移除闪避

**治疗**:
- `heal_10pct` / `heal_20pct` - 百分比治疗
- `heal_33pct_self_threshold_high` - 高血量自愈
- `hot_heal_medium` - 持续治疗

**DoT**:
- `skill_dot_small_bleed` - 流血
- `skill_dot_medium_blight` - 腐蚀

---

## 七、技能命名规则

| 类型 | 格式 | 示例 | 说明 |
|-----|------|------|------|
| 基础 | `{代码}_{名称}` | `abm_rake` | 基础技能 |
| 升级 | `{代码}_{名称}_u` | `abm_rake_u` | 升级版技能 |
| 路径 | `{代码}_{名称}_p{1/2/3}` | `abm_rake_p2` | 路径变体，如p2代表路径2中的技能变体 |
| 路径升级 | `{代码}_{名称}_p{数字}_u` | `abm_rake_p1_u` | 路径变体的升级版 |

---

## 八、修改步骤总结

1. **定位元素**: 使用 `element_start,{技能ID},ActorDataSkill` 找到技能
2. **理解结构**: 识别各个字段的作用
3. **修改数值**:
   - 伤害: 修改 `add_stats`
   - 效果: 修改 `*_effects` 字段
   - 类型: 修改 `m_IsMultiHit` 等属性
4. **验证格式**: 确保 CSV 格式正确（逗号分隔）
5. **测试**: 在游戏中验证修改效果

---

## 九、注意事项

1. **备份**: 修改前先备份原文件或提交到 git
2. **编码**: 使用 UTF-8 编码
3. **格式**: 保持 CSV 格式，注意逗号和换行
4. **平衡**: 建议小幅调整，避免过度强化
5. **测试**: 修改后在游戏中测试实际效果

---

*最后更新: 2026-01-04*
