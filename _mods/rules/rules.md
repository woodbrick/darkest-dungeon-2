# 游戏规则与机制

## DU价值体系

**基础**: 1 DU = 1点基础伤害等价价值

### 效果DU速查表
| 效果类型 | 1级 | 2级 | 3级 |
|---------|-----|-----|-----|
| 力量/脆弱 | 3 | 5 | 7 |
| 格挡 | 2.5 | 3.5 | 4.5 |
| 强格挡 | 3.5 | 5 | 6.5 |
| 闪避 | 2 | 4 | 7 |
| 强闪避 | 3 | 6 | 8 |
| 晕眩 | 4 | 7 | - |
| 反击 | 3 | 5 | - |

### 评估标准
- DU < 9: 弱势，需增强
- DU 9-13: 可接受
- DU > 13: 优秀

## 铁律：基础版与升级版同步修改

**规则**: 修改技能基础版时，**必须**同时修改升级版(`_u`)

**检查清单**:
- 基础版和升级版是否都被修改？
- 升级版是否使用升级效果标记(`add_2_`而非`add_1_`)？
- 升级版DU是否为基础版的1.5倍左右？

## 英雄代码

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

## 文件路径

**基础**: `hero_{代码}_data_export.Group.csv`
**DLC1**: `dlc_dul_cru/hero_{代码}_data_export.Group.csv`
**DLC2**: `dlc_catacombs/hero_{代码}_data_export.Group.csv`

## 饰品文件

| 文件 | 路径 |
|------|------|
| `trinkets_data_export.Group.csv` | 主目录 |
| `trinkets_data_export_DLC1.Group.csv` | dlc_dul_cru/ |
| `trinkets_data_export_DLC2.Group.csv` | dlc_catacombs/ |

## 技能命名规则

| 类型 | 格式 | 示例 |
|-----|------|------|
| 基础 | `{代码}_{名称}` | `abm_rake` |
| 升级 | `{代码}_{名称}_u` | `abm_rake_u` |
| 路径 | `{代码}_{名称}_p{1/2/3}` | `abm_rake_p2` |
| 路径升级 | `{代码}_{名称}_p{数字}_u` | `abm_rake_p1_u` |

## 伤害计算

**CSV格式**: `add_stats,基础值,随机值`
**实际伤害**: 基础值 ~ (基础值 + 随机值)

| CSV | 实际伤害 | 平均 |
|-----|---------|------|
| `5,5` | 5-10 | 7.5 |
| `8,8` | 8-16 | 12 |
| `3,3,2` | 3-10 | 6.5 |

## 目标与位置

### 位置编号
```
前排: 位置1, 位置2
后排: 位置3, 位置4
```

### launch_ranks (施放位置)
- `1,2` - 可从位置1或2施放
- `1,2,3,4` - 可从任何位置施放

### target_ranks (目标位置)
- `1` - 只攻击位置1
- `1,2` - 攻击位置1或2
- `1,2,3,4` - 攻击所有位置

### m_IsMultiHit
| 值 | 含义 |
|---|------|
| False | 单体攻击，逐个选择目标 |
| True | 群体攻击，一次性对所有目标生效 |

## 路径差异化

三条路径必须有明确不同的玩法定位

*最后更新: 2026-01-06*
