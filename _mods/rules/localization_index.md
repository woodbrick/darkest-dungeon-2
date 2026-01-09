# 本地化文件索引

## 中文翻译文件

### 简体中文 (zh_CN)

| 文件 | 路径 | 大小 | 覆盖范围 |
|------|------|------|---------|
| 主游戏 | `Localization/Poedit/zh_CN.po` | 4.28 MB | 核心游戏内容 |
| DLC1 (狂厄与十字) | `Localization/Poedit/dlc_dul_cru/zh_CN.po` | 3.47 MB | 决斗家/十字军英雄及内容 |
| DLC2 (地穴) | `Localization/Poedit/dlc_catacombs/zh_CN.po` | 3.67 MB | 炼化师英雄及地穴内容 |
| 王国模式 | `Localization/Poedit/game_type_override_kingdom/zh_CN.po` | 3.91 MB | 王国特定文本 |

### 繁体中文 (tw_CN)

| 文件 | 路径 | 大小 | 覆盖范围 |
|------|------|------|---------|
| 主游戏 | `Localization/Poedit/tw_CN.po` | 4.12 MB | 核心游戏内容 |
| DLC1 (狂厄与十字) | `Localization/Poedit/dlc_dul_cru/tw_CN.po` | 4.07 MB | 决斗家/十字军英雄及内容 |
| DLC2 (地穴) | `Localization/Poedit/dlc_catacombs/tw_CN.po` | 4.26 MB | 炼化师英雄及地穴内容 |
| 王国模式 | `Localization/Poedit/game_type_override_kingdom/tw_CN.po` | 3.73 MB | 王国特定文本 |

## 文件格式

所有翻译文件使用 **Gettext PO (.po)** 格式

### 结构说明
- `msgid`: 原文(英文)
- `msgstr`: 译文(中文)
- `msgctxt`: 翻译上下文(用于区分同词不同义)

### 编辑工具
- **Poedit 3.5** (官方推荐)
- 任何支持PO格式的文本编辑器

## 使用指南

### 查找特定翻译
```bash
# 搜索技能名称
grep -A 2 "skill_name" Localization/Poedit/zh_CN.po

# 搜索英雄路径
grep -A 2 "path_" Localization/Poedit/zh_CN.po
```

### 修改流程
1. 使用Poedit打开对应.po文件
2. 搜索目标msgid
3. 修改msgstr译文
4. 保存文件
5. 编译为二进制.mo文件(如需)

### 相关文档
- 源文本: `Localization/Sources/`
- 编译工具: `Localization/BuildPotFile/`

## 数据统计

**总翻译量**: 31.5 MB (简体 + 繁体)
- 简体中文: 15.3 MB
- 繁体中文: 16.2 MB

**语言代码**:
- `zh_CN`: 简体中文(中国)
- `tw_CN`: 繁体中文(台湾)

*最后更新: 2026-01-09*
