# 暗黑地牢2 游戏策划工作台

## 核心定位

**游戏策划工作流**：收集信息 → 分析决策 → 规划任务 → 协调实施

**工作目录**: `_mods/`

**工作规则**:
- 禁止创建新文件
- 优先编辑现有文件
- 数据输出到控制台或现有文档
- 输出文档严格按MECE原则：相互独立、完全穷尽
- 语言极度凝练
- 禁止重复内容
- 始终优先用子代理操作

---

## 文件结构规范

```
_mods/
├── CLAUDE.md                    # 主工作台文档(本文件)
├── scripts/                     # 通用工具脚本
│   ├── parse_universal.py      # 技能解析评估
│   ├── apply_universal.py      # 技能更新应用
│   └── scan_effects.py         # 效果扫描工具
├── rules/                       # 规则索引和数据记录
│   ├── rules.md                # 游戏规则与机制(DU体系/铁律/英雄代码)
│   ├── data_skills.md          # 技能数据字段说明
│   ├── hero_file_rules.md      # CSV结构规则
│   └── available_effects.md    # 效果标记完整清单
├── *_buff_proposal.md          # 英雄改进方案文档
└── *_changes_complete.yml      # 技能修改配置文件
```

**目录用途**:
- `scripts/`: 存放所有Python工具脚本(禁止特定英雄脚本)
- `rules/`: 存放游戏规则、数据结构、效果标记等参考文档
- 根目录: 工作台配置、英雄改动方案、YAML配置文件

---

## 文档索引

### 规则文档 (rules/)
| 文档 | 用途 |
|------|------|
| [rules/rules.md](rules/rules.md) | 游戏规则与机制 |
| [rules/data_skills.md](rules/data_skills.md) | 技能数据字段说明 |
| [rules/hero_file_rules.md](rules/hero_file_rules.md) | CSV结构规则 |
| [rules/available_effects.md](rules/available_effects.md) | 效果标记完整清单 |

### 英雄改动方案
| 英雄 | 方案文档 | YAML配置 |
|------|----------|----------|
| 小丑 (Jester) | [jester_buff_proposal.md](jester_buff_proposal.md) | [hero_jes_changes_complete.yml](hero_jes_changes_complete.yml) |
| 炼金术士 (Alchemist) | [alchemist_buff_proposal.md](alchemist_buff_proposal.md) | - |

---

## 核心原则

### 铁律：基础版与升级版同步修改

**规则**: 修改技能基础版时，**必须**同时修改升级版(`_u`)

**检查清单**:
- 基础版和升级版是否都被修改？
- 升级版是否使用升级效果标记(`add_2_`而非`add_1_`)？
- 升级版DU是否为基础版的1.5倍左右？

详细规则见: [rules/rules.md](rules/rules.md)

---

## 英雄速查

详细英雄代码/文件路径/饰品文件见: [rules/rules.md](rules/rules.md)

---

## 技能修改流程

1. **数据收集**: Task工具 + game-mechanics-researcher代理
2. **分析决策**: 识别弱势技能(DU<9)，设计改进方案
3. **规划任务**: 输出`{英雄}_buff_proposal.md`
4. **协调实施**: 生成`{英雄}_changes_complete.yml`，使用csv-balance-implementer代理

---

## 通用工具脚本

### 技能解析评估
```bash
cd _mods/scripts && python parse_universal.py {英雄代码}
```
**功能**:
- 解析英雄所有技能数据
- 计算每个技能的DU价值
- 按基础/路径分类展示
- 自动标识弱势技能(DU<9)

### 技能更新应用
```bash
cd _mods/scripts && python apply_universal.py ../{配置文件.yml}
```
**功能**:
- 读取YAML配置文件
- 验证铁律合规性(基础版/升级版同步)
- 精确修改CSV字段
- 输出修改日志

**配置格式**:
```yaml
skill_id:
  - field: target_effects
    old: add_1_block
    new: add_1_block_plus
```

### 禁止事项
- ❌ 禁止创建特定英雄的专用脚本
- ❌ 禁止重复实现已有功能
- ✅ 必须使用通用脚本处理所有英雄

---

*最后更新: 2026-01-06*
