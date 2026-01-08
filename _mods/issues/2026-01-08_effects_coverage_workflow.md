# 问题: 效果覆盖度验证流程缺失

**日期**: 2026-01-08
**状态**: ✅ 已解决
**优先级**: 高

## 问题描述

在分析修女(ves)技能平衡性时，发现 effects_du.yml 缺失39个效果定义，导致：
- DU计算不准确
- 技能强弱误判
- 平衡性方案基于错误数据

**覆盖情况**:
- 唯一效果: 84个
- 已定义: 45个
- 缺失: 39个
- **覆盖率仅53.6%**

## 根因分析

### 流程缺陷
1. **缺少强制验证环节** - 未检查覆盖率就进入DU分析
2. **parse_universal.py 功能不足** - 无法自动检测缺失效果
3. **提案生成时机错误** - 在效果补充前就输出 ves_buff_proposal.md

### 违反铁律
- **"DU < 5 的技能必然存在效果疏漏"** - 未执行该检查
- **单一事实原则** - effects_du.yml 不完整，导致DU计算错误

## 解决方案

### 已实施优化

#### 1. 增强 parse_universal.py
**新增功能**:
- `find_missing_effects()` - 自动扫描7个字段，检测缺失效果
- `print_missing_effects_report()` - 输出缺失效果清单(效果ID+字段+来源)
- `print_coverage_stats()` - 输出覆盖度统计(总数/已定义/缺失/百分比)

**使用示例**:
```bash
cd _mods/scripts && python parse_universal.py ves
```

**输出示例**:
```
⚠️  发现 48 个未定义效果:
效果ID                                     字段                             来源技能
--------------------------------------------------------------------------------
add_1_daze                               target_apply_limit_effects     ves_illumination, ves_illumination_u
ves_mantra_p1_heal                       performer_effects              ves_mantra_p1, ves_mantra_p1_u
...

📊 效果覆盖度统计:
----------------------------------------
总效果数 (含重复): 135
唯一效果数: 84
已定义: 45
缺失: 39
覆盖率: 53.6%

⚠️  警告: 覆盖率低于90%，建议补充缺失效果
```

#### 2. 设置覆盖率阈值
| 覆盖率 | 状态 | 操作 |
|--------|------|------|
| **100%** | ✅ 完美覆盖 | 可以进行DU分析 |
| **90-99%** | ✓ 覆盖率良好 | 补充少量缺失 |
| **<90%** | ⚠️ 警告 | **必须先补充效果** |

#### 3. 新增调研铁律
**DU计算前必做检查**:
1. ✅ 运行 `parse_universal.py <英雄>`
2. ✅ 确认覆盖率 ≥ 90%
3. ✅ 补充所有缺失效果到 `effects_du.yml`
4. ✅ 重新运行验证覆盖率 = 100%
5. ✅ 然后才能进行DU分析和平衡性调整

### 效率提升
- **旧方法**: 手动grep CSV → 逐个对比 → 每个技能5分钟
- **新方法**: 一条命令自动检测 → <5秒完成
- **效率提升**: 60倍+

## 效果验证

### 修复案例: ves_illumination
**修复前**:
- DU: 0.5
- 遗漏效果: remove_all_dodge, remove_all_dodge_plus, remove_anti_dodge_debuff

**修复后**:
- DU: 5.5 (+1000%)
- 新增3个闪避移除效果到 effects_du.yml

### 剩余工作
**修女39个缺失效果** (需补充):
- 信念加成相关 (15个)
- 审判P3控制 (10个)
- 猛击破防机制 (5个)
- 真言升级buff (7个)
- 路径2升级祝福 (2个)

## 流程改进

### 标准工作流(新)
```
1. 分析英雄 → parse_universal.py <代码>
2. 检查覆盖率 → 必须 ≥90%
3. 补充缺失效果 → 添加到 effects_du.yml
4. 验证覆盖率 → 重新运行，确认100%
5. DU分析 → 基于完整数据
6. 制定方案 → 输出提案文档
```

### 防止再发
- **文档更新时机**: 提案文档必须在覆盖率100%后生成
- **自动检查**: parse_universal.py 自动输出警告
- **问题追踪**: 所有流程问题记录到 `_mods/issues/`

## 相关文件
- [parse_universal.py](_mods/scripts/parse_universal.py) - 增强版检测脚本
- [effects_du.yml](_mods/rules/effects_du.yml) - 效果DU定义
- [MISSING_EFFECTS_TODO.md](_mods/MISSING_EFFECTS_TODO.md) - 缺失效果清单

---

**结论**: 该问题已通过增强 parse_universal.py 解决，新增自动检测和覆盖度统计功能，确保未来分析基于完整数据。
