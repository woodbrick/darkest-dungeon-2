# 缺失效果调研清单

> 本文档记录两类缺失问题：
> 1. **效果DU定义缺失** - `effects_du.yml` 中未定义的效果
> 2. **效果字段遗漏** - 调研时遗漏的CSV字段

---

## 第一部分：效果字段遗漏（新增）

### 易遗漏字段清单

| 字段名 | 用途 | 典型案例 | 影响 |
|--------|------|----------|------|
| `performer_after_target_effects` | 施放者后续效果 | hel_adrenaline_rush: 移除疲惫、攻击治疗buff | DU低估1-2 |
| `performer_team_others_effects` | 队友效果 | hel_raucous_revelry: 队友压力治疗 | DU低估0.25-1 |
| `target_buffs` | 目标buff标记 | 连击相关buff | DU完全忽略 |
| `performer_buffs` | 施放者buff标记 | 路径专属buff | DU完全忽略 |
| **群攻倍率** | 多目标效果计算 | hel_barbaric_yawp: 群攻×2 | DU低估50%+ |

### 已发现字段遗漏案例

#### hel_adrenaline_rush (地狱犬)
- **遗漏字段**: `performer_after_target_effects`
- **遗漏效果**:
  - `remove_all_winded` (0.5 DU)
  - `hellion_adrenaline_heal_hit_buff_e` (0.5 DU)
- **影响**: DU 3.0 → 5.0 (+66%)
- **日期**: 2026-01-07
- **教训**: 必须检查所有 `*_effects` 字段，不仅仅是 `target_effects` 和 `performer_effects`

#### hel_raucous_revelry / hel_raucous_revelry_u (地狱犬)
- **遗漏字段**: `performer_team_others_effects`
- **遗漏效果**:
  - `stress_heal_1_target_at_threshold` (0.25 DU/人)
- **影响**: DU 0.5 → 6.25/8.0 (+1150%/+1500%)
- **日期**: 2026-01-07
- **教训**: 团队技能必须检查 `performer_team_others_effects`

#### hel_barbaric_yawp / hel_barbaric_yawp_u (地狱犬)
- **遗漏问题**: 群攻倍率未应用
- **错误计算**: add_1_weak(2 DU) + remove_all_stealth(0.5 DU) = 2.5 DU
- **正确计算**: add_1_weak(2 DU × 2) + remove_all_stealth(0.5 DU × 2) = 5 DU
- **影响**: DU 1.05/6.1 → 4.5/9.5 (+329%/+56%)
- **日期**: 2026-01-07
- **教训**: 群攻技能(m_IsMultiHit:True)的效果DU必须×目标数量

### 效果字段检查清单（DU计算前必做）

```
□ 读取完整技能块 (element_start 到 element_end)
□ 检查 m_IsMultiHit 或 target_ranks 确认目标数量 ⚠️ 群攻倍率
□ 检查 target_effects
□ 检查 performer_effects
□ 检查 performer_after_target_effects ⚠️ 高风险
□ 检查 performer_team_others_effects ⚠️ 高风险
□ 检查 target_buffs
□ 检查 performer_buffs
□ 验证 DU < 5 的技能（必然有疏漏）
□ 计算总 DU 并对比阈值
```

### 调研铁律（更新版）

**DU < 5 的技能必然存在效果疏漏**

必须检查的6个字段（按优先级）:
1. `target_effects` - 目标效果
2. `performer_effects` - 施放者效果
3. `performer_after_target_effects` - **施放者后续效果** ⚠️ 易遗漏
4. `performer_team_others_effects` - **队友效果** ⚠️ 易遗漏
5. `target_buffs` - 目标buff
6. `performer_buffs` - 施放者buff

**群攻倍率规则**：
- 群攻技能的效果DU需×目标数量
- 检查 `m_IsMultiHit: True` 或 `target_ranks` 确认目标数量
- 案例：hel_barbaric_yawp (target_ranks=1,2)
  - 错误计算：add_1_weak(2 DU) + remove_all_stealth(0.5 DU) = 2.5 DU
  - 正确计算：add_1_weak(2 DU × 2) + remove_all_stealth(0.5 DU × 2) = 5 DU

---

## 第二部分：效果DU定义缺失

## 统计

- **已覆盖**: 29 个标准效果
- **缺失**: 15 个效果
- **覆盖率**: 66%

---

## 缺失效果列表

### 1. 条件治疗类 (5个)

| 效果ID | 描述 | 类型 | 优先级 |
|--------|------|------|--------|
| `stress_heal_1_target_at_threshold` | 阈值触发: 目标压力治疗1 | 条件触发 | 高 |
| `stress_heal_2_performer_at_threshold` | 阈值触发: 施法者压力治疗2 | 条件触发 | 高 |
| `stress_heal_3_performer_at_threshold` | 阈值触发: 施法者压力治疗3 | 条件触发 | 高 |
| `heal_20pct_self_threshold_med` | 阈值触发: 自我治疗20% | 条件触发 | 高 |
| `heal_25pct_self_threshold_med` | 阈值触发: 自我治疗25% | 条件触发 | 高 |

**调研要点**:
- 阈值条件是什么? (生命值百分比? 压力值?)
- 触发概率如何?
- 是否有冷却限制?

---

### 2. 路径专属Buff (2个)

| 效果ID | 描述 | 英雄 | 路径 | 优先级 |
|--------|------|------|------|--------|
| `path_buff_hel_ravager_bleed_chance_down` | 暴食者路径: 流血几率降低 | Hellion | Ravager (P1) | 中 |
| `path_buff_hel_berserker_bleed_chance_up` | 狂战士路径: 流血几率提升 | Hellion | Berserker (P2) | 中 |

**调研要点**:
- 具体的流血几率变化数值
- 是否影响抗性还是触发率
- 是否仅对特定技能生效?

---

### 3. 英雄专属效果 (8个)

#### 3.1 肾上腺素激增相关 (3个)

| 效果ID | 描述 | 来源技能 | 优先级 |
|--------|------|----------|--------|
| `hellion_adrenaline_heal_hit_buff_e` | 肾上腺素击中治疗buff | hel_adrenaline_rush | 高 |
| `hellion_damage_buff_remover` | 伤害buff移除器 | hellion被动 | 高 |
| `deathblow_chance_shaping_heroes_e` | 濒死抗性通用buff | 所有英雄 | 中 |

#### 3.2 嗜血相关 (4个)

| 效果ID | 描述 | 来源技能 | 优先级 |
|--------|------|----------|--------|
| `hellion_bloodlust_damage_buff_e` | 嗜血伤害buff | hel_bloodlust | 高 |
| `hellion_bloodlust_u_damage_buff_e` | 嗜血伤害buff(升级) | hel_bloodlust_u | 高 |
| `hel_bloodlust_remove_execution` | 嗜血处决移除标记 | hel_bloodlust_u | 高 |
| `hel_bloodlust_execution_buff_e` | 嗜血处决buff | hel_bloodlust_u | 高 |

#### 3.3 狂欢相关 (1个)

| 效果ID | 描述 | 来源技能 | 优先级 |
|--------|------|----------|--------|
| `hellion_revelry_deathblow_resist_e` | 狂欢濒死抗性buff | hel_raucous_revelry_u | 中 |

**调研要点**:
- 查找 `effect_data_export.Group.csv` 中的完整定义
- 确认buff的具体数值和持续时间
- 确认触发条件 (如肾上腺素的击中治疗是每次攻击触发?)

---

## 调研方法

### 方法1: 搜索effect_data_export.Group.csv

```bash
# 在游戏根目录的CSV文件中搜索
grep -n "effect_id,hellion_adrenaline_heal_hit_buff_e" effect_data_export.Group.csv
```

### 方法2: 使用game-mechanics-researcher代理

```
调用 game-mechanics-researcher 代理
任务: 调研Hellion专属效果的完整数据
范围: effect_data_export.Group.csv
输出: 效果名称、描述、DU价值评估
```

### 方法3: 参考已有技能推断

通过技能的上下文效果推断DU价值:
- `hellion_adrenaline_heal_hit_buff_e` 出现在 `hel_adrenaline_rush` 技能
- 该技能已有 `heal_percent_small` (DU=3.5)
- 可推断buff的DU约为 1-2

---

## 补充流程

1. **调研** → 使用上述方法获取效果数据
2. **评估** → 确定DU价值
3. **补充** → 添加到 `rules/effects_du.yml`
4. **验证** → 运行 `parse_universal.py hel` 确认无缺失

---

## 待补充格式示例

```yaml
# 在 effects_du.yml 中添加

stress_heal_1_target_at_threshold:
  name: 阈值压力治疗1
  desc: 条件触发时减少目标1点压力
  file: effect_data_export.Group.csv
  line: TBD
  du: 1.5  # 待评估

hellion_adrenaline_heal_hit_buff_e:
  name: 肾上腺素击中治疗buff
  desc: 攻击命中后触发治疗
  file: effect_data_export.Group.csv
  line: TBD
  du: 2  # 待评估
```

---

*最后更新: 2026-01-07*
*来源: hero_hel_data_export.Group.csv 分析*
