# 赏金猎人技能改进方案

## 1. 弱势技能评估

### 当前技能 DU 评估

| 技能 | 伤害 | 可用位置 | 作用范围 | 效果列表 | 计算DU | 状态 |
|------|------|----------|----------|----------|---------|------|
| bh_collect_bounty | 8-4 | 1,2,3 | 敌方1,2单体 | end_combo | 6 | ❌ 弱势 |
| bh_mark_for_death | 无 | 1,2,3,4 | 敌方1-4单体 | prime_combo, add_2_vulnerable, remove_all_dodge, remove_all_dodge_plus | 13 | ⚠️ 可接受 |
| bh_come_hither | 3-2 | 1,2,3,4 | 敌方3,4单体 | prime_combo, move_pull_2 | 8.5 | ❌ 弱势 |
| bh_uppercut | 3-2 | 1,2 | 敌方1,2单体 | add_1_stun, move_knockback_1 | 8 | ❌ 弱势 |
| bh_flashbang | 无 | 2,3,4 | 敌方1-3单体 | add_1_blind, add_1_daze, combo_add_1_stun, end_combo, move_shuffle | 13.5 | ⚠️ 可接受 |
| bh_finish_him | 6-4 | 1,2,3 | 敌方1-3单体 | ignored_token_remove_1_block_plus, ignored_token_remove_1_block | 6 | ❌ 弱势 |
| bh_caltrops | 2-1 | 2,3,4 | 敌方3,4单体 | skill_dot_medium_bleed, end_combo | 5 | ❌ 弱势 |
| bh_hurlbat | 6-4 | 3,4 | 敌方1-4单体 | end_combo_if_target_has_dodge, ignored_token_remove_1_dodge_plus_if_target_combo, ignored_token_remove_1_dodge_if_target_combo | 5 | ❌ 弱势 |
| bh_staredown | 无 | 1,2,3,4 | 敌方1-4单体 | add_2_weak, add_2_taunt_nr | 5.5 | ❌ 弱势 |
| bh_no_escape | 2-2 | 3,4 | 敌方3,4单体 | add_1_stun, prime_combo, remove_all_guard, ignored_token_remove_1_dodge_plus, ignored_token_remove_1_dodge, ignored_token_remove_1_guard | 14 | ⚠️ 可接受 |
| bh_bodyguard | 无 | 1,2,3,4 | 自身+队友 | add_3_guard, add_3_block | 9.5 | ⚠️ 可接受 |

**注**：DU计算使用available_effects.md的标准值

### 弱势技能汇总

**不修改的技能** (已达标)：
- ⚠️ 可接受(DU 9-13)：mark_for_death(13)、flashbang(13.5)、no_escape(14)、bodyguard(9.5)

**需要改进的技能** (DU < 9)：
1. **bh_collect_bounty** (6) - 基础伤害低，无额外效果
2. **bh_come_hither** (8.5) - 伤害偏低
3. **bh_uppercut** (8) - 伤害偏低
4. **bh_finish_him** (6) - 破格挡效果好但伤害不足
5. **bh_caltrops** (5) - 伤害极低，流血效果不足以补偿
6. **bh_hurlbat** (5) - 破闪避效果好但伤害不足
7. **bh_staredown** (5.5) - 控制技能但整体价值偏低

---

## 2. 优化方案

### 2.1 bh_collect_bounty（收人悬赏）

**问题**：基础伤害仅6，作为主要输出技能DU过低

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 8-4 | 10-6 | 6→8 |
| performer_buffs | combo_damage_boost_50pct | combo_damage_boost_100pct | +1.5 |

**预期DU**：8 + 1.5 = 9.5

**理由**：提升伤害和连击加成，使其成为可靠的输出技能

---

### 2.2 bh_come_hither（过来）

**问题**：伤害2.5偏低，虽有拉拽效果但整体DU不足

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 3-2 | 5-3 | 2.5→4 |

**预期DU**：4 + 3(prime_combo) + 3(move_pull_2) = 10

**理由**：提升伤害，保持功能不变

---

### 2.3 bh_uppercut（上勾拳）

**问题**：伤害2.5偏低，虽有眩晕但整体DU不足

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 3-2 | 5-3 | 2.5→4 |

**预期DU**：4 + 4(stun) + 1.5(knockback) = 9.5

**理由**：提升伤害，保持控制功能

---

### 2.4 bh_finish_him（终结他）

**问题**：破格挡效果好但伤害仅5，作为终结技缺乏爆发感

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 6-4 | 9-6 | 5→7.5 |
| performer_buffs | execution_2_tooltip, bh_target_stun_dmg_boost | execution_2_tooltip, bh_target_stun_dmg_boost, combo_damage_boost_100pct | +4 |

**预期DU**：7.5 + 0.5 + 0.5 + 4 = 12.5

**理由**：大幅提升伤害并添加连击加成，符合"终结技"定位

---

### 2.5 bh_caltrops（铁蒺藜）

**问题**：伤害1.5极低，流血效果不足以补偿

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 2-1 | 4-2 | 1.5→3 |
| target_effects | skill_dot_medium_bleed | skill_dot_large_bleed | +1.5 |

**预期DU**：3 + 5(bleed) = 8

**理由**：提升伤害并加强流血效果

---

### 2.6 bh_hurlbat（投掷战斧）

**问题**：破闪避效果好但伤害仅5

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 6-4 | 9-6 | 5→7.5 |

**预期DU**：7.5 + 1.5 + 2 = 11

**理由**：大幅提升伤害，保持破闪避功能

---

### 2.7 bh_staredown（怒视）

**问题**：控制效果但整体价值仅5.5

**方案**：
| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| target_effects | add_2_weak | add_3_weak | +1.5 |
| performer_effects | add_2_taunt_nr | add_2_taunt_nr, add_1_block | +2.5 |

**预期DU**：5(weak) + 3(taunt) + 2.5(block) = 10.5

**理由**：提升虚弱层数并添加自我保护

---

## 3. 预期效果

### 3.1 DU分布改进

| 技能 | 当前DU | 新DU | 提升 |
|------|--------|------|------|
| bh_collect_bounty | 6 | 9.5 | +3.5 |
| bh_come_hither | 8.5 | 10 | +1.5 |
| bh_uppercut | 8 | 9.5 | +1.5 |
| bh_finish_him | 6 | 12.5 | +6.5 |
| bh_caltrops | 5 | 8 | +3 |
| bh_hurlbat | 5 | 11 | +6 |
| bh_staredown | 5.5 | 10.5 | +5 |

**整体分布**：
- 优秀 (DU≥14)：2/11 (18%)
- 可接受 (DU 9-13)：9/11 (82%)
- 弱势 (DU<9)：0/11 (0%)

### 3.2 游玩乐趣提升

| 维度 | 改进前 | 改进后 |
|------|--------|--------|
| 连击爽快感 | 弱（伤害低） | 强（爆发高） |
| 技能定位 | 模糊 | 明确 |
| 选择乐趣 | 困难 | 清晰 |

---

## 4. 实施细节

### 4.1 bh_collect_bounty

**修改位置**：`expedition/hero_bh_data_export.Group.csv`

```csv
element_start,bh_collect_bounty,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,10,6,0.05,
element_end
element_start,bh_collect_bounty,ActorDataSkill
performer_buffs,combo_damage_boost_100pct,
```

### 4.2 bh_come_hither

```csv
element_start,bh_come_hither,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,5,3,0.1,
element_end
```

### 4.3 bh_uppercut

```csv
element_start,bh_uppercut,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,5,3,0.1,
element_end
```

### 4.4 bh_finish_him

```csv
element_start,bh_finish_him,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,9,6,0.1,
element_end
element_start,bh_finish_him,ActorDataSkill
performer_buffs,execution_2_tooltip,bh_target_stun_dmg_boost,combo_damage_boost_100pct,
```

### 4.5 bh_caltrops

```csv
element_start,bh_caltrops,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,4,2,0.05,
element_end
element_start,bh_caltrops,ActorDataEffects
target_effects,skill_dot_large_bleed,bh_caltrops_move_res_down_e,bh_caltrops_speed_down_e,end_combo,
```

### 4.6 bh_hurlbat

```csv
element_start,bh_hurlbat,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,9,6,0.15,
element_end
```

### 4.7 bh_staredown

```csv
element_start,bh_staredown,ActorDataEffects
target_effects,add_3_weak,
performer_effects,add_2_taunt_nr,add_1_block,
performer_after_target_effects,remove_all_vulnerable,
element_end
```

---

## 5. 风险评估

### 5.1 可能需要调整的技能

| 技能 | 风险 | 调整方案 |
|------|------|---------|
| bh_finish_him (DU 12.5) | 爆发过高 | 移除combo_damage_boost_100pct，DU降至8.5 |
| bh_hurlbat (DU 11) | 远程伤害过高 | 降低伤害至8-5，DU降至9.5 |

### 5.2 实施建议

1. **分阶段实施**：先实施伤害提升，测试后添加buff
2. **保留备份**：备份原始数据
3. **实战测试**：根据实际效果调整

---

*2026-01-09*
*设计原则：使用真实效果 + 控制DU范围 + 提升游玩乐趣*
