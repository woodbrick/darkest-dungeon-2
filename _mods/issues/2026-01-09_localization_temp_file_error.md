# 问题: 本地化临时文件错误导出全量数据

**日期**: 2026-01-09
**状态**: 🔍 诊断中
**优先级**: 中

## 问题描述

在检查上下文索引文件时，发现 `temp_leper.json` 存在严重数据膨胀问题：

**文件异常**:
- 文件路径: `_mods/scripts/temp_leper.json`
- 文件大小: **4.09MB** (4,090,526 字节)
- 包含条目: **131,659条**
- 文件名暗示: 仅包含 Leper（麻风勇士）相关条目
- 实际内容: **整个游戏的本地化数据**

**对比参考**:
- `lep_tempest_hp_change.json`: 1条条目，正确记录leper tempest路径修改
- `localization_changes.json`: 记录历史修改日志

## 错误表现

### 数据量异常
| 文件 | 预期 | 实际 | 异常倍数 |
|------|------|------|----------|
| temp_leper.json | ~50-100条(leper) | 131,659条 | 1300x+ |

### 内容范围异常
- **UI元素**: "Back", "The Mountain", "Button_Back"
- **颜色代码**: "#444F61FF", "#FFFFFFFF", "#ED1500FF"
- **平台文本**: "Open Microsoft Store to view DLC?"
- **所有英雄技能**: 包含hel/ves/gr/run等所有英雄数据
- **游戏系统**: 从战斗到UI全覆盖

## 根因分析

### 可能原因
1. **脚本错误**: po_manager.py 或相关脚本在提取leper本地化时，未正确过滤msgctxt
2. **复制粘贴错误**: 误将整个zh_CN.po转换为JSON
3. **调试产物**: 开发过程中生成的临时文件，未清理

### 影响范围
- **存储浪费**: 4MB vs 预期10KB (400倍膨胀)
- **可读性差**: 无法快速定位leper相关修改
- **版本控制**: Git需要追踪大量无关数据

## 修复方案

### ✅ 已完成
1. **删除错误文件** → `_mods/scripts/temp_leper.json` 已删除
2. **验证git状态** → 文件未提交到版本库，无需清理
3. **根因分析** → 确认为po_manager.py缺少过滤功能

### 过滤规则
```python
# 正确的过滤条件
leper_entries = [
    entry for entry in all_entries
    if entry.get('msgctxt') and 'lep' in str(entry['msgctxt']).lower()
]
```

### 预期输出
```json
{
  "metadata": {},
  "entries": [
    {
      "msgctxt": "buff_desc_path_descriptor_lep_tempest_override",
      "msgid": "...",
      "msgstr": "..."
    }
  ]
}
```

### 脚本改进建议 (可选)

#### 增强 po_manager.py export 命令
```python
# 添加 --filter 参数
export_parser.add_argument('--filter', help='msgctxt过滤模式')
export_parser.add_argument('--max-entries', type=int, default=1000,
                          help='最大导出条目数(防止误导出全量)')

# 在 export_dict() 中添加过滤逻辑
def export_dict(self, pattern: str = None, max_entries: int = 1000) -> dict:
    entries = self.entries
    if pattern:
        regex = re.compile(pattern, re.IGNORECASE)
        entries = [e for e in self.entries
                  if e.msgctxt and regex.search(e.msgctxt)]

    if len(entries) > max_entries:
        raise ValueError(f'导出条目过多({len(entries)})，请检查过滤条件')

    return {
        'metadata': self.metadata,
        'entries': [e.to_dict() for e in entries]
    }
```

#### 使用示例
```bash
# 正确：导出leper相关条目
python po_manager.py export zh_CN.po temp_leper.json --filter "lep"

# 防护：超过1000条时自动拒绝
python po_manager.py export zh_CN.po temp_all.json
# Error: 导出条目过多(131659)，请检查过滤条件
```

## 其他发现

### skills_index.yml 不完整
- **当前状态**: 仅包含 Hellion（hel）技能索引
- **缺失英雄**: 其他11个英雄（lep/ves/pd/run等）
- **优先级**: 低（不影响当前工作）

## 流程改进

### 本地化修改规范
1. **临时文件命名**: 必须包含时间戳和英雄代码
   - ❌ `temp_leper.json`
   - ✅ `temp_20260109_lep_tempest_hp.json`

2. **数据验证**: 脚本必须验证过滤后条目数量
   ```python
   assert len(leper_entries) < 200, "过滤结果异常，可能包含全量数据"
   ```

3. **自动清理**: 脚本执行后自动删除临时文件

## 相关文件
- `_mods/scripts/temp_leper.json` - 错误的全量导出
- `_mods/scripts/lep_tempest_hp_change.json` - 正确的leper修改
- `_mods/scripts/po_manager.py` - 可能的根因脚本
- `_mods/logs/localization_changes.json` - 修改历史记录

---

## 结论

**状态**: ✅ 已解决

temp_leper.json 是一个错误的全量导出文件，由 po_manager.py 缺少过滤功能导致。该文件已删除，未影响版本库。

**根本问题**: po_manager.py 的 export 命令需要添加 `--filter` 参数和数据量验证，防止误导出全量数据。

**优先级**: 低（不影响当前工作流程，可作为后续优化项）
