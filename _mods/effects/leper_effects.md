# 麻风剑士专属效果

> **英雄代码**：lep (Leper)
> **核心机制**：废墟增伤、自我致盲、高生存
> **更新日期**：2026-01-09

---

## 复仇技能 (Revenge)

### 复仇Buff

| 效果ID | DU | 说明 |
|--------|-----|------|
| leper_revenge_strength_buff_e | 2 | 3回合内每回合开始力量+1 |
| leper_revenge_crit_buff_e | 2 | 3回合内每回合开始暴击+1 |

**技能示例**：lep_revenge
- 基础：脆弱2×2(持久) + 复仇力量buff
- DU = 脆弱代价 + 力量buff收益

---

## 废墟技能 (Ruin)

### 废墟增伤机制

| 效果ID | DU | 说明 |
|--------|-----|------|
| leper_ruin_damage_buff_e | 7 | 触发+30%伤害（持续3回合） |
| leper_ruin_damage_buff_u_e | 9 | 触发+40%伤害（升级版） |
| leper_ruin_damage_buff_manager_e | 7 | 增伤触发器 |
| leper_ruin_damage_buff_manager_u_e | 9 | 增伤触发器（升级版） |
| leper_ruin_damage_buff_listener_e | 0 | 3回合后移除buff（机制实现） |
| leper_ruin_damage_buff_listener_u_e | 0 | 移除buff升级版（机制实现） |

**机制说明**：
- 施放废墟技能后获得manager
- 3回合内每次造成伤害触发增伤buff
- listener在3回合结束后移除buff
- DU评估考虑实战难度（难满3回合），理论值打折

**技能示例**：lep_ruin
- 基础：废墟增伤触发(DU 7)
- 升级：废墟增伤触发升级(DU 9) + 小流血代价

---

## 自我致盲机制

| 效果ID | DU | 说明 |
|--------|-----|------|
| leper_self_blind_chance | -1 | 攻击后有几率致盲自己（代价） |
| leper_self_blind_chance_u | -0.5 | 自我致盲升级版（代价减半） |

**技能示例**：lep_chop
- 基础：伤害 + 自我致盲几率 + end_combo(若致盲)
- DU = 伤害 - 1

---

## 坚守技能 (Withstand)

### 坚守Buff

| 效果ID | DU | 说明 |
|--------|-----|------|
| leper_withstand_block_buff_e | 2 | 坚守格挡标记 |
| leper_withstand_dot_resist_buff_e | 1.5 | DoT抗性+30% |
| leper_withstand_dot_resist_buff_u_e | 2 | DoT抗性升级版 |
| leper_withstand_move_resist_buff_e | 1.5 | 移动抗性+30% |
| leper_withstand_move_resist_buff_u_e | 2 | 移动抗性升级版 |

**技能示例**：lep_withstand
- 基础：格挡2 + 嘲讽2 + DoT抗性buff + 移动抗性buff
- DU = 伤害 + 效果DU = 2 + 1.5 + 1.5 = 11.5

---

## 反思技能 (Reflection)

| 效果ID | DU | 说明 |
|--------|-----|------|
| leper_reflection_debuff_res_buff_e | 1.5 | 反思减益抗性buff |

**技能示例**：lep_reflection
- 基础：压力治疗2 + 格挡1 + 减益抗性buff
- 升级：压力治疗3 + 强力格挡1 + 减益抗性buff

---

## 路径专属效果

### 君王路径 (Monarch)

| 效果ID | DU | 说明 |
|--------|-----|------|
| lep_monarch_chop_dmg_vs_cosmic | 1 | 对宇宙敌人伤害加成 |

**技能示例**：lep_chop_p3
- 修正DU = 基础DU - HP代价补偿 + 宇宙专精加成

---

## 麻风剑士专属移动/移除效果

| 效果ID | DU | 说明 |
|--------|-----|------|
| move_knockback_3 | 4 | 击退3格 |
| remove_all_blind | 1 | 移除所有致盲 |
| remove_all_combo_visible | 0.5 | 移除连击可见性 |
| remove_all_weak | 1 | 移除所有虚弱 |

---

## 技能DU计算示例

| 技能 | 伤害 | 效果 | 总DU |
|------|------|------|------|
| lep_ruin | 0 | 废墟增伤触发(7) | **7** |
| lep_ruin_u | 0 | 废墟增伤触发升级(9) + 小流血代价(-2.5) | **6.5** |
| lep_revenge | 0 | 脆弱2×2(-3) + 复仇力量buff(2) × 3回合 | **8** |
| lep_withstand | 0 | 格挡2(2) + 嘲讽2(3) + DoT抗性(1.5) + 移动抗性(1.5) | **11.5** |
| lep_reflection | 0 | 压力治疗2(2) + 格挡1(2.5) + 减益抗性(1.5) | **7** |

---

*如需添加麻风剑士新效果，在此文档中定义*
