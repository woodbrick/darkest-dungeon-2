# 状态持久化

## 状态文件结构

**文件位置**: `_mods/state/{hero_code}_balance_state.json`

```json
{
  "state_id": "bh_20260109_150430",
  "hero_code": "bh",
  "hero_name": "Bounty Hunter",
  "current_state": "AWAITING_CONFIRMATION",
  "start_time": "2026-01-09T15:04:30",
  "last_update": "2026-01-09T15:10:22",
  "context": {},
  "transitions": [],
  "checkpoints": {}
}
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `state_id` | 唯一标识：`{hero_code}_{timestamp}` |
| `hero_code` | 英雄代码 |
| `current_state` | 当前状态 |
| `context` | 工作数据（解析输出、覆盖率等） |
| `transitions` | 状态转换历史 |
| `checkpoints` | 已完成阶段标记 |

## 状态目录

```
_mods/state/
├── bh_balance_state.json          # 活跃状态
└── history/                       # 归档历史
    ├── bh_20260108_102030.json
    └── bh_20260109_150430.json
```

## 常用命令

```bash
# 创建状态
python _mods/scripts/state_manager.py create <hero_code>

# 查询状态
python _mods/scripts/state_manager.py query <hero_code>

# 更新状态
python _mods/scripts/state_manager.py update <hero_code> '{"current_state": "ANALYZING"}'

# 列出所有状态
python _mods/scripts/state_manager.py list

# 归档状态
python _mods/scripts/state_manager.py archive <hero_code>
```

---

**相关文档**:
- [SKILL.md](../SKILL.md) - 状态转换流程
- [workflow_recovery.md](workflow_recovery.md) - 流程恢复详解
