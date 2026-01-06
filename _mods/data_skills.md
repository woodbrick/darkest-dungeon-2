# 技能数据字段说明

## 文件结构

**路径**: `hero_{英雄代码}_data_export.Group.csv`
**编码**: UTF-8
**结构**: `element_start,{ID},{类型}` → `{字段},{值}...` → `element_end`

## 元素类型

### ActorDataStats - 属性数据
定义英雄或技能的基础属性

**字段**:
- `add_stats` - 属性值列表
- `key_map` - 属性键映射

### ActorDataSkill - 技能数据
定义技能的基本信息

**字段**:
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `m_IsFriendly` | Bool | 是否友方技能 | True/False |
| `launch_ranks` | List | 施放位置 | 1,2 表示从位置1或2施放 |
| `target_ranks` | List | 目标位置 | 1,2,3,4 表示可攻击所有位置 |
| `m_IsMultiHit` | Bool | 是否群体攻击 | True=群体, False=单体 |
| `m_Cooldown` | Int | 冷却回合数 | 0=无冷却 |
| `m_CanBeRiposted` | Bool | 可被反击 | True/False |
| `m_Tags` | List | 技能标签 | 用于特殊判定 |

### ActorDataEffects - 效果数据
定义技能的效果

**字段**:
| 字段 | 说明 |
|------|------|
| `performer_effects` | 施放者自身效果 |
| `target_effects` | 目标效果 |
| `performer_after_target_effects` | 攻击后施放者效果 |
| `on_hit_as_performer_to_performer_effects` | 命中时施放者获得效果 |
| `on_crit_as_performer_to_target_effects` | 暴击时目标效果 |

## 伤害属性配置

```csv
key_map,health_damage,health_damage_range,crit_chance
add_stats,3,3,0.05
```

**字段说明**:
- 第1位: 基础伤害值 (如: 3)
- 第2位: 随机伤害值 (如: 3) → 实际伤害 3-6
- 第3位: 暴击概率 (如: 0.05 = 5%)

*最后更新: 2026-01-06*
