# 公共基础效果

> **适用范围**：所有英雄共享的通用效果
> **数据来源**：effect_data_export.Group.csv
> **更新日期**：2026-01-09

---

## 控制效果 (Control)

| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_stun | 4 | 晕眩1次（跳过1回合） |
| add_2_stun | 7 | 晕眩2次 |
| add_1_daze | 2 | 减速1次 |
| add_2_daze | 3.5 | 减速2次 |
| add_3_daze | 5 | 减速3次 |
| add_1_blind | 4 | 致盲1次（攻击偏离） |
| add_2_blind | 6 | 致盲2次 |

---

## 增益效果 (Buffs)

### 力量 (Strength)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_strength | 3 | 下次攻击+50%伤害 |
| add_2_strength | 5 | 2次攻击+50%伤害 |
| add_3_strength | 7 | 3次攻击+50%伤害 |

### 格挡 (Block)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_block | 2.5 | 吸收1次50%伤害 |
| add_2_block | 3.5 | 吸收2次50%伤害 |
| add_3_block | 4.5 | 吸收3次50%伤害 |
| add_1_block_plus | 3.5 | 吸收1次75%伤害 |
| add_2_block_plus | 5 | 吸收2次75%伤害 |
| add_3_block_plus | 6.5 | 吸收3次75%伤害 |

### 闪避 (Dodge)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_dodge | 2 | 50%闪避1次 |
| add_2_dodge | 4 | 50%闪避2次 |
| add_3_dodge | 7 | 50%闪避3次 |
| add_1_dodge_plus | 3 | 75%闪避1次 |
| add_2_dodge_plus | 6 | 75%闪避2次 |

### 暴击 (Crit)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_crit | 6 | 下次攻击必暴击 |
| add_2_crit | 10 | 下2次攻击必暴击 |

### 反击 (Riposte)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_riposte | 3 | 受击反击1次 |
| add_2_riposte | 5 | 受击反击2次 |

### 其他增益
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_speed | 1.5 | 速度+1 |
| add_1_stealth | 1 | 隐身1层 |

---

## 减益效果 (Debuffs)

### 脆弱 (Vulnerable)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_vulnerable | 3 | 受击+50%伤害（1次） |
| add_2_vulnerable | 5 | 受击+50%伤害（2次） |
| add_3_vulnerable | 6 | 受击+50%伤害（3次） |

### 虚弱 (Weak)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_weak | 2 | 伤害-50%（1次） |
| add_2_weak | 3.5 | 伤害-50%（2次） |
| add_3_weak | 5 | 伤害-50%（3次） |

---

## 防御效果 (Defense)

### 嘲讽 (Taunt)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_taunt | 2.5 | 嘲讽（可移除） |
| add_1_taunt_nr | 3 | 嘲讽（不可移除） |
| add_2_taunt_nr | 4.5 | 嘲讽2层（不可移除） |

### 护卫 (Guard)
| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_guard | 2.5 | 护卫1层 |
| add_2_guard | 4 | 护卫2层 |
| add_3_guard | 5 | 护卫3层 |

---

## 移除效果 (Remove)

### 移除增益
| 效果ID | DU | 说明 |
|--------|-----|------|
| remove_all_block | 6 | 移除所有格挡 |
| remove_all_block_plus | 8 | 移除所有强力格挡 |
| remove_all_guard | 6 | 移除所有护卫 |
| remove_all_dodge | 5 | 移除所有闪避 |
| remove_all_dodge_plus | 6 | 移除所有强力闪避 |
| remove_all_strength | 8 | 移除所有力量 |
| remove_all_crit | 4 | 移除所有暴击 |
| remove_all_buffs | 10 | 移除所有增益 |

### 移除减益
| 效果ID | DU | 说明 |
|--------|-----|------|
| remove_all_bleed | 3 | 移除所有流血 |
| remove_all_blight | 3 | 移除所有腐蚀 |
| remove_all_burn | 3 | 移除所有燃烧 |
| remove_all_dots | 6 | 移除所有DoT |
| remove_all_daze | 4 | 移除所有眩晕 |

---

## 移动效果 (Move)

| 效果ID | DU | 说明 |
|--------|-----|------|
| move_forward_1 | 0.5 | 前进1格 |
| move_backward_1 | 0.5 | 后退1格 |
| move_pull_1 | 2 | 拉近1格 |
| move_pull_2 | 3 | 拉近2格 |
| move_knockback_1 | 1.5 | 击退1格 |
| move_knockback_2 | 2.5 | 击退2格 |
| move_knockback_3 | 4 | 击退3格 |
| move_shuffle | 1.5 | 随机洗牌 |
| move_swap | 2 | 交换位置 |

---

## 连击系统 (Combo)

| 效果ID | DU | 说明 |
|--------|-----|------|
| prime_combo | 3 | 启动连击 |
| end_combo | -1 | 结束连击（代价） |
| combo_damage_boost_50pct | 2.5 | 连击伤害+50% |
| combo_damage_boost_100pct | 4 | 连击伤害+100% |
| combo_crit_50pct | 3 | 连击暴击+50% |
| combo_crit_100pct | 5 | 连击暴击+100% |

---

## DoT效果

### 流血 (Bleed)
| 效果ID | DU | 总伤害 | 说明 |
|--------|-----|--------|------|
| skill_dot_small_bleed | 2 | 6 | 小流血 |
| skill_dot_medium_bleed | 3.5 | 9 | 中流血 |
| skill_dot_large_bleed | 5 | 12 | 大流血 |
| skill_dot_very_large_bleed | 7 | 15 | 超大流血 |
| skill_dot_massive_bleed | 9 | 18 | 巨量流血 |

### 腐蚀 (Blight)
| 效果ID | DU | 总伤害 | 说明 |
|--------|-----|--------|------|
| skill_dot_small_blight | 2 | 6 | 小腐蚀 |
| skill_dot_medium_blight | 3.5 | 9 | 中腐蚀 |
| skill_dot_large_blight | 5 | 12 | 大腐蚀 |

### 燃烧 (Burn)
| 效果ID | DU | 总伤害 | 说明 |
|--------|-----|--------|------|
| skill_dot_small_burn | 2.5 | 6 | 小燃烧 |
| skill_dot_medium_burn | 4 | 9 | 中燃烧 |
| skill_dot_large_burn | 6 | 12 | 大燃烧 |

---

## 连击特殊效果 (Combo Special)

| 效果ID | DU | 说明 |
|--------|-----|------|
| combo_add_1_stun | 4 | 连击结束施加晕眩 |
| combo_add_1_blind | 4 | 连击结束施加致盲 |
| combo_add_1_dodge | 4 | 连击结束施加闪避 |
| combo_add_1_block | 2.5 | 连击结束施加格挡 |
| end_combo_if_target_has_dodge | 0 | 条件连击结束 |

---

## 标记忽略效果 (Token Ignored)

### 格挡忽略
| 效果ID | DU | 说明 |
|--------|-----|------|
| ignored_token_remove_1_block | 0.5 | 破格挡附加 |
| ignored_token_remove_1_block_plus | 0.5 | 破强力格挡附加 |

### 闪避忽略
| 效果ID | DU | 说明 |
|--------|-----|------|
| ignored_token_remove_1_dodge | 1.5 | 破闪避附加 |
| ignored_token_remove_1_dodge_plus | 2 | 破强力闪避附加 |

### 护卫忽略
| 效果ID | DU | 说明 |
|--------|-----|------|
| ignored_token_remove_1_guard | 0.5 | 破护卫附加 |

---

## 其他效果

| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_mark | 2 | 标记1层 |
| add_2_mark | 3.5 | 标记2层 |
| add_1_debuff_resist | 1 | 减益抗性+1 |
| add_2_debuff_resist | 1.5 | 减益抗性+2 |
| add_1_immobilize | 3 | 定身1层 |
| add_2_immobilize | 5 | 定身2层 |

---

*文档维护：添加/修改效果时，保持表格格式和DU值的准确性*
