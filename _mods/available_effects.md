# 可用效果标记完整清单

*来源文件*: `effect_data_export.Group.csv`
*扫描日期*: 2026-01-04
*价值评估*: 基于 [skill_valuation_system.md](skill_valuation_system.md) 的 DU (Damage Unit) 估值体系

## 价值单位说明
- **1 DU** = 1点基础伤害的等价价值
- 正值 = 正面效果增益
- 负值 = 负面效果代价
- 条件效果已考虑折扣系数

---

## 增益效果 (add_*)

### 力量 (Strength) - 持续伤害提升
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_strength | 3 | 1次攻击+50%伤害 (约3点额外伤害) |
| add_2_strength | 5 | 2次攻击+50%伤害 (约6点额外伤害，考虑不确定性打折扣) |
| add_3_strength | 7 | 3次攻击+50%伤害 (约9点额外伤害，更大不确定性折扣) |

### 格挡 (Block) - 临时护盾

#### 标准格挡 (吸收50%伤害)
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_block | 2.5 | 吸收1次攻击50%伤害 |
| add_2_block | 3.5 | 吸收2次攻击50%伤害 |
| add_3_block | 4.5 | 吸收3次攻击50%伤害 |

#### 强力格挡 (吸收75%伤害)
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_block_plus | 3.5 | 吸收1次攻击75%伤害 |
| add_2_block_plus | 5 | 吸收2次攻击75%伤害 |
| add_3_block_plus | 6.5 | 吸收3次攻击75%伤害 |

### 护卫 (Guard) - 保护队友
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_guard | 2.5 | 承担队友伤害 |
| add_2_guard | 4 | 双重护卫 |
| add_3_guard | 5 | 牺牲型强力保护 |
| add_1_multi_guard | 4 | 同时保护多个队友 |

### 暴击 (Crit) - 下次必暴
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_crit | 6 | 下次攻击必定暴击 (约2倍伤害，额外6点伤害) |
| add_1_crit_80pct | 4.8 | 80%概率下次攻击暴击 |
| add_2_crit | 10 | 两次必定暴击 (边际递减) |

### 反击 (Riposte) - 受击反击
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_riposte | 3 | 受击时反击，战术价值高 |
| add_2_riposte | 5 | 双次反击 |

### 闪避 (Dodge)
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_dodge | 2 | 约20%闪避，持续3回合 |
| add_2_dodge | 3.5 | 高闪避率 |
| add_3_dodge | 4.5 | 极高闪避 |

### 隐身 (Stealth)
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_stealth | 1 | 免疫单体攻击，但伤害转移给队友且无法规避AOE |
| add_2_stealth | 1.5 | 双层隐身 |

### 其他增益
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_speed | 1.5 | 先手优势 |

---

## 减益效果 (Debuffs)

### 脆弱 (Vulnerable) - 受伤增加
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_vulnerable | 3 | 目标受到伤害+50% |
| add_2_vulnerable | 5 | 目标受到伤害+50% 持续2次攻击，不一定能触发 |
| add_3_vulnerable | 6 | 目标受到伤害+50% 持续3次攻击 |

### 虚弱 (Weak) - 伤害降低
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_weak | 2 | 目标造成伤害-50% |
| add_2_weak | 3.5 | 目标造成伤害-50% 持续2次 |
| add_3_weak | 5 | 目标造成伤害-50% 持续3次 |

### 控制效果 (Control)
| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_daze | 2 | 减速1次，延迟行动 |
| add_2_daze | 3.5 | 减速2次 |
| add_3_daze | 5 | 延迟多回合 |
| add_1_stun | 4 | 跳过1回合，极高价值 |

---

## 治疗效果 (heal_*)

*来源*: `effect_data_export.Group.csv`
*机制*: 固定数值治疗，暴击几率5%，暴击倍率0.5

### 固定数值治疗
| 效果 | 价值 | 说明 |
|------|------|------|
| heal_tiny | 0.5 | 恢复1点生命值 |
| heal_very_small | 1 | 恢复3点生命值 |
| heal_small | 1.5 | 恢复5点生命值 |
| heal_medium | 2.5 | 恢复10点生命值 |
| heal_large | 4 | 恢复16点生命值 |
| heal_very_large | 6 | 恢复25点生命值 |
| heal_massive | 8 | 恢复40点生命值 |

### 血量阈值治疗 (低血量加成)
| 效果 | 价值 | 说明 |
|------|------|------|
| heal_tiny_hp_low | 0.5 | 低血量时恢复1点 |
| heal_very_small_hp_low | 1 | 低血量时恢复3点 |
| heal_small_hp_low | 1.5 | 低血量时恢复5点 |
| heal_medium_hp_low | 2.5 | 低血量时恢复10点 |
| heal_large_hp_low | 4 | 低血量时恢复16点 |
| heal_very_large_hp_low | 6 | 低血量时恢复25点 |
| heal_massive_hp_low | 8 | 低血量时恢复40点 |

**注意**:
- 所有治疗效果有5%暴击几率，暴击时治疗量x0.5
- `*_hp_low` 版本需要满足 `target_meets_heal_threshold_low` 条件 |

### 百分比治疗
| 效果 | 价值 | 说明 |
|------|------|------|
| heal_5pct | 1 | 恢复5%生命值 (约2点，回血价值高) |
| heal_10pct | 2 | 恢复10%生命值 (约4点) |
| heal_15pct | 3 | 恢复15%生命值 (约6点) |
| heal_20pct | 4 | 恢复20%生命值 (约8点) |
| heal_25pct | 5 | 恢复25%生命值 (约10点) |
| heal_30pct | 6 | 恢复30%生命值 (约12点) |
| heal_33pct | 6.5 | 恢复33%生命值 (约13点) |
| heal_35pct | 7 | 恢复35%生命值 (约14点) |
| heal_40pct | 8 | 恢复40%生命值 (约16点) |
| heal_50pct | 10 | 恢复50%生命值 (约20点) |
| heal_60pct | 12 | 恢复60%生命值 (约24点) |
| heal_67pct | 13.5 | 恢复67%生命值 (约27点) |
| heal_70pct | 14 | 恢复70%生命值 (约28点) |
| heal_75pct | 15 | 恢复75%生命值 (约30点) |
| heal_80pct | 16 | 恢复80%生命值 (约32点) |
| heal_90pct | 18 | 恢复90%生命值 (约36点) |
| heal_100pct | 20 | 完全恢复生命值 (约40点) |

### 阈值治疗 (Threshold Healing)
| 效果 | 价值 | 说明 |
|------|------|------|
| heal_20pct_self_threshold_med | 2 | 中等血量阈值时自愈20% (约8点，条件限制大) |
| heal_33pct_self_threshold_high | 3 | 高血量阈值时自愈33% (约13点，条件限制) |
| heal_33pct_self_threshold_low | 1.6 | 低血量(33%)阈值时自愈33%，角色可能快速死亡 |
| heal_33pct_self_threshold_med | 2.5 | 中等血量阈值时自愈33% (约13点，条件限制) |
| heal_50pct_self_threshold_high | 6 | 高血量(50%+)时自愈50% (约20点，条件限制) |
| heal_50pct_self_threshold_med | 4 | 中等血量(50%)时自愈50% (约20点，低血量角色易死) |
| heal_75pct_self_threshold_med | 6 | 中等血量时自愈75% (约30点，条件限制) |

---

## 持续治疗 (Heal HOT - heal_hot_*)

*来源*: `dots_data_export.Group.csv`
*机制*: HOT (Heal Over Time) - 在施法者回合开始时触发

| 效果 | 价值 | 说明 |
|------|------|------|
| heal_hot_very_small | 1 | 持续3回合，每回合回复1点 (总约3点) |
| heal_hot_small | 2 | 持续3回合，每回合回复2点 (总约6点) |
| heal_hot_medium | 5 | 持续3回合，每回合回复3点 (总约9点) |
| heal_hot_large | 8 | 持续3回合，每回合回复4点 (总约12点) |
| heal_hot_very_large | 12 | 持续3回合，每回合回复5点 (总约15点) |
| heal_hot_massive | 16 | 持续3回合，每回合回复6点 (总约18点) |
| heal_hot_super_massive | 20 | 持续3回合，每回合回复10点 (总约30点，忽略友好伤害修正) |

**注意**:
- 所有HOT效果在 `performer_turn_start` (施法者回合开始) 时触发
- 持续时间均为 `DurationAmount: 3`
- `heal_hot_super_massive` 有 `m_IgnoreFriendlyDealtModifications: True` 标记 |

---

## DoT效果 (skill_dot_*)

*来源*: `dots_data_export.Group.csv`
*机制*: DoT (Damage Over Time) - 在施法者回合开始时触发
*持续时间*: 所有 DoT 持续3回合 (`DurationAmount: 3`)
*触发时机*: `performer_turn_start`
*伤害修正*: 所有 skill_*_dot 忽略友好/敌方的伤害修正

### 流血 (Bleed)
| 效果ID | 伤害/回合 | 总伤害 | 价值 | 说明 |
|--------|----------|--------|------|------|
| skill_very_small_bleed_dot | 1 | 3 | 0.5 | 超小流血DoT |
| skill_small_bleed_dot | 2 | 6 | 2 | 小流血DoT |
| skill_medium_bleed_dot | 3 | 9 | 3.5 | 中等流血DoT |
| skill_large_bleed_dot | 4 | 12 | 5 | 大流血DoT |
| skill_very_large_bleed_dot | 5 | 15 | 7 | 超大流血DoT |
| skill_massive_bleed_dot | 6 | 18 | 9 | 巨大流血DoT |
| skill_super_massive_bleed_dot | 10 | 30 | 12 | 超巨大流血DoT |

### 腐蚀 (Blight)
| 效果ID | 伤害/回合 | 总伤害 | 价值 | 说明 |
|--------|----------|--------|------|------|
| skill_very_small_blight_dot | 1 | 3 | 0.5 | 超小腐蚀DoT |
| skill_small_blight_dot | 2 | 6 | 2 | 小腐蚀DoT |
| skill_medium_blight_dot | 3 | 9 | 3.5 | 中等腐蚀DoT |
| skill_large_blight_dot | 4 | 12 | 5 | 大腐蚀DoT |
| skill_very_large_blight_dot | 5 | 15 | 7 | 超大腐蚀DoT |
| skill_massive_blight_dot | 6 | 18 | 9 | 巨大腐蚀DoT |

### 燃烧 (Burn)
| 效果ID | 伤害/回合 | 总伤害 | 价值 | 说明 |
|--------|----------|--------|------|------|
| skill_very_small_burn_dot | 1 | 3 | 1.5 | 超小燃烧DoT |
| skill_small_burn_dot | 2 | 6 | 2.5 | 小燃烧DoT |
| skill_medium_burn_dot | 3 | 9 | 4 | 中等燃烧DoT |
| skill_large_burn_dot | 4 | 12 | 6 | 大燃烧DoT |
| skill_very_large_burn_dot | 5 | 15 | 8 | 超大燃烧DoT |
| skill_massive_burn_dot | 6 | 18 | 10 | 巨大燃烧DoT |

### 恐怖 (Horror) - 压力DoT
| 效果ID | 效果 | 价值 | 说明 |
|--------|------|------|------|
| horror_dot_small | stress_damage_1_50pct | -0.5 | 50%概率造成1点压力，持续3回合 |
| horror_dot_medium | stress_damage_1_75pct | -0.75 | 75%概率造成1点压力，持续3回合 |
| horror_dot_large | stress_damage_1 | -1 | 必定造成1点压力，持续3回合 |

### 其他 DoT 变体
*这些是特殊用途的 DoT，通常用于特定英雄或场景*

| 效果ID | 类型 | 伤害/回合 | 说明 |
|--------|------|----------|------|
| taproot_damage | strangle | 2 | 特殊勒索效果，持续98回合 |
| run_controlled_burn_dot | burn | ? | 运行者专用燃烧DoT |
| run_controlled_burn_u_dot | burn | ? | 运行者专用燃烧DoT(升级版) |
| run_p1_skill_small_burn_dot | burn | 2 | 运行者P1技能燃烧 |
| self_skill_*_bleed_dot | bleed | 2/3 | 自我施加流血DoT |
| self_skill_*_blight_dot | blight | 2/3 | 自我施加腐蚀DoT |
| self_skill_*_burn_dot | burn | 2/3 | 自我施加燃烧DoT |

**注意**:
- 所有 skill_*_dot 效果都有 `m_IgnoreFriendlyDealtModifications: True` 标记
- 标准版本 (如 `large_bleed_dot`) 还有额外的 IgnoreReceivedModifications 标记
- DoT 效果名称格式: `skill_<等级>_<类型>_dot` 或 `<等级>_<类型>_dot`

---

## 压力效果 (stress_*)

### 压力伤害 (负面)
| 效果 | 价值 | 说明 |
|------|------|------|
| stress_damage_1 | -2 | 造成1点压力伤害 |
| stress_damage_1_10pct | -0.2 | 10%概率造成1点压力 |
| stress_damage_1_15pct | -0.3 | 15%概率造成1点压力 |
| stress_damage_1_25pct | -0.5 | 25%概率造成1点压力 |
| stress_damage_1_30pct | -0.6 | 30%概率造成1点压力 |
| stress_damage_1_33pct | -0.66 | 33%概率造成1点压力 |
| stress_damage_1_50pct | -1 | 50%概率造成1点压力 |
| stress_damage_1_66pct | -1.32 | 66%概率造成1点压力 |
| stress_damage_1_75pct | -1.5 | 75%概率造成1点压力 |

### 压力治疗 (正面)
| 效果 | 价值 | 说明 |
|------|------|------|
| stress_heal_1 | 1 | 恢复1点压力 |
| stress_heal_2 | 2 | 恢复2点压力 |
| stress_heal_3 | 3 | 恢复3点压力 |
| stress_heal_4 | 4 | 恢复4点压力 |
| stress_heal_5 | 5 | 恢复5点压力 |
| stress_heal_6 | 5.5 | 恢复6点压力 (边际递减) |
| stress_heal_7 | 6 | 恢复7点压力 (边际递减) |
| stress_heal_8 | 6.5 | 恢复8点压力 (边际递减，很难满压时触发) |
| stress_heal_9 | 7 | 恢复9点压力 (严重边际递减，几乎不可能满压时用) |

---

## 移除效果 (remove_all_*)

### 移除增益
| 效果 | 价值 | 说明 |
|------|------|------|
| remove_all_block | 6 | 移除所有格挡 |
| remove_all_block_plus | 8 | 移除所有格挡(加强版) |
| remove_all_guard | 6 | 移除所有护卫 |
| remove_all_dodge | 5 | 移除所有闪避 |
| remove_all_dodge_plus | 6 | 移除所有闪避(加强版) |
| remove_all_riposte | 6 | 移除所有反击，战术价值高 |
| remove_all_strength | 8 | 移除所有力量 |
| remove_all_crit | 4 | 移除所有暴击加成 |
| remove_all_buffs | 10 | 移除所有增益，强力 |
| remove_all_stealth | 3 | 移除所有隐身 |

### 移除减益/DoT
| 效果 | 价值 | 说明 |
|------|------|------|
| remove_all_bleed | 3 | 移除所有流血 |
| remove_all_blight | 3 | 移除所有腐蚀 |
| remove_all_burn | 3 | 移除所有燃烧 |
| remove_all_dots | 6 | 移除所有DoT |
| remove_all_daze | 4 | 移除所有眩晕 |

### 移除其他
| 效果 | 价值 | 说明 |
|------|------|------|
| remove_all_combo_visible | 3 | 移除所有可见连击标记 |
| remove_all_conviction | 3 | 移除所有信念(十字军) |

---

## 连击系统 (Combo)

### 连击标记
| 效果 | 价值 | 说明 |
|------|------|------|
| prime_combo | 3 | 给目标添加连击标记 |
| end_combo | -1 | 消耗连击标记结束连击 |

### 连击Buff (performer_buffs)
| 效果 | 价值 | 说明 |
|------|------|------|
| combo_crit_50pct | 3 | 对连击标记敌人+50%暴击率 |
| combo_crit_100pct | 5 | 对连击标记敌人+100%暴击率 |
| combo_damage_boost_50pct | 2.5 | 对连击标记敌人伤害+50% |
| combo_damage_boost_100pct | 4 | 对连击标记敌人伤害+100% |

---

## 移动效果 (move_*)

| 效果 | 价值 | 说明 |
|------|------|------|
| move_forward_1 | 0.5 | 前进1格，战术价值 |
| move_backward_1 | 0.5 | 后退1格，战术价值 |
| move_pull_1 | 1.5 | 拉近1格，破坏阵型 |
| move_pull_2 | 2.5 | 拉近2格，强力控制 |
| move_knockback_1 | 1.5 | 击退1格 |
| move_knockback_2 | 2.5 | 击退2格，强力控制 |
| move_swap | 1 | 交换位置，战术价值 |

---

## 嘲讽 (Taunt)

| 效果 | 价值 | 说明 |
|------|------|------|
| add_1_taunt | 2.5 | 嘲讽敌人强制攻击自己 |
| add_1_taunt_nr | 3 | 嘲讽(不可移除) |

---
