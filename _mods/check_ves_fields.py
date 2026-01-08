import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

csv_path = r'G:\Darkest Dungeon II\Darkest Dungeon II_Data\StreamingAssets\Excel\hero_ves_data_export.Group.csv'

# 先查看文件前几行
with open(csv_path, 'r', encoding='utf-8') as f:
    print("=== 前5行内容 ===")
    for i, line in enumerate(f):
        if i < 5:
            print(f"Line {i}: {line[:200]}")
        else:
            break

# 查看所有技能ID
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

print(f"\n=== 共 {len(rows)} 行数据 ===")

# 查找目标技能
target_skills = ['ves_mantra_p1', 'ves_mantra_p3', 'ves_illumination', 'ves_illumination_u', 'ves_illumination_p3']
print(f"\n=== 查找目标技能 ===")
for row in rows:
    skill_id = row.get('id', '')
    if skill_id in target_skills:
        print(f"找到: {skill_id}")
