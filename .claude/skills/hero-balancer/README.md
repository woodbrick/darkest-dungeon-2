# 英雄平衡性优化技能 - 文件结构

## 目录结构

```
hero-balancer/
├── SKILL.md                    # 技能入口（273行，熵值7bits）
│
├── core/                       # 核心流程文档
│   ├── statemachine.md         # 状态机完整说明
│   ├── data_collection.md      # 数据收集详解
│   ├── proposal_creation.md    # 方案制定详解
│   └── safety_mechanisms.md    # 安全机制详解
│
├── guides/                     # 使用指南
│   ├── quickstart.md           # 5分钟快速开始
│   ├── troubleshooting.md      # 故障排除
│   └── best_practices.md       # 最佳实践
│
├── examples/                   # 案例示例
│   └── runaway_buff_proposal.md # 逃离者方案案例
│
└── assets/                     # 资源文件
    ├── hero_buff_proposal_template.md # 方案模板
    ├── available_effects.md    # 效果参考（外部链接到_mods/rules）
    └── state_template.json     # 状态文件模板
```

## 文件职责（MECE原则）

### 流程层（hero-balancer/）
**职责**: 如何执行平衡性优化

| 文件 | 职责 | 行数 |
|------|------|------|
| SKILL.md | 技能入口、状态机概要、快速参考 | 273 |
| core/statemachine.md | 状态机完整说明、转换规则、持久化 | ~200 |
| core/data_collection.md | 数据收集流程、效果字段、覆盖率检查 | ~150 |
| core/proposal_creation.md | 方案制定、DU计算、改进建议 | ~100 |
| core/safety_mechanisms.md | 三重确认、备份、验证、回滚 | ~80 |
| guides/quickstart.md | 5分钟快速开始教程 | ~100 |
| guides/troubleshooting.md | 常见问题和解决方案 | ~100 |
| guides/best_practices.md | 最佳实践和经验总结 | ~100 |

### 规则层（_mods/rules/）
**职责**: 游戏机制和计算标准

| 文件 | 职责 | 类型 |
|------|------|------|
| du_evaluation.md | DU价值体系、评估标准 | 规则 |
| csv_structure.md | CSV结构说明、字段定义 | 规则 |
| effects_du.yml | 效果DU定义（数据文件） | 数据 |
| hero_index.md | 英雄代码索引 | 参考 |

### 工具层（_mods/scripts/）
**职责**: 具体实现脚本

| 文件 | 职责 | 语言 |
|------|------|------|
| parse_universal.py | 通用技能解析器 | Python |
| apply_universal.py | 通用方案应用器 | Python |
| state_manager.py | 状态管理工具 | Python |
| po_manager.py | 本地化管理工具 | Python |

## 引用关系

### 内部引用（流程层）
```
SKILL.md
  ├── 链接 → core/statemachine.md（状态机详解）
  ├── 链接 → core/data_collection.md（数据收集详解）
  ├── 链接 → core/proposal_creation.md（方案制定详解）
  ├── 链接 → core/safety_mechanisms.md（安全机制详解）
  ├── 链接 → guides/quickstart.md（快速开始）
  └── 链接 → examples/*（案例示例）
```

### 外部引用（流程层 → 规则层）
```
core/data_collection.md
  └── 外部引用 → ../../_mods/rules/du_evaluation.md（DU规则）
core/data_collection.md
  └── 外部引用 → ../../_mods/rules/csv_structure.md（CSV结构）
core/data_collection.md
  └── 外部引用 → ../../_mods/rules/effects_du.yml（效果DU）
```

## 设计原则

### 1. 单一事实来源（SSOT）
- 游戏规则只在 `_mods/rules/` 定义一份
- 流程文档通过外部引用链接到规则层
- 避免重复维护

### 2. MECE原则
- **相互独立**: 流程/规则/工具三层职责清晰
- **完全穷尽**: 覆盖所有使用场景（核心+guides）

### 3. 高信息密度
- SKILL.md精简到273行（熵值7bits）
- 详细内容拆分到core/和guides/
- 每个文件聚焦单一职责

### 4. 清晰的层次
```
用户视角:
  SKILL.md（概要）→ core/*.md（详解）→ guides/*.md（教程）

数据视角:
  流程层（如何做）→ 规则层（标准）→ 工具层（实现）
```

## 迁移记录

### v2.0 重构（2026-01-09）

#### 删除的重复文件
- ❌ `references/rules.md` → 使用 `_mods/rules/du_evaluation.md`
- ❌ `references/hero_file_rules.md` → 使用 `_mods/rules/csv_structure.md`
- ❌ `references/` 目录（已清空并删除）

#### 移动的文件
- `references/runaway_buff_proposal.md` → `examples/runaway_buff_proposal.md`
- `references/available_effects.md` → `assets/available_effects.md`

#### 新增的目录
- ✅ `core/` - 核心流程文档
- ✅ `guides/` - 使用指南
- ✅ `examples/` - 案例示例

#### 精简的文件
- `SKILL.md`: 682行 → 273行（-60%）
- 信息密度: 4-5 bits → 7 bits（+40%）

## 统计数据

### 文件数量
| 类型 | v1.0 | v2.0 | 变化 |
|------|------|------|------|
| 流程层文件 | 6 | 12+ | +100% |
| 重复文件 | 2 | 0 | -100% |
| 总文件数 | 8 | 12+ | +50% |

### 代码行数
| 类型 | v1.0 | v2.0 | 变化 |
|------|------|------|------|
| SKILL.md | 682 | 273 | -60% |
| 详细文档 | 0 | ~800 | +800 |
| 总行数 | 682 | ~1073 | +57% |

### 信息密度
| 指标 | v1.0 | v2.0 | 提升 |
|------|------|------|------|
| SKILL.md熵值 | 4-5 bits | 7 bits | +40% |
| 重复度 | 30% | 0% | -100% |
| MECE合规度 | 低 | 高 | ✅ |

## 维护指南

### 添加新英雄流程案例
```bash
# 放置在 examples/
cp _mods/<hero>_buff_proposal.md \
   .claude/skills/hero-balancer/examples/<hero>_buff_proposal.md

# 在 SKILL.md 的文档索引中添加链接
```

### 更新游戏规则
```bash
# 只在 _mods/rules/ 更新
# 流程层文档会自动引用最新版本
vim _mods/rules/du_evaluation.md
```

### 添加新指南
```bash
# 放置在 guides/
vim .claude/skills/hero-balancer/guides/<new_guide>.md

# 在 SKILL.md 的文档索引中添加链接
```

## 相关文档

- [SKILL.md](SKILL.md) - 技能入口
- [../../_mods/issues/2026-01-09_file_structure_redundancy_analysis.md](../../_mods/issues/2026-01-09_file_structure_redundancy_analysis.md) - 重构分析

---

**版本**: v2.0
**更新**: 2026-01-09
**维护**: 遵循MECE原则，保持0重复度
