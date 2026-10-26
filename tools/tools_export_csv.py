# -*- coding: utf-8 -*-
"""一次性迁移脚本：把现有 Python 数据导出为 CSV 数据集。

迁移后，CSV 成为唯一数据源（build.py 只读 CSV），本脚本与 seed/ 下的 Python 模块
仅作为历史留档，可在确认 CSV 完整后删除。

生成的数据集：
  data/entries.csv        每个代码一行：code, group, full_en, name_<lang>×N
  data/entry_text.csv     每个代码每种语言一行：code, lang, desc, note
  data/regions.csv        每个地区一行：id, flag, local_lang, script
  data/region_text.csv    每个地区每种语言一行：region_id, lang, label, intro, warn, basis, sources, foot_src
  data/region_codes.csv   地区专属代码覆盖：region_id, group, base_code, code, name, full, note
  data/region_extras.csv  地区特有条目
  data/region_conflicts.csv 地区特有易混代码
  data/conflicts.csv      基准易混代码
  data/conflict_text.csv  基准易混代码的分语言说明
  data/rules.csv          编号规则（骨架）
  data/rule_text.csv      编号规则的分语言标题与要点
  data/i18n.csv           界面文案：key + 每种语言一列
"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "seed")   # 旧版 Python 数据源留档在 seed/
for _p in (ROOT, SEED):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from data_common import LANGS
from data_regions import REGIONS
from data_conflict import CONFLICT, RULES
from i18n import I18N
from zh_hant import to_hans
from data_mat import MAT_FINISH, MAT_FF_E
from data_light import LIGHT
from data_finish import FINISH

GROUPS = {"mat": MAT_FINISH, "obj": MAT_FF_E, "light": LIGHT, "finish": FINISH}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "data")   # 数据集在仓库根目录 data/
os.makedirs(OUT_DIR, exist_ok=True)


def w(name, header, rows):
    path = os.path.join(OUT_DIR, name)
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    print("%-24s %5d 行" % (name, len(rows)))


def hans(s):
    """仅用于中文（简体）列的归一化。"""
    return to_hans(s) if s else s


def loc(lg, s):
    """按语言处理：只有 zh 做简体归一化，其余语言原样保留（日文汉字不被误改）。"""
    if not s:
        return s
    return hans(s) if lg == "zh" else s


# ---------------------------------------------------------------- entries
entries, etext = [], []
for g, items in GROUPS.items():
    for e in items:
        row = [e["code"], g, e["full"]]
        for lg in LANGS:
            row.append(loc(lg, e["loc"][lg]["name"]))
        entries.append(row)
        for lg in LANGS:
            etext.append([g, e["code"], lg, loc(lg, e["loc"][lg]["desc"]), loc(lg, e["loc"][lg]["note"])])
w("entries.csv", ["code", "group", "full_en"] + ["name_%s" % lg for lg in LANGS], entries)
w("entry_text.csv", ["group", "code", "lang", "desc", "note"], etext)

# ---------------------------------------------------------------- regions
regions, rtext = [], []
for r in REGIONS:
    regions.append([r["id"], r["flag"], r.get("local_lang", "zh"), r.get("script", "")])
    for lg in LANGS:
        label = r["label"].get(lg, r["label"]["zh"])
        intro = r["intro"].get(lg, r["intro"]["zh"])
        warn = (r.get("warn") or {}).get(lg, "")
        basis = (r.get("basis") or {}).get(lg, "")
        sources = (r.get("sources") or {}).get(lg, [])
        foot = (r.get("foot_src") or {}).get(lg, "")
        rtext.append([r["id"], lg, loc(lg, label), loc(lg, intro), loc(lg, warn), loc(lg, basis),
                      " ; ".join(loc(lg, x) for x in sources), loc(lg, foot)])
w("regions.csv", ["id", "flag", "local_lang", "script"], regions)
w("region_text.csv", ["region_id", "lang", "label", "intro", "warn", "basis", "sources", "foot_src"], rtext)

# ---------------------------------------------------------------- 地区覆盖
rcodes = []
for r in REGIONS:
    rid = r["id"]
    keys = set()
    for tbl in ("codes", "names", "fulls", "notes"):
        keys |= set((r.get(tbl) or {}).keys())
    for key in sorted(keys):
        group, _, code = key.rpartition(":")
        if not group:
            group, code = "", key
        rcodes.append([
            rid, group, code,
            (r.get("codes") or {}).get(key, ""),
            hans((r.get("names") or {}).get(key, "")),
            (r.get("fulls") or {}).get(key, ""),
            hans((r.get("notes") or {}).get(key, "")),
        ])
w("region_codes.csv", ["region_id", "group", "base_code", "code", "name", "full", "note"], rcodes)

rextras = []
for r in REGIONS:
    for e in r.get("extras", []):
        rextras.append([r["id"], e["code"], e["full"], hans(e["loc"]["zh"]["name"]),
                        hans(e["loc"]["zh"]["desc"]), hans(e["loc"]["zh"]["note"])])
w("region_extras.csv", ["region_id", "code", "full", "name", "desc", "note"], rextras)

rconf = []
for r in REGIONS:
    for c in r.get("conflicts", []):
        a = c["a"][1] if c["a"][0] == "lit" else ""
        b = c["b"][1] if c["b"][0] == "lit" else ""
        rconf.append([r["id"], c["code"], a, b, hans(c["howto"]["zh"])])
w("region_conflicts.csv", ["region_id", "code", "a_text", "b_text", "howto"], rconf)

# ---------------------------------------------------------------- 基准冲突
cbase, ctext = [], []
for c in CONFLICT:
    a_ref = ("%s:%s" % (c["a"][1], c["a"][2])) if c["a"][0] == "ref" else ""
    b_ref = ("%s:%s" % (c["b"][1], c["b"][2])) if c["b"][0] == "ref" else ""
    row = [c["code"], a_ref, b_ref]
    for lg in LANGS:                      # 字面量含义按语言分列
        row.append(loc(lg, c["a"][1][lg]) if c["a"][0] == "lit" else "")
    for lg in LANGS:
        row.append(loc(lg, c["b"][1][lg]) if c["b"][0] == "lit" else "")
    cbase.append(row)
    for lg in LANGS:
        ctext.append([c["code"], lg, loc(lg, c["howto"][lg])])
w("conflicts.csv", ["code", "a_ref", "b_ref"]
  + ["a_%s" % lg for lg in LANGS] + ["b_%s" % lg for lg in LANGS], cbase)
w("conflict_text.csv", ["code", "lang", "howto"], ctext)

# ---------------------------------------------------------------- 编号规则
rb, rt = [], []
for i, r in enumerate(RULES, 1):
    ex = r["example"]
    ex = ex if isinstance(ex, str) else ex["zh"]
    rb.append(["R%d" % i, ex])
    for lg in LANGS:
        rt.append(["R%d" % i, lg, loc(lg, r["title"][lg]), loc(lg, r["detail"][lg])])
w("rules.csv", ["rule_id", "example"], rb)
w("rule_text.csv", ["rule_id", "lang", "title", "detail"], rt)

# ---------------------------------------------------------------- i18n
irows = []
for k, v in I18N.items():
    irows.append([k] + [loc(lg, v.get(lg, "")) for lg in LANGS])
w("i18n.csv", ["key"] + LANGS, irows)

print("\n数据集已写入：", OUT_DIR)
