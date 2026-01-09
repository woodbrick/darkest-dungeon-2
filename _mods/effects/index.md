# 效果DU索引

> **单一事实原则**：每个效果只在一个文件中定义，修改时编辑对应英雄的专属文档

## 目录结构

```
_mods/effects/
├── index.md (本文件 - 导航索引)
├── base_effects.md (公共效果 - 所有英雄共享)
├── bounty_hunter_effects.md (赏金猎人专属)
├── leper_effects.md (麻风剑士专属)
├── hellion_effects.md (地狱犬专属)
├── vestal_effects.md (修女专属)
├── crusader_effects.md (十字军专属 - 待添加)
└── ...
```

## 快速导航

### 公共效果
- **[基础效果](base_effects.md)** - 所有英雄共享的效果（控制、增益、减益、移动、连击、DoT）

### 英雄专属效果

| 英雄 | 文档 | 说明 |
|------|------|------|
| 赏金猎人 | [bounty_hunter_effects.md](bounty_hunter_effects.md) | 连击、标记破坏 |
| 麻风剑士 | [leper_effects.md](leper_effects.md) | 废墟增伤、自我致盲、坚守 |
| 地狱犬 | [hellion_effects.md](hellion_effects.md) | 嗜血、狂欢、流血 |
| 修女 | [vestal_effects.md](vestal_effects.md) | 信念系统、祝福、治疗 |

---

## 使用说明

### 查找效果
1. **公共效果**（stun/weak/block/连击/DoT）→ [base_effects.md](base_effects.md)
2. **英雄专属效果** → 查看对应英雄文档

### 添加新效果
1. 确定效果属于公共还是英雄专属
2. 在对应文档中添加效果定义
3. 格式参考现有条目

### 修改DU值
- 直接编辑对应文件中的DU值
- 无需修改其他文件（单一事实原则）

---

*2026-01-09*
