# 赏金猎人技能重设计方案 - 游玩乐趣导向

## 1. 核心问题诊断

### 1.1 当前设计问题

| 问题类型 | 具体表现 | 影响乐趣 |
|---------|---------|---------|
| **连击体系断裂** | prime_combo启动后，连击技能收益低，终结技缺乏爆发 | 连击无爽快感 |
| **主题不突出** | "赏金猎人"缺乏追踪、猎杀的独特机制 | 缺乏角色代入感 |
| **技能孤立** | 保镖、控制、输出技能各自为战 | 缺乏配合深度 |
| **数值平庸** | 多数技能DU 5-8，缺乏高低差 | 选择困难且无亮点 |
| **战术单一** | 唯一最优解：标记→过来→收人 | 缺乏流派多样性 |

### 1.2 应该有的游玩体验

**核心幻想**：我是赏金猎人，追踪目标 → 设置陷阱 → 猎杀终结

**理想连击体验**：
```
标记目标（prime） → 连击压制（combo） → 爆发终结（end）
    ↓              ↓                 ↓
  锁定猎物      多次打击增强      斩杀或控制
```

**战术流派**：
- **猎杀流**：高爆发单点伤害
- **控制流**：眩晕+位移+破坏防御
- **陷阱流**：流血+持续压制
- **保镖流**：团队保护+反击

---

## 2. 重新设计框架

### 2.1 连击体系重构

#### 问题现状
- prime_combo技能DU 8-10，缺乏吸引力
- 中间连击技能缺失，直接跳到end_combo
- end_combo技能DU 5-7，终结感弱

#### 优化方案

**方案A：三层连击体系**
```
启动技（prime） → 增益技（combo） → 终结技（end）
   DU 10-12      DU 8-10      DU 12-15
```

**方案B：终结技爆发化**
- end_combo技能获得"对连击目标+50%伤害"
- 或添加"若目标连击状态，额外效果"

**方案C：标记-猎杀机制**
- mark_for_death添加"被标记目标受到的所有伤害+25%"
- 终结技对标记目标额外伤害

### 2.2 技能定位重组

#### 当前11个技能分类

| 类型 | 技能 | 问题 |
|------|------|------|
| **启动** | mark_for_death | DU 10可接受，但缺乏后续配合 |
| **连击** | collect_bounty, come_hither, uppercut, flashbang, finish_him, caltrops, hurlbat | DU 5-8，定位模糊 |
| **终结** | 所有end_combo技能 | 缺乏爆发感 |
| **控制** | staredown, no_escape | DU 5.5-9，功能单一 |
| **辅助** | bodyguard | DU 9.5，孤立无联动 |

#### 重组方案

**核心连击链（3-4个技能）**：
1. **mark_for_death**（启动）：标记脆弱+连击
2. **come_hither/uppercut**（压制）：拉拽/眩晕+连击加成
3. **finish_him/hurlbat**（终结）：破防+高伤害

**功能副技能（2-3个技能）**：
- **flashbang**：群体控制+连击
- **no_escape**：破护卫+锁定后排
- **caltrops**：流血陷阱

**特殊技（1个）**：
- **bodyguard**：团队保护（保留）

---

## 3. 技能重设计方案

### 3.1 连击核心链

#### mark_for_death（死亡标记）- 连击启动器
**定位**：锁定猎物，为后续连击提供增益

**方案A：标记增强**
```yaml
修改：
target_effects:
  - prime_combo (DU 3)
  - add_2_vulnerable → add_3_vulnerable (DU 7)
  - 新增：mark_target (被标记者受击+25%持续2回合) (DU 3)

预期DU：3 + 7 + 3 = 13
```

**方案B：连击计数器**
```yaml
修改：
target_effects:
  - prime_combo (DU 3)
  - add_2_vulnerable (DU 5)
  - 新增：combo_counter (连击次数+1) (DU 2)
performer_effects:
  - 新增：if_combo_counter_3_add_2_strength (DU 3)

预期DU：3 + 5 + 2 + 3 = 13
```

**推荐**：方案A更简单直接，符合"标记"主题

---

#### come_hither（过来）- 连击压制
**定位**：将目标拉到前排，配合近战终结技

**方案A：伤害+拉拽**
```yaml
修改：
伤害：3-2 → 5-3 (平均4)
target_effects:
  - prime_combo (DU 3)
  - move_pull_2 (DU 2.5)
  - 新增：if_target_pulled_add_1_vulnerable (DU 2)

预期DU：4 + 3 + 2.5 + 2 = 11.5
```

**方案B：连击增益**
```yaml
修改：
伤害：3-2 → 4-3 (平均3.5)
target_effects:
  - prime_combo (DU 3)
  - move_pull_2 (DU 2.5)
  - 新增：combo_extend (延长连击1回合) (DU 2)

预期DU：3.5 + 3 + 2.5 + 2 = 11
```

**推荐**：方案A更爽快，拉过来+脆弱，配合终结技

---

#### finish_him（终结他）- 连击终结
**定位**：爆发性伤害，破格挡斩杀

**方案A：破防爆发**
```yaml
修改：
伤害：6-4 → 10-6 (平均8)
target_effects:
  - ignored_token_remove_1_block_plus (DU 0.5)
  - ignored_token_remove_1_block (DU 0.5)
  - 新增：if_target_vulnerable_2_crit_damage_50pct (DU 3)
  - end_combo (DU 0)

预期DU：8 + 0.5 + 0.5 + 3 = 12
```

**方案B：斩杀机制**
```yaml
修改：
伤害：6-4 → 8-5 (平均6.5)
target_effects:
  - ignored_token_remove_1_block_plus (DU 0.5)
  - ignored_token_remove_1_block (DU 0.5)
  - 新增：if_target_hp_below_30pct_damage_200pct (DU 5)
  - end_combo (DU 0)

预期DU：6.5 + 0.5 + 0.5 + 5 = 12.5
```

**推荐**：方案A更稳定，对脆弱目标暴击伤害

---

### 3.2 功能副技能

#### flashbang（闪光弹）- 群体控制
**定位**：前排多目标控制+连击过渡

**方案A：增强控制**
```yaml
修改：
target_effects:
  - add_1_blind (DU 4)
  - add_1_daze (DU 2.5)
  - combo_add_1_stun (DU 4)
  - move_shuffle (DU 1.5)
  - 新增：if_blinded_target_add_1_weak (DU 1.5)
  - end_combo (DU 0)

预期DU：4 + 2.5 + 4 + 1.5 + 1.5 = 13.5
```

**方案B：控制链**
```yaml
修改：
target_effects:
  - add_1_blind (DU 4)
  - add_1_daze (DU 2.5)
  - combo_add_1_stun (DU 4)
  - 新增：move_shuffle_and_add_1_daze_to_others (DU 3)
  - end_combo (DU 0)

预期DU：4 + 2.5 + 4 + 3 = 13.5
```

**推荐**：方案A，致盲目标额外虚弱

---

#### no_escape（无处可逃）- 后排控制
**定位**：破护卫锁定后排

**方案A：伤害增强**
```yaml
修改：
伤害：2-2 → 4-3 (平均3.5)
target_effects:
  - add_1_stun (DU 4)
  - prime_combo (DU 3)
  - remove_all_guard (DU 2)
  - ignored_token_remove_1_dodge_plus (DU 2)
  - ignored_token_remove_1_dodge (DU 1.5)
  - ignored_token_remove_1_guard (DU 0.5)

预期DU：3.5 + 4 + 3 + 2 + 2 + 1.5 + 0.5 = 16.5
```

**推荐**：简单提升伤害，功能已完备

---

#### caltrops（铁蒺藜）- 陷阱技能
**定位**：流血陷阱+连击过渡

**方案A：陷阱增强**
```yaml
修改：
伤害：2-1 → 3-2 (平均2.5)
target_effects:
  - skill_dot_medium_bleed → skill_dot_large_bleed (DU 5)
  - 新增：if_target_moves_take_2_damage (DU 2)
  - 新增：add_1_immobilize (DU 3)
  - end_combo (DU 0)

预期DU：2.5 + 5 + 2 + 3 = 12.5
```

**方案B：流血扩散**
```yaml
修改：
伤害：2-1 → 2-1 (平均1.5)
target_effects:
  - skill_dot_medium_bleed (DU 3.5)
  - 新增：spread_bleed_to_adjacent (DU 3)
  - 新增：combo_add_1_bleed (DU 2)
  - end_combo (DU 0)

预期DU：1.5 + 3.5 + 3 + 2 = 10
```

**推荐**：方案A，陷阱感更强，定身+移动伤害

---

#### hurlbat（投掷战斧）- 远程破防
**定位**：远程破闪避+伤害

**方案A：破闪避增强**
```yaml
修改：
伤害：6-4 → 9-6 (平均7.5)
target_effects:
  - end_combo_if_target_has_dodge
  - ignored_token_remove_1_dodge_plus_if_target_combo (DU 2)
  - ignored_token_remove_1_dodge_if_target_combo (DU 1.5)

预期DU：7.5 + 2 + 1.5 = 11
```

**推荐**：大幅提升伤害，符合"投掷重武器"感

---

### 3.3 特殊技能

#### staredown（怒视）- 嘲讽控制
**定位**：前排控制+自我保护

**方案A：嘲讽增强**
```yaml
修改：
target_effects:
  - add_2_weak → add_3_weak (DU 3.5)
performer_effects:
  - add_2_taunt_nr (DU 3)
  - 新增：add_1_block (DU 2.5)

预期DU：3.5 + 3 + 2.5 = 9
```

**推荐**：添加自我格挡，提高生存

---

#### collect_bounty（收人悬赏）- 基础攻击
**定位**：简单伤害技能

**方案A：标记加成**
```yaml
修改：
伤害：8-4 → 10-6 (平均8)
target_effects:
  - 新增：if_target_vulnerable_damage_50pct (DU 2)
  - end_combo (DU 0)

预期DU：8 + 2 = 10
```

**推荐**：对脆弱目标额外伤害，符合"收人"主题

---

#### uppercut（上勾拳）- 近战控制
**定位**：前排眩晕+位移

**方案A：伤害增强**
```yaml
修改：
伤害：3-2 → 5-3 (平均4)
target_effects:
  - add_1_stun (DU 4)
  - move_knockback_1 (DU 1.5)

预期DU：4 + 4 + 1.5 = 9.5
```

**推荐**：提升伤害，保持控制功能

---

#### bodyguard（保镖）- 团队保护
**定位**：团队辅助（已完善）

**保持现状**
- DU 9.5已达标
- 功能独特，无需修改

---

## 4. 战术流派设计

### 4.1 猎杀流（单点爆发）

**核心技能**：mark_for_death → come_hither → finish_him

**连击体验**：
```
回合1：mark_for_death（标记脆弱+连击）
回合2：come_hither（拉拽+脆弱+连击）
回合3：finish_him（破格挡+对脆弱目标暴击）
```

**预期伤害**：
- 标记：脆弱3（目标受击+150%）
- 拉拽：伤害4 + 脆弱2
- 终结：伤害8 + 50%暴击 + 目标受击+150%
- 总等效DU：13 + 11.5 + 12 = 36.5

**玩法特点**：
- ✅ 爽快的单体爆发
- ✅ 明确的连击节奏
- ✅ 符合"赏金猎人"主题

---

### 4.2 控制流（群体压制）

**核心技能**：mark_for_death → flashbang → no_escape

**连击体验**：
```
回合1：mark_for_death（标记脆弱）
回合2：flashbang（致盲+眩晕+虚弱）
回合3：no_escape（破护卫+眩晕后排）
```

**玩法特点**：
- ✅ 多目标控制
- ✅ 破防御体系
- ✅ 团队贡献高

---

### 4.3 陷阱流（持续伤害）

**核心技能**：mark_for_death → caltrops → hurlbat

**连击体验**：
```
回合1：mark_for_death（标记）
回合2：caltrops（大流血+定身）
回合3：hurlbat（破闪避+高伤害）
```

**玩法特点**：
- ✅ 持续压制
- ✅ 限制敌人行动
- ✅ 后期爆发

---

## 5. 预期效果

### 5.1 DU分布改进

| 技能 | 当前DU | 新DU | 提升 |
|------|--------|------|------|
| mark_for_death | 10 | 13 | +3 |
| come_hither | 8 | 11.5 | +3.5 |
| finish_him | 6 | 12 | +6 |
| flashbang | 10.5 | 13.5 | +3 |
| no_escape | 9 | 16.5 | +7.5 |
| caltrops | 5 | 12.5 | +7.5 |
| hurlbat | 5 | 11 | +6 |
| staredown | 5.5 | 9 | +3.5 |
| collect_bounty | 6 | 10 | +4 |
| uppercut | 8 | 9.5 | +1.5 |
| bodyguard | 9.5 | 9.5 | 0 |

**整体分布**：
- 优秀 (DU≥14)：2/11 (18%)
- 可接受 (DU 9-13)：9/11 (82%)
- 弱势 (DU<9)：0/11 (0%)

---

### 5.2 游玩乐趣提升

| 维度 | 改进前 | 改进后 |
|------|--------|--------|
| **连击爽快感** | 弱（伤害低） | 强（爆发高） |
| **主题代入** | 模糊 | 明确（追踪-猎杀） |
| **战术深度** | 单一 | 多流派 |
| **技能配合** | 少 | 多 |
| **选择乐趣** | 困难 | 明确定位 |

---

## 6. 实施计划

### 6.1 第一阶段：核心连击链（优先）

1. **mark_for_death**：添加mark_target效果
2. **come_hither**：提升伤害+添加脆弱
3. **finish_him**：大幅提升伤害+对脆弱目标暴击

### 6.2 第二阶段：功能技能

4. **no_escape**：提升伤害
5. **caltrops**：大流血+定身+移动伤害
6. **hurlbat**：大幅提升伤害

### 6.3 第三阶段：辅助技能

7. **flashbang**：添加虚弱效果
8. **staredown**：添加自我格挡
9. **collect_bounty**：对脆弱目标额外伤害
10. **uppercut**：提升伤害

---

## 7. 风险评估

### 7.1 可能过强的技能

| 技能 | 风险 | 缓解措施 |
|------|------|---------|
| no_escape (DU 16.5) | 过高 | 降低伤害至3-2 (DU 15.5) |
| finish_him (DU 12) | 爆发过高 | 移除暴击加成，纯伤害提升 |
| caltrops (DU 12.5) | 控制过强 | 移除定身，保留流血+移动伤害 |

### 7.2 实施建议

1. **分步实施**：先实施核心连击链，测试平衡性
2. **数值微调**：根据实战数据调整伤害
3. **保留原版**：备份原始数据，可随时回退

---

## 8. 与原方案对比

| 维度 | 原方案 | 新方案 |
|------|--------|--------|
| **设计理念** | 数值平衡 | 游玩乐趣 |
| **修改幅度** | 小幅提升伤害 | 机制重构 |
| **连击体系** | 保持现状 | 三层连击链 |
| **主题突出** | 无 | 追踪-猎杀 |
| **战术流派** | 单一 | 多样 |
| **DU提升** | +1~3 | +3~7.5 |
| **实施难度** | 低 | 中 |

---

## 9. 总结

### 核心改进点

1. **连击体系化**：启动→压制→终结，清晰节奏
2. **标记机制**：mark_for_death成为核心，后续技能配合
3. **爆发提升**：终结技DU 5-7 → 12+
4. **流派多样**：猎杀/控制/陷阱三流派
5. **主题突出**：追踪目标→设置陷阱→猎杀终结

### 预期游玩体验

**作为赏金猎人**：
1. 标记目标（锁定猎物）
2. 拉拽过来/眩晕（控制）
3. 爆发终结（赏金到手）

**爽快感来源**：
- 明确的目标（被标记的敌人）
- 逐步压制（脆弱→眩晕→破防）
- 爆发终结（高伤害斩杀）

---

*2026-01-09*
*设计理念：游玩乐趣 > 数值平衡*
*核心目标：让赏金猎人玩起来像赏金猎人*
