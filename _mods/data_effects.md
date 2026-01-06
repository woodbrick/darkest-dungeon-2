# 效果数据字段说明

## 数据源

**来源文件**: `effect_data_export.Group.csv`
**DoT文件**: `dots_data_export.Group.csv`

## 增益效果 (add_*)

### 力量/脆弱
| 效果 | DU | 说明 |
|------|-----|------|
| add_1_strength | 3 | 1次攻击+50%伤害 |
| add_2_strength | 5 | 2次攻击+50%伤害 |
| add_1_vulnerable | 3 | 目标受击+50%伤害 |
| add_2_vulnerable | 5 | 目标受击+50%持续2次 |

### 格挡
| 效果 | DU | 说明 |
|------|-----|------|
| add_1_block | 2.5 | 吸收1次50%伤害 |
| add_2_block | 3.5 | 吸收2次50%伤害 |
| add_1_block_plus | 3.5 | 吸收1次75%伤害 |
| add_2_block_plus | 5 | 吸收2次75%伤害 |

### 控制
| 效果 | DU | 说明 |
|------|-----|------|
| add_1_daze | 2 | 减速1次 |
| add_1_stun | 4 | 跳过1回合 |

### 其他
| 效果 | DU | 说明 |
|------|-----|------|
| add_1_dodge | 2 | 50%闪避1次 |
| add_1_riposte | 3 | 受击反击 |
| add_1_crit | 6 | 下次必暴 |

## 治疗效果 (heal_*)

### 固定数值
| 效果 | DU | 说明 |
|------|-----|------|
| heal_small | 5 | 恢复5点生命 |
| heal_medium | 10 | 恢复10点生命 |
| heal_large | 16 | 恢复16点生命 |

### 百分比
| 效果 | DU | 说明 |
|------|-----|------|
| heal_10pct | 4 | 恢复10%生命 |
| heal_50pct | 20 | 恢复50%生命 |
| heal_100pct | 40 | 完全恢复 |

## DoT效果 (skill_dot_*)

**持续时间**: 所有DoT持续3回合
**触发时机**: performer_turn_start

### 流血
| 效果 | 伤害/回合 | 总伤害 | DU |
|------|----------|--------|-----|
| skill_dot_small_bleed | 2 | 6 | 2 |
| skill_dot_medium_bleed | 3 | 9 | 3.5 |
| skill_dot_large_bleed | 4 | 12 | 5 |

### 腐蚀
| 效果 | 伤害/回合 | 总伤害 | DU |
|------|----------|--------|-----|
| skill_dot_small_blight | 2 | 6 | 2 |
| skill_dot_medium_blight | 3 | 9 | 3.5 |
| skill_dot_large_blight | 4 | 12 | 5 |

## 压力效果 (stress_*)

### 压力治疗
| 效果 | DU | 说明 |
|------|-----|------|
| stress_heal_1 | 1 | 恢复1点压力 |
| stress_heal_2 | 2 | 恢复2点压力 |
| stress_heal_3 | 3 | 恢复3点压力 |

## 移动效果 (move_*)

| 效果 | DU | 说明 |
|------|-----|------|
| move_forward_1 | 0.5 | 前进1格 |
| move_backward_1 | 0.5 | 后退1格 |
| move_pull_1 | 1.5 | 拉近1格 |
| move_knockback_1 | 1.5 | 击退1格 |

## 连击系统

| 效果 | DU | 说明 |
|------|-----|------|
| prime_combo | 3 | 添加连击标记 |
| end_combo | -1 | 消耗连击标记 |

## 移除效果 (remove_all_*)

| 效果 | DU | 说明 |
|------|-----|------|
| remove_all_block | 6 | 移除所有格挡 |
| remove_all_dodge | 5 | 移除所有闪避 |
| remove_all_strength | 8 | 移除所有力量 |

*最后更新: 2026-01-06*
