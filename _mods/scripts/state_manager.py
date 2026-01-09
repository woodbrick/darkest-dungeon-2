#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英雄平衡性优化状态机管理器
用法:
  python state_manager.py init <hero_code>     # 初始化状态
  python state_manager.py update <state>       # 更新状态
  python state_manager.py get                  # 获取当前状态
  python state_manager.py resume               # 恢复未完成流程
  python state_manager.py list                 # 列出所有未完成流程
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# 修复Windows控制台中文乱码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class StateManager:
    """状态机管理器"""

    # 状态定义
    STATES = [
        'IDLE',
        'COLLECTING',
        'ANALYZING',
        'SUPPLEMENTING_EFFECTS',
        'PROPOSING',
        'AWAITING_CONFIRMATION',
        'IMPLEMENTING',
        'VERIFYING',
        'COMMITTING',
        'DONE',
        'CANCELLED'
    ]

    # 英雄名称映射
    HERO_NAMES = {
        'bh': 'Bounty Hunter',
        'cru': 'Crusader',
        'dul': 'Duelist',
        'flg': 'Flagellant',
        'gr': 'Grave Robber',
        'hel': 'Hellion',
        'hwm': 'Highwayman',
        'jes': 'Jester',
        'lep': 'Leper',
        'maa': 'Man-at-Arms',
        'occ': 'Occultist',
        'pd': 'Plague Doctor',
        'run': 'Runaway',
        'ves': 'Vestal',
        'abm': 'Alchemist'
    }

    def __init__(self):
        self.state_dir = Path(__file__).parent.parent / 'state'
        self.history_dir = self.state_dir / 'history'
        self.state_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)

    def get_state_file(self, hero_code: str) -> Path:
        """获取状态文件路径"""
        return self.state_dir / f'{hero_code}_balance_state.json'

    def init_state(self, hero_code: str) -> Dict:
        """初始化状态"""
        if hero_code not in self.HERO_NAMES:
            print(f'❌ 错误: 未知英雄代码 {hero_code}')
            return None

        state_file = self.get_state_file(hero_code)

        # 检查是否已存在未完成流程
        if state_file.exists():
            print(f'⚠️  警告: {hero_code} 已存在未完成流程')
            choice = input('是否覆盖？(y/N): ').strip().lower()
            if choice != 'y':
                return None

        # 创建新状态
        state_id = f"{hero_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        state = {
            'state_id': state_id,
            'hero_code': hero_code,
            'hero_name': self.HERO_NAMES[hero_code],
            'current_state': 'IDLE',
            'start_time': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'context': {},
            'transitions': [],
            'checkpoints': {}
        }

        self._save_state(state_file, state)
        print(f'✅ 状态文件已创建: {state_file}')
        return state

    def load_state(self, hero_code: str) -> Optional[Dict]:
        """加载状态"""
        state_file = self.get_state_file(hero_code)
        if not state_file.exists():
            print(f'❌ 错误: 未找到 {hero_code} 的状态文件')
            return None

        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def update_state(self, hero_code: str, new_state: str, **context_updates) -> bool:
        """更新状态"""
        if new_state not in self.STATES:
            print(f'❌ 错误: 无效状态 {new_state}')
            return False

        state = self.load_state(hero_code)
        if not state:
            return False

        old_state = state['current_state']

        # 记录转换
        state['transitions'].append({
            'from': old_state,
            'to': new_state,
            'timestamp': datetime.now().isoformat()
        })

        # 更新状态
        state['current_state'] = new_state
        state['last_update'] = datetime.now().isoformat()

        # 更新上下文
        if context_updates:
            state['context'].update(context_updates)

        # 更新检查点
        state['checkpoints'][f'{new_state.lower()}_done'] = True

        # 保存
        state_file = self.get_state_file(hero_code)
        self._save_state(state_file, state)

        print(f'✅ 状态更新: {old_state} → {new_state}')
        return True

    def archive_state(self, hero_code: str) -> bool:
        """归档状态到历史记录"""
        state = self.load_state(hero_code)
        if not state:
            return False

        state_file = self.get_state_file(hero_code)
        archive_file = self.history_dir / f"{state['state_id']}.json"

        # 移动文件
        state_file.rename(archive_file)
        print(f'✅ 状态已归档: {archive_file}')
        return True

    def list_unfinished(self) -> List[Dict]:
        """列出所有未完成流程"""
        unfinished = []

        for state_file in self.state_dir.glob('*_balance_state.json'):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    unfinished.append(state)
            except Exception as e:
                print(f'⚠️  警告: 无法读取 {state_file.name}: {e}')

        return unfinished

    def display_state(self, hero_code: str):
        """显示状态信息"""
        state = self.load_state(hero_code)
        if not state:
            return

        print(f'\n{"="*60}')
        print(f'英雄: {state["hero_name"]} ({state["hero_code"]})')
        print(f'当前状态: {state["current_state"]}')
        print(f'开始时间: {state["start_time"][:19].replace("T", " ")}')
        print(f'最后更新: {state["last_update"][:19].replace("T", " ")}')

        if state['context']:
            print(f'\n上下文:')
            for key, value in state['context'].items():
                if isinstance(value, dict):
                    print(f'  {key}:')
                    for k, v in value.items():
                        print(f'    {k}: {v}')
                else:
                    print(f'  {key}: {value}')

        if state['transitions']:
            print(f'\n状态转换历史:')
            for trans in state['transitions']:
                timestamp = trans['timestamp'][:19].replace("T", " ")
                print(f'  {timestamp}: {trans["from"]} → {trans["to"]}')

        print('='*60)

    def _save_state(self, state_file: Path, state: Dict):
        """保存状态到文件"""
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    manager = StateManager()
    command = sys.argv[1]

    if command == 'init':
        if len(sys.argv) < 3:
            print('用法: python state_manager.py init <hero_code>')
            return
        hero_code = sys.argv[2].lower()
        manager.init_state(hero_code)

    elif command == 'update':
        if len(sys.argv) < 4:
            print('用法: python state_manager.py update <hero_code> <new_state>')
            return
        hero_code = sys.argv[2].lower()
        new_state = sys.argv[3]
        manager.update_state(hero_code, new_state)

    elif command == 'get':
        if len(sys.argv) < 3:
            # 列出所有未完成流程
            unfinished = manager.list_unfinished()
            if not unfinished:
                print('✅ 无未完成流程')
                return

            print(f'\n发现 {len(unfinished)} 个未完成流程:\n')
            for state in unfinished:
                print(f'  • {state["hero_name"]} ({state["hero_code"]})')
                print(f'    状态: {state["current_state"]}')
                print(f'    开始: {state["start_time"][:19].replace("T", " ")}')
                print()
            return

        hero_code = sys.argv[2].lower()
        manager.display_state(hero_code)

    elif command == 'list':
        unfinished = manager.list_unfinished()
        if not unfinished:
            print('✅ 无未完成流程')
            return

        print(f'\n发现 {len(unfinished)} 个未完成流程:\n')
        for state in unfinished:
            print(f'  • {state["hero_name"]} ({state["hero_code"]})')
            print(f'    状态: {state["current_state"]}')
            print(f'    开始: {state["start_time"][:19].replace("T", " ")}')
            print()

    elif command == 'archive':
        if len(sys.argv) < 3:
            print('用法: python state_manager.py archive <hero_code>')
            return
        hero_code = sys.argv[2].lower()
        manager.archive_state(hero_code)

    else:
        print(f'❌ 未知命令: {command}')
        print(__doc__)


if __name__ == '__main__':
    main()
