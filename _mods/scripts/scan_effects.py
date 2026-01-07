#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 effect_data_export.Group.csv 文件，提取所有可用的效果标记
"""

import csv
import re
import sys
import io
from collections import defaultdict
from pathlib import Path

# 修复Windows控制台中文乱码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 文件路径
EFFECT_FILE = Path("g:/Darkest Dungeon II/Darkest Dungeon II_Data/StreamingAssets/Excel/effect_data_export.Group.csv")
OUTPUT_FILE = Path("_mods/available_effects.md")

def parse_element(lines, start_idx):
    """解析一个元素，返回元素ID和字段字典"""
    element_id = None
    element_type = None
    fields = {}

    i = start_idx
    if i < len(lines) and lines[i].strip().startswith('element_start,'):
        # 解析 element_start 行
        parts = lines[i].strip().split(',')
        if len(parts) >= 3:
            element_id = parts[1].strip()
            element_type = parts[2].strip()
        i += 1

        # 解析字段行，直到 element_end
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('element_end'):
                break
            if ',' in line and not line.startswith('#'):
                parts = line.split(',', 1)
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name and field_value:
                        # 如果字段已存在，转换为列表
                        if field_name in fields:
                            if not isinstance(fields[field_name], list):
                                fields[field_name] = [fields[field_name]]
                            fields[field_name].append(field_value)
                        else:
                            fields[field_name] = field_value
            i += 1

    return element_id, element_type, fields

def categorize_effect(effect_id):
    """根据效果ID前缀分类"""
    categories = {
        'add_': '增益/减益效果',
        'remove_all_': '移除效果',
        'move_': '移动效果',
        'heal_': '治疗效果',
        'hot_': '持续治疗(HoT)',
        'stress_': '压力效果',
        'skill_dot_': 'DoT效果',
        'prime_combo': '连击系统',
        'end_combo': '连击系统',
        'combo_': '连击系统(Buff)',
    }

    for prefix, category in categories.items():
        if effect_id.startswith(prefix):
            return category
    return '其他效果'

def scan_effects():
    """扫描效果文件"""
    print(f"正在扫描: {EFFECT_FILE}")

    with open(EFFECT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    effects = defaultdict(list)

    i = 0
    while i < len(lines):
        element_id, element_type, fields = parse_element(lines, i)
        if element_id:
            category = categorize_effect(element_id)
            effects[category].append(element_id)

            # 跳过到下一个元素
            while i < len(lines) and not lines[i].strip().startswith('element_start,'):
                i += 1
        else:
            i += 1

    # 按类别排序
    category_order = [
        '增益/减益效果',
        '治疗效果',
        '持续治疗(HoT)',
        'DoT效果',
        '压力效果',
        '移动效果',
        '移除效果',
        '连击系统',
        '连击系统(Buff)',
        '其他效果',
    ]

    # 输出到文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 可用效果标记列表\n\n")
        f.write(f"*扫描文件*: `effect_data_export.Group.csv`\n\n")
        f.write("---\n\n")

        for category in category_order:
            if category in effects and effects[category]:
                f.write(f"## {category}\n\n")

                # 排序并去重
                unique_effects = sorted(set(effects[category]))

                # 按前缀分组
                groups = defaultdict(list)
                for effect in unique_effects:
                    # 获取主要前缀用于分组
                    if '_' in effect:
                        prefix = effect.split('_')[0] + '_'
                    else:
                        prefix = 'other'
                    groups[prefix].append(effect)

                # 输出分组
                for prefix in sorted(groups.keys()):
                    f.write(f"### {prefix.rstrip('_')} 系列\n\n")
                    for effect in sorted(groups[prefix]):
                        f.write(f"- `{effect}`\n")
                    f.write("\n")

                f.write("---\n\n")

    print(f"扫描完成! 共找到 {sum(len(v) for v in effects.values())} 个效果")
    print(f"输出文件: {OUTPUT_FILE}")

    # 打印统计
    print("\n效果统计:")
    for category in category_order:
        if category in effects:
            print(f"  {category}: {len(effects[category])}")

    return effects

if __name__ == '__main__':
    scan_effects()
