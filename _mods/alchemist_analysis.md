# 炼金术士 (Alchemist/Abomination) 完整能力分析报告

---

## 一、基础属性

- **生命值**: 40
- **速度**: 3
- **压力上限**: 10
- **死亡抵抗**: 1

**抗性**:

- **stun**: 0.3
- **blight**: 0.3
- **bleed**: 0.2
- **burn**: 0.1
- **disease**: 0.4
- **move**: 0.3
- **debuff**: 0.2
- **death**: 0.6

---

## 二、变身技能 (Transformation)

### 基础变身 (abm_transform)

- **冷却**: 5 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1, abm_stress_damage_1_33pct

### 升级变身 (abm_transform_u)

- **冷却**: 3 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, add_1_strength, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1

### 路径1变身 (abm_transform_p1)

- **冷却**: 5 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1, abm_stress_damage_1_33pct

### 路径1升级 (abm_transform_p1_u)

- **冷却**: 3 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, add_1_strength, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1

### 路径2变身 (abm_transform_p2)

- **冷却**: 5 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_p2_res_ignore_e, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1, abm_stress_damage_1_75pct

### 路径2升级 (abm_transform_p2_u)

- **冷却**: 3 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_p2_u_res_ignore_e, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1, abm_stress_damage_1_33pct

### 路径3变身 (abm_transform_p3)

- **冷却**: 4 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_p3_stress_nr, abm_moribund_stress_res_debuff_e, abm_transform_spd_buff_e
- **队友效果**: abm_stress_damage_1, abm_stress_damage_1_33pct

### 路径3升级 (abm_transform_p3_u)

- **冷却**: 2 回合
- **施放位置**: 1, 2, 3, 4
- **免费动作**: 是
- **自身效果**: abm_transform_mode, abm_transform_p3_stress_nr, abm_moribund_stress_res_debuff_e, abm_transform_spd_buff_e, dot_horror_large
- **队友效果**: abm_stress_damage_1


---

## 三、野兽形态技能 (Beast Form)

### 利爪 - 基础 (abm_rake)

- **伤害**: 3-3 (+2随机) = 5 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_dmg_buff_e
- **攻击后效果**: stress_damage_1

### 利爪 - 升级 (abm_rake_u)

- **伤害**: 3-3 (+2随机) = 5 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_u_dmg_buff_e
- **攻击后效果**: stress_damage_1

### 利爪 - 路径2 (abm_rake_p2)

- **伤害**: 3-3 (+1随机) = 4 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_p2_bleed_buff_e
- **目标效果**: skill_dot_small_bleed
- **攻击后效果**: stress_damage_2

### 利爪 - 路径2升级 (abm_rake_p2_u)

- **伤害**: 4-4 (+1随机) = 5 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_p2_u_bleed_buff_e
- **目标效果**: skill_dot_small_bleed
- **攻击后效果**: stress_damage_2

### 利爪 - 路径3 (abm_rake_p3)

- **伤害**: 3-3 (+2随机) = 5 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_dmg_buff_e, abm_rake_p3_extra_buff_chance

### 利爪 - 路径3升级 (abm_rake_p3_u)

- **伤害**: 3-3 (+2随机) = 5 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2
- **多段攻击**: True
- **自身效果**: abm_rake_u_dmg_buff_e, abm_rake_p3_u_extra_buff_chance

### 重击 - 基础 (abm_slam)

- **伤害**: 4-4 (+3随机) = 7 平均
- **施放位置**: 2, 3, 4
- **目标位置**: 1, 2, 3
- **多段攻击**: False
- **自身效果**: move_forward_1
- **目标效果**: move_knockback_1, add_1_daze
- **攻击后效果**: stress_damage_1

### 重击 - 升级 (abm_slam_u)

- **伤害**: 6-6 (+2随机) = 8 平均
- **施放位置**: 2, 3, 4
- **目标位置**: 1, 2, 3
- **多段攻击**: False
- **自身效果**: move_forward_1
- **目标效果**: move_knockback_1, add_1_daze, remove_all_dodge, remove_all_dodge_plus, ignored_token_remove_1_dodge_plus, ignored_token_remove_1_dodge
- **攻击后效果**: stress_damage_1

### 狂怒 - 基础 (abm_rage)

- **伤害**: 5-5 (+2随机) = 7 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2, 3
- **多段攻击**: False
- **攻击后效果**: stress_damage_1

### 狂怒 - 升级 (abm_rage_u)

- **伤害**: 6-6 (+2随机) = 8 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2, 3
- **多段攻击**: False
- **攻击后效果**: stress_damage_1

### 咆哮 - 基础 (abm_howl)

- **伤害**: 0.1-0.1 (+?随机) = 0.1+? 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2, 3, 4
- **多段攻击**: False
- **目标效果**: move_pull_1, add_2_vulnerable, remove_all_riposte
- **攻击后效果**: stress_damage_1

### 咆哮 - 升级 (abm_howl_u)

- **伤害**: 2-2 (+1随机) = 3 平均
- **施放位置**: 1, 2
- **目标位置**: 1, 2, 3, 4
- **多段攻击**: False
- **目标效果**: move_pull_2, add_2_vulnerable, remove_all_riposte
- **攻击后效果**: stress_damage_1


---

## 四、人类形态技能 (Human Form)

### 锁链 - 基础 (abm_manacles)

- **伤害**: 3-3 (+1随机) = 4 平均
- **施放位置**: 1, 2, 3
- **目标位置**: 2, 3, 4
- **目标效果**: move_pull_1, prime_combo, remove_all_crit

### 锁链 - 升级 (abm_manacles_u)

- **伤害**: 4-4 (+2随机) = 6 平均
- **施放位置**: 1, 2, 3
- **目标位置**: 2, 3, 4
- **目标效果**: move_pull_2, prime_combo, remove_all_strength, remove_all_crit

### 锁链 - 路径1 (abm_manacles_p1)

- **伤害**: 3-3 (+3随机) = 6 平均
- **施放位置**: 3, 4
- **目标位置**: 1, 2, 3
- **目标效果**: prime_combo

### 锁链 - 路径1升级 (abm_manacles_p1_u)

- **伤害**: 5-5 (+3随机) = 8 平均
- **施放位置**: 3, 4
- **目标位置**: 1, 2, 3
- **目标效果**: prime_combo, gen_debuff_stun_res_10pct_e


---

## 五、解除变身技能 (Revert)

### 基础解除 (abm_revert)

- **冷却**: 1 回合
- **免费动作**: True
- **效果**: abm_revert_mode, remove_abm_beast_buff, abm_revert_spd_debuff_e, stress_heal_2, hot_heal_medium

### 升级解除 (abm_revert_u)

- **冷却**: 1 回合
- **免费动作**: True
- **效果**: abm_revert_mode, remove_abm_beast_buff, abm_revert_spd_debuff_e, stress_heal_2, hot_heal_medium

### 路径1解除 (abm_revert_p1)

- **冷却**: 1 回合
- **免费动作**: True
- **效果**: abm_revert_mode, remove_abm_beast_buff, abm_revert_spd_debuff_e, stress_heal_2, hot_heal_medium, move_backward_1

### 路径1升级 (abm_revert_p1_u)

- **冷却**: 1 回合
- **免费动作**: True
- **效果**: abm_revert_mode, remove_abm_beast_buff, abm_revert_spd_debuff_e, stress_heal_2, hot_heal_medium, move_backward_1


---

## 六、问题总结

### 6.1 变身机制问题
1. **队友压力负担**: 变身会对所有队友造成压力 (1点 + 33%/75%概率额外1点)
2. **冷却时间**: 基础5回合较长，升级后3回合仍偏长
3. **免费动作**: ✓ 变身是免费动作，这是优点
4. **解除消耗**: 需要手动解除，虽然是免费动作但仍占用操作

### 6.2 野兽形态技能问题
1. **伤害偏低**: 
   - 利爪: 3-5伤害 (2次攻击 = 6-10总计)
   - 狂怒: 5-7伤害 (单次)
   - 重击: 4-7伤害 (有控制效果)
2. **自我压力**: 野兽技能使用后会对自身造成压力伤害
3. **技能有限**: 野兽形态只有3个技能，灵活性不足
4. **无生存能力**: 无治疗、无防御增益、无吸血

### 6.3 人类形态技能问题
1. **锁链伤害低**: 3-4伤害，主要是辅助技能
2. **酸液效果**: 需要查看具体数据

### 6.4 基础属性问题
1. **生命值偏低**: 40点对比其他近战英雄偏少
2. **抗性不足**: 
   - 流血抗性: 仅20%
   - 燃烧抗性: 仅10% (致命弱点)

