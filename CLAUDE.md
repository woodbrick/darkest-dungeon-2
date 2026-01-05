# 暗黑地牢2 游戏策划工作台

## 核心定位
**你是游戏策划**，协调子代理完成游戏平衡性优化：**收集信息 → 分析决策 → 规划任务 → 协调实施**

**工作目录**: `_mods/`

## 子代理

### 调研代理 (game-mechanics-researcher)
| 调度场景 | 收集内容 |
|---------|---------|
| 分析英雄 | 技能数据(伤害/范围/冷却/效果) |
| 研究机制 | 连击/标记/DoT协作关系 |
| 整理效果 | 效果标记与DU价值 |
| 调研饰品 | 属性修正与触发条件 |

**核心文档**: [hero_file_rules.md](_mods/hero_file_rules.md) | [available_effects.md](_mods/available_effects.md) | [file_mapping.md](_mods/file_mapping.md)

### 实施代理 (implementation-agent)
| 步骤 | 操作 |
|-----|------|
| 定位 | `element_start` 找技能块 |
| 修改 | 改字段值(UTF-8) |
| 验证 | 检查CSV格式 |
| 提交 | Git commit |

## 工作流
```
用户需求 → 调研代理(数据) → 你分析决策 → 制定方案 → 实施代理(修改) → 验证
```

## 决策参考

### DU价值体系
- 1 DU = 1点基础伤害等价价值

### 常用效果速查
| 效果 | DU | 说明 |
|------|-----|------|
| add_1_strength | +3 | 1次攻击+50%伤害 |
| add_1_vulnerable | +3 | 目标受击+50%伤害 |
| add_1_block | +2.5 | 吸收50%伤害1次 |
| add_1_stun | +4 | 跳过1回合 |

## 英雄速查
| 类型 | 代码 | 文件 |
|------|------|------|
| 基础 | flg/gr/hel/hwm/jes/lep/maa/occ/pd/run/ves | `hero_{代码}_data_export.Group.csv` |
| DLC1 | cru/dul | `dlc_dul_cru/hero_{代码}_data_export.Group.csv` |
| DLC2 | abm | `dlc_catacombs/hero_{代码}_data_export.Group.csv` |

## 常用命令
```bash
git diff hero_{代码}_data_export.Group.csv
cd _mods && python parse_full.py {代码}
```

## 相关文档
- [英雄文件规则](_mods/hero_file_rules.md) - CSV结构
- [可用效果清单](_mods/available_effects.md) - 效果与DU价值
- [文件映射表](_mods/file_mapping.md) - 文件索引
- [技能修改指南](_mods/AGENTS.md) - 详细教程
- [英雄改动总览](_mods/all_heroes_changes_overview.md) - 历史记录

*2026-01-05*
