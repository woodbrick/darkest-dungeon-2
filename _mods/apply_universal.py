#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用技能更新脚本
用法: python apply_universal.py <英雄代码> <配置文件>
示例: python apply_universal.py jes hero_jes_changes.yml
"""

import sys
import yaml
from pathlib import Path

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

def read_csv(csv_path):
    """读取CSV文件"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_csv(csv_path, lines):
    """写入CSV文件"""
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def find_skill_block(lines, skill_id):
    """查找技能块位置"""
    for i, line in enumerate(lines):
        if f'id,{skill_id}' in line:
            return i
    return None

def modify_skill_field(lines, start_idx, field_name, old_value, new_value):
    """修改技能字段"""
    for i in range(start_idx, min(start_idx + 50, len(lines))):
        line = lines[i]

        if line.strip().startswith('element_start'):
            if i > start_idx:  # 遇到下一个技能块
                break
            continue

        if not line.strip() or line.strip().startswith('#'):
            continue

        if f'{field_name},' in line:
            if old_value in line:
                lines[i] = line.replace(old_value, new_value)
                return True, i
            elif f'{field_name},{old_value}' in line:
                lines[i] = f'{field_name},{new_value}\n'
                return True, i

    return False, None

def apply_changes(hero_code, config):
    """应用配置变更"""
    csv_path = get_dlc_path(hero_code)

    if not Path(csv_path).exists():
        print(f'错误: 文件不存在 {csv_path}')
        return False

    lines = read_csv(csv_path)
    changes_count = 0
    errors = []

    for skill_id, modifications in config.items():
        start_idx = find_skill_block(lines, skill_id)

        if start_idx is None:
            errors.append(f'未找到技能: {skill_id}')
            continue

        skill_modified = False

        for mod in modifications:
            field_name = mod.get('field')
            old_value = mod.get('old')
            new_value = mod.get('new')

            if not all([field_name, old_value, new_value]):
                errors.append(f'配置错误: {skill_id} - {mod}')
                continue

            success, line_idx = modify_skill_field(lines, start_idx, field_name, old_value, new_value)

            if success:
                changes_count += 1
                skill_modified = True
                print(f'✓ {skill_id}: {field_name} {old_value} → {new_value}')
            else:
                errors.append(f'修改失败: {skill_id} - {field_name} {old_value} → {new_value}')

        if skill_modified:
            print(f'已修改: {skill_id}')

    if changes_count > 0:
        write_csv(csv_path, lines)
        print(f'\n总计修改: {changes_count} 处')

    if errors:
        print(f'\n错误: {len(errors)} 个')
        for err in errors:
            print(f'  - {err}')
        return False

    return True

def load_config(config_path):
    """加载YAML配置"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f'配置文件加载失败: {e}')
        return None

def validate_config(config):
    """验证配置完整性"""
    errors = []

    for skill_id, modifications in config.items():
        # 检查是否有升级版
        has_base = not skill_id.endswith('_u')
        has_upgrade = f'{skill_id}_u' in config if has_base else True

        # 检查基础版和升级版同步
        if has_base and has_upgrade and skill_id.endswith('_u') is False:
            base_mods = config.get(skill_id, [])
            upgrade_mods = config.get(f'{skill_id}_u', [])

            if base_mods and not upgrade_mods:
                errors.append(f'铁律违反: {skill_id} 已修改但 {skill_id}_u 未修改')

    return errors

def main():
    if len(sys.argv) < 3:
        print('用法: python apply_universal.py <英雄代码> <配置文件>')
        print('示例: python apply_universal.py jes hero_jes_changes.yml')
        sys.exit(1)

    hero_code = sys.argv[1].lower()
    config_path = sys.argv[2]

    if not Path(config_path).exists():
        print(f'错误: 配置文件不存在 {config_path}')
        sys.exit(1)

    config = load_config(config_path)
    if not config:
        sys.exit(1)

    print(f'=== 验证配置 ===')
    validation_errors = validate_config(config)
    if validation_errors:
        print('配置验证失败:')
        for err in validation_errors:
            print(f'  ❌ {err}')
        print('\n请修正配置后重试')
        sys.exit(1)
    print('✓ 配置验证通过')

    print(f'\n=== 应用修改 ({hero_code.upper()}) ===')
    success = apply_changes(hero_code, config)

    if success:
        print(f'\n✓ 修改完成')
        print(f'\n验证命令:')
        print(f'  git diff {get_dlc_path(hero_code)}')
    else:
        print(f'\n❌ 修改失败，请检查错误信息')
        sys.exit(1)

if __name__ == '__main__':
    main()
