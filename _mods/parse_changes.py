#!/usr/bin/env python3
"""
解析英雄技能改动脚本
基于 git diff 输出生成结构化的改动数据
"""

import subprocess
import re
import json
from collections import defaultdict

def get_git_diff(file_path):
    """获取文件的 git diff"""
    result = subprocess.run(
        ['git', 'diff', file_path],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return result.stdout

def parse_hero_diff(diff_text):
    """解析英雄的 git diff"""
    lines = diff_text.split('\n')

    changes = {
        'base_stats': {},
        'skills': {}
    }

    current_element = None
    current_section = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检测新的 element_start
        if line.startswith('element_start,'):
            parts = line.split(',')
            if len(parts) >= 2:
                current_element = parts[1]
                # 判断是英雄基础数据还是技能
                if current_element.startswith('hel_'):
                    changes['skills'][current_element] = {
                        'changes': []
                    }
                elif current_element == 'hellion':
                    current_section = 'base_stats'
                    changes['base_stats'] = {}

        # 解析基础属性
        elif current_section == 'base_stats' and line.startswith('add_stats,'):
            # 查找下一行看是否有修改
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('+add_stats,'):
                    # 提取旧的属性值
                    old_vals = line.split(',')[1:]
                    # 提取新的属性值
                    new_vals = next_line.split(',')[1:]
                    # 映射属性名（从 key_map 行获取）
                    changes['base_stats']['raw_old'] = old_vals
                    changes['base_stats']['raw_new'] = new_vals

        # 解析技能改动
        elif current_element and current_element.startswith('hel_'):
            # 检测属性修改 (health_damage, crit_chance 等)
            if line.startswith('-') and 'add_stats,' in line:
                old_vals = line.split(',')[1:]
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('+add_stats,'):
                        new_vals = next_line.split(',')[1:]
                        changes['skills'][current_element]['changes'].append({
                            'type': 'stats',
                            'old': old_vals,
                            'new': new_vals
                        })

            # 检测效果修改 (target_effects)
            elif line.startswith('-target_effects,'):
                old_effects = line[len('-target_effects,'):].split(',')
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('+target_effects,'):
                        new_effects = next_line[len('+target_effects,'):].split(',')
                        changes['skills'][current_element]['changes'].append({
                            'type': 'target_effects',
                            'old': old_effects,
                            'new': new_effects
                        })

            # 检测目标范围修改
            elif line.startswith('-target_ranks,'):
                old_ranks = line.split(',')[1:]
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('+target_ranks,'):
                        new_ranks = next_line.split(',')[1:]
                        changes['skills'][current_element]['changes'].append({
                            'type': 'target_ranks',
                            'old': old_ranks,
                            'new': new_ranks
                        })

            # 检测新增效果行
            elif line.startswith('+target_effects,') and not (i > 0 and lines[i-1].strip().startswith('-target_effects,')):
                effects = line[len('+target_effects,'):].split(',')
                changes['skills'][current_element]['changes'].append({
                    'type': 'new_target_effects',
                    'effects': effects
                })

        i += 1

    return changes

def analyze_hero(hero_code):
    """分析指定英雄"""
    file_path = f'hero_{hero_code}_data_export.Group.csv'
    print(f"分析 {file_path}...")

    diff_text = get_git_diff(file_path)

    if not diff_text.strip():
        print(f"  没有检测到改动")
        return None

    changes = parse_hero_diff(diff_text)

    # 保存为 JSON
    output_file = f'_mods/{hero_code}_changes_raw.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(changes, f, ensure_ascii=False, indent=2)

    print(f"  保存到 {output_file}")
    return changes

if __name__ == '__main__':
    import sys
    hero_code = sys.argv[1] if len(sys.argv) > 1 else 'hel'
    analyze_hero(hero_code)
