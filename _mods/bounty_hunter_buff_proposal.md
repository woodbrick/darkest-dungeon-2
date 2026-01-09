# 赏金猎人技能改进方案

## 1. 当前技能 DU 评估

### 1.1 伤害计算规则

根据 [hero_file_rules.md](_mods/rules/hero_file_rules.md)：

```
实际伤害 = 基础值 ~ (基础值 + 随机值)
平均伤害 = (基础值 + 基础值 + 随机值) / 2
```

| CSV数值 | 实际伤害范围 | 平均伤害 |
|---------|-------------|----------|
| 8,4 | 8-12 | 10 |
| 6,4 | 6-10 | 8 |
| 3,2 | 3-5 | 4 |
| 2,2 | 2-4 | 3 |
| 2,1 | 2-3 | 2.5 |

### 1.2 技能 DU 评估表

| 技能 | 伤害 | 平均伤害 | 效果列表 | 效果DU | 总DU | 状态 |
|------|------|----------|----------|--------|------|------|
| bh_collect_bounty | 8,4 | 10 | end_combo, combo_damage_boost_50pct | -1+2.5=1.5 | **11.5** | ✅ 可接受 |
| bh_mark_for_death | 无 | 0 | prime_combo, add_2_vulnerable, remove_all_dodge, remove_all_dodge_plus | 3+5+5+6=19 | **19** | ✅ 优秀 |
| bh_come_hither | 3,2 | 4 | prime_combo, move_pull_2 | 3+3=6 | **10** | ✅ 可接受 |
| bh_uppercut | 3,2 | 4 | add_1_stun, move_knockback_1 | 4+1.5=5.5 | **9.5** | ✅ 可接受 |
| bh_flashbang | 无 | 0 | add_1_blind, add_1_daze, combo_add_1_stun, end_combo, move_shuffle | 4+2+4-1+1.5=10.5 | **10.5** | ✅ 可接受 |
| bh_finish_him | 6,4 | 8 | ignored_token_remove_1_block_plus, ignored_token_remove_1_block | 0.5+0.5=1 | **9** | ✅ 可接受 |
| bh_caltrops | 2,1 | 2.5 | skill_dot_medium_bleed, end_combo | 3.5-1=2.5 | **5** | ❌ 弱势 |
| bh_hurlbat | 6,4 | 8 | end_combo_if_target_has_dodge, ignored_token_remove_1_dodge_plus, ignored_token_remove_1_dodge | 0+2+1.5=3.5 | **11.5** | ✅ 可接受 |
| bh_staredown | 无 | 0 | add_2_weak, add_2_taunt_nr | 3.5+4.5=8 | **8** | ❌ 弱势 |
| bh_no_escape | 2,2 | 3 | add_1_stun, prime_combo, remove_all_guard, ignored_token_remove_1_dodge_plus, ignored_token_remove_1_dodge, ignored_token_remove_1_guard | 4+3+6+2+1.5+0.5=17 | **20** | ✅ 优秀 |
| bh_bodyguard | 无 | 0 | add_3_guard, add_3_block | 5+4.5=9.5 | **9.5** | ✅ 可接受 |

**注**：DU计算使用 [available_effects.md](_mods/rules/available_effects.md) 的标准值

### 1.3 技能分布统计

| 状态 | DU范围 | 数量 | 占比 | 技能 |
|------|--------|------|------|------|
| ✅ 优秀 | DU≥14 | 2 | 18% | mark_for_death(19), no_escape(20) |
| ✅ 可接受 | DU 9-13 | 7 | 64% | collect_bounty(11.5), come_hither(10), uppercut(9.5), flashbang(10.5), finish_him(9), hurlbat(11.5), bodyguard(9.5) |
| ❌ 弱势 | DU<9 | 2 | 18% | caltrops(5), staredown(8) |

---

## 2. 问题分析

### 2.1 需要改进的技能

#### bh_caltrops（铁蒺藜）- DU 5

**问题诊断**：
- 伤害 2,1 (平均2.5) 偏低
- skill_dot_medium_bleed (DU 3.5) 价值不足
- 作为陷阱技能，缺乏足够的威慑力

**当前体验**：
- 投放陷阱后伤害有限
- 流血效果不足以惩罚移动
- 与其他伤害技能相比缺乏竞争力

#### bh_staredown（怒视）- DU 8

**问题诊断**：
- add_2_weak (DU 3.5) 减益效果一般
- add_2_taunt_nr (DU 4.5) 嘲讽层数适中
- 缺乏自我保护手段

**当前体验**：
- 嘲讽后自身承受伤害
- 虚弱层数不足以压制输出
- 作为控制技能生存能力差

---

## 3. 优化方案

### 3.1 bh_caltrops（铁蒺藜）

**方案A：加强流血效果**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| target_effects | skill_dot_medium_bleed | skill_dot_large_bleed | 3.5→5 (+1.5) |

**预期DU**：2.5 + 5 - 1 = **6.5**

**理由**：将流血从小幅提升到大幅，增强陷阱威慑力

---

**方案B：提升伤害**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 2,1 | 3,2 | 2.5→4 (+1.5) |

**预期DU**：4 + 3.5 - 1 = **6.5**

**理由**：提升基础伤害，保持流血效果

---

**方案C：综合加强（推荐）**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| 伤害 | 2,1 | 3,2 | 2.5→4 (+1.5) |
| target_effects | skill_dot_medium_bleed | skill_dot_large_bleed | 3.5→5 (+1.5) |

**预期DU**：4 + 5 - 1 = **8**

**理由**：同时提升伤害和流血，使陷阱技能具有足够威胁

---

### 3.2 bh_staredown（怒视）

**方案A：提升虚弱层数**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| target_effects | add_2_weak | add_3_weak | 3.5→5 (+1.5) |

**预期DU**：5 + 4.5 = **9.5**

**理由**：提升虚弱层数，增强压制力

---

**方案B：添加自我保护**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| performer_effects | add_2_taunt_nr | add_2_taunt_nr, add_1_block | 4.5→4.5+2.5 (+2.5) |

**预期DU**：3.5 + 4.5 + 2.5 = **10.5**

**理由**：嘲讽时获得格挡，提高生存能力

---

**方案C：综合加强（推荐）**

| 字段 | 原值 | 新值 | DU变化 |
|------|------|------|--------|
| target_effects | add_2_weak | add_3_weak | 3.5→5 (+1.5) |
| performer_effects | add_2_taunt_nr | add_2_taunt_nr, add_1_block | 4.5→4.5+2.5 (+2.5) |

**预期DU**：5 + 4.5 + 2.5 = **12**

**理由**：同时提升压制力和生存能力

---

## 4. 实施细节

### 4.1 bh_caltrops（方案C - 推荐）

**修改位置**：`expedition/hero_bh_data_export.Group.csv`

**修改1：伤害**
```csv
element_start,bh_caltrops,ActorDataStats
key_map,health_damage,health_damage_range,crit_chance,
add_stats,3,2,0.05,
element_end
```

**修改2：流血效果**
```csv
element_start,bh_caltrops,ActorDataEffects
target_effects,skill_dot_large_bleed,bh_caltrops_move_res_down_e,bh_caltrops_speed_down_e,end_combo,
element_end
```

---

### 4.2 bh_staredown（方案C - 推荐）

**修改位置**：`expedition/hero_bh_data_export.Group.csv`

```csv
element_start,bh_staredown,ActorDataEffects
target_effects,add_3_weak,
performer_effects,add_2_taunt_nr,add_1_block,
performer_after_target_effects,remove_all_vulnerable,
element_end
```

---

## 5. 预期效果

### 5.1 核心改进（必改）

| 技能 | 当前DU | 新DU | 提升 |
|------|--------|------|------|
| bh_caltrops | 5 | 8 | +3 |
| bh_staredown | 8 | 12 | +4 |

**整体分布**：
- 优秀 (DU≥14)：2/11 (18%)
- 可接受 (DU 9-13)：9/11 (82%)
- 弱势 (DU<9)：0/11 (0%)

### 5.2 游玩乐趣提升

| 维度 | 改进前 | 改进后 |
|------|--------|--------|
| 陷阱技能威胁 | 弱（DU 5） | 强（DU 8） |
| 控制技能生存 | 低（无保护） | 高（有格挡） |

---

## 6. 实施建议

### 6.1 分阶段实施

**第一阶段（核心改进）**：
1. bh_caltrops - 提升伤害+加强流血
2. bh_staredown - 提升虚弱+添加格挡

### 6.2 测试验证

1. **数值验证**：修改后运行parse脚本验证DU计算
2. **实战测试**：实际游戏中测试技能表现
3. **平衡调整**：根据测试结果微调数值

### 6.3 风险控制

| 风险 | 缓解措施 |
|------|---------|
| bh_caltrops DU 8仍偏低 | 可进一步伤害提升至4,3 (DU 8.5) |
| bh_staredown生存仍不足 | 可提升格挡至add_2_block (DU 13.5) |

---

## 7. 总结

### 7.1 核心改进点

1. **bh_caltrops**：伤害+流血双提升，DU 5→8
2. **bh_staredown**：虚弱+格挡双提升，DU 8→12

### 7.2 预期效果

- 消除所有弱势技能（DU<9）
- 82%技能达到可接受水平（DU 9-13）
- 18%技能达到优秀水平（DU≥14）
- 提升陷阱技能和控制技能的游玩体验

---

*2026-01-09*
*设计原则：真实效果 + 正确DU计算 + 平衡性优化*
