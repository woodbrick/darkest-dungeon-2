#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用技能解析评估脚本
用法: python parse_universal.py <英雄代码>
示例: python parse_universal.py jes
"""

import csv
import sys
from pathlib import Path

# 效果DU价值表
EFFECT_DU = {
    # 力量/脆弱
    'add_1_strength': 3,
    'add_2_strength': 5,
    'add_1_vulnerable': 3,
    'add_2_vulnerable': 5,

    # 格挡
    'add_1_block': 2.5,
    'add_1_block_plus': 3.5,
    'add_2_block_plus': 5.5,

    # 闪避
    'add_1_dodge': 4,
    'add_1_dodge_plus': 6,
    'add_2_dodge': 6,
    'add_2_dodge_plus': 8,

    # 晕眩/致盲
    'add_1_stun': 4,
    'add_2_stun': 7,
    'add_1_blind': 4,
    'add_2_blind': 6,

    # 反击
    'add_1_riposte': 3,
    'add_2_riposte': 5,

    # 移动/位移
    'move_forward_1': 1.5,
    'move_backward_1': 1.5,
    'move_pull_1': 1.5,
    'move_pull_2': 2.5,
    'move_knockback_1': 1.5,
    'move_knockback_2': 2.5,

    # 流血
    'skill_dot_small_bleed': 2,
    'skill_dot_medium_bleed': 3.5,
    'skill_dot_large_bleed': 5,

    # 压力治疗
    'stress_heal_1': 1,
    'stress_heal_2': 2,
    'stress_heal_3': 3,
    'stress_heal_4': 4,

    # 连击
    'prime_combo': 3,

    # 暴击
    'add_1_crit': 1.8,
    'add_2_crit': 3,
}

def get_dlc_path(hero_code):
    """获取英雄CSV路径"""
    base_heroes = ['flg', 'gr', 'hel', 'hwm', 'jes', 'lep', 'maa', 'occ', 'pd', 'run', 'ves']
    dlc1_heroes = ['cru', 'dul']
    dlc2_heroes = ['abm']

    if hero_code in base_heroes:
        return f'hero_{hero_code}_data_export.Group.csv'
    elif hero_code in dlc1_heroes:
        return f'dlc_dul_cru/hero_{hero_code}_data_export.Group.csv'
    elif hero_code in dlc2_heroes:
        return f'dlc_catacombs/hero_{hero_code}_data_export.Group.csv'
    else:
        raise ValueError(f'未知英雄代码: {hero_code}')

def parse_skill_block(lines, start_idx):
    """解析单个技能块"""
    skill = {}

    for i in range(start_idx, len(lines)):
        line = lines[i].strip()

        if not line or line.startswith('#'):
            continue

        if line.startswith('element_start'):
            if skill:  # 已有技能数据，返回
                return skill, i
            skill['name'] = line.split(',', 1)[1].strip() if ',' in line else ''
            continue

        if 'element_start' in line and i > start_idx:
            return skill, i

        if ',' not in line:
            continue

        key, value = [x.strip() for x in line.split(',', 1)]

        if key in ['id', 'damage_min', 'damage_max', 'target_ranks', 'usable_ranks']:
            skill[key] = value
        elif key == 'target_effects':
            skill['target_effects'] = value
        elif key == 'performer_effects':
            skill['performer_effects'] = value
        elif key == 'target_apply_limit_effects':
            skill['target_apply_limit_effects'] = value

    return skill, len(lines)

def calculate_du(skill):
    """计算技能DU价值"""
    du = 0.0

    # 基础伤害
    if 'damage_min' in skill and 'damage_max' in skill:
        try:
            min_d = float(skill['damage_min'])
            max_d = float(skill['damage_max'])
            du += (min_d + max_d) / 2
        except:
            pass

    # 目标效果
    if 'target_effects' in skill:
        effects = [e.strip() for e in skill['target_effects'].split('|') if e.strip()]
        for effect in effects:
            if effect in EFFECT_DU:
                du += EFFECT_DU[effect]

    # 施放者效果
    if 'performer_effects' in skill:
        effects = [e.strip() for e in skill['performer_effects'].split('|') if e.strip()]
        for effect in effects:
            if effect in EFFECT_DU:
                du += EFFECT_DU[effect]

    return round(du, 2)

def parse_hero_skills(hero_code):
    """解析英雄所有技能"""
    csv_path = get_dlc_path(hero_code)

    if not Path(csv_path).exists():
        print(f'错误: 文件不存在 {csv_path}')
        return []

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    skills = []
    i = 0

    while i < len(lines):
        if 'element_start' in lines[i]:
            skill, i = parse_skill_block(lines, i)
            if skill and 'id' in skill:
                skill['du'] = calculate_du(skill)
                skills.append(skill)
        else:
            i += 1

    return skills

def print_skill_table(skills):
    """输出技能表格"""
    # 按类型分组
    base_skills = [s for s in skills if not s['id'].endswith(('_u', '_p1', '_p2', '_p3'))]
    path1_skills = [s for s in skills if s['id'].endswith('_p1')]
    path2_skills = [s for s in skills if s['id'].endswith('_p2')]
    path3_skills = [s for s in skills if s['id'].endswith('_p3')]

    print('\n=== 基础技能 ===')
    print(f"{'技能ID':<30} {'伤害':<10} {'目标':<15} {'DU':<8} {'状态'}")
    print('-' * 80)

    for skill in base_skills:
        skill_id = skill['id']
        damage = f"{skill.get('damage_min', '-')}~{skill.get('damage_max', '-')}" if 'damage_min' in skill else '-'
        target = skill.get('target_ranks', '-')
        du = skill['du']
        status = '❌ 弱势' if du < 9 else ('⚠️ 可接受' if du < 13 else '✅ 优秀')

        print(f"{skill_id:<30} {damage:<10} {target:<15} {du:<8.2f} {status}")

        # 输出升级版
        u_skill = next((s for s in skills if s['id'] == f"{skill_id}_u"), None)
        if u_skill:
            u_damage = f"{u_skill.get('damage_min', '-')}~{u_skill.get('damage_max', '-')}" if 'damage_min' in u_skill else '-'
            u_target = u_skill.get('target_ranks', '-')
            u_du = u_skill['du']
            u_status = '❌ 弱势' if u_du < 9 else ('⚠️ 可接受' if u_du < 13 else '✅ 优秀')
            print(f"{u_skill['id']:<30} {u_damage:<10} {u_target:<15} {u_du:<8.2f} {u_status}")

    if path1_skills:
        print('\n=== 路径1技能 ===')
        print(f"{'技能ID':<30} {'伤害':<10} {'目标':<15} {'DU':<8} {'状态'}")
        print('-' * 80)
        for skill in path1_skills:
            damage = f"{skill.get('damage_min', '-')}~{skill.get('damage_max', '-')}" if 'damage_min' in skill else '-'
            target = skill.get('target_ranks', '-')
            du = skill['du']
            status = '❌ 弱势' if du < 9 else ('⚠️ 可接受' if du < 13 else '✅ 优秀')
            print(f"{skill['id']:<30} {damage:<10} {target:<15} {du:<8.2f} {status}")

    if path2_skills:
        print('\n=== 路径2技能 ===')
        print(f"{'技能ID':<30} {'伤害':<10} {'目标':<15} {'DU':<8} {'状态'}")
        print('-' * 80)
        for skill in path2_skills:
            damage = f"{skill.get('damage_min', '-')}~{skill.get('damage_max', '-')}" if 'damage_min' in skill else '-'
            target = skill.get('target_ranks', '-')
            du = skill['du']
            status = '❌ 弱势' if du < 9 else ('⚠️ 可接受' if du < 13 else '✅ 优秀')
            print(f"{skill['id']:<30} {damage:<10} {target:<15} {du:<8.2f} {status}")

    if path3_skills:
        print('\n=== 路径3技能 ===')
        print(f"{'技能ID':<30} {'伤害':<10} {'目标':<15} {'DU':<8} {'状态'}")
        print('-' * 80)
        for skill in path3_skills:
            damage = f"{skill.get('damage_min', '-')}~{skill.get('damage_max', '-')}" if 'damage_min' in skill else '-'
            target = skill.get('target_ranks', '-')
            du = skill['du']
            status = '❌ 弱势' if du < 9 else ('⚠️ 可接受' if du < 13 else '✅ 优秀')
            print(f"{skill['id']:<30} {damage:<10} {target:<15} {du:<8.2f} {status}")

def main():
    if len(sys.argv) < 2:
        print('用法: python parse_universal.py <英雄代码>')
        print('示例: python parse_universal.py jes')
        sys.exit(1)

    hero_code = sys.argv[1].lower()
    skills = parse_hero_skills(hero_code)

    if not skills:
        print(f'未找到英雄 {hero_code} 的技能数据')
        sys.exit(1)

    print(f'\n=== {hero_code.upper()} 技能评估 ===')
    print_skill_table(skills)

if __name__ == '__main__':
    main()
