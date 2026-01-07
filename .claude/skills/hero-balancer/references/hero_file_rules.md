# 暗黑地牢2 英雄文件规则说明

## 一、文件结构

### 1.1 CSV格式
- **路径**: `hero_{英雄代码}_data_export.Group.csv`
- **编码**: UTF-8
- **结构**: `element_start,{ID},{类型}` → `{字段},{值}...` → `element_end`

### 1.2 元素类型

#### ActorDataStats - 属性数据
定义英雄或技能的基础属性
- `add_stats` - 属性值列表
- `key_map` - 属性键映射

#### ActorDataSkill - 技能数据
定义技能的基本信息
- `m_IsFriendly` - 是否友方技能 (True/False)
- `launch_ranks` - 施放位置 (如: 1,2 表示从位置1或2施放)
- `target_ranks` - 目标位置 (如: 1,2,3,4 表示可攻击所有位置)
- `m_IsMultiHit` - 是否群体攻击 (True=群体, False=单体)
- `m_Cooldown` - 冷却回合数
- `m_CanBeRiposted` - 可被反击 (True/False)
- `m_Tags` - 技能标签

#### ActorDataEffects - 效果数据
定义技能的效果
- `performer_effects` - 施放者自身效果
- `target_effects` - 目标效果
- `performer_after_target_effects` - 攻击后施放者效果
- `on_hit_as_performer_to_performer_effects` - 命中时施放者获得效果
- `on_crit_as_performer_to_target_effects` - 暴击时目标效果

---

## 二、伤害计算

### 2.1 计算公式
**CSV格式**: `add_stats,基础值,随机值`
**实际伤害**: 基础值 ~ (基础值 + 随机值)

| CSV | 实际伤害 | 平均 |
|-----|---------|------|
| `5,5` | 5-10 | 7.5 |
| `8,8` | 8-16 | 12 |
| `3,3,2` | 3-10 (带修正) | 6.5 |

**注意**: 第三位数值是额外修正值，直接加到最大伤害上

### 2.2 伤害属性配置
```csv
key_map,health_damage,health_damage_range,crit_chance
add_stats,3,3,0.05
```
- 第1位: 基础伤害值 (如: 3)
- 第2位: 随机伤害值 (如: 3) → 实际伤害 3-6
- 第3位: 暴击概率 (如: 0.05 = 5%)

### 2.3 多段攻击
每次独立计算伤害，如 `3-3` ×2次 = 每次3-6，总计 6-12

---

## 三、目标与群体

### 3.1 位置编号
```
前排: 位置1, 位置2
后排: 位置3, 位置4
```

### 3.2 launch_ranks (施放位置)
- `1,2` - 可从位置1或2施放
- `1,2,3,4` - 可从任何位置施放

### 3.3 target_ranks (目标位置)
- `1` - 只攻击位置1
- `1,2` - 攻击位置1或2
- `1,2,3,4` - 攻击所有位置

### 3.4 m_TargetRelativeRanks (相对位置)
- `-1,0,1` - 相对施放位置的偏移
- 用于友方技能或特殊技能

### 3.5 m_IsMultiHit 属性
| 值 | 含义 |
|---|------|
| False | 单体攻击，逐个选择目标 |
| True | 群体攻击，一次性对所有目标生效 |

**群体技能示例**:
```csv
m_IsMultiHit,True
target_ranks,1,2,3,4
```
一次性对4个位置的所有敌人造成伤害和效果，每个目标独立计算

---

## 四、常用效果标记

### 4.1 增益效果
- `add_1_strength` / `add_2_strength` - 添加1/2层力量
- `add_1_block` / `add_2_block` / `add_3_block` - 添加1/2/3层格挡
- `add_1_guard` / `add_2_guard` / `add_3_guard` - 添加1/2/3层护卫
- `add_1_riposte` - 添加反击，受击时反击
- `add_1_crit` / `add_2_crit` - 添加暴击标记，下次攻击必定暴击
- `add_1_crit_80pct` - 添加暴击标记，80%概率下次攻击暴击

### 4.2 减益效果
- `add_1_vulnerable` / `add_2_vulnerable` - 添加1/2层脆弱
- `add_1_weak` / `add_2_weak` - 添加1/2层虚弱
- `add_1_daze` - 添加1层眩晕
- `add_1_stun` - 添加1层昏迷

### 4.3 移动效果
- `move_forward_1` - 前进1格
- `move_backward_1` - 后退1格
- `move_pull_1` - 拉近1格
- `move_pull_2` - 拉近2格
- `move_knockback_1` - 击退1格

### 4.4 移除效果
- `remove_all_block` - 移除所有格挡
- `remove_all_guard` - 移除所有护卫
- `remove_all_dodge` - 移除所有闪避
- `remove_all_riposte` - 移除所有反击
- `remove_all_strength` - 移除所有力量
- `remove_all_crit` - 移除所有暴击加成

### 4.5 连击系统
- `prime_combo` - 给目标添加连击预备标记
- `end_combo` - 消耗连击标记结束连击

**连击相关Buff** (通过 `performer_buffs` 字段添加)：
- `combo_crit_50pct` - 对连击标记敌人攻击时+50%暴击率
- `combo_crit_100pct` - 对连击标记敌人攻击时+100%暴击率
- `combo_damage_boost_50pct` - 对连击标记敌人伤害+50%
- `combo_damage_boost_100pct` - 对连击标记敌人伤害+100%

### 4.6 治疗效果
- `heal_5pct` / `heal_10pct` / `heal_15pct` / `heal_20pct` / `heal_25pct` / `heal_30pct` - 百分比治疗
- `heal_33pct` / `heal_35pct` / `heal_40pct` / `heal_50pct` / `heal_60pct` / `heal_67pct` / `heal_70pct` / `heal_75pct` - 更高百分比治疗
- `heal_33pct_self_threshold_high` - 高血量阈值时自愈33%
- `heal_50pct_self_threshold_high` - 高血量阈值时自愈50%
- `heal_33pct_self_threshold_low` - 低血量阈值时自愈33%
- `heal_small` / `heal_medium` / `heal_large` - 固定数值治疗

**持续治疗 (HoT)**：
- `hot_heal_small` - 小额持续治疗
- `hot_heal_medium` - 中额持续治疗
- `hot_heal_large` - 大额持续治疗
- `hot_heal_very_large` - 超大额持续治疗
- `hot_heal_massive` - 极大额持续治疗

### 4.7 DoT效果
**流血 (Bleed)**：
- `skill_dot_very_small_bleed` / `skill_dot_small_bleed` / `skill_dot_medium_bleed` / `skill_dot_large_bleed` / `skill_dot_very_large_bleed` - 各级流血
- `skill_dot_massive_bleed` / `skill_dot_super_massive_bleed` - 超高额流血

**腐蚀 (Blight)**：
- `skill_dot_very_small_blight` / `skill_dot_small_blight` / `skill_dot_medium_blight` / `skill_dot_large_blight` / `skill_dot_very_large_blight` - 各级腐蚀
- `skill_dot_massive_blight` - 超高额腐蚀

**燃烧 (Burn)**：
- `skill_dot_small_burn` / `skill_dot_medium_burn` / `skill_dot_large_burn` / `skill_dot_very_large_burn` - 各级燃烧
- `skill_dot_massive_burn` - 超高额燃烧

### 4.8 压力效果
- `stress_damage_1` - 造成1点压力伤害
- `stress_heal_1` / `stress_heal_2` / `stress_heal_3` / `stress_heal_4` / `stress_heal_5` - 治疗1-5点压力

---

## 五、技能命名规则

| 类型 | 格式 | 示例 | 说明 |
|-----|------|------|------|
| 基础 | `{代码}_{名称}` | `abm_rake` | 基础技能 |
| 升级 | `{代码}_{名称}_u` | `abm_rake_u` | 升级版技能 |
| 路径 | `{代码}_{名称}_p{1/2/3}` | `abm_rake_p2` | 路径变体，如p2代表路径2中的技能变体 |
| 路径升级 | `{代码}_{名称}_p{数字}_u` | `abm_rake_p1_u` | 路径变体的升级版 |

---

## 六、英雄代码速查

| 代码 | 英雄 | 类型 |
|-----|------|-----|
| flg | Flagellant | 基础 |
| gr | Grave Robber | 基础 |
| hel | Hellion | 基础 |
| hwm | Highwayman | 基础 |
| jes | Jester | 基础 |
| lep | Leper | 基础 |
| maa | Man-at-Arms | 基础 |
| occ | Occultist | 基础 |
| pd | Plague Doctor | 基础 |
| run | Runaway | 基础 |
| ves | Vestal | 基础 |
| cru | Crusader | DLC1 |
| dul | Duelist | DLC1 |
| abm | Alchemist | DLC2 |

---

*2026-01-04*
