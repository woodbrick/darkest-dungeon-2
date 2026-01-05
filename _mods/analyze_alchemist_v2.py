#!/usr/bin/env python3
"""炼金术士技能分析工具 V2 - 修复版"""

from pathlib import Path
from collections import defaultdict

def parse_csv_elements(filepath: Path) -> dict:
    """解析CSV文件为元素字典"""
    elements = defaultdict(lambda: {'entries': []})
    current_id = None
    current_type = None
    current_lines = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue

            if line.startswith('element_start,'):
                # 保存前一个元素
                if current_id and current_lines:
                    elements[current_id]['entries'].append({
                        'type': current_type,
                        'lines': current_lines
                    })

                # 开始新元素
                parts = line.split(',')
                if len(parts) >= 3:
                    current_id = parts[1]
                    current_type = parts[2]
                    current_lines = []
                else:
                    current_id = None
                    current_type = None
                    current_lines = []

            elif line.startswith('element_end'):
                # 保存当前元素
                if current_id and current_lines:
                    elements[current_id]['entries'].append({
                        'type': current_type,
                        'lines': current_lines
                    })
                current_id = None
                current_type = None
                current_lines = []

            elif current_id:
                current_lines.append(line)

    return dict(elements)


def get_field_value(lines: list, field: str) -> str:
    """从行列表中获取字段值"""
    for line in lines:
        if line.startswith(field + ','):
            parts = line.split(',')
            if len(parts) > 1:
                return ','.join(parts[1:]).rstrip(',')
    return None


def get_field_list(lines: list, field: str) -> list:
    """从行列表中获取字段值列表"""
    for line in lines:
        if line.startswith(field + ','):
            parts = line.split(',')
            return [p.strip() for p in parts[1:] if p.strip()]
    return []


def find_entry_by_type(elements: dict, element_id: str, entry_type: str) -> dict:
    """查找指定类型的条目"""
    if element_id not in elements:
        return None

    for entry in elements[element_id]['entries']:
        if entry['type'] == entry_type:
            return entry
    return None


def analyze_alchemist(filepath: Path):
    """分析炼金术士数据"""
    elements = parse_csv_elements(filepath)

    report = []
    report.append("# 炼金术士 (Alchemist/Abomination) 完整能力分析报告\n\n")
    report.append("---\n\n")

    # ========== 基础属性 ==========
    report.append("## 一、基础属性\n\n")

    stats_entry = find_entry_by_type(elements, 'abomination', 'ActorDataStats')
    if stats_entry:
        add_stats = get_field_value(stats_entry['lines'], 'add_stats')
        if add_stats:
            stats_vals = add_stats.split(',')
            report.append(f"- **生命值**: {stats_vals[0] if len(stats_vals) > 0 else 'N/A'}\n")
            report.append(f"- **速度**: {stats_vals[1] if len(stats_vals) > 1 else 'N/A'}\n")
            report.append(f"- **压力上限**: {stats_vals[2] if len(stats_vals) > 2 else 'N/A'}\n")
            report.append(f"- **死亡抵抗**: {stats_vals[3] if len(stats_vals) > 3 else 'N/A'}\n")

        report.append("\n**抗性**:\n\n")
        for line in stats_entry['lines']:
            if line.startswith('sub_stat,resistance,'):
                parts = line.split(',')
                if len(parts) >= 4:
                    res_type = parts[2]
                    res_val = parts[3]
                    report.append(f"- **{res_type}**: {res_val}\n")

    # ========== 变身技能 ==========
    report.append("\n---\n\n")
    report.append("## 二、变身技能 (Transformation)\n\n")

    transform_skills = [
        ('abm_transform', '基础变身'),
        ('abm_transform_u', '升级变身'),
        ('abm_transform_p1', '路径1变身'),
        ('abm_transform_p1_u', '路径1升级'),
        ('abm_transform_p2', '路径2变身'),
        ('abm_transform_p2_u', '路径2升级'),
        ('abm_transform_p3', '路径3变身'),
        ('abm_transform_p3_u', '路径3升级'),
    ]

    for skill_id, desc in transform_skills:
        skill_entry = find_entry_by_type(elements, skill_id, 'ActorDataSkill')
        effects_entry = find_entry_by_type(elements, skill_id, 'ActorDataEffects')

        if skill_entry:
            report.append(f"### {desc} ({skill_id})\n\n")

            cooldown = get_field_value(skill_entry['lines'], 'm_Cooldown')
            launch_ranks = get_field_list(skill_entry['lines'], 'launch_ranks')

            report.append(f"- **冷却**: {cooldown if cooldown else 'N/A'} 回合\n")
            report.append(f"- **施放位置**: {', '.join(launch_ranks) if launch_ranks else '任意'}\n")
            report.append(f"- **免费动作**: {'是' if get_field_value(skill_entry['lines'], 'm_IsFreeAction') == 'True' else '否'}\n")

            if effects_entry:
                performer_effects = get_field_list(effects_entry['lines'], 'performer_effects')
                team_effects = get_field_list(effects_entry['lines'], 'performer_team_others_effects')

                if performer_effects:
                    report.append(f"- **自身效果**: {', '.join(performer_effects)}\n")
                if team_effects:
                    report.append(f"- **队友效果**: {', '.join(team_effects)}\n")

            report.append("\n")

    # ========== 野兽形态技能 ==========
    report.append("\n---\n\n")
    report.append("## 三、野兽形态技能 (Beast Form)\n\n")

    beast_skills = [
        ('abm_rake', '利爪', '基础'),
        ('abm_rake_u', '利爪', '升级'),
        ('abm_rake_p2', '利爪', '路径2'),
        ('abm_rake_p2_u', '利爪', '路径2升级'),
        ('abm_rake_p3', '利爪', '路径3'),
        ('abm_rake_p3_u', '利爪', '路径3升级'),
        ('abm_slam', '重击', '基础'),
        ('abm_slam_u', '重击', '升级'),
        ('abm_rage', '狂怒', '基础'),
        ('abm_rage_u', '狂怒', '升级'),
        ('abm_howl', '咆哮', '基础'),
        ('abm_howl_u', '咆哮', '升级'),
    ]

    for skill_id, skill_name, variant in beast_skills:
        skill_entry = find_entry_by_type(elements, skill_id, 'ActorDataSkill')
        stats_entry = find_entry_by_type(elements, skill_id, 'ActorDataStats')
        effects_entry = find_entry_by_type(elements, skill_id, 'ActorDataEffects')

        if skill_entry or stats_entry:
            report.append(f"### {skill_name} - {variant} ({skill_id})\n\n")

            if stats_entry:
                add_stats = get_field_value(stats_entry['lines'], 'add_stats')
                if add_stats:
                    stats_vals = add_stats.split(',')
                    dmg_min = stats_vals[0] if len(stats_vals) > 0 else '?'
                    dmg_max = stats_vals[1] if len(stats_vals) > 1 else '?'
                    try:
                        dmg_total = int(dmg_min) + int(dmg_max)
                    except:
                        dmg_total = f"{dmg_min}+{dmg_max}"
                    report.append(f"- **伤害**: {dmg_min}-{dmg_min} (+{dmg_max}随机) = {dmg_total} 平均\n")

            if skill_entry:
                launch_ranks = get_field_list(skill_entry['lines'], 'launch_ranks')
                target_ranks = get_field_list(skill_entry['lines'], 'target_ranks')
                multi_hit = get_field_value(skill_entry['lines'], 'm_IsMultiHit')

                if launch_ranks:
                    report.append(f"- **施放位置**: {', '.join(launch_ranks)}\n")
                if target_ranks:
                    report.append(f"- **目标位置**: {', '.join(target_ranks)}\n")
                if multi_hit:
                    report.append(f"- **多段攻击**: {multi_hit}\n")

            if effects_entry:
                performer_effects = get_field_list(effects_entry['lines'], 'performer_effects')
                target_effects = get_field_list(effects_entry['lines'], 'target_effects')
                after_effects = get_field_list(effects_entry['lines'], 'performer_after_target_effects')

                if performer_effects:
                    report.append(f"- **自身效果**: {', '.join(performer_effects)}\n")
                if target_effects:
                    report.append(f"- **目标效果**: {', '.join(target_effects)}\n")
                if after_effects:
                    report.append(f"- **攻击后效果**: {', '.join(after_effects)}\n")

            report.append("\n")

    # ========== 人类形态技能 ==========
    report.append("\n---\n\n")
    report.append("## 四、人类形态技能 (Human Form)\n\n")

    human_skills = [
        ('abm_manacles', '锁链', '基础'),
        ('abm_manacles_u', '锁链', '升级'),
        ('abm_manacles_p1', '锁链', '路径1'),
        ('abm_manacles_p1_u', '锁链', '路径1升级'),
        ('abm_acid', '酸液', '基础'),
        ('abm_acid_u', '酸液', '升级'),
        ('abm_acid_p3', '酸液', '路径3'),
        ('abm_acid_p3_u', '酸液', '路径3升级'),
    ]

    for skill_id, skill_name, variant in human_skills:
        skill_entry = find_entry_by_type(elements, skill_id, 'ActorDataSkill')
        stats_entry = find_entry_by_type(elements, skill_id, 'ActorDataStats')
        effects_entry = find_entry_by_type(elements, skill_id, 'ActorDataEffects')

        if skill_entry or stats_entry:
            report.append(f"### {skill_name} - {variant} ({skill_id})\n\n")

            if stats_entry:
                add_stats = get_field_value(stats_entry['lines'], 'add_stats')
                if add_stats:
                    stats_vals = add_stats.split(',')
                    dmg_min = stats_vals[0] if len(stats_vals) > 0 else '?'
                    dmg_max = stats_vals[1] if len(stats_vals) > 1 else '?'
                    try:
                        dmg_total = int(dmg_min) + int(dmg_max)
                    except:
                        dmg_total = f"{dmg_min}+{dmg_max}"
                    report.append(f"- **伤害**: {dmg_min}-{dmg_min} (+{dmg_max}随机) = {dmg_total} 平均\n")

            if skill_entry:
                launch_ranks = get_field_list(skill_entry['lines'], 'launch_ranks')
                target_ranks = get_field_list(skill_entry['lines'], 'target_ranks')

                if launch_ranks:
                    report.append(f"- **施放位置**: {', '.join(launch_ranks)}\n")
                if target_ranks:
                    report.append(f"- **目标位置**: {', '.join(target_ranks)}\n")

            if effects_entry:
                target_effects = get_field_list(effects_entry['lines'], 'target_effects')

                if target_effects:
                    report.append(f"- **目标效果**: {', '.join(target_effects)}\n")

            report.append("\n")

    # ========== 解除技能 ==========
    report.append("\n---\n\n")
    report.append("## 五、解除变身技能 (Revert)\n\n")

    revert_skills = [
        ('abm_revert', '基础解除'),
        ('abm_revert_u', '升级解除'),
        ('abm_revert_p1', '路径1解除'),
        ('abm_revert_p1_u', '路径1升级'),
    ]

    for skill_id, desc in revert_skills:
        skill_entry = find_entry_by_type(elements, skill_id, 'ActorDataSkill')
        effects_entry = find_entry_by_type(elements, skill_id, 'ActorDataEffects')

        if skill_entry:
            report.append(f"### {desc} ({skill_id})\n\n")

            cooldown = get_field_value(skill_entry['lines'], 'm_Cooldown')
            free_action = get_field_value(skill_entry['lines'], 'm_IsFreeAction')

            report.append(f"- **冷却**: {cooldown if cooldown else 'N/A'} 回合\n")
            report.append(f"- **免费动作**: {free_action}\n")

            if effects_entry:
                performer_effects = get_field_list(effects_entry['lines'], 'performer_effects')

                if performer_effects:
                    report.append(f"- **效果**: {', '.join(performer_effects)}\n")

            report.append("\n")

    # ========== 问题总结 ==========
    report.append("\n---\n\n")
    report.append("## 六、问题总结\n\n")

    report.append("### 6.1 变身机制问题\n")
    report.append("1. **队友压力负担**: 变身会对所有队友造成压力 (1点 + 33%/75%概率额外1点)\n")
    report.append("2. **冷却时间**: 基础5回合较长，升级后3回合仍偏长\n")
    report.append("3. **免费动作**: ✓ 变身是免费动作，这是优点\n")
    report.append("4. **解除消耗**: 需要手动解除，虽然是免费动作但仍占用操作\n\n")

    report.append("### 6.2 野兽形态技能问题\n")
    report.append("1. **伤害偏低**: \n")
    report.append("   - 利爪: 3-5伤害 (2次攻击 = 6-10总计)\n")
    report.append("   - 狂怒: 5-7伤害 (单次)\n")
    report.append("   - 重击: 4-7伤害 (有控制效果)\n")
    report.append("2. **自我压力**: 野兽技能使用后会对自身造成压力伤害\n")
    report.append("3. **技能有限**: 野兽形态只有3个技能，灵活性不足\n")
    report.append("4. **无生存能力**: 无治疗、无防御增益、无吸血\n\n")

    report.append("### 6.3 人类形态技能问题\n")
    report.append("1. **锁链伤害低**: 3-4伤害，主要是辅助技能\n")
    report.append("2. **酸液效果**: 需要查看具体数据\n\n")

    report.append("### 6.4 基础属性问题\n")
    report.append("1. **生命值偏低**: 40点对比其他近战英雄偏少\n")
    report.append("2. **抗性不足**: \n")
    report.append("   - 流血抗性: 仅20%\n")
    report.append("   - 燃烧抗性: 仅10% (致命弱点)\n\n")

    return ''.join(report)


def main():
    filepath = Path(r'G:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel\dlc_catacombs\hero_abm_data_export.Group.csv')
    output = Path(__file__).parent / 'alchemist_analysis.md'

    print("正在分析炼金术士数据...")
    try:
        report = analyze_alchemist(filepath)

        with open(output, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✓ 分析完成！报告已保存至: {output}")
        print(f"  文件大小: {len(report)} 字符")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
