#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取火枪手完整技能数据 V2
"""

import csv
import sys

def extract_jester_data():
    """提取火枪手数据"""

    csv_file = r'g:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel\hero_jes_data_export.Group.csv'

    skills = {}
    current_skill = None
    current_element = None
    current_class = None
    key_map = None

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            # 检测元素开始
            if row[0] == 'element_start' and len(row) > 2:
                current_element = row[1]
                current_class = row[2]

                # 识别技能ID
                if current_element.startswith('jes_') and current_element != 'jester' and 'Skill' in current_class:
                    current_skill = current_element
                    skills[current_skill] = {
                        'id': current_element,
                        'm_NameId': None,
                        'launch_ranks': [],
                        'target_ranks': [],
                        'cooldown': None,
                        'damage': None,
                        'damage_mod': None,
                        'target_effects': [],
                        'performer_buffs': [],
                        'performer_after_target_effects': [],
                        'combo': None
                    }
                    key_map = None

            # 如果当前在处理技能
            elif current_skill and current_skill in skills:

                # 技能名称
                if row[0] == 'm_NameId' and len(row) > 1:
                    skills[current_skill]['m_NameId'] = row[1]

                # Key map (用于判断后续add_stats的类型)
                elif row[0] == 'key_map':
                    key_map = row[1:]

                # 可用位置
                elif row[0] == 'launch_ranks' and len(row) > 1:
                    skills[current_skill]['launch_ranks'] = row[1:]

                # 目标位置
                elif row[0] == 'target_ranks' and len(row) > 1:
                    skills[current_skill]['target_ranks'] = row[1:]

                # 冷却时间
                elif row[0] == 'cooldown' and len(row) > 1:
                    skills[current_skill]['cooldown'] = row[1]

                # 伤害数据 (health_damage在key_map中)
                elif row[0] == 'add_stats' and key_map and 'health_damage' in key_map and len(row) > 1:
                    try:
                        skills[current_skill]['damage'] = f"{row[1]}±{row[2]}"
                        if len(row) > 3:
                            skills[current_skill]['damage_mod'] = row[3]
                    except:
                        pass

                # 目标效果
                elif row[0] == 'target_effects' and len(row) > 1:
                    effects = [e for e in row[1:] if e]
                    if effects:
                        skills[current_skill]['target_effects'].extend(effects)

                # 施法者增益
                elif row[0] == 'performer_buffs' and len(row) > 1:
                    buffs = [b for b in row[1:] if b]
                    if buffs:
                        skills[current_skill]['performer_buffs'].extend(buffs)

                # 施法者在目标后的效果
                elif row[0] == 'performer_after_target_effects' and len(row) > 1:
                    effects = [e for e in row[1:] if e]
                    if effects:
                        skills[current_skill]['performer_after_target_effects'].extend(effects)

                # 连击数据
                elif row[0] == 'combo' and len(row) > 1:
                    skills[current_skill]['combo'] = row[1]

            # 元素结束
            elif row[0] == 'element_end':
                current_skill = None
                key_map = None

    return skills

def format_output(skills):
    """格式化输出"""
    output = []
    output.append("# 火枪手 (Jester) 完整技能数据\n")

    # 按技能ID排序
    sorted_skills = sorted(skills.items())

    for skill_id, skill in sorted_skills:
        output.append(f"## {skill['m_NameId'] or skill_id}")
        output.append("")

        # 基础信息
        output.append(f"- **技能ID**: {skill_id}")

        if skill['launch_ranks']:
            output.append(f"- **可用位置**: {', '.join(skill['launch_ranks'])}")
        if skill['target_ranks']:
            output.append(f"- **目标位置**: {', '.join(skill['target_ranks'])}")
        if skill['cooldown']:
            output.append(f"- **冷却**: {skill['cooldown']}")

        # 伤害
        if skill['damage']:
            mod_str = f" (修正: {skill['damage_mod']})" if skill['damage_mod'] else ""
            output.append(f"- **伤害**: {skill['damage']}{mod_str}")

        # 连击
        if skill['combo']:
            output.append(f"- **连击**: {skill['combo']}")

        # 效果
        if skill['target_effects']:
            output.append(f"- **目标效果**:")
            for effect in skill['target_effects']:
                output.append(f"  - {effect}")

        if skill['performer_buffs']:
            output.append(f"- **施法者增益**:")
            for buff in skill['performer_buffs']:
                output.append(f"  - {buff}")

        if skill['performer_after_target_effects']:
            output.append(f"- **施法者(目标后)效果**:")
            for effect in skill['performer_after_target_effects']:
                output.append(f"  - {effect}")

        output.append("")
        output.append("---")
        output.append("")

    return '\n'.join(output)

def main():
    """主函数"""
    print("Extracting Jester data...")

    skills = extract_jester_data()

    print(f"Found {len(skills)} skills\n")

    output = format_output(skills)

    print(output)

    # 保存到文件
    with open('jes_data.txt', 'w', encoding='utf-8') as f:
        f.write(output)

    print("\nSaved to jes_data.txt")

if __name__ == '__main__':
    main()
