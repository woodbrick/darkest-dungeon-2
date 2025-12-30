# 暗黑地牢 2 文件映射表

## 概述

本文档列出了英雄和饰品相关的游戏数据文件路径，方便查找和修改。

---

## 一、英雄数据文件

### 1.1 基础英雄（主目录）

| 英雄名称 | 代码 | 英文 | 文件路径 | 文件大小 | 说明 |
|---------|------|------|----------|---------|------|
| 苦修者 | flg | Flagellant | `hero_flg_data_export.Group.csv` | 39 KB | 基础英雄，DLC内容 |
| 盗墓贼 | gr | Grave Robber | `hero_gr_data_export.Group.csv` | 43 KB | 基础英雄 |
| 赫利俄斯 | hel | Hellion | `hero_hel_data_export.Group.csv` | 31 KB | 基础英雄 |
| 强盗 | hwm | Highwayman | `hero_hwm_data_export.Group.csv` | 41 KB | 基础英雄 |
| 小丑 | jes | Jester | `hero_jes_data_export.Group.csv` | 52 KB | 基础英雄 |
| 麻风病人 | lep | Leper | `hero_lep_data_export.Group.csv` | 36 KB | 基础英雄 |
| 步兵 | maa | Man-at-Arms | `hero_maa_data_export.Group.csv` | 40 KB | 基础英雄 |
| 神秘学者 | occ | Occultist | `hero_occ_data_export.Group.csv` | 67 KB | 基础英雄 |
| 瘟疫医生 | pd | Plague Doctor | `hero_pd_data_export.Group.csv` | 50 KB | 基础英雄 |
| 逃亡者 | run | Runaway | `hero_run_data_export.Group.csv` | 48 KB | 基础英雄 |
| 修女 | ves | Vestal | `hero_ves_data_export.Group.csv` | 37 KB | 基础英雄 |

**路径**: `g:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel\`

### 1.2 DLC 英雄

| 英雄名称 | 代码 | 英文 | 文件路径 | DLC | 说明 |
|---------|------|------|----------|-----|------|
| 十字军 | cru | Crusader | `dlc_dul_cru/hero_cru_data_export.Group.csv` | DLC1 | The Binding Blade |
| 决斗者 | dul | Duelist | `dlc_dul_cru/hero_dul_data_export.Group.csv` | DLC1 | The Binding Blade |
| 炼金术士 | abm | Alchemist | `dlc_catacombs/hero_abm_data_export.Group.csv` | DLC2 | The Void Between |

**路径**: `g:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel\dlc_dul_cru\`

### 1.3 英雄规则文件

| 文件名 | 路径 | 说明 |
|-------|------|------|
| `hero_rules_data_export.Group.csv` | 主目录 | 英雄通用规则 |

### 1.4 特殊模式英雄数据

部分英雄在特殊模式下有独立数据文件：

| 文件名 | 路径 | 说明 |
|-------|------|------|
| `hero_bh_data_export.Group.csv` | `expedition/` | 远征模式强盗（Bandit Highwayman） |
| `hero_bh_data_export.Group.csv` | `kingdom/` | 王国模式强盗 |

---

## 二、饰品数据文件

### 2.1 基础饰品

| 文件名 | 路径 | 说明 |
|-------|------|------|
| `trinkets_data_export.Group.csv` | 主目录 | 基础饰品数据 |
| `trinkets_actor_effect_trigger_data_export.Group.csv` | 主目录 | 饰品触发效果 |
| `trinket_set_data_export.Group.csv` | 主目录 | 饰品套装数据 |

### 2.2 DLC 饰品

#### DLC1: The Binding Blade

| 文件名 | 路径 | 说明 |
|-------|------|------|
| `trinkets_data_export_DLC1.Group.csv` | `dlc_dul_cru/` | DLC1 饰品数据 |
| `trinkets_actor_effect_trigger_data_export_DLC1.Group.csv` | `dlc_dul_cru/` | DLC1 饰品触发效果 |

#### DLC2: The Void Between

| 文件名 | 路径 | 说明 |
|-------|------|------|
| `trinkets_data_export_DLC2.Group.csv` | `dlc_catacombs/` | DLC2 饰品数据 |

---

## 三、英雄故事文件（Combat Props）

英雄战斗场景中的道具和环境对象文件，命名格式：`herostory_{英雄代码}_combat_{场景编号}_{对象名称}.csv`

### 3.1 基础英雄故事文件

#### 盗墓贼 (Grave Robber)
- `herostory_gr_combat_1_husband` - 丈夫的棺材
- `herostory_gr_combat_1_liquor_cabinet` - 酒柜
- `herostory_gr_combat_1_prop_1/2` - 道具1/2
- `herostory_gr_combat_2_coffin_*` - 各种棺材（守卫、丈夫、陷阱、宝藏）
- `herostory_gr_combat_2_guard` - 守卫
- `herostory_gr_combat_2_prop` - 道具

#### 瘟疫医生 (Plague Doctor)
- `herostory_pd_combat_1_*` - 教授场景（书堆、讲台、教授、学生）
- `herostory_pd_combat_2_*` - 实验室场景（装置、食尸鬼教授、实验装备）

#### 逃亡者 (Runaway)
- `herostory_run_combat_1_*` - 修女场景（修女、支柱1/2/3）
- `herostory_run_combat_2_*` - 炉子场景（椅子、废料堆、炉子）

#### 修女 (Vestal)
- `herostory_ves_1_*` - 火焰场景（火焰、空间、窗户、木堆）
- `herostory_ves_2_*` - 酷刑室场景（笼子、椅子、铁处女、枷锁、酷刑者）

#### 神秘学者 (Occultist)
- `herostory_occ_combat_1_shade` - 阴影
- `herostory_occ_combat_2_*` - 降神会场景（降神桌、潜行者）
- `herostory_occ_combat_2_shambler` - 潜行者

#### 赫利俄斯 (Hellion)
- `herostory_hel_combat_1_*` - 部落场景（部落成员、邪教徒、树）
- `herostory_hel_combat_2_villager` - 村民

#### 强盗 (Highwayman)
- `herostory_hwy_combat_1_*` - 护卫场景（护卫、废墟1/2）
- `herostory_hwy_combat_2_*` - 马车场景（灌木1/2/3、马车、护卫）

#### 小丑 (Jester)
- `herostory_jes_combat_1_gravestone` - 墓碑
- `herostory_jes_combat_1_violinist` - 小提琴手

#### 麻风病人 (Leper)
- `herostory_leper_combat_1_*` - 宫廷场景（顾问、请愿者）
- `herostory_leper_combat_2_advisor` - 顾问

#### 步兵 (Man-at-Arms)
- `herostory_maa_combat_1_*` - 士兵场景（敌方士兵、友方士兵）
- `herostory_maa_combat_2_ghost` - 幽灵

#### 苦修者 (Flagellant)
- `herostory_flg_1_death` - 死亡场景
- `herostory_flg_1_data` - 基础数据

### 3.2 DLC 英雄故事文件

#### DLC1: The Binding Blade
##### 决斗者 (Duelist)
- `herostory_dul_1_*` - 导师场景（导师、练习假人、训练假人）
- `herostory_dul_2_*` - 卧室场景（衣服、床垫、枕头、酒杯）

##### 十字军 (Crusader)
- `herostory_cru_combat_1_*` - 农田场景（庄稼1/2/3、麦束、空地）
- `herostory_cru_combat_2_*` - 废墟村庄场景（灌木1/2、废墟1/2/3、树）
- `herostory_cru_2_warlord_spared` - 饶恕军阀

#### DLC2: The Void Between
##### 炼金术士 (Alchemist)
- `herostory_abm_1_*` - 实验室场景（药桌、桶、药剂、植物、凳子）
- `herostory_abm_2_*` - 地下室场景（野兽、僧侣、酷刑者）

---

## 四、英雄技能数据结构

英雄数据文件包含以下主要元素类型：

### 4.1 基础属性元素
- **元素ID**: 英雄代码（如 `hellion`, `flagellant`）
- **包含字段**:
  - `add_stats` - 基础属性（生命值、速度、等等）
  - `m_NameOverrideId` - 名称覆盖ID（可选）

### 4.2 技能元素
- **元素ID**: `{英雄代码}_{技能名称}`
- **包含字段**:
  - `target_ranks` - 目标位置（1,2,3,4 代表前排到后排）
  - `add_stats` - 技能属性（伤害数据：最小-最大-随机，如 "4-4-0"）
  - `target_effects` - 目标效果（暴击、连击、状态效果等）
  - `use_limit` - 使用限制
  - `cooldown` - 冷却时间

### 4.3 技能命名规则
- 基础技能: `{代码}_{名称}` (如 `hel_wicked_hack`)
- 升级技能: `{代码}_{名称}_u` (如 `hel_wicked_hack_u`)
- 路径1技能: `{代码}_{名称}_p1` (如 `hel_wicked_hack_p1`)
- 路径2技能: `{代码}_{名称}_p2` (如 `hel_if_it_bleeds_p2`)
- 路径3技能: `{代码}_{名称}_p3` (如 `hel_barbaric_yawp_p3`)

---

## 五、文件修改指南

### 5.1 Git 工作流
```bash
# 查看英雄文件改动
git diff hero_{英雄代码}_data_export.Group.csv

# 查看所有英雄改动
git diff hero_*_data_export.Group.csv

# 查看饰品改动
git diff trinkets_data_export.Group.csv
```

### 5.2 分析脚本
使用 `_mods/` 目录下的 Python 脚本分析改动：

```bash
# 分析单个英雄
python parse_full.py {英雄代码}

# 示例：分析赫利俄斯
python parse_full.py hel
```

### 5.3 修改建议
1. **备份原文件**: 修改前先提交到 git
2. **使用 UTF-8 编码**: 所有文件使用 UTF-8 编码
3. **保持格式**: CSV 格式要求严格，注意逗号和引号
4. **测试验证**: 修改后在游戏中测试效果

---

## 六、英雄代码速查表

| 代码 | 英文中文名 | 中文名称 | 类型 |
|------|-----------|---------|------|
| flg | Flagellant | 苦修者 | 基础（DLC） |
| gr | Grave Robber | 盗墓贼 | 基础 |
| hel | Hellion | 赫利俄斯 | 基础 |
| hwm | Highwayman | 强盗 | 基础 |
| jes | Jester | 小丑 | 基础 |
| lep | Leper | 麻风病人 | 基础 |
| maa | Man-at-Arms | 步兵 | 基础 |
| occ | Occultist | 神秘学者 | 基础 |
| pd | Plague Doctor | 瘟疫医生 | 基础 |
| run | Runaway | 逃亡者 | 基础 |
| ves | Vestal | 修女 | 基础 |
| cru | Crusader | 十字军 | DLC1 |
| dul | Duelist | 决斗者 | DLC1 |
| abm | Alchemist | 炼金术士 | DLC2 |

---

## 七、数据文件字段说明

### 7.1 CSV 文件结构
- **element_start**: 元素开始标记
- **element_end**: 元素结束标记
- **字段格式**: `字段名,值1,值2,值3,...`
- **行前缀**:
  - `-` 表示删除的行
  - `+` 表示新增的行
  - 无前缀表示未改动的行

### 7.2 常用字段

#### add_stats（属性数据）
- 格式: `add_stats,生命值,速度,其他,...`
- 技能伤害: `add_stats,最小伤害,最大伤害,随机值,其他,...`
- 示例: `add_stats,4,4,0` 表示 4-4 伤害

#### target_ranks（目标范围）
- 格式: `target_ranks,位置1,位置2,...`
- 位置: 1=前排1, 2=前排2, 3=后排1, 4=后排2
- 示例: `target_ranks,1,2,` 表示可攻击前两个位置

#### target_effects（目标效果）
- 格式: `target_effects,效果1,效果2,...`
- 常见效果:
  - `end_combo` - 结束连击
  - `prime_combo` - 预备连击
  - `prime_combo_33pct` - 33% 预备连击
  - `add_1_weak` - 添加1虚弱
  - `add_1_daze` - 添加1眩晕
  - `add_1_strength` - 添加1力量
  - `add_1_guard` - 添加1格挡

---

## 八、附录

### 8.1 DLC 目录说明
- `dlc_dul_cru/` - The Binding Blade（DLC1）
- `dlc_catacombs/` - The Void Between（DLC2）
- `dlc_supporter/` - 支持者内容（Soundtrack等）

### 8.2 特殊目录
- `expedition/` - 远征模式数据
- `kingdom/` - 王国模式数据

### 8.3 相关资源
- 游戏版本: 根据文件时间戳判断
- Git 分支: `excel-files`
- 最后更新: 2025-12-30

---

*文档创建时间: 2025-12-30*
*基于游戏数据文件分析*
