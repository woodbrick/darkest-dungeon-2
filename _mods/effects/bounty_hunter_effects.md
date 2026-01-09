# 赏金猎人专属效果

> **英雄代码**：bh (Bounty Hunter)
> **核心机制**：连击系统、标记破坏
> **更新日期**：2026-01-09

---

## 连击标记破坏 (Combo Token Break)

赏金猎人使用公共效果 `ignored_token_remove_*` 系列，详见 [base_effects.md](base_effects.md#标记忽略效果-token-ignored)。

| 效果 | DU | 说明 |
|------|-----|------|
| ignored_token_remove_1_block | 0.5 | 破格挡附加效果 |
| ignored_token_remove_1_block_plus | 0.5 | 破强力格挡附加效果 |
| ignored_token_remove_1_dodge | 1.5 | 破闪避附加效果 |
| ignored_token_remove_1_dodge_plus | 2 | 破强力闪避附加效果 |
| ignored_token_remove_1_guard | 0.5 | 破护卫附加效果 |

---

## 连击特殊效果

赏金猎人使用公共连击效果，详见 [base_effects.md](base_effects.md#连击特殊效果-combo-special)。

| 效果 | DU | 说明 |
|------|-----|------|
| end_combo_if_target_has_dodge | 0 | 条件连击结束（仅当目标有闪避时） |

---

## 技能效果组合

赏金猎人技能主要使用公共效果组合，典型配置：

| 技能 | 效果组合 | 总DU |
|------|---------|------|
| mark_for_death | prime_combo(3) + add_2_vulnerable(5) + remove_all_dodge(5) + remove_all_dodge_plus(6) | 19 |
| collect_bounty | 伤害10 + end_combo(-1) + combo_damage_boost_50pct(2.5) | 11.5 |
| finish_him | 伤害8 + ignored_token_remove_1_block_plus(0.5) + ignored_token_remove_1_block(0.5) | 9 |

---

## 当前状态

- **无专属效果**：赏金猎人所有效果都使用公共定义
- **连击特色**：主要通过效果组合实现玩法

---

*如需添加赏金猎人专属效果，在此文档中定义*
