#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英雄技能改动分析脚本
基于 git diff 生成结构化的改动总结
"""

import subprocess
import sys
import json

# 英雄配置
HEROES = {
    'hel': {'name': '赫利俄斯', 'en': 'Hellion'},
    'hwm': {'name': '强盗', 'en': 'Highwayman'},
    'jes': {'name': '小丑', 'en': 'Jester'},
    'lep': {'name': '麻风病人', 'en': 'Leper'},
    'maa': {'name': '步兵', 'en': 'Man-at-Arms'},
    'occ': {'name': '神秘学者', 'en': 'Occultist'},
    'pd': {'name': '瘟疫医生', 'en': 'Plague Doctor'},
    'run': {'name': '逃亡者', 'en': 'Runaway'},
    'ves': {'name': '修女', 'en': 'Vestal'},
}

def get_git_diff(hero_code):
    """获取指定英雄的 git diff"""
    file_path = f'hero_{hero_code}_data_export.Group.csv'
    # 切换到正确的目录
    result = subprocess.run(
        ['git', 'diff', file_path],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=r'g:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel'
    )
    return result.stdout

def extract_changes(hero_code, diff_text):
    """从 diff 文本中提取改动"""
    lines = diff_text.split('\n')

    changes = {
        'base_stats': {},
        'skills': {},
        'raw_changes': []  # 保存原始改动行供后续翻译
    }

    i = 0
    current_skill = None

    while i < len(lines):
        line = lines[i].strip()

        # 跳过空行和 diff 头部
        if not line or line.startswith('diff') or line.startswith('index') or line.startswith('---') or line.startswith('+++'):
            i += 1
            continue

        # 记录所有修改行
        if line.startswith('-') or line.startswith('+'):
            # 保存原始改动
            changes['raw_changes'].append({
                'line': line,
                'line_num': i,
                'context_prev': lines[i-1] if i > 0 else '',
                'context_next': lines[i+1] if i+1 < len(lines) else '',
            })

        i += 1

    return changes

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python analyze_changes.py <hero_code>")
        print("示例: python analyze_changes.py hel")
        sys.exit(1)

    hero_code = sys.argv[1]

    if hero_code not in HEROES:
        print(f"未知英雄代码: {hero_code}")
        print(f"支持的英雄: {', '.join(HEROES.keys())}")
        sys.exit(1)

    print(f"分析 {HEROES[hero_code]['name']} ({hero_code})...")

    # 获取 diff
    diff_text = get_git_diff(hero_code)

    if not diff_text.strip():
        print("没有检测到改动")
        return

    # 提取改动
    changes = extract_changes(hero_code, diff_text)

    # 保存原始数据
    output_file = f'{hero_code}_changes_raw.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(changes, f, ensure_ascii=False, indent=2)

    print(f"原始改动数据已保存到: {output_file}")
    print(f"共找到 {len(changes['raw_changes'])} 行改动")

    # 显示前20行改动供检查
    print("\n前20行改动:")
    for i, change in enumerate(changes['raw_changes'][:20]):
        print(f"{i+1}. {change['line']}")

if __name__ == '__main__':
    main()
