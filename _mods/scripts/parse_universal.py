#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用技能解析评估脚本
用法: python parse_universal.py <英雄代码>
示例: python parse_universal.py jes
"""

import csv
import sys
import io
import yaml
from pathlib import Path

# 修复Windows控制台中文乱码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载效果DU配置(唯一DU数据源)
def load_effects_du():
    """从YAML文件加载效果DU价值 - 单一事实来源"""
    config_path = Path(__file__).parent.parent / 'rules' / 'effects_du.yml'

    if not config_path.exists():
        print(f'警告: DU配置文件不存在 {config_path}')
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
        # 新格式: {effect_id: {name, desc, file, line, du}}
        # 转换为: {effect_id: du}
        return {k: v.get('du', 0) for k, v in data.items()} if isinstance(data, dict) else {}

EFFECT_DU = load_effects_du()

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

def parse_hero_skills(hero_code):
    """解析英雄所有技能，合并多个element块"""
    csv_path = get_dlc_path(hero_code)

    # 尝试从多个可能的位置查找文件
    possible_paths = [
        Path(csv_path),  # 当前目录
        Path('..') / csv_path,  # 上级目录
        Path('../..') / csv_path,  # 上上级目录
        Path('../..') / 'dlc_dul_cru' / Path(csv_path).name,  # DLC1目录
        Path('../..') / 'dlc_catacombs' / Path(csv_path).name,  # DLC2目录
    ]

    actual_path = None
    for p in possible_paths:
        if p.exists():
            actual_path = p
            break

    if not actual_path:
        print(f'错误: 文件不存在 {csv_path}')
        return []

    with open(actual_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 按技能ID合并数据
    skills_data = {}
    current_skill_id = None
    current_element_type = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('element_start'):
            parts = line.split(',')
            if len(parts) >= 3:
                current_skill_id = parts[1].strip()
                current_element_type = parts[2].strip()

                if current_skill_id not in skills_data:
                    skills_data[current_skill_id] = {
                        'id': current_skill_id,
                        'name': current_skill_id
                    }
            continue

        if line == 'element_end':
            current_skill_id = None
            current_element_type = None
            continue

        if current_skill_id is None or ',' not in line:
            continue

        key, value = [x.strip() for x in line.split(',', 1)]

        # 解析伤害数据
        if current_element_type == 'ActorDataStats':
            if key == 'add_stats' and current_skill_id:
                stats = [x.strip() for x in value.split(',')]
                if len(stats) >= 2:
                    try:
                        skills_data[current_skill_id]['damage_min'] = stats[0]
                        skills_data[current_skill_id]['damage_max'] = str(float(stats[0]) + float(stats[1]))
                    except:
                        pass

        # 解析技能和效果数据
        if current_element_type in ['ActorDataSkill', 'ActorDataEffects']:
            if key in ['target_ranks', 'launch_ranks']:
                skills_data[current_skill_id][key] = value
            elif key in ['target_effects', 'performer_effects', 'performer_after_target_effects',
                        'performer_team_others_effects', 'target_apply_limit_effects',
                        'target_buffs', 'performer_buffs']:
                # 效果字段用逗号分隔多个效果，需要用|重新连接以便后续处理
                effects = [x.strip() for x in value.split(',') if x.strip()]
                if key in skills_data[current_skill_id]:
                    # 已存在，追加
                    existing = skills_data[current_skill_id][key].split('|')
                    all_effects = existing + effects
                    skills_data[current_skill_id][key] = '|'.join(all_effects)
                else:
                    skills_data[current_skill_id][key] = '|'.join(effects)

    # 计算DU并过滤
    skills = []
    for skill_id, skill_data in skills_data.items():
        # 过滤技能: 必须以hero_开头且包含技能标识
        # 排除: move技能、尸体数据、act_out技能
        if (skill_id.endswith('_move') or
            skill_id.endswith('_corpse') or
            skill_id.startswith('act_out_') or
            'move' in skill_id.lower()):
            continue
        skill_data['du'] = calculate_du(skill_data)
        skills.append(skill_data)

    return skills

def calculate_du(skill):
    """计算技能DU价值 - 完整7字段检查"""
    du = 0.0

    # 定义需要检查的所有效果字段
    effect_fields = [
        'target_effects',
        'performer_effects',
        'performer_after_target_effects',
        'performer_team_others_effects',
        'target_apply_limit_effects',
        'target_buffs',
        'performer_buffs'
    ]

    # 基础伤害
    if 'damage_min' in skill and 'damage_max' in skill:
        try:
            min_d = float(skill['damage_min'])
            max_d = float(skill['damage_max'])
            du += (min_d + max_d) / 2
        except:
            pass

    # 遍历所有效果字段
    for field in effect_fields:
        if field in skill:
            effects = [e.strip() for e in skill[field].split('|') if e.strip()]
            for effect in effects:
                if effect in EFFECT_DU:
                    du += EFFECT_DU[effect]

    return round(du, 2)

def find_missing_effects(skill):
    """查找技能中未定义的效果 - 返回缺失效果列表"""
    missing = []

    effect_fields = [
        'target_effects',
        'performer_effects',
        'performer_after_target_effects',
        'performer_team_others_effects',
        'target_apply_limit_effects',
        'target_buffs',
        'performer_buffs'
    ]

    for field in effect_fields:
        if field in skill:
            effects = [e.strip() for e in skill[field].split('|') if e.strip()]
            for effect in effects:
                if effect not in EFFECT_DU:
                    missing.append({
                        'effect': effect,
                        'field': field,
                        'skill': skill['id']
                    })

    return missing

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

def print_missing_effects_report(skills):
    """输出缺失效果报告"""
    all_missing = []

    for skill in skills:
        missing = find_missing_effects(skill)
        all_missing.extend(missing)

    if not all_missing:
        print('\n✅ 所有效果均已定义')
        return

    print(f'\n⚠️  发现 {len(all_missing)} 个未定义效果:')
    print('=' * 80)
    print(f"{'效果ID':<40} {'字段':<30} {'来源技能'}")
    print('-' * 80)

    # 按效果去重
    unique_effects = {}
    for m in all_missing:
        key = m['effect']
        if key not in unique_effects:
            unique_effects[key] = []
        unique_effects[key].append(m)

    for effect, items in sorted(unique_effects.items()):
        first = items[0]
        skills_list = ', '.join(set([i['skill'] for i in items]))
        print(f"{effect:<40} {first['field']:<30} {skills_list}")

    print('\n建议: 将上述效果添加到 _mods/rules/effects_du.yml')
    print_coverage_stats(skills, len(unique_effects))

def print_coverage_stats(skills, missing_count):
    """输出效果覆盖度统计"""
    # 统计总效果数
    total_effects = 0
    for skill in skills:
        effect_fields = [
            'target_effects',
            'performer_effects',
            'performer_after_target_effects',
            'performer_team_others_effects',
            'target_apply_limit_effects',
            'target_buffs',
            'performer_buffs'
        ]
        for field in effect_fields:
            if field in skill:
                effects = [e.strip() for e in skill[field].split('|') if e.strip()]
                total_effects += len(effects)

    # 去重统计
    unique_effects = set()
    for skill in skills:
        effect_fields = [
            'target_effects',
            'performer_effects',
            'performer_after_target_effects',
            'performer_team_others_effects',
            'target_apply_limit_effects',
            'target_buffs',
            'performer_buffs'
        ]
        for field in effect_fields:
            if field in skill:
                effects = [e.strip() for e in skill[field].split('|') if e.strip()]
                unique_effects.update(effects)

    defined_count = len(unique_effects) - missing_count
    coverage_rate = (defined_count / len(unique_effects) * 100) if unique_effects else 100

    print('\n📊 效果覆盖度统计:')
    print('-' * 40)
    print(f"总效果数 (含重复): {total_effects}")
    print(f"唯一效果数: {len(unique_effects)}")
    print(f"已定义: {defined_count}")
    print(f"缺失: {missing_count}")
    print(f"覆盖率: {coverage_rate:.1f}%")

    if coverage_rate < 90:
        print(f'\n⚠️  警告: 覆盖率低于90%，建议补充缺失效果')
    elif coverage_rate < 100:
        print(f'\n✓ 覆盖率良好，仍有提升空间')
    else:
        print(f'\n✅ 完美覆盖！')

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
    print_missing_effects_report(skills)

if __name__ == '__main__':
    main()
