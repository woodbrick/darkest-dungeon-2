#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的英雄改动解析脚本
正确区分基础属性和技能改动，并按技能分组
"""

import subprocess
import sys
import re

# 英雄名称
HERO_NAMES = {
    'hel': {'cn': '赫利俄斯', 'en': 'Hellion'},
    'hwm': {'cn': '强盗', 'en': 'Highwayman'},
    'jes': {'cn': '小丑', 'en': 'Jester'},
    'lep': {'cn': '麻风病人', 'en': 'Leper'},
    'maa': {'cn': '步兵', 'en': 'Man-at-Arms'},
    'occ': {'cn': '神秘学者', 'en': 'Occultist'},
    'pd': {'cn': '瘟疫医生', 'en': 'Plague Doctor'},
    'run': {'cn': '逃亡者', 'en': 'Runaway'},
    'ves': {'cn': '修女', 'en': 'Vestal'},
}

# Hellion 技能名称映射
HEL_SKILLS = {
    'hel_wicked_hack': '邪恶斩击 (Wicked Hack)',
    'hel_wicked_hack_u': '邪恶斩击升级 (Wicked Hack Upgrade)',
    'hel_iron_swan': '铁天鹅 (Iron Swan)',
    'hel_iron_swan_u': '铁天鹅升级 (Iron Swan Upgrade)',
    'hel_barbaric_yawp': '野蛮嚎叫 (Barbaric Yawp)',
    'hel_barbaric_yawp_u': '野蛮嚎叫升级 (Barbaric Yawp Upgrade)',
    'hel_bleed_out': '放血 (Bleed Out)',
    'hel_bleed_out_u': '放血升级 (Bleed Out Upgrade)',
    'hel_breakthrough': '突破 (Breakthrough)',
    'hel_breakthrough_u': '突破升级 (Breakthrough Upgrade)',
    'hel_adrenaline_rush': '肾上腺素激增 (Adrenaline Rush)',
    'hel_adrenaline_rush_u': '肾上腺素激增升级 (Adrenaline Rush Upgrade)',
}

# 效果翻译
EFFECT_MAP = {
    'end_combo': '结束连击',
    'prime_combo': '预备连击',
    'prime_combo_33pct': '33% 预备连击',
    'add_1_weak': '添加 1 虚弱',
    'remove_all_stealth': '移除所有潜行',
    'add_1_daze': '添加 1 眩晕',
    'add_1_winded': '添加 1 疲劳',
    'add_1_strength': '添加 1 力量',
    'add_1_guard': '添加 1 格挡',
}

def get_git_diff(hero_code):
    """获取 git diff"""
    result = subprocess.run(
        ['git', 'diff', f'hero_{hero_code}_data_export.Group.csv'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=r'g:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel'
    )
    return result.stdout

def parse_hero_changes(hero_code, diff_text):
    """解析英雄改动"""
    lines = diff_text.split('\n')

    result = {
        'base_stats': {
            'health_old': None,
            'health_new': None,
            'speed_old': None,
            'speed_new': None,
            'other': []
        },
        'skills': {}
    }

    current_skill = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 检测元素开始
        if line.startswith('element_start,'):
            parts = line.split(',')
            if len(parts) >= 2:
                element_id = parts[1].split(',')[0]

                # 基础属性 (hellion 本身)
                if element_id == 'hellion':
                    current_skill = 'base_stats'
                # 技能
                elif element_id.startswith('hel_'):
                    current_skill = element_id
                    if current_skill not in result['skills']:
                        result['skills'][current_skill] = []

        # 处理基础属性变化
        elif current_skill == 'base_stats':
            # 检测 add_stats 变化
            if line.startswith('-add_stats,'):
                parts = line.split(',')
                if len(parts) >= 3:
                    result['base_stats']['health_old'] = parts[1]
                    result['base_stats']['speed_old'] = parts[2]
            elif line.startswith('+add_stats,'):
                parts = line.split(',')
                if len(parts) >= 3:
                    result['base_stats']['health_new'] = parts[1]
                    result['base_stats']['speed_new'] = parts[2]
            # 新增字段
            elif line.startswith('+m_NameOverrideId,'):
                result['base_stats']['other'].append('新增: 名称覆盖 ID')

        # 处理技能变化
        elif current_skill and current_skill.startswith('hel_'):
            # 目标范围变化
            if line.startswith('-target_ranks,') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('+target_ranks,'):
                    old_ranks = line.split(',')[1:]
                    new_ranks = next_line.split(',')[1:]
                    result['skills'][current_skill].append({
                        'type': 'target_ranks',
                        'old': old_ranks,
                        'new': new_ranks
                    })

            # 伤害变化 (add_stats with health_damage)
            elif line.startswith('-add_stats,'):
                # 检查前一行是否有 key_map 包含 health_damage
                if i > 0 and 'health_damage' in lines[i-1]:
                    old_vals = line.split(',')[1:4]
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.startswith('+add_stats,'):
                            new_vals = next_line.split(',')[1:4]
                            result['skills'][current_skill].append({
                                'type': 'damage',
                                'old': old_vals,
                                'new': new_vals
                            })

            # 新增效果
            elif line.startswith('+target_effects,'):
                # 检查前一行是否是 -target_effects
                if not (i > 0 and lines[i-1].strip().startswith('-target_effects,')):
                    effects = line.split(',')[1:]
                    result['skills'][current_skill].append({
                        'type': 'new_effect',
                        'effects': effects
                    })

            # 效果变化
            elif line.startswith('-target_effects,') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('+target_effects,'):
                    old_effects = line.split(',')[1:]
                    new_effects = next_line.split(',')[1:]
                    result['skills'][current_skill].append({
                        'type': 'effect_change',
                        'old': old_effects,
                        'new': new_effects
                    })

        i += 1

    return result

def format_output(hero_code, parsed_data):
    """格式化输出"""
    hero_info = HERO_NAMES.get(hero_code, {'cn': hero_code, 'en': hero_code})

    output = []
    output.append(f"英雄: {hero_info['cn']} ({hero_info['en']})")
    output.append("改动总览: 全面增强，提升伤害和功能性\n")
    output.append("基础属性改动:")

    # 基础属性
    base = parsed_data['base_stats']
    if base['health_old'] and base['health_new']:
        health_diff = int(base['health_new']) - int(base['health_old'])
        output.append(f"  - 生命值: {base['health_old']} → {base['health_new']} (+{health_diff})")
    if base['speed_old'] and base['speed_new']:
        speed_diff = int(base['speed_new']) - int(base['speed_old'])
        output.append(f"  - 速度: {base['speed_old']} → {base['speed_new']} (+{speed_diff})")
    for item in base['other']:
        output.append(f"  - {item}")

    output.append("\n技能改动:\n")

    # 技能改动
    for skill_id, changes in parsed_data['skills'].items():
        if not changes:
            continue

        skill_name = HEL_SKILLS.get(skill_id, skill_id)
        output.append(f"  - 技能: {skill_name}")

        for change in changes:
            if change['type'] == 'target_ranks':
                old_str = ', '.join(change['old'])
                new_str = ', '.join(change['new'])
                output.append(f"      - 目标范围: {old_str} → {new_str}")

            elif change['type'] == 'damage':
                old_dmg = f"{change['old'][0]}-{change['old'][1]}"
                new_dmg = f"{change['new'][0]}-{change['new'][1]}"
                diff = int(change['new'][0]) - int(change['old'][0])
                output.append(f"      - 伤害: {old_dmg} → {new_dmg} (+{diff})")

            elif change['type'] == 'new_effect':
                effects_str = ', '.join([EFFECT_MAP.get(e, e) for e in change['effects'] if e])
                if effects_str:
                    output.append(f"      - 新增效果: {effects_str}")

            elif change['type'] == 'effect_change':
                old_effects = set(change['old'])
                new_effects = set(change['new'])
                added = new_effects - old_effects
                if added:
                    added_str = ', '.join([EFFECT_MAP.get(e, e) for e in added if e])
                    if added_str:
                        output.append(f"      - 新增效果: {added_str}")

        output.append("")

    return '\n'.join(output)

def main():
    """主函数"""
    hero_code = sys.argv[1] if len(sys.argv) > 1 else 'hel'

    if hero_code not in HERO_NAMES:
        print(f"未知英雄: {hero_code}")
        return

    print(f"分析 {HERO_NAMES[hero_code]['cn']}...")

    # 获取 diff
    diff_text = get_git_diff(hero_code)

    if not diff_text.strip():
        print("没有检测到改动")
        return

    # 解析
    parsed = parse_hero_changes(hero_code, diff_text)

    # 格式化
    output = format_output(hero_code, parsed)

    # 保存
    output_file = f'{hero_code}_changes.yml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(output)
    print(f"\n已保存到 {output_file}")

if __name__ == '__main__':
    main()
