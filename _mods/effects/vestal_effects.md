# 修女专属效果

> **英雄代码**：ves (Vestal)
> **核心机制**：信念系统、祝福、治疗
> **更新日期**：2026-01-09

---

## 信念机制 (Conviction)

### 信念标记

| 效果ID | DU | 说明 |
|--------|-----|------|
| conviction | 1.5 | 信念标记（修女资源，最多3层） |
| ves_pay_conviction_cost | -0.5 | 消耗所有信念层（代价） |
| ves_blessing_add_1_conviction | 2 | 回合开始获得1层信念（炽天使路径） |

**机制说明**：
- 信念是修女的资源系统，最多3层
- 每层强化技能效果
- 强化技能需要消耗信念

---

## 祝福Buff (Blessings)

### 勇气祝福 (Fortitude)

| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_blessing_of_fortitude | 4 | 回合开始随机获得格挡或闪避（3回合） |
| add_1_blessing_of_fortitude_u | 5.5 | 回合开始随机获得强力格挡或强力闪避（3回合） |
| add_1_blessing_of_fortitude_p2 | 5 | 回合开始获得格挡/闪避+1信念（炽天使路径） |

### 光明祝福 (Light)

| 效果ID | DU | 说明 |
|--------|-----|------|
| add_1_blessing_of_light | 4 | 回合开始获得力量（3回合） |
| add_1_blessing_of_light_u | 5 | 回合开始75%力量或25%暴击（3回合） |
| add_1_blessing_of_light_p2 | 5 | 回合开始获得力量+1信念（炽天使路径） |

---

## 修女治疗 (Vestal Healing)

### 神圣恩典系列 (Divine Grace)

| 效果ID | DU | 说明 |
|--------|-----|------|
| ves_divine_grace_heal | 3.5 | 恢复20%生命（无信念） |
| ves_divine_grace_heal_u | 5 | 恢复30%生命（无信念，升级版） |
| ves_divine_grace_conviction_heal_2 | 5 | 恢复30%生命+5%暴击（2层信念） |
| ves_divine_grace_conviction_heal_2_u | 6 | 恢复40%生命+5%暴击（2层信念，升级） |
| ves_divine_grace_conviction_heal_3 | 6 | 恢复40%生命+5%暴击（3层信念） |
| ves_divine_grace_conviction_heal_3_u | 7.5 | 恢复50%生命+15%暴击（3层信念，升级） |

### 真言系列 (Mantra)

| 效果ID | DU | 说明 |
|--------|-----|------|
| ves_mantra_heal | 2 | 恢复10%生命（无信念） |
| ves_mantra_heal_u | 2 | 恢复10%生命（无信念，升级版） |
| ves_mantra_heal_2_conviction | 3.5 | 恢复20%生命（2层信念） |
| ves_mantra_heal_3_conviction | 5 | 恢复30%生命（3层信念） |
| ves_mantra_heal_conviction_u | 5 | 恢复30%生命（2+层信念，升级版） |
| ves_seraph_mantra_heal | 5 | 恢复30%生命（炽天使路径） |
| ves_seraph_mantra_heal_u | 7 | 恢复50%生命（炽天使路径升级） |

### 持续治疗 (HoT)

| 效果ID | DU | 说明 |
|--------|-----|------|
| hot_heal_small | 2 | 每回合恢复少量生命（HOT） |
| hot_heal_medium | 3.5 | 每回合恢复中量生命（HOT） |
| hot_heal_large | 5 | 每回合恢复大量生命（HOT） |

---

## 审判燃烧 (Judgement Burn)

| 效果ID | DU | 说明 |
|--------|-----|------|
| ves_judgement_burn | 3.5 | 施加中燃烧（3层信念） |
| ves_judgement_burn_u | 5 | 施加大燃烧（3层信念，升级版） |

---

## 抗性Buff (Resistance Buffs)

| 效果ID | DU | 说明 |
|--------|-----|------|
| ves_ministration_bleed_res_buff_e | 1.5 | 流血抗性+30%（3回合） |
| ves_ministration_blight_res_buff_e | 1.5 | 腐蚀抗性+30%（3回合） |
| ves_ministration_burn_res_buff_e | 1.5 | 燃烧抗性+30%（3回合） |
| ves_ministration_debuff_res_buff_e | 1.5 | 减益抗性+30%（3回合） |
| ves_ministration_stun_res_buff_e | 2 | 眩晕抗性+30%（3回合） |

---

## 状态移除 (Remove Effects)

### 祝福相关

| 效果ID | DU | 说明 |
|--------|-----|------|
| remove_all_blessings | 0.5 | 移除所有祝福 |

### 通用移除（修女使用）

| 效果ID | DU | 说明 |
|--------|-----|------|
| remove_all_dots | 2 | 移除所有DoT |
| remove_all_stun | 1 | 移除所有眩晕 |
| remove_all_stun_type_tokens | 1 | 移除眩晕类标记（眩晕、致盲等） |

---

## 标记销毁 (Token Destroy)

| 效果ID | DU | 说明 |
|--------|-----|------|
| destroy_1_positive_token | 0.5 | 销毁1个正面标记 |
| destroy_1_positive_token_30_pct | 0.15 | 30%几率销毁1个正面标记 |
| destroy_2_positive_token | 1 | 销毁2个正面标记 |
| destroy_3_positive_token | 1.5 | 销毁3个正面标记 |
| destroy_all_positive_tokens | 2 | 销毁所有正面标记 |

---

## 阈值触发治疗 (Threshold Healing)

### 压力治疗

| 效果ID | DU | 说明 |
|--------|-----|------|
| stress_heal_1_performer_at_threshold | 1 | 施法者阈值压力治疗1 |
| stress_heal_1_target_at_threshold | 1 | 目标阈值压力治疗1 |
| stress_heal_2_performer_at_threshold | 2 | 施法者阈值压力治疗2 |
| stress_heal_2_target_at_threshold | 2 | 目标阈值压力治疗2 |
| stress_heal_3_performer_at_threshold | 3 | 施法者阈值压力治疗3 |
| stress_heal_3_target_at_threshold | 3 | 目标阈值压力治疗3 |

### 生命治疗

| 效果ID | DU | 说明 |
|--------|-----|------|
| heal_20pct_self_threshold_med | 3.5 | 阈值触发自我治疗20% |
| heal_25pct_self_threshold_med | 4.5 | 阈值触发自我治疗25% |

---

## 技能DU计算示例

| 技能 | 效果 | 总DU |
|------|------|------|
| ves_divine_grace | 神圣恩典基础治疗(3.5) | **3.5** |
| ves_divine_grace (2层信念) | 神圣恩典2层治疗(5) | **5** |
| ves_divine_grace (3层信念) | 神圣恩典3层治疗(6) | **6** |
| ves_mantra | 真言基础治疗(2) | **2** |
| ves_judgement (3层信念) | 伤害 + 审判燃烧(3.5) | 伤害 + 3.5 |

---

*如需添加修女新效果，在此文档中定义*
