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

## 文档索引

### 核心方法论
| 文档 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | 技能修改详细教程 |
| [available_effects.md](available_effects.md) | 效果标记与DU价值 |
| [file_mapping.md](file_mapping.md) | 文件映射表 |
| [hero_file_rules.md](hero_file_rules.md) | CSV结构规则 |

### 英雄改动方案
| 英雄 | 方案文档 | YAML配置 |
|------|----------|----------|
| 小丑 (Jester) | [jester_buff_proposal.md](jester_buff_proposal.md) | [hero_jes_changes_complete.yml](hero_jes_changes_complete.yml) |
| 炼金术士 (Alchemist) | [alchemist_buff_proposal.md](alchemist_buff_proposal.md) - |

---

## 核心原则

### 铁律：基础版与升级版同步修改

**规则**: 修改技能基础版时，**必须**同时修改升级版(`_u`)

**检查清单**:
- 基础版和升级版是否都被修改？
- 升级版是否使用升级效果标记(`add_2_`而非`add_1_`)？
- 升级版DU是否为基础版的1.5倍左右？

### DU价值体系

**基础**: 1 DU = 1点基础伤害等价价值

**效果DU**:
| 力量 | 脆弱 | 格挡 | 闪避 | 晕眩 | 反击 |
|------|------|------|------|------|------|
| 1级:3 | 1级:3 | 1级:2.5 | 1级:4 | 1级:4 | 1级:3 |
| 2级:5 | 2级:5 | 强格挡:3.5 | | 2级:7 | 2级:5 |

**评估标准**:
- DU < 9: 弱势，需增强
- DU 9-13: 可接受
- DU > 13: 优秀

### 路径差异化

三条路径必须有明确不同的玩法定位

---

## 英雄速查

### 英雄代码

**基础英雄**: flg, gr, hel, hwm, jes, lep, maa, occ, pd, run, ves
**DLC1**: cru, dul
**DLC2**: abm

### 文件路径

**基础**: `hero_{代码}_data_export.Group.csv`
**DLC1**: `dlc_dul_cru/hero_{代码}_data_export.Group.csv`
**DLC2**: `dlc_catacombs/hero_{代码}_data_export.Group.csv`

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
cd _mods && python parse_universal.py {英雄代码}
```
**功能**:
- 解析英雄所有技能数据
- 计算每个技能的DU价值
- 按基础/路径分类展示
- 自动标识弱势技能(DU<9)

### 技能更新应用
```bash
cd _mods && python apply_universal.py {英雄代码} {配置文件.yml}
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
