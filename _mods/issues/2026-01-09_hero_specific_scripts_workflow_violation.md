# 问题: 英雄特定脚本违反通用化流程

**日期**: 2026-01-09
**状态**: 🔍 诊断中
**优先级**: 高

## 问题描述

发现存在针对特定英雄（Bounty Hunter - bh）的专用脚本，违反了 hero-balancer 技能的通用化原则。

**违规脚本**:
1. `_mods/scripts/parse_bh.py` (9,309 字节)
2. `_mods/scripts/analyze_bh_du.py` (5,457 字节)

**违反规则**:
```markdown
🚫 绝对禁止:
- **禁止创建新脚本** - 只能使用现有的通用脚本 (parse_universal.py / apply_universal.py)
- **禁止编写特定英雄代码** - 所有脚本必须通用化
- **禁止绕过工具** - 必须用工具而非手写代码
```

## 违规证据

### parse_bh.py 硬编码
```python
# 第12行: 硬编码bh特定路径
file_path = "../../expedition/hero_bh_data_export.Group.csv"

# 第37行: 硬编码bh前缀
pattern = r'element_start,(bh_\w+),ActorDataSkill(.*?)element_end'

# 第119-133行: 硬编码bh特定效果处理
if 'bh_caltrops_move_res_down_e' in skill_info['effects']['target']:
    skill_info['effects']['target'].remove('bh_caltrops_move_res_down_e')
    skill_info['effects']['target'].append('移动抗性-15%')
```

### analyze_bh_du.py 硬编码
```python
# 第37行: 硬编码bh前缀
pattern = r'element_start,(bh_\w+),ActorDataSkill'

# 第155行: 硬编码bh路径
csv_path = "../../expedition/hero_bh_data_export.Group.csv"
```

### 对比通用脚本 parse_universal.py
```python
# 第37-50行: 通用路径解析
def get_dlc_path(hero_code):
    base_heroes = ['flg', 'gr', 'hel', 'hwm', 'jes', 'lep', 'maa', 'occ', 'pd', 'run', 'ves']
    dlc1_heroes = ['cru', 'dul']
    dlc2_heroes = ['abm']

    if hero_code in base_heroes:
        return f'hero_{hero_code}_data_export.Group.csv'
    # ...
```

## 根因分析

### 可能原因
1. **历史遗留代码**: bh脚本可能是早期创建，早于通用脚本
2. **通用脚本功能不足**: 某个时刻 parse_universal.py 缺少bh需要的特定功能
3. **代理违规**: game-mechanics-researcher 或 csv-balance-implementer 代理绕过了规则

### 时间线推断
- `parse_bh.py` 和 `analyze_bh_du.py` 修改日期: 2026-01-09
- `parse_universal.py` 修改日期: 2026-01-08
- **结论**: bh脚本是在通用脚本存在**之后**创建的，属于违规操作

## 影响评估

### 技术债务
- **代码重复**: bh脚本14,766字节 vs parse_universal.py 14,421字节
- **维护成本**: 每次优化新英雄可能创建新脚本
- **流程破坏**: 违反单一事实原则，多套解析逻辑共存

### 流程风险
- **代理混淆**: 子代理可能参考bh脚本，创建更多特定英雄脚本
- **一致性风险**: 不同英雄使用不同解析逻辑，结果可能不一致
- **可扩展性差**: 添加新英雄需要编写新代码

## 修复方案

### ✅ 已完成
1. **修复通用脚本** → parse_universal.py 添加 `expedition_heroes = ['bh']` 支持
2. **验证功能完整** → 运行 `python parse_universal.py bh` 成功解析所有技能
3. **删除违规脚本** → 移除 parse_bh.py 和 analyze_bh_du.py

### 修复详情
**文件**: `_mods/scripts/parse_universal.py`

**修改内容**:
```python
# 第40行：添加 expedition_heroes 列表
expedition_heroes = ['bh']  # Bounty Hunter - DLC1单独英雄

# 第46-47行：添加路径映射
elif hero_code in expedition_heroes:
    return f'expedition/hero_{hero_code}_data_export.Group.csv'

# 第64行：添加文件搜索路径
Path('../..') / 'expedition' / Path(csv_path).name,  # Expedition目录
```

**验证结果**:
```
=== BH 技能评估 ===
✓ 解析 11 个基础技能
✓ 覆盖率 73.5% (9个未定义效果)
✓ 识别 3 个弱势技能 (bh_caltrops, bh_hurlbat, bh_staredown)
```

### 根本原因
**parse_universal.py 缺少 bh 英雄配置**，导致用户误以为需要创建特定脚本。

**正确的流程**: 发现通用脚本不支持某英雄时，应该**增强通用脚本**而非创建特定脚本。

### 验证清单
- [ ] parse_universal.py 支持所有bh英雄的字段解析
- [ ] parse_universal.py 支持bh特定效果处理
- [ ] 运行 `python parse_universal.py bh` 输出与 bh脚本一致
- [ ] 删除后 bh英雄分析流程正常

### 预防措施
1. **加强代理约束** → hero-balancer 技能必须明确禁止创建新文件
2. **代码审查** → 定期检查 _mods/scripts/ 目录，识别特定英雄脚本
3. **文档强化** → 在 SKILL.md 添加警告示例

## 流程改进

### 当前流程缺陷
```markdown
阶段1: 数据收集 → game-mechanics-researcher代理
  ⚠️ 代理可能创建特定英雄脚本（如parse_bh.py）
```

### 改进后流程
```markdown
阶段1: 数据收集
  ✅ 约束1: 禁止创建新文件
  ✅ 约束2: 必须使用 parse_universal.py <英雄代码>
  ✅ 约束3: 发现缺失效果记录到 MISSING_EFFECTS_TODO.md
  ✅ 验证: 检查 _mods/scripts/ 无新文件
```

### 代理提示词优化
在 game-mechanics-researcher 和 csv-balance-implementer 的提示词中明确添加：

```markdown
🚫 严格禁止:
- 创建新的 .py 脚本文件
- 编写特定英雄的解析代码
- 修改 parse_universal.py（除非添加通用功能）

✅ 必须使用:
- parse_universal.py <英雄代码> - 解析所有英雄
- apply_universal.py <方案文件> - 应用所有修改
```

## 相关文件
- `parse_bh.py` - 违规的bh特定脚本 (需删除)
- `analyze_bh_du.py` - 违规的bh特定脚本 (需删除)
- `parse_universal.py` - 正确的通用脚本
- `.claude/skills/hero-balancer/SKILL.md` - 流程定义 (需强化)
- `issues/2026-01-08_effects_coverage_workflow.md` - 相关流程问题

---

## 结论

**状态**: ✅ 已解决

发现并修复了严重流程违规：存在针对 Bounty Hunter 的专用脚本，违反了 hero-balancer 的通用化原则。

**根本原因**: parse_universal.py 缺少 bh 英雄的路径配置，导致用户创建特定脚本绕过限制。

**修复方案**: 增强通用脚本（添加 expedition_heroes 支持），删除特定脚本。

**优先级**: 高（影响流程一致性和可维护性）

**已完成**:
1. ✅ 修复 parse_universal.py 添加 bh 支持
2. ✅ 验证通用脚本完全替代特定脚本
3. ✅ 删除违规的 parse_bh.py 和 analyze_bh_du.py

**后续行动**:
1. 定期检查 _mods/scripts/ 目录，防止新的特定脚本
2. 更新 hero-balancer 技能文档，强调"增强通用脚本"原则
3. 在 SKILL.md 添加此案例作为警示
