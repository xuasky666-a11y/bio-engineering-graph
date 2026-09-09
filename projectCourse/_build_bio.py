#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一次性脚本：构造「大连理工大学生物学院 · 生物工程专业」OBE 图谱数据，
并注入 dna.html 的内联数据行 window.OBE_RELATION_DATA。

设计原则：
- 沿用 OBE 十概念骨架与全部关系动词（耦合/组装/支撑/直通/提取/需求/拆解/供给/
  拆分/组合/解构/聚合/重构/适用/应用/适配/再现/场景单元-专业认知/专业认知-专业认知）。
- 只按「归属关系」单向定义，脚本自动生成出入双向对称数据，避免手工出错。
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DNA = HERE / "dna.html"

# ============ 实体定义 ============
JOB = "生物制药工程师、发酵工程师、基因工程研发工程师"

PROJECTS = ["生物制药工艺项目实战", "发酵工程生产项目实战", "基因工程产品研发项目实战"]
COURSES = ["基因工程", "发酵工程", "细胞工程"]
UNITS = [
    "教学单元1 工具酶与基因操作载体",
    "教学单元2 基因克隆与重组DNA构建",
    "教学单元3 基因表达与检测技术",
    "教学单元4 菌种选育与保藏",
    "教学单元5 培养基与灭菌技术",
    "教学单元6 发酵过程控制与放大",
    "教学单元7 细胞培养技术",
    "教学单元8 细胞融合与杂交瘤技术",
    "教学单元9 产物分离与纯化",
]
SCENE_MODULES = [
    "重组人胰岛素规模化生产",
    "青霉素抗生素发酵生产",
    "重组蛋白表达与纯化",
    "基因工程疫苗制备",
    "单克隆抗体制备",
]
SCENE_UNITS = [
    "工程菌高密度发酵生产胰岛素",
    "青霉素发酵罐过程优化",
    "重组质粒构建与工程菌转化",
    "疫苗抗原表达与灭活",
    "杂交瘤细胞筛选与培养",
    "目标蛋白分离纯化",
]
SCENE_GRAINS = [
    "工程菌接种与扩培",
    "发酵罐参数调控",
    "质粒酶切与连接",
    "工程菌转化与筛选",
    "抗原灭活与配制",
    "细胞融合与杂交瘤筛选",
    "层析分离纯化操作",
    "产物浓缩冻干与质检",
]
ABILITY_MODULES = [
    "菌种选育与保藏能力",
    "发酵过程控制能力",
    "基因克隆与表达能力",
    "分离纯化能力",
    "细胞培养与操作能力",
]
KNOWLEDGE_UNITS = [
    "微生物学与菌种知识",
    "培养基与灭菌原理",
    "发酵动力学与过程控制",
    "分子生物学与基因操作原理",
    "酶学与工具酶知识",
    "细胞生物学与培养原理",
    "免疫学与抗体知识",
    "分离纯化与下游加工知识",
]
KNOWLEDGE_GRAINS = [
    "微生物分类与生理", "菌种生长曲线", "菌种保藏方法",
    "培养基组成与配制", "灭菌原理与方法",
    "发酵动力学模型", "溶氧与pH控制", "发酵放大原理",
    "DNA复制与基因表达", "基因克隆原理", "PCR与基因扩增",
    "限制性内切酶与连接酶", "载体与质粒结构",
    "细胞结构与功能", "细胞培养条件", "细胞生长调控",
    "抗原抗体反应", "单克隆抗体原理",
    "层析分离原理", "膜分离技术", "浓缩与干燥", "产物质量检测",
]

CONCEPTS = ["岗位", "项目化课", "专业认知课", "教学单元", "能力模块",
            "知识单元", "知识颗粒", "场景模块", "场景单元", "场景颗粒"]
concept_entities = {
    "岗位": [JOB],
    "项目化课": PROJECTS,
    "专业认知课": COURSES,
    "教学单元": UNITS,
    "能力模块": ABILITY_MODULES,
    "知识单元": KNOWLEDGE_UNITS,
    "知识颗粒": KNOWLEDGE_GRAINS,
    "场景模块": SCENE_MODULES,
    "场景单元": SCENE_UNITS,
    "场景颗粒": SCENE_GRAINS,
}
entity_concept = {}
for c, es in concept_entities.items():
    for e in es:
        entity_concept[e] = c

# ============ 归属映射 ============
unit_to_course = {
    UNITS[0]: COURSES[0], UNITS[1]: COURSES[0], UNITS[2]: COURSES[0],
    UNITS[3]: COURSES[1], UNITS[4]: COURSES[1], UNITS[5]: COURSES[1],
    UNITS[6]: COURSES[2], UNITS[7]: COURSES[2], UNITS[8]: COURSES[2],
}
course_to_projects = {
    COURSES[0]: [PROJECTS[2], PROJECTS[0]],
    COURSES[1]: [PROJECTS[1], PROJECTS[0]],
    COURSES[2]: [PROJECTS[0], PROJECTS[2]],
}
scene_module_to_units = {
    SCENE_MODULES[0]: [SCENE_UNITS[0]],
    SCENE_MODULES[1]: [SCENE_UNITS[1]],
    SCENE_MODULES[2]: [SCENE_UNITS[2], SCENE_UNITS[5]],
    SCENE_MODULES[3]: [SCENE_UNITS[3]],
    SCENE_MODULES[4]: [SCENE_UNITS[4]],
}
scene_unit_to_grains = {
    SCENE_UNITS[0]: [SCENE_GRAINS[0], SCENE_GRAINS[1]],
    SCENE_UNITS[1]: [SCENE_GRAINS[1]],
    SCENE_UNITS[2]: [SCENE_GRAINS[2], SCENE_GRAINS[3]],
    SCENE_UNITS[3]: [SCENE_GRAINS[4]],
    SCENE_UNITS[4]: [SCENE_GRAINS[5]],
    SCENE_UNITS[5]: [SCENE_GRAINS[6], SCENE_GRAINS[7]],
}
scene_module_to_projects = {
    SCENE_MODULES[0]: [PROJECTS[0]],
    SCENE_MODULES[1]: [PROJECTS[1]],
    SCENE_MODULES[2]: [PROJECTS[2]],
    SCENE_MODULES[3]: [PROJECTS[0], PROJECTS[2]],
    SCENE_MODULES[4]: [PROJECTS[0]],
}
scene_unit_to_course = {
    SCENE_UNITS[0]: COURSES[1], SCENE_UNITS[1]: COURSES[1],
    SCENE_UNITS[2]: COURSES[0], SCENE_UNITS[3]: COURSES[0],
    SCENE_UNITS[4]: COURSES[2], SCENE_UNITS[5]: COURSES[2],
}
unit_coupling = {
    UNITS[0]: {"scene": [SCENE_GRAINS[2]], "know": [KNOWLEDGE_GRAINS[11], KNOWLEDGE_GRAINS[12]]},
    UNITS[1]: {"scene": [SCENE_GRAINS[2], SCENE_GRAINS[3]], "know": [KNOWLEDGE_GRAINS[9], KNOWLEDGE_GRAINS[10]]},
    UNITS[2]: {"scene": [SCENE_GRAINS[3], SCENE_GRAINS[4]], "know": [KNOWLEDGE_GRAINS[8], KNOWLEDGE_GRAINS[21]]},
    UNITS[3]: {"scene": [SCENE_GRAINS[0]], "know": [KNOWLEDGE_GRAINS[0], KNOWLEDGE_GRAINS[1], KNOWLEDGE_GRAINS[2]]},
    UNITS[4]: {"scene": [], "know": [KNOWLEDGE_GRAINS[3], KNOWLEDGE_GRAINS[4]]},
    UNITS[5]: {"scene": [SCENE_GRAINS[1]], "know": [KNOWLEDGE_GRAINS[5], KNOWLEDGE_GRAINS[6], KNOWLEDGE_GRAINS[7]]},
    UNITS[6]: {"scene": [SCENE_GRAINS[5]], "know": [KNOWLEDGE_GRAINS[13], KNOWLEDGE_GRAINS[14], KNOWLEDGE_GRAINS[15]]},
    UNITS[7]: {"scene": [SCENE_GRAINS[5]], "know": [KNOWLEDGE_GRAINS[16], KNOWLEDGE_GRAINS[17]]},
    UNITS[8]: {"scene": [SCENE_GRAINS[6], SCENE_GRAINS[7]], "know": [KNOWLEDGE_GRAINS[18], KNOWLEDGE_GRAINS[19], KNOWLEDGE_GRAINS[20]]},
}
ability_to_kunits = {
    ABILITY_MODULES[0]: [KNOWLEDGE_UNITS[0]],
    ABILITY_MODULES[1]: [KNOWLEDGE_UNITS[1], KNOWLEDGE_UNITS[2]],
    ABILITY_MODULES[2]: [KNOWLEDGE_UNITS[3], KNOWLEDGE_UNITS[4]],
    ABILITY_MODULES[3]: [KNOWLEDGE_UNITS[7]],
    ABILITY_MODULES[4]: [KNOWLEDGE_UNITS[5], KNOWLEDGE_UNITS[6]],
}
ability_to_projects = {
    ABILITY_MODULES[0]: [PROJECTS[1]],
    ABILITY_MODULES[1]: [PROJECTS[1]],
    ABILITY_MODULES[2]: [PROJECTS[2], PROJECTS[0]],
    ABILITY_MODULES[3]: [PROJECTS[0], PROJECTS[2]],
    ABILITY_MODULES[4]: [PROJECTS[0]],
}
kunit_to_grains = {
    KNOWLEDGE_UNITS[0]: [KNOWLEDGE_GRAINS[0], KNOWLEDGE_GRAINS[1], KNOWLEDGE_GRAINS[2]],
    KNOWLEDGE_UNITS[1]: [KNOWLEDGE_GRAINS[3], KNOWLEDGE_GRAINS[4]],
    KNOWLEDGE_UNITS[2]: [KNOWLEDGE_GRAINS[5], KNOWLEDGE_GRAINS[6], KNOWLEDGE_GRAINS[7]],
    KNOWLEDGE_UNITS[3]: [KNOWLEDGE_GRAINS[8], KNOWLEDGE_GRAINS[9], KNOWLEDGE_GRAINS[10]],
    KNOWLEDGE_UNITS[4]: [KNOWLEDGE_GRAINS[11], KNOWLEDGE_GRAINS[12]],
    KNOWLEDGE_UNITS[5]: [KNOWLEDGE_GRAINS[13], KNOWLEDGE_GRAINS[14], KNOWLEDGE_GRAINS[15]],
    KNOWLEDGE_UNITS[6]: [KNOWLEDGE_GRAINS[16], KNOWLEDGE_GRAINS[17]],
    KNOWLEDGE_UNITS[7]: [KNOWLEDGE_GRAINS[18], KNOWLEDGE_GRAINS[19], KNOWLEDGE_GRAINS[20], KNOWLEDGE_GRAINS[21]],
}
kunit_to_course = {
    KNOWLEDGE_UNITS[0]: COURSES[1], KNOWLEDGE_UNITS[1]: COURSES[1], KNOWLEDGE_UNITS[2]: COURSES[1],
    KNOWLEDGE_UNITS[3]: COURSES[0], KNOWLEDGE_UNITS[4]: COURSES[0],
    KNOWLEDGE_UNITS[5]: COURSES[2], KNOWLEDGE_UNITS[6]: COURSES[2], KNOWLEDGE_UNITS[7]: COURSES[2],
}

# ============ 生成有向边 ============
E = []
def add(fe, verb, te):
    E.append((fe, verb, te))

for p in PROJECTS:
    add(p, "直通", JOB)
for c, ps in course_to_projects.items():
    for p in ps:
        add(c, "支撑", p)
for u, c in unit_to_course.items():
    add(u, "组装", c)
for u, cp in unit_coupling.items():
    for g in cp["scene"]:
        add(g, "耦合", u)
    for g in cp["know"]:
        add(g, "耦合", u)
# 场景链
for cm in SCENE_MODULES:
    add(JOB, "提取", cm)
    add(cm, "再现", JOB)
for cm, css in scene_module_to_units.items():
    for cs in css:
        add(cm, "拆解", cs)
        add(cs, "供给", cm)
for cs, cks in scene_unit_to_grains.items():
    for ck in cks:
        add(cs, "拆分", ck)
        add(ck, "组合", cs)
for cm, ps in scene_module_to_projects.items():
    for p in ps:
        add(cm, "适用", p)
for cs, c in scene_unit_to_course.items():
    add(cs, "场景单元-专业认知", c)
# 能力/知识链
for nm in ABILITY_MODULES:
    add(JOB, "需求", nm)
    add(nm, "适配", JOB)
for nm, kss in ability_to_kunits.items():
    for ks in kss:
        add(nm, "重构", ks)
        add(ks, "供给", nm)
for ks, zks in kunit_to_grains.items():
    for zk in zks:
        add(ks, "解构", zk)
        add(zk, "聚合", ks)
for nm, ps in ability_to_projects.items():
    for p in ps:
        add(nm, "应用", p)
for ks, c in kunit_to_course.items():
    add(ks, "专业认知-专业认知", c)

# ============ 构建 data（出入双向对称）============
data = {c: {e: {"出": {}, "入": {}} for e in es} for c, es in concept_entities.items()}
for fe, verb, te in E:
    fc, tc = entity_concept[fe], entity_concept[te]
    data[fc][fe]["出"].setdefault(verb, []).append({"概念": tc, "实体": te})
    data[tc][te]["入"].setdefault(verb, []).append({"概念": fc, "实体": fe})

# ============ 构建 meta ============
relation_verbs = {}
for c in CONCEPTS:
    outv, inv = [], []
    for e in concept_entities[c]:
        for v in data[c][e]["出"]:
            if v not in outv:
                outv.append(v)
        for v in data[c][e]["入"]:
            if v not in inv:
                inv.append(v)
    relation_verbs[c] = {"出": outv, "入": inv}

total = sum(len(es) for es in concept_entities.values())
meta = {
    "说明": "大连理工大学生物学院·生物工程专业图谱：按 OBE 十概念的出/入关系动词挂载目标实体。中轴 教学单元→组装→专业认知课→支撑→项目化课→直通→岗位；左场景链、右能力/知识链向下拆解至最小颗粒，颗粒经耦合汇入教学单元。向上托为默认阅读视角。",
    "阅读方向": {
        "默认": "向上托",
        "向上托": "各颗粒度汇总成课直至岗位；展示回聚类动词与中轴（组装、支撑、直通、耦合、供给、聚合、组合、适配、再现、场景单元-专业认知、专业认知-专业认知等）",
        "向下拆": "从岗位沿场景链、能力/知识链拆至最小颗粒；不含项目化课、专业认知课、教学单元；仅分解类动词（提取、需求、拆解、拆分、解构、重构等）",
    },
    "实体总数": total,
    "概念": CONCEPTS,
    "关系动词": relation_verbs,
}
result = {"meta": meta, "data": data}
js = "window.OBE_RELATION_DATA = " + json.dumps(result, ensure_ascii=False, separators=(",", ":")) + ";"

# ============ 注入 dna.html ============
lines = DNA.read_text(encoding="utf-8").split("\n")
hit = False
for i, l in enumerate(lines):
    if l.strip().startswith("window.OBE_RELATION_DATA"):
        lines[i] = "    " + js
        lines[i - 1] = "    /* 数据源：大连理工大学生物学院·生物工程专业 OBE 图谱（_build_bio.py 生成） */"
        lines[i - 2] = "    /* Inline data for single-file delivery. */"
        hit = True
        break
if not hit:
    raise SystemExit("未找到 window.OBE_RELATION_DATA 数据行")
DNA.write_text("\n".join(lines), encoding="utf-8")
print(f"注入完成：{total} 个实体，{len(E)} 条有向边（{len(E) * 2} 个出/入挂载点）")
