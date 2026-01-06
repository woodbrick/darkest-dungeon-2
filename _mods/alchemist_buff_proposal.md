# 炼金术士 (Alchemist) 强化方案

*参考 DU 评估体系：[available_effects.md](available_effects.md)*

---

## 1. 弱势技能评估

### 评估标准
- **DU 价值** < 7：弱势技能，需要增强
- **DU 价值** 7-10：可接受技能
- **DU 价值** > 10：优秀技能
- **升级版 (_u)**：期望 DU 为基础版的 **1.5倍**

### 当前技能 DU 评估

#### 基础技能
| 技能 | 伤害 | 可用位置 | 打击位置 | 效果列表 | 计算DU | 状态 |
|------|------|----------|----------|----------|---------|------|
| abm_howl | 2±1 | 1,2 | 1,2,3,4 | 拉近1 脆弱2 反击清除 暴击眩晕 压力1 | 12.5 | ✅ 优秀 |
| abm_howl_u | 3±2 | 1,2 | 1,2,3,4 | 拉近2 脆弱2 反击清除 暴击眩晕 压力1 | 15.5 | ✅ 优秀 |
| abm_rake | 4±2 | 1,2 | 1,2 | 压力1 | 2 | ❌ 弱势 |
| abm_rake_u | 4±3 | 1,2 | 1,2 | 连击暴击50% 压力1 | 5 | ❌ 弱势 |
| abm_rage | 6±3 | 1,2 | 1,2,3 | 压力1 | 4 | ❌ 弱势 |
| abm_rage_u | 7±3 | 1,2 | 1,2,3 | 移除格挡 移除护卫 压力1 | 17 | ✅ 优秀 |
| abm_slam | 4±3 | 2,3,4 | 1,2,3 | 击退1 眩晕1 前进1 压力1 | 7.5 | ⚠️ 可接受 |
| abm_slam_u | 6±2 | 2,3,4 | 1,2,3 | 击退1 眩晕1 前进1 闪避清除x2 压力1 | 10.5 | ✅ 优秀 |

#### 路径1技能 (连击爆发)
| 技能 | 伤害 | 可用位置 | 打击位置 | 效果列表 | 计算DU | 状态 |
|------|------|----------|----------|----------|---------|------|
| abm_howl_p1 | 1±1×目标(条件) | 2,3,4 | 1,2,3,4 | 脆弱1×目标 暴击连击 压力1×目标 腐蚀条件 | 4 | ⚠️ 可接受 |
| abm_howl_p1_u | 2±1×目标(条件) | 2,3,4 | 1,2,3,4 | 移除格挡x2 脆弱1×目标 暴击连击 压力1×目标 腐蚀条件 | 6 | ❌ 弱势 |
| abm_rake_p1 | 4±2 | 1,2 | 1,2 | 压力1 | 2 | ❌ 弱势 |
| abm_rake_p1_u | 4±3 | 1,2 | 1,2 | 连击暴击50% 压力1 | 5 | ❌ 弱势 |

#### 路径2技能 (反击生存)
| 技能 | 伤害价值 | 可用位置 | 打击位置 | 效果列表 | 总DU |
|------|----------|----------|----------|----------|-------|
| abm_howl_p2 | 6 | 1,2,3,4 | 2,3,4 | 流血条件 混乱移动 | 9 |
| abm_howl_p2_u | 12 | 1,2,3,4 | 2,3,4 | 混乱移动 压力治疗2 | 15 |
| abm_rake_p2 | 7 | 1,2 | 1,2 | 流血小 目标压力2 | 5 |
| abm_rake_p2_u | 9 | 1,2 | 1,2 | 流血小 目标压力2 | 7 |
| abm_rage_p2 | 7.5 | 1,2 | 1,2,3 | 压力治疗2 失败目标压力2 | 5.5 |
| abm_rage_p2_u | 9 | 1,2 | 1,2,3 | 压力治疗2 失败目标压力2 | 7 |

#### 路径3技能 (濒死爆发)
| 技能 | 伤害价值 | 可用位置 | 打击位置 | 效果列表 | 总DU |
|------|----------|----------|----------|----------|-------|
| abm_howl_p3 | 0 | 1,2,3,4 | 2,3,4 | 复制1标记到敌人 自我压力4 | -4 |
| abm_howl_p3_u | 0 | 1,2,3,4 | 2,3,4 | 偷取1标记到己方 自我压力4 | 1 |
| abm_rake_p3 | 4 | 1,2 | 1,2 | 压力治疗1 | 5 |
| abm_rake_p3_u | 4 | 1,2 | 1,2 | 压力治疗1 | 5 |
| abm_rage_p3 | 3 | 1,2 | 1,2,3 | 嘲讽 压力治疗2 | 8 |
| abm_rage_p3_u | 3.75 | 1,2 | 1,2,3 | 嘲讽 压力治疗2 | 8.75 |

### 变身技能 DU 评估

| 技能 | 当前DU | 队友压力代价 | 状态 |
|------|--------|-------------|------|
| abm_transform | -1.32 | -1.32 | ❌ 负收益 |
| abm_transform_u | -2 | -2 | ❌ 负收益 |
| abm_transform_p1 | -1.32 | -1.32 | ❌ 负收益 |
| abm_transform_p1_u | -1.32 | -1.32 | ❌ 负收益 |
| abm_transform_p2 | -3.5 | -3.5 | ❌ 严重负收益 |
| abm_transform_p2_u | -2 | -2 | ❌ 负收益 |
| abm_transform_p3 | +1.68 | -1.32 | ⚠️ 低收益 |
| abm_transform_p3_u | +1 | -2 | ⚠️ 低收益 |

### 弱势技能汇总

**优化策略**：最小改动，只加强弱势技能

**不修改的技能** (已优秀)：
- 基础：abm_howl (12.5), abm_howl_u (15.5), abm_rage_u (17), abm_slam_u (10.5)
- 路径1：abm_howl_p1_u (12)
- 路径2：abm_rage_p2 (7.5), abm_rage_p2_u (9.5)
- 路径3：abm_rage_p3_u (10.75)

**需要改进的技能** (DU < 7)：
1. **利爪系列** (4个) - 主要输出技能，伤害4太低
2. **路径1咆哮** (1个) - 1伤害+腐蚀条件，DU仅3
3. **路径2咆哮/利爪** (4个) - 伤害低+流血条件限制
4. **路径3咆哮/利爪** (4个) - 无伤害或濒死条件限制

**修改目标**：
- 基础版：DU 拉齐到 10+
- 升级版：DU 达到 15 (基础版1.5倍)

---

## 2. 机制流派设计

### 设计原则
1. **保留队友压力代价** - 角色核心特色
2. **增强变身收益** - 让代价有回报
3. **移除自我压力** - 野兽技能移除 stress_damage_1
4. **路径差异化** - 三个路径有明确定位

### 路径1：连击爆发流 (Combo Burst)

**核心理念**：高爆发伤害 + 闪避生存 + 连击配合

**变身收益**：
- 基础：+add_1_strength(3 DU)
- 升级：+add_2_strength(5 DU), +add_1_dodge(2 DU)
- 总收益：+3.68/+5.68 DU (净提升)

**技能配合**：
- abm_manacles：prime_combo(3) - 给敌人连击标记
- abm_rake_p1：伤害10 + combo_crit_50pct(3) = 13 DU
- abm_rake_p1_u：伤害11 + combo_crit_100pct(5) = 16 DU

**战斗流程**：
1. 变身 (获得力量+闪避)
2. 锁链 (prime_combo)
3. 利爪 (对连击标记高暴击高伤)
4. 解除变身 (免费治疗)

**定位**：快速战斗，2-3回合解决战斗

### 路径2：反击生存流 (Riposte Survival)

**核心理念**：反击输出 + 持续再生 + 长期作战

**变身收益**：
- 基础：+add_1_riposte(3), +hot_heal_medium(5) = +8 DU
- 升级：+add_1_riposte(3), +hot_heal_large(8) = +11 DU
- 总收益：+4.5/+9 DU (净提升)

**技能配合**：
- abm_rake_p2：伤害10 + skill_dot_small_bleed(2) - stress_damage_1(2) = 10 DU
- abm_rage_p2：伤害9 + stress_heal_2(2) - stress_damage_1(2) = 9 DU

**战斗流程**：
1. 变身 (获得反击+再生)
2. 利爪持续输出 (受击反击)
3. 靠再生保持血量
4. 适合长期战斗

**定位**：持久战，反击输出+持续治疗

### 路径3：濒死爆发流 (Berserk Threshold)

**核心理念**：腐蚀DoT + 阈值自愈 + 濒死爆发

**变身收益**：
- 基础：+add_1_strength(3), +heal_50pct_self_threshold_med(4) = +7 DU
- 升级：+add_2_strength(5), +heal_50pct_self_threshold_high(6) = +13 DU
- 总收益：+8.68/+14 DU (净提升)

**技能配合**：
- abm_rake_p3：伤害11×0.5 + stress_heal_1(1) = 6.5 DU
- abm_rage_p3：伤害7.5×0.5 + crit_chance(1) + add_1_taunt_nr(3) + stress_heal_2(2) = 9.75 DU

**战斗流程**：
1. 变身 (获得力量+阈值自愈)
2. 低血量时触发自愈
3. 利爪/狂怒濒死爆发
4. 腐蚀DoT持续伤害

**定位**：高风险高回报，濒死时最强

### 流派对比

| 维度 | 路径1 (连击爆发) | 路径2 (反击生存) | 路径3 (濒死爆发) |
|------|----------------|-----------------|-----------------|
| **变身DU收益** | +3.68/+5.68 | +4.5/+9 | +8.68/+14 |
| **队友压力** | -1.32 | -2至-3.5 | -1.32至-2 |
| **战斗节奏** | 快速(2-3回合) | 长期(4+回合) | 不定 |
| **核心机制** | 连击暴击 | 反击再生 | 濒死自愈 |
| **生存能力** | 闪避 | 反击+HOT | 阈值自愈 |
| **输出能力** | 爆发 | 稳定 | 濒死爆发 |

---

## 3. 技能改进列表

**设计原则**：用特殊效果替代纯伤害数值，增强游戏性

### 3.1 基础技能改进

| 技能 | 当前DU | 修改方案 | 修改后DU | 提升 |
|------|--------|----------|----------|------|
| abm_rake | 2 | +skill_small_bleed_dot(2), 移除压力1(2) | 6 | +4 |
| abm_rake_u | 5 | +skill_medium_bleed_dot(3.5), 移除压力1(2) | 10.5 | +5.5 |
| abm_rage | 4 | 移除压力1(2), +add_1_vulnerable(3) | 9 | +5 |
| abm_slam | 7.5 | 不修改 | 7.5 | 0 |

**修改效果说明**：
- **abm_rake**：添加流血小DoT (总伤害6)，移除自我压力
- **abm_rake_u**：流血中DoT (总伤害9)，升级版更强
- **abm_rage**：移除自我压力，给敌人脆弱标记（配合下次攻击）

**修改字段**：
- `abm_rake/rake_u`: `target_effects` (新增 skill_small_bleed_dot / skill_medium_bleed_dot)
- `abm_rake/rake_u`: `performer_after_target_effects` (移除 stress_damage_1)
- `abm_rage`: `performer_after_target_effects` (移除 stress_damage_1)
- `abm_rage`: `target_effects` (新增 add_1_vulnerable)

---

### 3.2 路径1技能改进 (连击爆发)

| 技能 | 当前DU | 修改方案 | 修改后DU | 提升 |
|------|--------|----------|----------|------|
| abm_howl_p1 | 4 | 轻微加强：压力伤害减半(×0.5) | 6 | +2 |
| abm_howl_p1_u | 6 | 移除压力1(2), 改为压力0.5×目标 | 8 | +2 |
| abm_rake_p1 | 2 | +combo_crit_50pct(3), 移除压力1(2) | 7 | +5 |
| abm_rake_p1_u | 5 | +combo_crit_100pct(5), 移除压力1(2) | 12 | +7 |

**修改效果说明**：
- **abm_howl_p1**：腐蚀条件限制实际命中，压力反冲减半提高可用性
- **abm_howl_p1_u**：移除自我压力，轻微提升群体价值
- **abm_rake_p1**：对连击标记高暴击，路径1核心输出

**修改字段**：
- `abm_howl_p1`: `performer_after_target_effects` (stress_damage_1 → stress_damage_1_50pct)
- `abm_howl_p1_u`: `performer_after_target_effects` (移除 stress_damage_1)
- `abm_rake_p1/p1_u`: `performer_buffs` (新增 combo_crit_50pct / combo_crit_100pct)
- `abm_rake_p1/p1_u`: `performer_after_target_effects` (移除 stress_damage_1)

---

### 3.3 路径2技能改进 (反击生存)

| 技能 | 当前DU | 修改方案 | 修改后DU | 提升 |
|------|--------|----------|----------|------|
| abm_howl_p2 | -1 | 移除压力1(2), 改压力治疗1(1) | 2 | +3 |
| abm_howl_p2_u | 0.5 | 移除压力1(2), +heal_hot_medium(5) | 5.5 | +5 |
| abm_rake_p2 | 3 | +skill_medium_bleed_dot(3.5), 移除压力1(2) | 8.5 | +5.5 |
| abm_rake_p2_u | 4 | +skill_large_bleed_dot(5), 移除压力1(2) | 11 | +7 |

**修改效果说明**：
- **abm_howl_p2**：移除负面压力，改为压力治疗
- **abm_howl_p2_u**：添加持续治疗HOT，每回合回复3点
- **abm_rake_p2**：流血DoT增强 (总伤害9)，配合反击持续输出

**修改字段**：
- `abm_howl_p2/p2_u`: `performer_after_target_effects` (stress_damage_1 → stress_heal_1)
- `abm_howl_p2_u`: `performer_buffs` (新增 heal_hot_medium)
- `abm_rake_p2/p2_u`: `target_effects` (skill_small_bleed_dot → skill_medium_bleed_dot / skill_large_bleed_dot)
- `abm_rake_p2/p2_u`: `performer_after_target_effects` (移除 stress_damage_1)

---

### 3.4 路径3技能改进 (濒死爆发)

| 技能 | 当前DU | 修改方案 | 修改后DU | 提升 |
|------|--------|----------|----------|------|
| abm_howl_p3 | -4 | 移除复制标记(改为无), 压力4→压力1, +steal_1_pos_copy_steal_tag_tokens(5) | 6 | +10 |
| abm_howl_p3_u | 1 | 压力4→压力2, +add_1_vulnerable(3)×2目标 | 7 | +6 |
| abm_rake_p3 | 5 | +add_1_strength(3), 移除压力1(2) | 10 | +5 |
| abm_rake_p3_u | 5 | +add_2_strength(5), 移除压力1(2) | 12 | +7 |

**修改效果说明**：
- **abm_howl_p3**：移除负面复制标记效果(给敌人标记)，改为偷取1标记，减弱压力代价(4→1)
- **abm_howl_p3_u**：保留偷取标记机制，减弱压力代价(4→2)，给2目标脆弱1层
- **abm_rake_p3**：濒死时获得力量1，爆发伤害
- **abm_rake_p3_u**：濒死时获得力量2，升级版更强

**修改字段**：
- `abm_howl_p3`: `target_effects` (移除 copy_1_pos_copy_steal_tag_tokens，新增 steal_1_pos_copy_steal_tag_tokens)
- `abm_howl_p3`: `performer_effects` (stress_damage_4 → stress_damage_1)
- `abm_howl_p3_u`: `performer_effects` (stress_damage_4 → stress_damage_2)
- `abm_howl_p3_u`: `target_effects` (新增 add_1_vulnerable ×2)
- `abm_rake_p3/p3_u`: `performer_buffs` (新增 add_1_strength / add_2_strength)
- `abm_rake_p3/p3_u`: `performer_after_target_effects` (移除 stress_damage_1)

---

## 4. 修改汇总

### 修改文件
`dlc_catacombs/hero_abm_data_export.Group.csv`

### 修改技能总数
- **基础技能**：3个 (rake系列, rage基础版)
- **路径1技能**：3个 (howl_p1, rake_p1系列)
- **路径2技能**：4个 (howl_p2系列, rake_p2系列)
- **路径3技能**：4个 (howl_p3系列, rake_p3系列)
- **合计**：14个技能

### 不修改的技能 (已优秀)
- abm_howl / abm_howl_u (12.5 / 15.5)
- abm_rage_u (17)
- abm_slam / abm_slam_u (7.5 / 10.5)
- abm_rage_p2 / abm_rage_p2_u (7.5 / 9.5)
- abm_rage_p3_u (10.75)
- 所有变身技能 (已可接受)
- 所有人类形态技能

### 预期效果

**利爪系列** (主要输出技能)：
- 添加流血DoT (总伤害6-9)，移除自我压力
- DU 从 2/5 → 6/10.5
- 升级版流血更强，持续输出

**狂怒基础版**：
- 移除自我压力，添加脆弱标记
- DU 从 4 → 9
- 为下次攻击铺垫，战术价值提升

**路径1 (连击爆发)**：
- 咆哮P1：压力反冲减半，提高群体可用性
- 咆哮P1_U：移除自我压力，轻微提升
- 利爪对连击标记高暴击
- DU 咆哮从 4/6 → 6/8，利爪从 2/5 → 7/12

**路径2 (反击生存)**：
- 咆哮改为压力治疗/持续回血
- 利爪流血DoT增强 (总伤害9-12)
- DU 从 3/4 → 8.5/11，反击续航提升

**路径3 (濒死爆发)**：
- 咆哮P3：移除负面复制标记效果，改为偷取1标记，减弱压力代价(4→1)
- 咆哮P3_U：保留偷取标记机制，减弱压力代价(4→2)，给2目标脆弱
- 利爪获得力量，移除自我压力，濒死爆发
- DU 咆哮从 -4/1 → 6/7，利爪从 5/5 → 10/12

---

## 5. 效果参考

所有DU价值评估基于 [available_effects.md](available_effects.md)，包括：
所有DU价值评估基于 [available_effects.md](available_effects.md)，包括：

### 增益效果 (add_*)
- add_1_strength: +3 DU
- add_2_strength: +5 DU
- add_1_dodge: +2 DU
- add_1_riposte: +3 DU

### 治疗效果 (heal_*)
- hot_heal_medium: +5 DU
- hot_heal_large: +8 DU
- heal_50pct_self_threshold_med: +4 DU
- heal_50pct_self_threshold_high: +6 DU

### 压力效果 (stress_*)
- stress_damage_1: -2 DU
- stress_damage_2: -4 DU
- stress_damage_4: -8 DU
- stress_heal_1: +1 DU
- stress_heal_2: +2 DU

### 移除效果 (remove_all_*)
- remove_all_block: +6 DU
- remove_all_guard: +6 DU
- remove_all_riposte: +6 DU

### 连击系统 (combo)
- prime_combo: +3 DU
- combo_crit_50pct: +3 DU
- combo_crit_100pct: +5 DU

### 移动效果 (move_*)
- move_pull_1: +1.5 DU
- move_pull_2: +2.5 DU

### DoT效果
- skill_small_bleed_dot: +2 DU
- skill_medium_bleed_dot: +3.5 DU
- skill_large_bleed_dot: +5 DU

### 标记操作效果
- copy_1_pos_copy_steal_tag_tokens: -4 DU (复制己方1个标记到敌人，负面效果)
- steal_1_pos_copy_steal_tag_tokens: +5 DU (偷取敌人1个标记，双重收益)
- steal_all_pos_copy_steal_tag_tokens: +12 DU (偷取所有标记，极高控制价值)
