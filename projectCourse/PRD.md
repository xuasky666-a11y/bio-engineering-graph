# OBE 课程架构 · 项目说明

> 纯 HTML 演示，无构建、无后端、无自动灌数脚本。数据以 `dependance/` 为准，人工维护。

---

## 1. 目录与职责

| 路径 | 用途 |
|------|------|
| **`tower.html`** | **主交付页**：金字塔分层可视化，数据内联，双击即可打开 |
| **`dna.html`** | DNA 关系图谱（旧版数据，待专项升级） |
| **`dependance/`** | 实体关系数据与规范文档 |
| **`met/`** | 教研用 Excel 源表，仅供人工梳理，不参与页面运行 |
| [`story.md`](./story.md) | 讲解稿（配合看板使用） |

---

## 2. 演示页

| 文件 | 说明 |
|------|------|
| `tower.html` | 十一概念 · 241 实体 · 含课组层；默认 **↑ 向上托**，可切 **↓ 向下拆** |
| `dna.html` | 十概念旧数据（69 实体），暂不维护 |

- **打开方式**：双击 HTML（推荐 Chrome / Edge），`tower.html` 无需本地服务器。
- **方向开关**：向上托走中轴 `颗粒→课组→教学单元→专业认知课→项目化课→岗位`；向下拆仅场景链与能力/知识链，不含中轴三门课与课组（见 `dependance/OBErelation.md` §六）。

---

## 3. 数据文件（均在 `dependance/`）

| 文件 | 说明 |
|------|------|
| `exampleRelation.json` | 节点与关系（JSON 主源，含 `meta` + `data`） |
| `data.js` | 同上，导出为 `window.OBE_RELATION_DATA`（供查阅或复制） |
| `example.md` | 三课汇总实体清单（241 实体统计） |
| `exampleRelationChain.md` | 202 条关系链核对 |
| `OBErelation.md` | OBE 十一概念关系规范 |

### 数据概要

- **概念**：11（岗位、项目化课、专业认知课、教学单元、课组名称、能力/知识/场景 模块·单元·颗粒）
- **实体总数**：241
- **中轴链路**：`颗粒 →耦合→ 课组 →实现→ 教学单元 →组装→ 专业认知课 →支撑→ 项目化课 →直通→ 岗位`
- **数据来源**：Python 程序设计、前端页面设计与制作、数媒9 项目实战 三份 Excel（存于 `met/`）

### `meta` 字段（`exampleRelation.json` 与 `data.js` 对齐）

| 字段 | 说明 |
|------|------|
| `说明` | 数据用途简述 |
| `数据来源` | Excel 文件名列表 |
| `阅读方向` | 向上托 / 向下拆 语义 |
| `实体总数` | 241 |
| `概念` | 十一概念名数组 |
| `关系动词` | 各概念出/入动词表 |
| `实体清单` | 按概念分组的实体名列表 |
| `实体清单合计` | 241 |

---

## 4. 数据与页面关系

```
met/*.xlsx  ──人工梳理──►  dependance/exampleRelation.json
                              │
                              ├─► dependance/data.js（查阅/复制用）
                              └─► tower.html 内联脚本（实际运行数据）
```

- `tower.html` **自包含**：内联 `window.OBE_RELATION_DATA`，不依赖外部 `data.js`。
- 数据变更时：先改 `exampleRelation.json`，再同步 `data.js` 与 `tower.html` 内联块（人工或一次性脚本，不维护常驻生成器）。

---

## 5. 使用步骤

1. 阅读 [`story.md`](./story.md) 了解讲解叙事。
2. 查阅 [`dependance/OBErelation.md`](./dependance/OBErelation.md) 理解概念关系。
3. 双击打开 `tower.html`，用顶栏切换方向、缩放、点选节点查看右侧关系链。

---

## 6. 非目标（明确不做）

- 不从 Excel 自动灌数，不提供 `npm` / Vite 工程站。
- 不维护 Node 前端、Python 常驻脚本或设计系统导出物。
- `dna.html` 升级留待专项处理。
- `met/` 中 Excel 变更需**人工**同步到 `dependance/` 与 `tower.html`。

---

*文档版本 v2.0 · 以 `dependance/` 现有数据为准。*
