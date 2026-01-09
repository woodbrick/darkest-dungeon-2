#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英雄平衡性优化 - 状态管理工具函数
纯工具函数，不包含业务逻辑和流程控制。
状态定义和转换规则在 SKILL.md 中定义。
用法:
  python state_manager.py create <hero_code>     # 创建状态文件
  python state_manager.py query <hero_code>      # 查询状态
  python state_manager.py update <hero_code>     # 更新状态数据
  python state_manager.py list                   # 列出所有状态
  python state_manager.py archive <hero_code>    # 归档状态
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Any

# 修复Windows控制台中文乱码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# =============================================================================
# 纯工具函数
# =============================================================================

def get_state_dir() -> Path:
    """获取状态目录路径"""
    return Path(__file__).parent.parent / 'state'


def get_history_dir() -> Path:
    """获取历史记录目录路径"""
    return get_state_dir() / 'history'


def get_state_file(hero_code: str) -> Path:
    """获取状态文件路径"""
    return get_state_dir() / f'{hero_code}_balance_state.json'


def load_json(path: Path) -> Optional[Dict]:
    """加载JSON文件"""
    if not path.exists():
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'❌ 错误: 无法读取 {path}: {e}')
        return None


def save_json(path: Path, data: Dict) -> bool:
    """保存JSON文件"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'❌ 错误: 无法保存 {path}: {e}')
        return False


def create_state(hero_code: str, initial_data: Dict) -> Optional[Path]:
    """创建新状态文件

    Args:
        hero_code: 英雄代码
        initial_data: 初始状态数据（必须包含 state_id, hero_code, hero_name等）

    Returns:
        状态文件路径，失败返回None
    """
    state_file = get_state_file(hero_code)

    # 检查是否已存在
    if state_file.exists():
        print(f'⚠️  警告: {hero_code} 状态文件已存在')
        return None

    # 保存状态
    if save_json(state_file, initial_data):
        print(f'✅ 状态文件已创建: {state_file}')
        return state_file
    return None


def query_state(hero_code: str) -> Optional[Dict]:
    """查询当前状态

    Args:
        hero_code: 英雄代码

    Returns:
        状态数据，不存在返回None
    """
    return load_json(get_state_file(hero_code))


def update_state_file(hero_code: str, updates: Dict) -> bool:
    """更新状态文件数据

    Args:
        hero_code: 英雄代码
        updates: 要更新的字段（支持嵌套更新）

    Returns:
        成功返回True，失败返回False
    """
    state = query_state(hero_code)
    if not state:
        return False

    # 递归更新字典
    def deep_update(target: Dict, source: Dict) -> Dict:
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                deep_update(target[key], value)
            else:
                target[key] = value
        return target

    # 更新数据
    deep_update(state, updates)
    state['last_update'] = datetime.now().isoformat()

    # 保存
    return save_json(get_state_file(hero_code), state)


def archive_state(hero_code: str) -> bool:
    """归档状态文件到历史记录

    Args:
        hero_code: 英雄代码

    Returns:
        成功返回True，失败返回False
    """
    state = query_state(hero_code)
    if not state:
        return False

    state_file = get_state_file(hero_code)
    history_dir = get_history_dir()
    history_dir.mkdir(parents=True, exist_ok=True)

    archive_file = history_dir / f"{state['state_id']}.json"

    try:
        state_file.rename(archive_file)
        print(f'✅ 状态已归档: {archive_file}')
        return True
    except Exception as e:
        print(f'❌ 错误: 无法归档 {state_file}: {e}')
        return False


def list_all_states() -> List[Dict]:
    """列出所有状态文件

    Returns:
        状态数据列表
    """
    states = []
    state_dir = get_state_dir()

    if not state_dir.exists():
        return states

    for state_file in state_dir.glob('*_balance_state.json'):
        state = load_json(state_file)
        if state:
            states.append(state)

    return states


def display_state(hero_code: str) -> None:
    """显示状态信息

    Args:
        hero_code: 英雄代码
    """
    state = query_state(hero_code)
    if not state:
        print(f'❌ 错误: 未找到 {hero_code} 的状态文件')
        return

    print(f'\n{"="*60}')
    print(f'英雄: {state.get("hero_name", "N/A")} ({state.get("hero_code", "N/A")})')
    print(f'当前状态: {state.get("current_state", "N/A")}')
    print(f'开始时间: {state.get("start_time", "N/A")[:19].replace("T", " ")}')
    print(f'最后更新: {state.get("last_update", "N/A")[:19].replace("T", " ")}')

    if 'context' in state and state['context']:
        print(f'\n上下文:')
        for key, value in state['context'].items():
            if isinstance(value, dict):
                print(f'  {key}:')
                for k, v in value.items():
                    print(f'    {k}: {v}')
            else:
                print(f'  {key}: {value}')

    if 'transitions' in state and state['transitions']:
        print(f'\n状态转换历史:')
        for trans in state['transitions']:
            timestamp = trans['timestamp'][:19].replace("T", " ")
            print(f'  {timestamp}: {trans["from"]} → {trans["to"]}')

    print('='*60)


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == 'create':
        if len(sys.argv) < 3:
            print('用法: python state_manager.py create <hero_code>')
            return
        hero_code = sys.argv[2].lower()

        # 示例：创建初始状态
        from datetime import datetime
        state_id = f"{hero_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        initial_data = {
            'state_id': state_id,
            'hero_code': hero_code,
            'hero_name': f'Hero_{hero_code.upper()}',
            'current_state': 'IDLE',
            'start_time': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'context': {},
            'transitions': [],
            'checkpoints': {}
        }
        create_state(hero_code, initial_data)

    elif command == 'query':
        if len(sys.argv) < 3:
            # 列出所有状态
            states = list_all_states()
            if not states:
                print('✅ 无状态文件')
                return

            print(f'\n发现 {len(states)} 个状态文件:\n')
            for state in states:
                print(f'  • {state.get("hero_name", "N/A")} ({state.get("hero_code", "N/A")})')
                print(f'    状态: {state.get("current_state", "N/A")}')
                print(f'    开始: {state.get("start_time", "N/A")[:19].replace("T", " ")}')
                print()
            return

        hero_code = sys.argv[2].lower()
        display_state(hero_code)

    elif command == 'update':
        if len(sys.argv) < 4:
            print('用法: python state_manager.py update <hero_code> <json_updates>')
            return
        hero_code = sys.argv[2].lower()
        try:
            updates = json.loads(sys.argv[3])
            update_state_file(hero_code, updates)
        except json.JSONDecodeError as e:
            print(f'❌ 错误: 无效的JSON格式: {e}')

    elif command == 'list':
        states = list_all_states()
        if not states:
            print('✅ 无状态文件')
            return

        print(f'\n发现 {len(states)} 个状态文件:\n')
        for state in states:
            print(f'  • {state.get("hero_name", "N/A")} ({state.get("hero_code", "N/A")})')
            print(f'    状态: {state.get("current_state", "N/A")}')
            print(f'    开始: {state.get("start_time", "N/A")[:19].replace("T", " ")}')
            print()

    elif command == 'archive':
        if len(sys.argv) < 3:
            print('用法: python state_manager.py archive <hero_code>')
            return
        hero_code = sys.argv[2].lower()
        archive_state(hero_code)

    else:
        print(f'❌ 未知命令: {command}')
        print(__doc__)


if __name__ == '__main__':
    main()
