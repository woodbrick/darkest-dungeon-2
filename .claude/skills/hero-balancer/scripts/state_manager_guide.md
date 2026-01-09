# state_manager.py 工具函数指南

`state_manager.py` 提供纯工具函数，不包含业务逻辑。状态定义和转换规则在 [SKILL.md](../SKILL.md) 中定义。

---

## 函数列表

### 核心函数

| 函数名 | 签名 | 说明 |
|--------|------|------|
| `create_state()` | `create_state(hero_code: str, initial_data: Dict) -> Optional[Path]` | 创建新状态文件 |
| `query_state()` | `query_state(hero_code: str) -> Optional[Dict]` | 查询当前状态 |
| `update_state_file()` | `update_state_file(hero_code: str, updates: Dict) -> bool` | 更新状态数据 |
| `archive_state()` | `archive_state(hero_code: str) -> bool` | 归档状态文件 |

### 辅助函数

| 函数名 | 签名 | 说明 |
|--------|------|------|
| `load_json()` | `load_json(path: Path) -> Optional[Dict]` | 加载JSON文件 |
| `save_json()` | `save_json(path: Path, data: Dict) -> bool` | 保存JSON文件 |
| `list_all_states()` | `list_all_states() -> List[Dict]` | 列出所有状态 |
| `display_state()` | `display_state(hero_code: str) -> None` | 显示状态信息 |

---

## 命令行用法

### 创建状态
```bash
python _mods/scripts/state_manager.py create <hero_code>
```

### 查询状态
```bash
# 查询单个英雄
python _mods/scripts/state_manager.py query <hero_code>

# 列出所有状态
python _mods/scripts/state_manager.py query
```

### 更新状态
```bash
python _mods/scripts/state_manager.py update <hero_code> '{"current_state": "COLLECTING"}'
```

### 列出状态
```bash
python _mods/scripts/state_manager.py list
```

### 归档状态
```bash
python _mods/scripts/state_manager.py archive <hero_code>
```

---

## 状态文件结构

```json
{
  "state_id": "bh_20260109_150430",
  "hero_code": "bh",
  "hero_name": "Bounty Hunter",
  "current_state": "AWAITING_CONFIRMATION",
  "start_time": "2026-01-09T15:04:30",
  "last_update": "2026-01-09T15:10:22",
  "context": {
    "weak_skills": ["bh_caltrops", "bh_hurlbat"],
    "coverage": 0.735
  },
  "transitions": [
    {
      "from": "IDLE",
      "to": "COLLECTING",
      "timestamp": "2026-01-09T15:04:30"
    }
  ],
  "checkpoints": {
    "collecting_done": true,
    "analyzing_done": true
  }
}
```

---

## 架构原则

### ✅ 应该做的
- SKILL.md: 定义状态转换规则、验证条件、流程控制逻辑
- scripts/: 提供纯工具函数（JSON操作、文件操作）

### ❌ 不应该做的
- scripts/: 不包含状态定义、转换规则、业务逻辑

---

## 使用示例

### 示例1: 创建初始状态
```python
from datetime import datetime
from _mods.scripts.state_manager import create_state

hero_code = 'bh'
state_id = f"{hero_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
initial_data = {
    'state_id': state_id,
    'hero_code': hero_code,
    'hero_name': 'Bounty Hunter',
    'current_state': 'IDLE',
    'start_time': datetime.now().isoformat(),
    'last_update': datetime.now().isoformat(),
    'context': {},
    'transitions': [],
    'checkpoints': {}
}

create_state(hero_code, initial_data)
```

### 示例2: 更新状态
```python
from _mods.scripts.state_manager import update_state_file

# 更新当前状态和上下文
updates = {
    'current_state': 'ANALYZING',
    'context': {
        'coverage': 0.735,
        'weak_skills': ['bh_caltrops', 'bh_hurlbat']
    }
}

update_state_file('bh', updates)
```

### 示例3: 查询和归档
```python
from _mods.scripts.state_manager import query_state, archive_state

# 查询状态
state = query_state('bh')
print(f"Current state: {state['current_state']}")

# 归档完成的流程
if state['current_state'] == 'DONE':
    archive_state('bh')
```

---

**相关文档**:
- [SKILL.md](../SKILL.md) - 状态转换流程定义
- [state_persistence.md](../references/state_persistence.md) - 状态持久化详解
