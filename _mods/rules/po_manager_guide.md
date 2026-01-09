# PO文件管理器使用指南

## 概述

`po_manager.py` 是通用的Gettext PO文件读写工具，支持读取、搜索、导出和回写翻译内容，并自动记录变更历史。

## 功能特性

- ✅ 读取PO文件条目
- ✅ 搜索原文/译文/上下文
- ✅ 导出为JSON格式
- ✅ 从JSON回写修改
- ✅ 自动备份原文件
- ✅ 翻译统计信息
- ✅ 自动记录变更历史
- ✅ 查看修改日志
- ✅ 支持所有语言PO文件

## 安装依赖

```bash
# 无需额外依赖，使用Python标准库
python 3.8+
```

## 路径说明

脚本自动解析相对路径，基于以下目录结构：
```
StreamingAssets/
  ├── Excel/           # 工作目录
  │   └── _mods/scripts/
  └── Localization/    # 翻译文件
      └── Poedit/
```

## 命令参考

### 1. 统计信息

查看翻译完成度和元数据：

```bash
cd _mods/scripts
python po_manager.py stats Poedit/zh_CN.po
```

输出示例：
```
✓ 解析完成: 18806 个条目

📊 翻译统计:
  总条目: 18806
  已翻译: 18805 (100.0%)
  模糊: 0 (0.0%)
  未翻译: 1 (0.0%)

📝 元数据:
  Language: zh_CN
```

### 2. 读取搜索

搜索特定翻译条目：

```bash
# 搜索所有条目
python po_manager.py read Poedit/zh_CN.po

# 搜索包含"skill"的条目
python po_manager.py read Poedit/zh_CN.po "skill"

# 搜索英雄名称
python po_manager.py read Poedit/zh_CN.po "hero"
```

输出示例：
```
找到 135 个匹配条目:

[1] Button_Back
    原文: Back
    译文: 返回
```

### 3. 导出JSON

导出为JSON便于编辑：

```bash
python po_manager.py export Poedit/zh_CN.po output.json
```

JSON格式：
```json
{
  "metadata": {
    "Language": "zh_CN"
  },
  "entries": [
    {
      "msgid": "Back",
      "msgstr": "返回",
      "msgctxt": "Button_Back",
      "fuzzy": false
    }
  ]
}
```

### 4. 回写修改

从JSON回写到PO文件：

```bash
python po_manager.py write Poedit/zh_CN.po modified.json
```

**安全机制**：
- ✅ 自动备份原文件为 `.po.bak`
- ✅ 只更新匹配的条目
- ✅ 未匹配条目输出警告
- ✅ **自动记录所有变更到日志**

### 5. 查看变更日志

查看所有修改历史：

```bash
# 查看所有日志
python po_manager.py log

# 查看最近5次修改
python po_manager.py log --last 5
```

日志输出示例：
```
📋 变更日志 (共 1 条记录)

[1] 2026-01-09 10:05:39
    文件: Poedit/zh_CN.po
    来源: modified.json
    修改数: 2
      [1] [Button_Back]
          原文: Back
          旧译: 返回
          新译: 后退
      [2] [Mountain]
          原文: The Mountain
          旧译: 山峰
          新译: 巅峰
```

**日志内容**：
- 时间戳
- 修改的文件路径
- 修改来源（JSON文件名）
- 修改数量
- 详细变更（原文、旧译文、新译文）

## 工作流示例

### 标准修改流程

```bash
# 1. 导出要修改的PO文件
python po_manager.py export Poedit/zh_CN.po skills.json

# 2. 使用文本编辑器修改skills.json中的msgstr字段

# 3. 回写修改（自动记录变更）
python po_manager.py write Poedit/zh_CN.po skills.json

# 4. 验证修改
python po_manager.py read Poedit/zh_CN.po "skill"

# 5. 查看变更历史
python po_manager.py log --last 1
```

### 追溯历史修改

```bash
# 查看最近的修改
python po_manager.py log --last 10

# 日志文件位置: _mods/logs/localization_changes.json
# 可直接查看JSON格式或使用脚本格式化输出
```

## 支持的文件

| 文件 | 路径 |
|------|------|
| 简体中文主游戏 | `Poedit/zh_CN.po` |
| 繁体中文主游戏 | `Poedit/tw_CN.po` |
| DLC1简体 | `Poedit/dlc_dul_cru/zh_CN.po` |
| DLC2简体 | `Poedit/dlc_catacombs/zh_CN.po` |

## 常见问题

### Q: 搜索无结果？
A: 确保搜索模式正确，支持正则表达式。使用具体关键词而非宽泛模式。

### Q: 回写失败？
A: 检查JSON格式是否正确，确保msgid与原文完全匹配。

### Q: 如何处理当前目录文件？
A: 脚本自动检测，文件存在则使用当前路径，不存在则解析为相对路径。

## 技术细节

- **编码**: UTF-8
- **格式**: Gettext Portable Object
- **解析器**: 正则表达式(无外部依赖)
- **备份**: 自动创建.bak文件
- **路径**: 智能相对路径解析
- **日志**: JSON格式，存储在 `_mods/logs/localization_changes.json`

### 日志文件格式

```json
[
  {
    "timestamp": "2026-01-09T10:05:39.292340",
    "file": "Poedit/zh_CN.po",
    "source": "modified.json",
    "count": 2,
    "changes": [
      {
        "msgid": "Back",
        "msgctxt": "Button_Back",
        "old_msgstr": "返回",
        "new_msgstr": "后退"
      }
    ]
  }
]
```

### 日志维护

- 日志文件自动创建，无需手动管理
- 每次write操作追加记录
- 可手动编辑或清空日志文件
- 建议定期备份日志文件

*最后更新: 2026-01-09*
