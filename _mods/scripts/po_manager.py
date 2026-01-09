#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PO文件管理器 - 读取和回写翻译文案
用法:
  读取: python po_manager.py read <po_file> [pattern]
  回写: python po_manager.py write <po_file> <json_file>
  导出: python po_manager.py export <po_file> <json_file>

示例:
  python po_manager.py read ../Localization/Poedit/zh_CN.po "skill_name"
  python po_manager.py export ../Localization/Poedit/zh_CN.po output.json
  python po_manager.py write ../Localization/Poedit/zh_CN.po output.json
"""

import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 修复Windows控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class POEntry:
    """PO文件条目"""

    def __init__(self):
        self.msgid: str = ""
        self.msgstr: str = ""
        self.msgctxt: Optional[str] = None
        self.fuzzy: bool = False
        self.comments: List[str] = []

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'msgid': self.msgid,
            'msgstr': self.msgstr,
            'msgctxt': self.msgctxt,
            'fuzzy': self.fuzzy,
            'comments': self.comments
        }


def resolve_path(path: str) -> Path:
    """解析路径(支持相对路径和绝对路径)"""
    p = Path(path).expanduser()
    if not p.is_absolute():
        # 目录结构:
        # StreamingAssets/
        #   ├── Excel/           (工作目录)
        #   └── Localization/    (目标目录)
        # 用户输入: Poedit/zh_CN.po
        # 脚本位置: Excel/_mods/scripts/
        # 需要向上3级到StreamingAssets，再进入Localization
        base_dir = Path(__file__).parent.parent.parent.parent
        p = base_dir / 'Localization' / path
    return p.resolve()


def get_changelog_path() -> Path:
    """获取变更日志文件路径"""
    logs_dir = Path(__file__).parent.parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    return logs_dir / 'localization_changes.json'


def load_changelog() -> List[dict]:
    """加载变更日志"""
    log_path = get_changelog_path()
    if not log_path.exists():
        return []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_changelog(logs: List[dict]):
    """保存变更日志"""
    log_path = get_changelog_path()
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def log_changes(po_file: str, changes: List[dict], source_file: str = ''):
    """记录变更到日志文件"""
    if not changes:
        return

    logs = load_changelog()

    # 提取相对路径作为文件标识
    file_id = po_file
    if 'Localization' in po_file:
        file_id = po_file.split('Localization')[-1].lstrip('/\\')

    record = {
        'timestamp': datetime.now().isoformat(),
        'file': file_id,
        'source': source_file,
        'count': len(changes),
        'changes': changes
    }

    logs.append(record)
    save_changelog(logs)
    print(f'✓ 变更已记录到日志: {len(changes)} 条修改')


class POFile:
    """PO文件解析器"""

    def __init__(self, filepath: str, resolve: bool = True):
        # 自动解析路径
        if resolve and not Path(filepath).is_absolute():
            filepath = str(resolve_path(filepath))
        self.filepath = Path(filepath)
        self.entries: List[POEntry] = []
        self.metadata: Dict[str, str] = {}

    def parse(self):
        """解析PO文件"""
        if not self.filepath.exists():
            raise FileNotFoundError(f'文件不存在: {self.filepath}')

        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析元数据
        meta_match = re.search(r'"([^"]+):\s*([^"]*)\\n"', content)
        if meta_match:
            # 提取所有元数据字段
            for match in re.finditer(r'"([^"]+):\s*([^"]*)\\n"', content[:500]):
                self.metadata[match.group(1)] = match.group(2)

        # 解析条目
        entry_pattern = re.compile(
            r'(?:#.*\n)*'  # 注释
            r'(?:msgctxt\s+"([^"]*)"\n)?'  # 上下文(可选)
            r'msgid\s+"([^"]*)"\n'
            r'msgid_plural\s+"([^"]*)"\n'
            r'msgstr\[\d+\]\s+"([^"]*)"\n',
            re.MULTILINE
        )

        # 简单条目模式
        simple_pattern = re.compile(
            r'(?:#.*\n)*'  # 注释
            r'(?:msgctxt\s+"([^"]*)"\n)?'  # 上下文(可选)
            r'msgid\s+"([^"]*(?:\\n[^"]*)*)"\n'  # 支持多行
            r'msgstr\s+"([^"]*(?:\\n[^"]*)*)"\n',
            re.MULTILINE
        )

        # 查找所有条目
        for match in simple_pattern.finditer(content):
            entry = POEntry()
            entry.msgctxt = match.group(1)
            entry.msgid = match.group(2).replace('\\n', '\n').replace('\\"', '"')
            entry.msgstr = match.group(3).replace('\\n', '\n').replace('\\"', '"')

            # 检查fuzzy标记
            pos = match.start()
            lines_before = content[:pos].split('\n')
            if lines_before and '#, fuzzy' in lines_before[-1]:
                entry.fuzzy = True

            self.entries.append(entry)

        print(f'✓ 解析完成: {len(self.entries)} 个条目')

    def find(self, pattern: str, use_context: bool = False) -> List[POEntry]:
        """查找匹配的条目"""
        results = []
        regex = re.compile(pattern, re.IGNORECASE)

        for entry in self.entries:
            # 搜索msgid
            if regex.search(entry.msgid):
                results.append(entry)
                continue

            # 搜索msgstr
            if regex.search(entry.msgstr):
                results.append(entry)
                continue

            # 搜索上下文
            if use_context and entry.msgctxt and regex.search(entry.msgctxt):
                results.append(entry)

        return results

    def export_dict(self) -> dict:
        """导出为字典格式"""
        return {
            'metadata': self.metadata,
            'entries': [e.to_dict() for e in self.entries]
        }

    def import_dict(self, data: dict) -> List[dict]:
        """从字典导入并回写，返回变更记录"""
        if 'entries' not in data:
            raise ValueError('无效的JSON格式: 缺少entries字段')

        # 创建msgid到entry的映射
        entry_map = {}
        for entry in self.entries:
            key = f'{entry.msgctxt or ""}|{entry.msgid}'
            entry_map[key] = entry

        # 更新msgstr并记录变更
        updated = 0
        changes = []

        for item in data['entries']:
            msgid = item.get('msgid', '')
            msgctxt = item.get('msgctxt')
            msgstr = item.get('msgstr', '')

            key = f'{msgctxt or ""}|{msgid}'

            if key in entry_map:
                old_msgstr = entry_map[key].msgstr
                # 只记录实际变更
                if old_msgstr != msgstr:
                    entry_map[key].msgstr = msgstr
                    updated += 1
                    changes.append({
                        'msgid': msgid,
                        'msgctxt': msgctxt,
                        'old_msgstr': old_msgstr,
                        'new_msgstr': msgstr
                    })
            else:
                print(f'⚠ 警告: 未找到条目 "{msgid[:50]}..."')

        print(f'✓ 更新了 {updated} 个条目')
        return changes

    def write(self, output_path: Optional[str] = None):
        """回写到PO文件"""
        target = Path(output_path) if output_path else self.filepath

        # 备份原文件
        if target == self.filepath:
            backup = target.with_suffix('.po.bak')
            backup.write_bytes(target.read_bytes())
            print(f'✓ 已备份到: {backup}')

        # 生成PO内容
        lines = []

        # 元数据
        lines.extend([
            'msgid ""',
            'msgstr ""',
        ])
        for key, value in self.metadata.items():
            lines.append(f'"{key}: {value}\\n"')
        lines.append('')

        # 条目
        for entry in self.entries:
            # 模糊标记
            if entry.fuzzy:
                lines.append('#, fuzzy')

            # 上下文
            if entry.msgctxt:
                lines.append(f'msgctxt "{entry.msgctxt}"')

            # msgid (处理多行和转义)
            msgid_clean = entry.msgid.replace('"', '\\"').replace('\n', '\\n')
            lines.append(f'msgid "{msgid_clean}"')

            # msgstr
            msgstr_clean = entry.msgstr.replace('"', '\\"').replace('\n', '\\n')
            lines.append(f'msgstr "{msgstr_clean}"')
            lines.append('')

        # 写入文件
        content = '\n'.join(lines)
        target.write_text(content, encoding='utf-8')
        print(f'✓ 已写入: {target}')


def main():
    parser = argparse.ArgumentParser(
        description='PO文件管理器 - 读取和回写翻译文案',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 读取所有条目
  python po_manager.py read zh_CN.po

  # 搜索特定条目
  python po_manager.py read zh_CN.po "skill_name"

  # 导出为JSON
  python po_manager.py export zh_CN.po output.json

  # 从JSON回写
  python po_manager.py write zh_CN.po output.json

  # 统计信息
  python po_manager.py stats zh_CN.po

  # 查看变更日志
  python po_manager.py log

  # 查看最近的修改
  python po_manager.py log --last 5

路径说明:
  支持相对于Localization/Poedit/的路径
  例如: zh_CN.po, dlc_catacombs/zh_CN.po
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # read命令
    read_parser = subparsers.add_parser('read', help='读取PO文件')
    read_parser.add_argument('po_file', help='PO文件路径')
    read_parser.add_argument('pattern', nargs='?', help='搜索模式(可选)')

    # export命令
    export_parser = subparsers.add_parser('export', help='导出为JSON')
    export_parser.add_argument('po_file', help='PO文件路径')
    export_parser.add_argument('json_file', help='输出JSON文件路径')

    # write命令
    write_parser = subparsers.add_parser('write', help='从JSON回写')
    write_parser.add_argument('po_file', help='PO文件路径')
    write_parser.add_argument('json_file', help='输入JSON文件路径')

    # stats命令
    stats_parser = subparsers.add_parser('stats', help='统计信息')
    stats_parser.add_argument('po_file', help='PO文件路径')

    # log命令
    log_parser = subparsers.add_parser('log', help='查看变更日志')
    log_parser.add_argument('--last', type=int, help='显示最近N条记录', default=0)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # log命令不需要加载PO文件
    if args.command == 'log':
        logs = load_changelog()

        if not logs:
            print('\n📋 暂无变更记录')
            return 0

        # 过滤最近N条
        if args.last > 0:
            logs = logs[-args.last:]

        print(f'\n📋 变更日志 (共 {len(logs)} 条记录)\n')

        for i, record in enumerate(reversed(logs), 1):
            timestamp = record['timestamp'][:19].replace('T', ' ')
            print(f'[{i}] {timestamp}')
            print(f'    文件: {record["file"]}')
            print(f'    来源: {record["source"] or "直接修改"}')
            print(f'    修改数: {record["count"]}')

            # 显示详细变更
            for j, change in enumerate(record['changes'][:5], 1):
                msgid = change['msgid'][:50]
                old_msgstr = change['old_msgstr'][:30]
                new_msgstr = change['new_msgstr'][:30]
                msgctxt = change.get('msgctxt') or '无上下文'

                print(f'      [{j}] [{msgctxt}]')
                print(f'          原文: {msgid}')
                print(f'          旧译: {old_msgstr}')
                print(f'          新译: {new_msgstr}')

            if record['count'] > 5:
                print(f'      ... 还有 {record["count"] - 5} 条')

            print()

        return 0

    # 加载PO文件
    po_path = Path(args.po_file)
    if not po_path.is_absolute():
        if po_path.exists():
            # 当前目录文件，不解析
            po = POFile(str(po_path), resolve=False)
        else:
            # 尝试解析为相对路径
            po = POFile(str(po_path), resolve=True)
    else:
        po = POFile(str(po_path), resolve=False)

    try:
        po.parse()
    except FileNotFoundError as e:
        print(f'✗ 错误: {e}')
        return 1

    # 执行命令
    if args.command == 'read':
        results = po.find(args.pattern or '.*')

        print(f'\n找到 {len(results)} 个匹配条目:\n')
        for i, entry in enumerate(results[:20], 1):  # 限制显示前20个
            print(f'[{i}] {entry.msgctxt or "无上下文"}')
            print(f'    原文: {entry.msgid[:80]}')
            print(f'    译文: {entry.msgstr[:80]}')
            print()

        if len(results) > 20:
            print(f'... 还有 {len(results) - 20} 个条目\n')

    elif args.command == 'export':
        data = po.export_dict()

        with open(args.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f'✓ 已导出到: {args.json_file}')

    elif args.command == 'write':
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        changes = po.import_dict(data)
        po.write()

        # 记录变更
        log_changes(str(po.filepath), changes, args.json_file)

    elif args.command == 'stats':
        total = len(po.entries)
        translated = sum(1 for e in po.entries if e.msgstr)
        fuzzy = sum(1 for e in po.entries if e.fuzzy)
        untranslated = total - translated

        print(f'\n📊 翻译统计:')
        print(f'  总条目: {total}')
        print(f'  已翻译: {translated} ({translated/total*100:.1f}%)')
        print(f'  模糊: {fuzzy} ({fuzzy/total*100:.1f}%)')
        print(f'  未翻译: {untranslated} ({untranslated/total*100:.1f}%)')
        print(f'\n📝 元数据:')
        for key, value in po.metadata.items():
            if key in ['Language', 'Project-Id-Version', 'PO-Revision-Date']:
                print(f'  {key}: {value}')

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
