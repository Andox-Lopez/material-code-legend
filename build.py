# -*- coding: utf-8 -*-
"""施工图材料代码多语多地区对照表 —— 构建脚本（数据源为 CSV）

用法：
    python build.py
输出（同一目录）：
    index.html                        在线版：运行时从 data/*.csv 读取
    施工图材料代码多语对照表.html          离线版：全部 CSV 内嵌，单文件零依赖
    施工图材料代码多语对照表.xlsx          多地区 × 多语言 Excel
    logo.svg                          站点标识

数据源（唯一真相源，均为 CSV，UTF-8 with BOM）：
    data/entries.csv        每个代码一行：code, group, full_en, name_<lang>…
    data/entry_text.csv     每个代码每种语言一行：group, code, lang, desc, note
    data/regions.csv        每个地区一行：id, flag, local_lang, script
    data/region_text.csv    每个地区每种语言一行：region_id, lang, label, intro, warn, basis, sources, foot_src
    data/region_codes.csv   地区代码覆盖：region_id, group, base_code, code, name, full, note
    data/region_extras.csv  地区特有条目
    data/region_conflicts.csv 地区特有易混代码
    data/conflicts.csv      基准易混代码
    data/conflict_text.csv  基准易混代码的分语言说明
    data/rules.csv          编号规则骨架
    data/rule_text.csv      编号规则的分语言标题与要点
    data/i18n.csv           界面文案：key + 每种语言一列
"""
import base64
import csv
import io
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = BASE

LANGS = ["zh", "en", "ja", "ko", "es", "fr", "it", "pt", "ru"]
CSV_FILES = [
    "entries.csv", "entry_text.csv", "regions.csv", "region_text.csv",
    "region_codes.csv", "region_extras.csv", "region_conflicts.csv",
    "conflicts.csv", "conflict_text.csv", "rules.csv", "rule_text.csv", "i18n.csv",
]

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Material Code Legend">
<title>施工图材料代码对照表</title>
<defs>
<linearGradient id="mcl-bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0a3a66"/><stop offset="0.55" stop-color="#125e9f"/><stop offset="1" stop-color="#1e86dd"/>
</linearGradient>
<linearGradient id="mcl-top" x1="0.2" y1="0" x2="0.8" y2="1">
<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d8ecff"/>
</linearGradient>
</defs>
<rect width="64" height="64" rx="14" fill="url(#mcl-bg)"/>
<g stroke="#ffffff" stroke-opacity="0.15" stroke-width="1">
<path d="M16 0V64M32 0V64M48 0V64M0 16H64M0 32H64M0 48H64"/>
</g>
<rect x="0.75" y="0.75" width="62.5" height="62.5" rx="13.25" fill="none" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.5"/>
<g>
<rect x="22" y="8" width="20" height="8" rx="4" fill="#f0b429"/>
<rect x="25.5" y="11" width="5.5" height="2" rx="1" fill="#0a3a66" fill-opacity="0.6"/>
<rect x="32.5" y="11" width="4" height="2" rx="1" fill="#0a3a66" fill-opacity="0.38"/>
</g>
<g stroke-linejoin="round">
<path d="M12 44.5 L32 34 L52 44.5 L32 55 Z" fill="#ffffff" fill-opacity="0.5"/>
<path d="M12 36.5 L32 26 L52 36.5 L32 47 Z" fill="#ffffff" fill-opacity="0.75"/>
<path d="M12 28.5 L32 18 L52 28.5 L32 39 Z" fill="url(#mcl-top)"/>
</g>
</svg>"""

FAVICON_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("ascii")


# ---------------------------------------------------------------- CSV 读取
def read_csv_text(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8-sig", newline="") as f:
        return f.read()


def read_csv_rows(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- 繁体映射
def hant_map():
    """为使用繁体的地区（hk / mo / tw）预生成 zh → 繁体 的对照表，供页面在运行时转换。

    在构建期用 zhconv 计算，既保证在线版与离线版结果完全一致，
    也让页面只保留一份纯 CSV（简体）作为数据源。
    """
    from zh_hant import to_hant
    texts = set()
    # 只收"中文那一列"的文本：繁体转换只作用于中文，其余语言保持原样
    # （此前把所有语言都收进来，既把日/韩等误转成中文繁体，又让对照表膨胀到数 MB。）
    for r in read_csv_rows("entries.csv"):
        texts.add(r.get("name_zh", ""))
    for r in read_csv_rows("entry_text.csv"):
        if r.get("lang") != "zh":
            continue
        texts.add(r.get("desc", ""))
        texts.add(r.get("note", ""))
    for r in read_csv_rows("region_text.csv"):
        if r.get("lang") != "zh":
            continue
        for k in ("label", "intro", "warn", "basis", "foot_src"):
            texts.add(r.get(k, ""))
        for s in (r.get("sources", "") or "").split(" ; "):
            texts.add(s)
    for r in read_csv_rows("i18n.csv"):
        texts.add(r.get("zh", ""))
    for r in read_csv_rows("conflict_text.csv"):
        texts.add(r.get("zh", ""))
    for r in read_csv_rows("rule_text.csv"):
        if r.get("lang") != "zh":
            continue
        texts.add(r.get("title", ""))
        texts.add(r.get("detail", ""))
        texts.add(r.get("example", ""))
    for r in read_csv_rows("region_extras.csv"):
        texts.add(r.get("name", ""))
        texts.add(r.get("desc", ""))
        texts.add(r.get("note", ""))
    for r in read_csv_rows("region_codes.csv"):
        texts.add(r.get("name", ""))
        texts.add(r.get("note", ""))
    for r in read_csv_rows("conflicts.csv"):
        texts.add(r.get("a_zh", ""))
        texts.add(r.get("b_zh", ""))
    for r in read_csv_rows("region_conflicts.csv"):
        texts.add(r.get("a_zh", ""))
        texts.add(r.get("b_zh", ""))
        texts.add(r.get("howto_zh", ""))
    texts = {t for t in texts if t.strip()}

    out = {}
    for r in read_csv_rows("regions.csv"):
        if (r.get("script") or "") != "hant":
            continue
        rid = r["id"]
        # 排序后输出：否则集合迭代顺序会让每次构建产生噪声 diff
        out[rid] = {t: to_hant(t, rid) for t in sorted(texts)}
    return out


# ---------------------------------------------------------------- 页面装配（与前端 assemble() 保持一致）
def assemble_python():
    """按 CSV 装配成页面用的数据结构（供 Excel 导出与自检使用）。"""
    entries = read_csv_rows("entries.csv")
    etext = read_csv_rows("entry_text.csv")
    regions = read_csv_rows("regions.csv")
    rtext = {(r["region_id"], r["lang"]): r for r in read_csv_rows("region_text.csv")}
    rcodes = read_csv_rows("region_codes.csv")
    rextras = read_csv_rows("region_extras.csv")
    rconf = read_csv_rows("region_conflicts.csv")
    conflicts = read_csv_rows("conflicts.csv")
    ctext = {(r["code"], r["lang"]): r for r in read_csv_rows("conflict_text.csv")}
    rules = read_csv_rows("rules.csv")
    rtext2 = {(r["rule_id"], r["lang"]): r for r in read_csv_rows("rule_text.csv")}

    by_key = {}
    for r in entries:
        e = {"code": r["code"], "base": r["code"], "group": r["group"], "full": r["full_en"],
             "name": {}, "loc": {}}
        for lg in LANGS:
            e["name"][lg] = r.get("name_" + lg, "")
            e["loc"][lg] = {"desc": "", "note": ""}
        by_key[(r["group"], r["code"])] = e
    for r in etext:
        e = by_key.get((r["group"], r["code"]))
        if e and r["lang"] in LANGS:
            e["loc"][r["lang"]] = {"desc": r.get("desc", ""), "note": r.get("note", "")}

    out = {}
    for rg in regions:
        rid = rg["id"]
        local_lang = rg.get("local_lang", "zh")
        view = {"id": rid, "flag": rg["flag"], "local_lang": rg.get("local_lang", "zh"),
                "script": rg.get("script", ""), "label": {}, "intro": {}, "warn": {},
                "sources": {}, "foot_src": {}, "groups": {}, "extras": [],
                "conflicts": [], "rules": [], "diff": [], "index": []}
        for lg in LANGS:
            t = rtext.get((rid, lg), {})
            view["label"][lg] = t.get("label", "")
            view["intro"][lg] = t.get("intro", "")
            view["warn"][lg] = t.get("warn", "")
            view["sources"][lg] = [x for x in (t.get("sources", "") or "").split(" ; ") if x.strip()]
            view["foot_src"][lg] = t.get("foot_src", "")

        ov = {}
        for r in rcodes:
            if r["region_id"] != rid:
                continue
            ov[(r.get("group", ""), r["base_code"])] = r

        for g in ("mat", "obj", "light", "finish"):
            rows = []
            for (eg, ec), e in by_key.items():
                if eg != g:
                    continue
                o = ov.get((g, ec)) or ov.get(("", ec))
                code = (o or {}).get("code") or e["code"]
                name = (o or {}).get("name") or e["name"]["zh"]
                local_name = name or e["name"].get(local_lang) or e["name"].get("zh") or e["code"]
                row = {"code": code, "base": e["code"], "group": g,
                       "full": (o or {}).get("full") or e["full"],
                       "name": local_name,
                       "loc": {k: dict(v) for k, v in e["loc"].items()},
                       "rnote": (o or {}).get("note", "")}
                rows.append(row)
                if code != e["code"]:
                    view["diff"].append({"base": e["code"], "code": code,
                                         "name": local_name, "full": row["full"], "group": g})
            view["groups"][g] = rows

        for r in rextras:
            if r["region_id"] != rid:
                continue
            ex = {"code": r["code"], "base": r["code"], "full": r["full"], "name": r["name"], "loc": {}}
            for lg in LANGS:
                ex["loc"][lg] = {"desc": r["desc"], "note": r["note"]}
            view["extras"].append(ex)

        for c in conflicts:
            a = by_key.get(tuple(c["a_ref"].split(":"))) if c["a_ref"] else None
            b = by_key.get(tuple(c["b_ref"].split(":"))) if c["b_ref"] else None
            item = {"code": c["code"], "a": {}, "b": {}, "howto": {}, "is_extra": False}
            for lg in LANGS:
                item["a"][lg] = (a["name"][lg] if a else "") or c.get("a_" + lg, "")
                item["b"][lg] = (b["name"][lg] if b else "") or c.get("b_" + lg, "")
                item["howto"][lg] = ctext.get((c["code"], lg), {}).get(lg, "")
            view["conflicts"].append(item)
        for c in rconf:
            if c["region_id"] != rid:
                continue
            item = {"code": c["code"], "a": {}, "b": {}, "howto": {}, "is_extra": True}
            for lg in LANGS:
                item["a"][lg] = c.get("a_" + lg, "")
                item["b"][lg] = c.get("b_" + lg, "")
                item["howto"][lg] = c.get("howto_" + lg, "")
            view["conflicts"].append(item)

        for rr in rules:
            item = {"title": {}, "detail": {}, "example": {}}
            for lg in LANGS:
                t = rtext2.get((rr["rule_id"], lg), {})
                item["title"][lg] = t.get("title", "")
                item["detail"][lg] = t.get("detail", "")
                item["example"][lg] = t.get("example", rr["example"])
            view["rules"].append(item)

        for g in ("mat", "obj", "light", "finish"):
            for row in view["groups"][g]:
                view["index"].append({"code": row["code"], "base": row["base"], "full": row["full"],
                                      "group": g, "name": row["name"]})
        for ex in view["extras"]:
            view["index"].append({"code": ex["code"], "base": ex["code"], "full": ex["full"],
                                  "group": "extra", "name": ex["name"]})

        if view["script"] == "hant":
            from zh_hant import to_hant
            cv = lambda x: to_hant(x, rid) if x else x
            view["label"]["zh"] = cv(view["label"]["zh"])
            view["intro"]["zh"] = cv(view["intro"]["zh"])
            view["warn"]["zh"] = cv(view["warn"]["zh"])
            view["foot_src"]["zh"] = cv(view["foot_src"]["zh"])
            view["sources"]["zh"] = [cv(x) for x in view["sources"]["zh"]]
            for g in ("mat", "obj", "light", "finish"):
                for row in view["groups"][g]:
                    row["name"] = cv(row["name"])
                    row["loc"]["zh"] = {"desc": cv(row["loc"]["zh"]["desc"]),
                                        "note": cv(row["loc"]["zh"]["note"])}
            for ex in view["extras"]:
                ex["name"] = cv(ex["name"])
                ex["loc"]["zh"] = {"desc": cv(ex["loc"]["zh"]["desc"]), "note": cv(ex["loc"]["zh"]["note"])}
            for c in view["conflicts"]:
                c["a"]["zh"] = cv(c["a"]["zh"]); c["b"]["zh"] = cv(c["b"]["zh"]); c["howto"]["zh"] = cv(c["howto"]["zh"])
            for r in view["rules"]:
                r["title"]["zh"] = cv(r["title"]["zh"]); r["detail"]["zh"] = cv(r["detail"]["zh"])
        out[rid] = view
    return out


# ---------------------------------------------------------------- 静态配置
SECTIONS = [
    {"key": "mat", "group": "mat", "title": "g_mat", "sub": "g_mat_sub", "col": "col_desc"},
    {"key": "obj", "group": "obj", "title": "g_obj", "sub": "g_obj_sub", "col": "col_desc"},
    {"key": "light", "group": "light", "title": "g_light", "sub": "g_light_sub", "col": "col_desc2"},
    {"key": "finish", "group": "finish", "title": "g_finish", "sub": "g_finish_sub", "col": "col_desc2"},
    {"key": "extra", "group": "extra", "title": "g_extra_title", "sub": "g_extra_sub", "col": "col_desc2"},
    {"key": "conflict", "group": "conflict", "title": "g_conflict", "sub": "g_conflict_sub"},
    {"key": "rules", "group": None, "title": "g_rules", "sub": "g_rules_sub"},
]

TABS = [
    {"id": "all", "label": "tab_all"},
    {"id": "mat", "label": "tab_mat"},
    {"id": "obj", "label": "tab_obj"},
    {"id": "light", "label": "tab_light"},
    {"id": "finish", "label": "tab_finish"},
    {"id": "extra", "label": "tab_extra"},
    {"id": "conflict", "label": "tab_conflict"},
]

LANG_META = {
    "zh": {"label": "中文", "en_label": "Chinese", "html": "zh-CN"},
    "en": {"label": "English", "en_label": "English", "html": "en"},
    "ja": {"label": "日本語", "en_label": "Japanese", "html": "ja"},
    "ko": {"label": "한국어", "en_label": "Korean", "html": "ko"},
    "es": {"label": "Español", "en_label": "Spanish", "html": "es"},
    "fr": {"label": "Français", "en_label": "French", "html": "fr"},
    "it": {"label": "Italiano", "en_label": "Italian", "html": "it"},
    "pt": {"label": "Português", "en_label": "Portuguese", "html": "pt"},
    "ru": {"label": "Русский", "en_label": "Russian", "html": "ru"},
}


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark" data-lang="zh" data-region="cn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>施工图材料代码 多语对照表</title>
<meta name="description" content="施工图材料大类代码 · 按地区划分的缩写与全称对照 · 中日英韩西法意葡俄多语言 · Material Legend">
<link rel="icon" type="image/svg+xml" href="__FAVICON__">
<link rel="apple-touch-icon" href="__FAVICON__">
<meta name="theme-color" content="#0a3a66">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117; --bg2:#0a0e14; --panel:#141a22; --panel2:#182029;
  --line:#232c38; --line2:#2c3644;
  --ink:#e7eef6; --ink2:#c3cedb; --muted:#8b98a9; --faint:#5d6b7c;
  --accent:#4da3ff; --accent-soft:rgba(77,163,255,.13); --accent-line:rgba(77,163,255,.4);
  --warn:#f0b429; --warn-soft:rgba(240,180,41,.1); --warn-line:rgba(240,180,41,.35);
  --ok:#3fd08a; --shadow:0 10px 30px rgba(0,0,0,.35); --radius:14px;
}
html[data-theme="light"]{
  --bg:#f4f6f9; --bg2:#eef1f5; --panel:#ffffff; --panel2:#f8fafc;
  --line:#e2e8f0; --line2:#d5dde7;
  --ink:#0f172a; --ink2:#26344a; --muted:#5c6b7f; --faint:#8797a8;
  --accent:#0f4c81; --accent-soft:rgba(15,76,129,.08); --accent-line:rgba(15,76,129,.28);
  --warn:#a15c07; --warn-soft:rgba(161,92,7,.08); --warn-line:rgba(161,92,7,.28);
  --ok:#12775a; --shadow:0 8px 24px rgba(15,23,42,.08);
}
body{
  font-family:"Inter","Segoe UI",system-ui,-apple-system,"Microsoft YaHei","PingFang SC",
    "Hiragino Sans GB","Noto Sans CJK SC","Malgun Gothic","Apple SD Gothic Neo",sans-serif;
  background:var(--bg);color:var(--ink);font-size:14.5px;line-height:1.6;
  -webkit-font-smoothing:antialiased;transition:background .25s,color .25s;
}
body::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    linear-gradient(90deg,var(--accent-soft) 1px,transparent 1px) 0 0/56px 56px,
    linear-gradient(var(--accent-soft) 1px,transparent 1px) 0 0/56px 56px;
  opacity:.5;
}
.wrap{position:relative;z-index:1;max-width:1280px;margin:0 auto;padding:30px 26px 80px}

/* ---------- hero ---------- */
.hero{
  border:1px solid var(--line);border-radius:var(--radius);
  background:linear-gradient(160deg,var(--panel) 0%,var(--bg2) 100%);
  padding:24px 26px 20px;box-shadow:var(--shadow);
}
/* 头部固定两行：标题行 + 控件行，不随语言与窗口宽度浮动 */
.hero-top{display:flex;gap:14px 20px;align-items:flex-start;flex-wrap:wrap;justify-content:space-between}
.brand{display:flex;gap:14px;align-items:center;flex:1 1 100%;min-width:0}
.logo{
  width:46px;height:46px;flex:0 0 46px;border-radius:13px;overflow:hidden;line-height:0;
  box-shadow:0 4px 14px rgba(10,58,102,.28)
}
.logo svg{width:100%;height:100%;display:block}
h1{font-size:24px;font-weight:700;letter-spacing:.4px;line-height:1.25}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--muted);font-size:12.8px;margin-top:5px}
/* 控件组永不内部换行：宽度不足时整组移到标题下方，各语言表现一致 */
.hero-tools{display:flex;gap:14px;align-items:flex-end;flex-wrap:nowrap;min-width:0;flex:1 1 100%;justify-content:flex-start}
.lang-pick{display:flex;flex-direction:column;gap:4px;min-width:0}
.lang-pick select{
  border:1px solid var(--line);background:var(--panel2);color:var(--ink);border-radius:10px;
  padding:8px 30px 8px 12px;font-size:13px;font-family:inherit;cursor:pointer;outline:none;
  appearance:none;-webkit-appearance:none;min-width:152px;text-overflow:ellipsis;
  background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);
  background-position:calc(100% - 15px) 50%,calc(100% - 10px) 50%;
  background-size:5px 5px,5px 5px;background-repeat:no-repeat
}
.lang-pick select:hover{border-color:var(--accent-line)}
.hero-btns{display:flex;gap:8px;align-items:center;padding-bottom:1px}
.icon-btn{
  border:1px solid var(--line);background:var(--panel2);color:var(--ink2);cursor:pointer;
  width:38px;height:38px;border-radius:10px;display:grid;place-items:center;transition:.16s
}
.icon-btn:hover{border-color:var(--accent-line);color:var(--accent)}
.icon-btn svg{width:18px;height:18px}
.region-pick{display:flex;flex-direction:column;gap:4px;flex:0 1 auto;min-width:0}
.region-pick span{font-size:10.5px;color:var(--faint);letter-spacing:.5px;padding-left:3px;white-space:nowrap}
.region-pick select{
  border:1px solid var(--line);background:var(--panel2);color:var(--ink);border-radius:10px;
  padding:8px 30px 8px 12px;font-size:13px;font-family:inherit;cursor:pointer;outline:none;
  appearance:none;-webkit-appearance:none;max-width:196px;text-overflow:ellipsis;
  background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);
  background-position:calc(100% - 15px) 50%,calc(100% - 10px) 50%;
  background-size:5px 5px,5px 5px;background-repeat:no-repeat
}
.region-pick select:hover{border-color:var(--accent-line)}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.stat{
  border:1px solid var(--line);background:var(--panel2);border-radius:10px;
  padding:8px 14px;min-width:96px
}
.stat b{display:block;font-size:18px;color:var(--accent);line-height:1.2;font-family:"Consolas","SF Mono",monospace}
.stat span{font-size:11.5px;color:var(--muted)}

/* ---------- notice ---------- */
body.loading #main{opacity:.35}
.boot-err{display:none;margin-top:14px;border:1px solid var(--warn-line);background:var(--warn-soft);
  border-radius:10px;padding:12px 16px;color:var(--warn);font-size:13px}
.notice{
  margin-top:16px;border:1px solid var(--warn-line);background:var(--warn-soft);
  border-left:3px solid var(--warn);border-radius:0 12px 12px 0;padding:14px 18px;
  font-size:12.8px;color:var(--ink2);line-height:1.75
}
.notice b{color:var(--warn)}
.notice .warnline{display:block;margin-top:6px;color:var(--muted)}
.region-note{
  margin-top:16px;border:1px solid var(--accent-line);background:var(--accent-soft);
  border-left:3px solid var(--accent);border-radius:0 12px 12px 0;padding:14px 18px;
  font-size:12.8px;color:var(--ink2);line-height:1.75
}
.region-note b{color:var(--accent)}
.region-note .rf{font-size:15px;margin-right:6px}
.region-note .rmeta{margin-left:10px;color:var(--muted);font-size:12.2px}
.region-note .warnline{display:block;margin-top:6px;color:var(--muted)}
/* ---------- 本地区资料依据 ---------- */
.sources{
  margin-top:14px;border:1px solid var(--line);background:var(--panel);
  border-radius:12px;padding:14px 18px;font-size:12.6px;color:var(--ink2)
}
.sources-head{
  font-size:12.6px;font-weight:700;color:var(--ink);display:flex;align-items:center;
  gap:10px;flex-wrap:wrap;margin-bottom:9px
}
.sources-head:before{content:"";width:4px;height:15px;background:var(--accent);border-radius:2px;flex:0 0 4px}
.sources-head em{font-style:normal;font-weight:400;font-size:11.8px;color:var(--muted)}
.sources ul{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:6px 22px}
.sources li{position:relative;padding-left:15px;line-height:1.65;color:var(--ink2)}
.sources li:before{content:"";position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:var(--accent-line)}

/* ---------- toolbar ---------- */
.toolbar{
  position:sticky;top:0;z-index:40;margin-top:18px;padding:12px 0 10px;
  background:linear-gradient(var(--bg) 72%,transparent);backdrop-filter:blur(10px)
}
.tabs{display:flex;gap:7px;flex-wrap:wrap}
.tab{
  border:1px solid var(--line);background:var(--panel);color:var(--ink2);border-radius:999px;
  padding:6px 15px;font-size:12.8px;cursor:pointer;transition:.16s;font-family:inherit;white-space:nowrap
}
.tab:hover{border-color:var(--accent-line)}
.tab.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
html[data-theme="light"] .tab.on{color:#fff}
.searchrow{display:flex;gap:12px;align-items:center;margin-top:11px;flex-wrap:wrap}
.search{
  flex:1 1 320px;display:flex;align-items:center;gap:9px;border:1px solid var(--line);
  background:var(--panel);border-radius:11px;padding:0 12px;transition:.16s
}
.search:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.search svg{width:16px;height:16px;color:var(--muted);flex:0 0 16px}
.search input{
  flex:1;border:0;background:transparent;color:var(--ink);font-family:inherit;font-size:13.4px;
  padding:10px 0;outline:none;min-width:120px
}
.search input::-webkit-search-cancel-button{display:none}
.clear-btn{border:0;background:transparent;color:var(--faint);cursor:pointer;font-size:16px;line-height:1;padding:4px}
.clear-btn:hover{color:var(--danger)}
.seg{display:flex;border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:3px;gap:3px}
.seg button{
  border:0;background:transparent;color:var(--muted);padding:5px 13px;border-radius:8px;
  font-size:12.5px;cursor:pointer;font-family:inherit;transition:.15s
}
.seg button.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
.count{font-size:12.2px;color:var(--muted);white-space:nowrap}

/* ---------- section ---------- */
section.blk{margin-top:26px}
h2{
  font-size:15.5px;font-weight:700;display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  margin-bottom:11px
}
h2:before{content:"";width:4px;height:17px;background:var(--accent);border-radius:2px;flex:0 0 4px}
h2 em{font-style:normal;font-weight:400;font-size:12px;color:var(--muted)}
.h2count{
  margin-left:auto;font-size:11.5px;color:var(--muted);border:1px solid var(--line);
  border-radius:999px;padding:2px 10px;font-family:"Consolas","SF Mono",monospace
}
.card{
  background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden;box-shadow:var(--shadow)
}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:13.2px;min-width:720px}
thead th{
  background:var(--panel2);text-align:left;font-weight:600;font-size:11.8px;color:var(--muted);
  padding:11px 13px;border-bottom:1px solid var(--line);letter-spacing:.4px;white-space:nowrap;
  position:sticky;top:0
}
tbody td{padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--accent-soft)}
td.code,th.code{
  font-family:"Consolas","SF Mono","JetBrains Mono",monospace;font-weight:700;color:var(--accent);
  white-space:nowrap;letter-spacing:.6px;cursor:copy;font-size:13.4px
}
td.code:hover{text-decoration:underline dotted}
td.full{color:var(--muted);font-size:12.4px}
td.name{color:var(--ink);font-weight:600}
td.desc{color:var(--ink2);font-size:12.8px}
td.note{color:var(--muted);font-size:12.2px}
tr.conflict td.code{color:var(--warn)}
.badge{
  display:inline-block;font-size:10.5px;border-radius:5px;padding:1px 7px;margin-left:6px;
  background:var(--warn-soft);color:var(--warn);border:1px solid var(--warn-line);vertical-align:1px
}
.badge.region{background:var(--accent-soft);color:var(--accent);border-color:var(--accent-line)}
.badge.base{
  background:transparent;color:var(--faint);border-color:var(--line2);font-weight:400;
  font-family:"Consolas",monospace;margin-left:6px
}
.subname{display:block;font-size:11.8px;color:var(--faint);font-weight:400;margin-top:2px}
.rnote{
  display:block;margin-bottom:5px;padding-left:8px;border-left:2px solid var(--accent);
  color:var(--accent);font-size:12px
}
mark{background:rgba(240,180,41,.32);color:inherit;padding:0 2px;border-radius:3px}
html[data-theme="light"] mark{background:rgba(240,180,41,.42)}

/* ---------- 地区对照表 ---------- */
.diffmap{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px}
.dcell{
  border:1px solid var(--line);border-radius:10px;padding:11px 13px;background:var(--panel);
  display:flex;flex-direction:column;gap:4px
}
.dcell .dtop{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dcell .from{font-family:"Consolas",monospace;font-size:11.5px;color:var(--faint)}
.dcell .arrow{color:var(--muted);font-size:11px}
.dcell .to{font-family:"Consolas",monospace;font-weight:700;color:var(--accent);font-size:14px;letter-spacing:.5px}
.dcell .dn{font-size:12.6px;color:var(--ink);font-weight:600}
.dcell .df{font-size:11.6px;color:var(--muted)}
.dcell .dnote{font-size:11.5px;color:var(--faint);border-top:1px dashed var(--line);padding-top:4px}

/* ---------- rules ---------- */
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));gap:13px}
.rule{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 17px}
.rule h3{font-size:13.2px;margin-bottom:8px;color:var(--accent)}
.rule .eg{
  font-family:"Consolas",monospace;font-size:12px;background:var(--accent-soft);color:var(--ink);
  padding:4px 9px;border-radius:6px;display:inline-block;margin-bottom:9px;word-break:break-all
}
.rule p{font-size:12.4px;color:var(--muted);line-height:1.7}

/* ---------- index cards ---------- */
.idx{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:12px}
.icard{
  background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:13px 14px;
  cursor:pointer;transition:.16s;display:flex;flex-direction:column;gap:5px
}
.icard:hover{border-color:var(--accent-line);transform:translateY(-2px);box-shadow:var(--shadow)}
.icard .code{
  font-family:"Consolas","SF Mono",monospace;font-weight:700;color:var(--accent);
  font-size:15px;letter-spacing:.8px;display:flex;align-items:center;gap:8px
}
.icard .full{font-size:12.2px;color:var(--ink2);line-height:1.5}
.icard .name{font-size:12.4px;color:var(--muted);font-weight:600}
.icard .grp{
  font-size:10.5px;color:var(--faint);border:1px solid var(--line);border-radius:5px;
  padding:1px 6px;margin-left:auto
}
.letter{
  grid-column:1/-1;font-size:12px;font-weight:700;color:var(--accent);
  border-bottom:1px solid var(--line);padding-bottom:5px;margin-top:6px;letter-spacing:1px
}

/* ---------- footer ---------- */
.foot{margin-top:36px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);font-size:12.2px;line-height:1.85}
.foot p{margin-bottom:5px}
.foot b{color:var(--ink2)}
.foot .muted{color:var(--faint);font-size:11.6px;margin-top:8px}
.empty{padding:38px;text-align:center;color:var(--muted);font-size:13px}

/* ---------- toast ---------- */
#toast{
  position:fixed;left:50%;bottom:28px;transform:translate(-50%,16px);opacity:0;pointer-events:none;
  background:var(--ink);color:var(--bg);padding:9px 18px;border-radius:999px;font-size:12.8px;
  z-index:90;transition:.22s;box-shadow:var(--shadow)
}
#toast.on{opacity:1;transform:translate(-50%,0)}

@media (max-width:900px){
  .wrap{padding:18px 14px 60px}
  h1{font-size:20px}
  .hero{padding:18px 16px 16px}
  .hero-tools{width:100%}
}
/* 手机上控件自身折行（桌面与平板仍保持两行结构） */
/* 手机端：地区 / 语言 / (主题+打印) 三栏 */
@media (max-width:560px){
  .hero-tools{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;align-items:end}
  .region-pick select,.lang-pick select{width:100%;min-width:0;max-width:none;padding-right:26px}
  .region-pick span,.lang-pick span{font-size:10px}
  .hero-btns{gap:6px}
  .icon-btn{width:34px;height:34px}
}
@media print{
  body{background:#fff;color:#000}
  body::before{display:none}
  .toolbar,.hero-tools,.idx,.region-pick{display:none!important}
  .hero,.card,.rule,.dcell{box-shadow:none;border-color:#ccc;background:#fff}
  .wrap{max-width:none;padding:0}
  tbody tr{break-inside:avoid}
  thead th{position:static}
}
</style>
</head>
<body class="loading">
<div class="wrap">

  <header class="hero">
    <div class="hero-top">
      <div class="brand">
        <div class="logo">
          __LOGO__
        </div>
        <div>
          <h1 id="hTitle"></h1>
          <div class="sub" id="hSub"></div>
        </div>
      </div>
      <div class="hero-tools">
        <label class="region-pick">
          <span id="regionLabel"></span>
          <select id="regionSel"></select>
        </label>
        <label class="lang-pick">
          <span id="langLabel"></span>
          <select id="langSel"></select>
        </label>
        <div class="hero-btns">
          <button class="icon-btn" id="themeBtn" title="theme"></button>
          <button class="icon-btn" id="printBtn" title="print">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 9V3h12v6"/><path d="M6 18H4v-6h16v6h-2"/><path d="M8 14h8v7H8z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    <div class="stats" id="stats"></div>
  </header>

  <div class="boot-err" id="bootErr"></div>
  <div class="region-note" id="regionNote"></div>
  <div class="notice" id="notice"></div>
  <div class="sources" id="sources"></div>

  <div class="toolbar">
    <div class="tabs" id="tabs"></div>
    <div class="searchrow">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.2-3.2"/>
        </svg>
        <input id="q" type="search" autocomplete="off" spellcheck="false">
        <button class="clear-btn" id="clearBtn" title="clear">×</button>
      </div>
      <div class="seg" id="viewSeg"></div>
      <span class="count" id="cnt"></span>
    </div>
  </div>

  <main id="main"></main>

  <footer class="foot">
    <p id="footSrc"></p>
    <p id="footLang"></p>
    <p id="footLicense"></p>
    <p class="muted" id="footDate"></p>
  </footer>
</div>

<div id="toast"></div>

<script>
var MODE = "__MODE__", EMBEDDED = __EMBEDDED__, CSVBASE = "__CSVBASE__";
var HANT = __HANT__, SECTIONS = __SECTIONS__, TABS = __TABS__, LANGS = __LANGS__;
var PAYLOAD = null, I18N = null, REGIONS = null;

var state = { lang: "zh", region: "cn", group: "all", view: "table", q: "" };

try{
  var qp = (typeof URLSearchParams !== "undefined") ? new URLSearchParams(location.search) : null;
  var sv = localStorage.getItem("mcl.lang");
  if(sv && LANGS.some(function(l){return l.id===sv})) state.lang = sv;
  var sr = localStorage.getItem("mcl.region");
  if(sr) state.region = sr;
  if(qp){
    var ql = qp.get("lang"), qr = qp.get("region");
    if(ql && LANGS.some(function(l){return l.id===ql})) state.lang = ql;
    if(qr) state.region = qr;
  }
  var st = localStorage.getItem("mcl.theme");
  if(st === "light" || st === "dark") document.documentElement.setAttribute("data-theme", st);
}catch(e){}

function syncUrl(){
  try{
    var u = new URL(location.href);
    u.searchParams.set("lang", state.lang);
    u.searchParams.set("region", state.region);
    history.replaceState(null, "", u.toString());
  }catch(e){}
}

/* ================= CSV 读取与装配 ================= */
var CSV_FILES = ["entries.csv","entry_text.csv","regions.csv","region_text.csv",
  "region_codes.csv","region_extras.csv","region_conflicts.csv","conflicts.csv",
  "conflict_text.csv","rules.csv","rule_text.csv","i18n.csv"];
var LANGS_ORDER = ["zh","en","ja","ko","es","fr","it","pt","ru"];

function parseCSV(text){
  var rows=[], row=[], field="", i=0, inQ=false;
  text = text.replace(/^\uFEFF/, "");
  while(i < text.length){
    var ch = text.charAt(i);
    if(inQ){
      if(ch === '"'){
        if(text.charAt(i+1) === '"'){ field += '"'; i += 2; continue; }
        inQ = false; i++; continue;
      }
      field += ch; i++; continue;
    }
    if(ch === '"'){ inQ = true; i++; continue; }
    if(ch === ','){ row.push(field); field = ""; i++; continue; }
    if(ch === '\r'){ i++; continue; }
    if(ch === '\n'){ row.push(field); rows.push(row); row = []; field = ""; i++; continue; }
    field += ch; i++;
  }
  if(field !== "" || row.length){ row.push(field); rows.push(row); }
  var head = rows.shift() || [];
  var out = [];
  for(var r=0;r<rows.length;r++){
    if(rows[r].length === 1 && rows[r][0] === "") continue;
    var o = {};
    for(var c=0;c<head.length;c++) o[head[c]] = (rows[r][c] !== undefined) ? rows[r][c] : "";
    out.push(o);
  }
  return out;
}

function mapObj(o, fn){
  var r = {};
  for(var k in o){ if(Object.prototype.hasOwnProperty.call(o,k)) r[k] = fn(o[k]); }
  return r;
}

function assemble(texts){
  var L = LANGS_ORDER, csv = {};
  CSV_FILES.forEach(function(n){ csv[n] = parseCSV(texts[n] || ""); });

  var i18n = {};
  csv["i18n.csv"].forEach(function(r){
    var o = {};
    L.forEach(function(lg){ o[lg] = r[lg] || ""; });
    i18n[r.key] = o;
  });

  var byKey = {};
  csv["entries.csv"].forEach(function(r){
    var e = {code:r.code, base:r.code, group:r.group, full:r.full_en, name:{}, loc:{}, s:""};
    L.forEach(function(lg){ e.name[lg] = r["name_"+lg] || ""; e.loc[lg] = {desc:"", note:""}; });
    byKey[r.group+"|"+r.code] = e;
  });
  csv["entry_text.csv"].forEach(function(r){
    var e = byKey[r.group+"|"+r.code]; if(!e) return;
    if(!e.loc[r.lang]) e.loc[r.lang] = {desc:"", note:""};
    e.loc[r.lang].desc = r.desc || "";
    e.loc[r.lang].note = r.note || "";
  });

  var rtext = {}, ctext = {}, rtext2 = {}, ovByRegion = {};
  csv["region_text.csv"].forEach(function(r){ rtext[r.region_id+"|"+r.lang] = r; });
  csv["conflict_text.csv"].forEach(function(r){ ctext[r.code+"|"+r.lang] = r; });
  csv["rule_text.csv"].forEach(function(r){ rtext2[r.rule_id+"|"+r.lang] = r; });
  csv["region_codes.csv"].forEach(function(r){
    var m = ovByRegion[r.region_id] || (ovByRegion[r.region_id] = {});
    m[(r.group||"")+"|"+r.base_code] = r;
  });

  var regions = {};
  csv["regions.csv"].forEach(function(rg){
    var rid = rg.id, localLang = rg.local_lang || "zh";
    var view = {id:rid, flag:rg.flag, local_lang:localLang, script:rg.script||"",
                label:{}, intro:{}, warn:{}, sources:{}, foot_src:{}, groups:{}, extras:[],
                conflicts:[], rules:[], diff:[], index:[]};
    L.forEach(function(lg){
      var t = rtext[rid+"|"+lg] || {};
      view.label[lg] = t.label || "";
      view.intro[lg] = t.intro || "";
      view.warn[lg] = t.warn || "";
      view.sources[lg] = (t.sources||"").split(" ; ").filter(function(x){return x.trim();});
      view.foot_src[lg] = t.foot_src || "";
    });
    var ov = ovByRegion[rid] || {};
    ["mat","obj","light","finish"].forEach(function(g){
      var rows = [];
      Object.keys(byKey).forEach(function(k){
        var e = byKey[k];
        if(e.group !== g) return;
        var o = ov[g+"|"+e.code] || ov["|"+e.code];
        var code = (o && o.code) || e.code;
        var row = {code:code, base:e.code, group:g, full:(o && o.full) || e.full,
                   name:(o && o.name) || e.name[localLang] || e.name.zh || e.code,
                   loc:{}, rnote:(o && o.note) || "", s:""};
        L.forEach(function(lg){ row.loc[lg] = e.loc[lg]; });
        var parts = [code, e.code, row.full, row.name];
        L.forEach(function(lg){ parts.push(e.name[lg], e.loc[lg].desc, e.loc[lg].note); });
        row.s = parts.join(" ").toLowerCase();
        rows.push(row);
        if(code !== e.code) view.diff.push({base:e.code, code:code, name:row.name, full:row.full, group:g});
      });
      view.groups[g] = rows;
    });
    csv["region_extras.csv"].forEach(function(r){
      if(r.region_id !== rid) return;
      var ex = {code:r.code, base:r.code, full:r.full, name:r.name, loc:{}, s:""};
      L.forEach(function(lg){ ex.loc[lg] = {desc:r.desc, note:r.note}; });
      ex.s = [r.code, r.full, r.name, r.desc, r.note].join(" ").toLowerCase();
      view.extras.push(ex);
    });
    csv["conflicts.csv"].forEach(function(c){
      var a = c.a_ref ? byKey[c.a_ref.replace(":", "|")] : null;
      var b = c.b_ref ? byKey[c.b_ref.replace(":", "|")] : null;
      var item = {code:c.code, a:{}, b:{}, howto:{}, is_extra:false};
      L.forEach(function(lg){
        item.a[lg] = (a ? a.name[lg] : "") || c["a_"+lg] || "";
        item.b[lg] = (b ? b.name[lg] : "") || c["b_"+lg] || "";
        item.howto[lg] = (ctext[c.code+"|"+lg] || {})[lg] || "";
      });
      view.conflicts.push(item);
    });
    csv["region_conflicts.csv"].forEach(function(c){
      if(c.region_id !== rid) return;
      var item = {code:c.code, a:{}, b:{}, howto:{}, is_extra:true};
      L.forEach(function(lg){
        item.a[lg] = c["a_"+lg] || ""; item.b[lg] = c["b_"+lg] || ""; item.howto[lg] = c["howto_"+lg] || "";
      });
      view.conflicts.push(item);
    });
    csv["rules.csv"].forEach(function(rr){
      var item = {title:{}, detail:{}, example:{}};
      L.forEach(function(lg){
        var t = rtext2[rr.rule_id+"|"+lg] || {};
        item.title[lg] = t.title || "";
        item.detail[lg] = t.detail || "";
        item.example[lg] = t.example || rr.example;
      });
      view.rules.push(item);
    });
    ["mat","obj","light","finish"].forEach(function(g){
      view.groups[g].forEach(function(row){
        view.index.push({code:row.code, base:row.base, full:row.full, group:g, name:row.name});
      });
    });
    view.extras.forEach(function(ex){
      view.index.push({code:ex.code, base:ex.code, full:ex.full, group:"extra", name:ex.name});
    });
    regions[rid] = view;
  });

  /* 繁体地区：把中文换成繁体，并生成该地区用的 i18n_zh */
  Object.keys(regions).forEach(function(rid){
    var v = regions[rid];
    if(v.script !== "hant") return;
    var map = HANT[rid] || {};
    function cv(x){ return (x && map[x]) ? map[x] : x; }
    /* 每种语言各自一列：只有中文那一格需要转繁体，其余语言保持原样 */
    function cvZh(o){
      var r = {};
      for(var k in o){
        if(!Object.prototype.hasOwnProperty.call(o,k)) continue;
        var v = o[k];
        if(k !== "zh"){ r[k] = v; continue; }
        r[k] = Array.isArray(v) ? v.map(cv) : cv(v);   // sources 是数组，逐条转换
      }
      return r;
    }
    v.label = cvZh(v.label);
    v.intro = cvZh(v.intro);
    v.warn = cvZh(v.warn);
    v.foot_src = cvZh(v.foot_src);
    v.sources = cvZh(v.sources);
    Object.keys(v.groups).forEach(function(g){
      v.groups[g].forEach(function(row){
        row.name = cv(row.name);
        row.loc = cvZh(row.loc);
      });
    });
    v.extras.forEach(function(ex){ ex.name = cv(ex.name); });
    v.conflicts.forEach(function(c){
      c.a = cvZh(c.a); c.b = cvZh(c.b); c.howto = cvZh(c.howto);
    });
    v.rules.forEach(function(r){
      r.title = cvZh(r.title); r.detail = cvZh(r.detail); r.example = cvZh(r.example);
    });
    v.i18n_zh = {};
    Object.keys(i18n).forEach(function(k){ v.i18n_zh[k] = cv(i18n[k].zh); });
  });

  return {regions:regions, regionOrder:Object.keys(regions), i18n:i18n,
          sections:SECTIONS, tabs:TABS, langs:LANGS};
}

function boot(){
  var ready;
  if(MODE === "offline"){
    ready = Promise.resolve(EMBEDDED);
  } else {
    ready = Promise.all(CSV_FILES.map(function(n){
      return fetch(CSVBASE + n).then(function(r){
        if(!r.ok) throw new Error(n + " → HTTP " + r.status);
        return r.text();
      });
    })).then(function(list){
      var o = {};
      CSV_FILES.forEach(function(n,i){ o[n] = list[i]; });
      return o;
    });
  }
  ready.then(function(texts){
    PAYLOAD = assemble(texts);
    I18N = PAYLOAD.i18n;
    REGIONS = PAYLOAD.regions;
    if(!REGIONS[state.region]) state.region = PAYLOAD.regionOrder[0];
    document.body.classList.remove("loading");
    renderHeader(); renderMain(); bind();
  }).catch(function(err){
    document.body.classList.remove("loading");
    var el = document.getElementById("bootErr");
    if(el){ el.style.display = "block"; el.textContent = "数据加载失败：" + err.message; }
  });
}

function $(s, r){ return (r||document).querySelector(s); }
function t(k){
  var R = REGIONS[state.region];
  if(state.lang === "zh" && R && R.i18n_zh && R.i18n_zh[k]) return R.i18n_zh[k];
  return (I18N[k] && I18N[k][state.lang]) || (I18N[k] && I18N[k].en) || k;
}
function REG(){ return REGIONS[state.region]; }
function esc(s){
  return String(s==null?"":s).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
function hl(text, kw){
  var s = String(text==null?"":text);
  if(!kw) return esc(s);
  var low = s.toLowerCase(), i = low.indexOf(kw);
  if(i < 0) return esc(s);
  return esc(s.slice(0,i)) + "<mark>" + esc(s.slice(i, i+kw.length)) + "</mark>" + esc(s.slice(i+kw.length));
}
function toast(msg){
  var el = $("#toast");
  el.textContent = msg; el.classList.add("on");
  clearTimeout(el._tm); el._tm = setTimeout(function(){ el.classList.remove("on"); }, 1500);
}
function hits(row, kw){ return !kw || row.s.indexOf(kw) > -1; }
function groupRows(R, g){
  if(g === "extra") return R.extras;
  return R.groups[g] || [];
}

/* ---------------- header ---------------- */
function renderHeader(){
  var meta = LANGS.filter(function(l){return l.id===state.lang})[0] || LANGS[0];
  var R = REG();
  document.documentElement.setAttribute("lang", meta.html);
  document.documentElement.setAttribute("data-lang", state.lang);
  document.documentElement.setAttribute("data-region", state.region);
  document.title = t("title").replace(/<[^>]+>/g, "") + " · " + R.label[state.lang];
  $("#hTitle").innerHTML = t("title");
  $("#hSub").innerHTML = esc(t("subtitle")) + " · " + esc(t("domain"));

  $("#regionLabel").textContent = t("region_label");
  $("#regionSel").innerHTML = PAYLOAD.regionOrder.map(function(id){
    var r = REGIONS[id];
    return '<option value="'+id+'"'+(id===state.region?" selected":"")+'>'+
      r.flag+" "+esc(r.label[state.lang])+'</option>';
  }).join("");

  var total = R.index.length;
  $("#stats").innerHTML =
    '<div class="stat"><b>'+total+'</b><span>'+esc(t("unit"))+'</span></div>' +
    '<div class="stat"><b>'+PAYLOAD.regionOrder.length+'</b><span>'+esc(t("region_label"))+'</span></div>' +
    '<div class="stat"><b>'+LANGS.length+'</b><span>'+esc(t("languages"))+'</span></div>' +
    '<div class="stat"><b>'+R.conflicts.length+'</b><span>'+esc(t("badge_conflict"))+'</span></div>';

  // 地区条：地区名 + 本地区要点 + 切换提示
  $("#regionNote").innerHTML =
    '<span class="rf">'+R.flag+'</span><b>'+esc(R.label[state.lang])+'</b>'+
    '<span class="rmeta">'+esc(t("region_summary")
        .replace("{n}", R.index.length)
        .replace("{d}", R.diff.length)
        .replace("{e}", R.extras.length))+'</span>'+
    '<span class="warnline">'+esc(t("region_hint"))+'</span>';

  // 「先读这句」：完全随当前地区切换——资料出处与风险提示都按当地体系给出
  var introTxt = (R.intro && R.intro[state.lang]) || t("src_note");
  var warnTxt = (R.warn && R.warn[state.lang]) || t("warn_note");
  $("#notice").innerHTML =
    "<b>"+esc(t("note_label"))+"：</b>"+esc(introTxt)+
    '<span class="warnline">'+esc(warnTxt)+'</span>';

  // 本地区资料依据（当地权威标准 / 法规 / 实务惯例）
  var srcs = (R.sources && R.sources[state.lang]) || [];
  $("#sources").innerHTML = srcs.length
    ? '<div class="sources-head">'+esc(t("g_sources_title"))+'<em>'+esc(t("g_sources_sub"))+'</em></div>'+
      '<ul>'+srcs.map(function(s){ return '<li>'+esc(s)+'</li>'; }).join("")+'</ul>'
    : '';

  $("#langLabel").textContent = t("lang_label");
  $("#langSel").innerHTML = LANGS.map(function(l){
    return '<option value="'+l.id+'"'+(l.id===state.lang?" selected":"")+'>'+esc(l.label)+'</option>';
  }).join("");

  var th = document.documentElement.getAttribute("data-theme")==="light" ? t("theme_dark") : t("theme_light");
  $("#themeBtn").title = th;
  $("#themeBtn").innerHTML = document.documentElement.getAttribute("data-theme")==="light"
    ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/></svg>';

  renderTabs();
  $("#viewSeg").innerHTML =
    '<button data-view="table" class="'+(state.view==="table"?"on":"")+'">'+esc(t("view_table"))+'</button>' +
    '<button data-view="index" class="'+(state.view==="index"?"on":"")+'">'+esc(t("view_index"))+'</button>';

  $("#q").placeholder = t("search_ph");
  $("#printBtn").title = t("print_title");
  $("#clearBtn").title = t("clear_title");
  $("#footSrc").innerHTML = esc((R.foot_src && R.foot_src[state.lang]) || t("foot_src"));
  $("#footLang").innerHTML = esc(t("foot_lang"));
  $("#footLicense").innerHTML = esc(t("foot_license")) +
    ' · <a href="https://github.com/Andox-Lopez/material-code-legend/blob/main/LICENSE" target="_blank" rel="noopener">LICENSE</a>';
  $("#footDate").innerHTML = esc(t("foot_date"));
}

function renderTabs(){
  var R = REG();
  var tabs = TABS.filter(function(x){
    if(x.id === "extra") return R.extras.length > 0;
    return true;
  });
  $("#tabs").innerHTML = tabs.map(function(x){
    return '<button class="tab'+(x.id===state.group?" on":"")+'" data-tab="'+x.id+'">'+esc(t(x.label))+'</button>';
  }).join("");
}

/* ---------------- 地区代码对照 ---------------- */
function diffHtml(R){
  if(!R.diff.length) return "";
  var kw = state.q.toLowerCase();
  var list = R.diff.filter(function(d){ return hits(d, kw); });
  if(!list.length) return "";
  var cells = list.map(function(d){
    return '<div class="dcell"><div class="dtop">'+
      '<span class="from">'+esc(d.base)+'</span><span class="arrow">→</span>'+
      '<span class="to">'+esc(d.code)+'</span></div>'+
      '<div class="dn">'+hl(d.name, kw)+'</div>'+
      '<div class="df">'+hl(d.full, kw)+'</div>'+
      (d.note ? '<div class="dnote">'+hl(d.note, kw)+'</div>' : '')+'</div>';
  }).join("");
  return '<section class="blk"><h2>'+esc(t("g_region_title"))+'<em>'+esc(t("g_region_sub"))+'</em>'+
    '<span class="h2count">'+list.length+'</span></h2><div class="diffmap">'+cells+'</div></section>';
}

/* ---------------- tables ---------------- */
function tableFor(sec, R){
  var kw = state.q.toLowerCase();
  var lg = state.lang;
  var head, rows, body = "";

  if(sec.key === "conflict"){
    head = ["col_code","col_a","col_b","col_desc2"];
    body = R.conflicts.filter(function(r){ return hits(r, kw); }).map(function(r){
      return '<tr class="conflict'+(r.is_extra?" extra":"")+'">'+
        '<td class="code" data-copy="'+esc(r.code)+'">'+esc(r.code)+
          (r.is_extra ? '<span class="badge region">'+esc(t("region_badge"))+'</span>' : '')+'</td>'+
        '<td class="name">'+hl(r.a[lg], kw)+'</td>'+
        '<td class="desc">'+hl(r.b[lg], kw)+'</td>'+
        '<td class="note">'+hl(r.howto[lg], kw)+'</td></tr>';
    }).join("");
  } else {
    head = ["col_code","col_full","col_region_name", sec.col, "col_note"];
    body = groupRows(R, sec.group).filter(function(r){ return hits(r, kw); }).map(function(r){
      var L = r.loc[lg] || {desc:"", note:""};
      var alt = "";
      if(R.local_lang !== lg && r.loc[lg]){
        alt = ""; // 名称副标题统一使用地区语言，这里保持单一
      }
      var rnote = r.rnote
        ? '<span class="rnote">'+hl(r.rnote, kw)+'</span>' : '';
      var baseTag = (r.code !== r.base)
        ? '<span class="badge base">'+esc(t("col_base_code"))+' '+esc(r.base)+'</span>' : '';
      return '<tr>'+
        '<td class="code" data-copy="'+esc(r.code)+'">'+esc(r.code)+baseTag+
          (sec.group === "extra" ? '<span class="badge region">'+esc(t("region_badge"))+'</span>' : '')+'</td>'+
        '<td class="full">'+hl(r.full, kw)+'</td>'+
        '<td class="name">'+hl(r.name, kw)+alt+'</td>'+
        '<td class="desc">'+hl(L.desc, kw)+'</td>'+
        '<td class="note">'+rnote+hl(L.note, kw)+'</td></tr>';
    }).join("");
  }

  return '<div class="card"><div class="scroll"><table><thead><tr>'+
    head.map(function(k,i){
      var cls = i===0 ? ' class="code"' : (k==="col_full" ? ' class="full"' : "");
      return "<th"+cls+">"+esc(t(k))+"</th>";
    }).join("")+'</tr></thead><tbody>'+(body || "")+'</tbody></table></div>';
}

function rulesHtml(R){
  var kw = state.q.toLowerCase();
  var lg = state.lang;
  var items = R.rules.filter(function(r){ return hits(r, kw); });
  return '<div class="rules">' + items.map(function(r, i){
    var ex = (typeof r.example === "string") ? r.example : (r.example[lg] || "");
    return '<div class="rule"><h3>'+(i+1)+'. '+hl(r.title[lg], kw)+'</h3>'+
      '<div class="eg">'+esc(ex)+'</div><p>'+hl(r.detail[lg], kw)+'</p></div>';
  }).join("") + '</div>';
}

/* ---------------- index cards ---------------- */
function indexHtml(R){
  var kw = state.q.toLowerCase();
  var lg = state.lang;
  var list = R.index.filter(function(r){
    if(state.group !== "all" && state.group !== r.group) return false;
    return hits(r, kw);
  }).sort(function(a,b){
    var c = a.code.localeCompare(b.code);
    return c !== 0 ? c : a.group.localeCompare(b.group);
  });
  if(!list.length) return '<div class="card"><div class="empty">'+esc(t("no_result"))+'</div></div>';

  var out = "", lastLetter = "";
  list.forEach(function(r){
    var L = r.code.charAt(0);
    if(L !== lastLetter){ out += '<div class="letter">'+esc(L)+'</div>'; lastLetter = L; }
    out += '<div class="icard" data-code="'+esc(r.code)+'" data-group="'+esc(r.group)+'">'+
      '<div class="code">'+esc(r.code)+'<span class="grp">'+esc(t(tabLabelFor(r.group)))+'</span></div>'+
      '<div class="full">'+hl(r.full, kw)+'</div>'+
      (r.name === r.full ? "" : '<div class="name">'+hl(r.name, kw)+'</div>')+'</div>';
  });
  return '<div class="idx">'+out+'</div>';
}

function tabLabelFor(g){
  var map = {mat:"tab_mat", obj:"tab_obj", light:"tab_light", finish:"tab_finish",
             extra:"tab_extra", conflict:"tab_conflict"};
  return map[g] || "tab_all";
}

/* ---------------- main ---------------- */
function renderMain(){
  var R = REG();
  var main = $("#main");
  var kw = state.q.toLowerCase();

  if(state.view === "index"){
    var n = R.index.filter(function(r){
      if(state.group !== "all" && state.group !== r.group) return false;
      return hits(r, kw);
    }).length;
    main.innerHTML =
      '<section class="blk"><h2>'+esc(t("g_index"))+'<em>'+esc(t("g_index_sub"))+'</em>'+
      '<span class="h2count">'+n+'</span></h2>'+indexHtml(R)+'</section>'+
      ((state.group === "all" && R.diff.length) ? diffHtml(R) : '')+
      '<section class="blk"><h2>'+esc(t("g_rules"))+'<em>'+esc(t("g_rules_sub"))+'</em></h2>'+rulesHtml(R)+'</section>';
    updateCount(n);
    return;
  }

  var html = (state.group === "all" ? diffHtml(R) : ""), visible = 0;
  SECTIONS.forEach(function(sec){
    if(sec.key === "rules"){
      if(state.group !== "all") return;
      html += '<section class="blk"><h2>'+esc(t(sec.title))+'<em>'+esc(t(sec.sub))+'</em></h2>'+rulesHtml(R)+'</section>';
      return;
    }
    if(state.group !== "all" && state.group !== sec.group) return;
    if(sec.group === "extra" && !R.extras.length) return;
    var n = (sec.key === "conflict" ? R.conflicts : groupRows(R, sec.group))
      .filter(function(r){ return hits(r, kw); }).length;
    visible += n;
    html += '<section class="blk"><h2>'+esc(t(sec.title))+'<em>'+esc(t(sec.sub))+'</em>'+
      '<span class="h2count">'+n+'</span></h2>'+tableFor(sec, R)+'</section>';
  });
  main.innerHTML = html;
  updateCount(visible);
}

function updateCount(n){
  var kw = state.q.trim();
  $("#cnt").textContent = t("showing") + " " + n + " " + t("unit") +
    (kw ? "（" + t("keyword") + ": " + kw + "）" : "");
}

/* ---------------- events ---------------- */
function bind(){
  $("#regionSel").addEventListener("change", function(e){
    state.region = e.target.value;
    syncUrl();
    state.group = "all";
    try{ localStorage.setItem("mcl.region", state.region); }catch(err){}
    renderHeader(); renderMain();
  });
  $("#langSel").addEventListener("change", function(e){
    state.lang = e.target.value;
    try{ localStorage.setItem("mcl.lang", state.lang); }catch(err){}
    syncUrl(); renderHeader(); renderMain();
  });
  $("#tabs").addEventListener("click", function(e){
    var b = e.target.closest(".tab"); if(!b) return;
    state.group = b.dataset.tab;
    renderTabs(); renderMain();
  });
  $("#viewSeg").addEventListener("click", function(e){
    var b = e.target.closest("button"); if(!b) return;
    state.view = b.dataset.view;
    $("#viewSeg").innerHTML =
      '<button data-view="table" class="'+(state.view==="table"?"on":"")+'">'+esc(t("view_table"))+'</button>' +
      '<button data-view="index" class="'+(state.view==="index"?"on":"")+'">'+esc(t("view_index"))+'</button>';
    renderMain();
  });
  $("#q").addEventListener("input", function(e){ state.q = e.target.value; renderMain(); });
  $("#clearBtn").addEventListener("click", function(){ state.q = ""; $("#q").value = ""; renderMain(); $("#q").focus(); });
  $("#themeBtn").addEventListener("click", function(){
    var cur = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", cur);
    try{ localStorage.setItem("mcl.theme", cur); }catch(err){}
    renderHeader();
  });
  $("#printBtn").addEventListener("click", function(){ window.print(); });
  $("#main").addEventListener("click", function(e){
    var code = e.target.closest("[data-copy]");
    if(code){
      var txt = code.getAttribute("data-copy");
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt);
      } else {
        var ta = document.createElement("textarea");
        ta.value = txt; document.body.appendChild(ta); ta.select();
        try{ document.execCommand("copy"); }catch(err){}
        document.body.removeChild(ta);
      }
      toast(t("copied") + " · " + txt);
      return;
    }
    var card = e.target.closest(".icard");
    if(card){
      state.q = card.getAttribute("data-code");
      state.group = "all";
      state.view = "table";
      $("#q").value = state.q;
      renderTabs();
      $("#viewSeg").innerHTML =
        '<button data-view="table" class="'+(state.view==="table"?"on":"")+'">'+esc(t("view_table"))+'</button>' +
        '<button data-view="index" class="'+(state.view==="index"?"on":"")+'">'+esc(t("view_index"))+'</button>';
      renderMain();
      window.scrollTo({top:0, behavior:"smooth"});
    }
  });
  document.addEventListener("keydown", function(e){
    if(e.key === "/" && document.activeElement !== $("#q")){ e.preventDefault(); $("#q").focus(); }
    if(e.key === "Escape" && document.activeElement === $("#q")){ state.q=""; $("#q").value=""; renderMain(); }
  });
}

boot();
</script>
</body>
</html>"""



# ---------------------------------------------------------------- 输出
def build_html(mode):
    """mode: online（从 data/ 读取 CSV）或 offline（把 CSV 全部内嵌）。"""
    texts = {n: read_csv_text(n) for n in CSV_FILES}
    hant = hant_map()
    js = HTML_TEMPLATE
    js = js.replace("__MODE__", mode)
    js = js.replace("__CSVBASE__", "data/")
    js = js.replace("__FAVICON__", FAVICON_URI)
    js = js.replace("__LOGO__", LOGO_SVG)
    js = js.replace("__HANT__", json.dumps(hant, ensure_ascii=False, separators=(",", ":")))
    js = js.replace("__SECTIONS__", json.dumps(SECTIONS, ensure_ascii=False, separators=(",", ":")))
    js = js.replace("__TABS__", json.dumps(TABS, ensure_ascii=False, separators=(",", ":")))
    js = js.replace("__LANGS__", json.dumps(
        [{"id": lg, **LANG_META[lg]} for lg in LANGS], ensure_ascii=False, separators=(",", ":")))
    if mode == "offline":
        js = js.replace("__EMBEDDED__", json.dumps(texts, ensure_ascii=False, separators=(",", ":")))
    else:
        js = js.replace("__EMBEDDED__", "null")
    name = "施工图材料代码多语对照表.html" if mode == "offline" else "index.html"
    path = os.path.join(OUT, name)
    # 固定用 LF 落盘：与 git 仓库中的版本一致，避免每次构建产生换行符噪声 diff
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(js.replace("\r\n", "\n"))
    return path, len(js)


def build_xlsx():
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("skip xlsx (openpyxl not installed)")
        return None

    THIN = Side(style="thin", color="D9D9D9")
    BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    HEAD_FILL = PatternFill("solid", fgColor="0F4C81")
    HEAD_FONT = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
    BODY_FONT = Font(name="微软雅黑", size=10)
    CODE_FONT = Font(name="Consolas", size=10, bold=True, color="0F4C81")

    def sheet(wb, name, headers, rows, widths, row_h=30):
        safe = re.sub(r"[\/?*\[\]:]", "·", str(name))[:31]
        ws = wb.create_sheet(safe)
        ws.sheet_view.showGridLines = False
        ws.append(headers)
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
            cell = ws.cell(row=1, column=c)
            cell.fill, cell.font = HEAD_FILL, HEAD_FONT
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = BORDER
        ws.row_dimensions[1].height = 26
        for r in rows:
            ws.append(list(r))
            i = ws.max_row
            ws.row_dimensions[i].height = row_h
            for c in range(1, len(headers) + 1):
                cell = ws.cell(row=i, column=c)
                cell.border = BORDER
                cell.font = CODE_FONT if c == 1 else BODY_FONT
                cell.alignment = (Alignment(horizontal="center", vertical="center") if c == 1
                                  else Alignment(vertical="center", wrap_text=True))
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = "A1:" + get_column_letter(len(headers)) + str(ws.max_row)
        return ws

    views = assemble_python()
    wb = Workbook()
    wb.remove(wb.active)
    for rid, v in views.items():
        label = v["label"]["zh"] or rid
        for lg in LANGS:
            rows = []
            for g in ("mat", "obj", "light", "finish"):
                for row in v["groups"][g]:
                    rows.append((row["code"], row["base"], row["full"], row["name"],
                                 row["loc"][lg]["desc"], row["loc"][lg]["note"]))
            for row in v["extras"]:
                rows.append((row["code"], row["code"], row["full"], row["name"],
                             row["loc"][lg]["desc"], row["loc"][lg]["note"]))
            sheet(wb, "{}·{}·{}".format(rid.upper(), label, LANG_META[lg]["label"][:4]),
                  ["代码", "通用代码", "Full name (EN)", "当地名称 / Local name",
                   "说明 / Description", "备注 / Notes"],
                  rows, [11, 11, 32, 28, 46, 42])
        crows = []
        for c in v["conflicts"]:
            crows.append((c["code"], c["a"]["zh"], c["b"]["zh"], c["howto"]["zh"]))
        sheet(wb, "{}·{}·易混".format(rid.upper(), label),
              ["代码", "含义 A", "含义 B / C", "区分方法"], crows, [14, 38, 42, 54], row_h=44)
        srows = []
        for lg in LANGS:
            srows.append((rid.upper(), label, LANG_META[lg]["label"],
                          v["intro"][lg], v["warn"][lg], " ; ".join(v["sources"][lg]),
                          v["foot_src"][lg]))
        sheet(wb, "{}·{}·提示".format(rid.upper(), label),
              ["地区", "Region", "语言", "先读这句 / Read this first",
               "风险提示 / Caution", "资料来源 / Sources", "页脚口径 / Footer note"],
              srows, [12, 20, 10, 60, 60, 70, 60], row_h=90)
    path = os.path.join(OUT, "施工图材料代码多语对照表.xlsx")
    try:
        wb.save(path)
    except PermissionError:
        path = os.path.join(OUT, "施工图材料代码多语对照表(多地区).xlsx")
        wb.save(path)
    return path


if __name__ == "__main__":
    p1, n1 = build_html("online")
    print("online  html:", os.path.basename(p1), "%.0f KB" % (n1 / 1024))
    p2, n2 = build_html("offline")
    print("offline html:", os.path.basename(p2), "%.0f KB" % (n2 / 1024))
    with io.open(os.path.join(OUT, "logo.svg"), "w", encoding="utf-8", newline="") as f:
        f.write(LOGO_SVG.replace("\r\n", "\n"))
    print("logo.svg 已输出")
    views = assemble_python()
    for rid, v in views.items():
        print("  region {:6s} entries={:3d} diff={:3d} extras={:2d} conflicts={:2d}".format(
            rid, len(v["index"]), len(v["diff"]), len(v["extras"]), len(v["conflicts"])))
    x = build_xlsx()
    if x:
        print("xlsx:", os.path.basename(x))
