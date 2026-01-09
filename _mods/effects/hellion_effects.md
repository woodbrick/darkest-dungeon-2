# 地狱犬专属效果

> **英雄代码**：hel (Hellion)
> **核心机制**：嗜血、狂欢、流血
> **更新日期**：2026-01-09

---

## 嗜血技能 (Bloodlust)

### 嗜血伤害Buff

| 效果ID | DU | 说明 |
|--------|-----|------|
| hellion_bloodlust_damage_buff_e | 7 | 嗜血技能伤害加成 |
| hellion_bloodlust_u_damage_buff_e | 9 | 嗜血技能伤害加成（升级版） |

### 嗜血处决机制

| 效果ID | DU | 说明 |
|--------|-----|------|
| hellion_bloodlust_execution_buff_e | 5 | 嗜血触发时的增伤buff |
| hel_bloodlust_execution_buff_e | 5 | 嗜血处决buff（别名） |
| hellion_bloodlust_remove_execution | 0 | 移除嗜血buff（机制实现） |
| hel_bloodlust_remove_execution | 0 | 移除嗜血buff（别名） |

**机制说明**：
- 嗜血技能提供持续伤害加成
- 触发处决时获得额外增伤buff
- 处决后移除嗜血buff

---

## 狂欢技能 (Revelry)

| 效果ID | DU | 说明 |
|--------|-----|------|
| hellion_revelry_deathblow_resist_plus_e | 2 | 狂欢提供的死亡抵抗加成 |

---

## 肾上腺素技能 (Adrenaline)

| 效果ID | DU | 说明 |
|--------|-----|------|
| hellion_adrenaline_heal_hit_buff_e | 4 | 攻击时回复生命的buff |

---

## 路径专属效果

### 劫掠者路径 (Ravager)

| 效果ID | DU | 说明 |
|--------|-----|------|
| path_buff_hel_ravager_bleed_chance_down | 2 | 降低敌人流血抗性 |

### 狂战士路径 (Berserker)

| 效果ID | DU | 说明 |
|--------|-----|------|
| path_buff_hel_berserker_bleed_chance_up | 2 | 忽略敌人流血抗性 |

---

## 技能DU计算示例

| 技能 | 伤害 | 效果 | 总DU |
|------|------|------|------|
| hel_bloodlust | 0 | 嗜血伤害buff(7) | **7** |
| hel_bloodlust_u | 0 | 嗜血伤害buff升级(9) | **9** |
| hel_revelry | 伤害 | 狂欢buff | 伤害 + 2 |

---

*如需添加地狱犬新效果，在此文档中定义*
