# -*- coding: utf-8 -*-
"""生成《施工图材料代码多语对照表》单文件网页（+ 多语言 XLSX）

结构：地区（Region） → 分组 → 条目
  * 8 个地区/市场各自的缩写惯例：通用代码 → 当地代码、当地名称、地区特有条目与易混代码
  * 5 种界面/说明语言：中文 / English / 日本語 / 한국어 / Español
  * 香港、台湾地区使用繁体并套用当地惯用词（亞加力、壓克力、傢俬、傢俱…）

用法：python build.py
输出：施工图材料代码多语对照表.html / .xlsx（同目录）
"""
import io
import json
import os
import base64
import re

from data_common import LANGS, LANG_META
from data_mat import MAT_FINISH, MAT_FF_E
from data_light import LIGHT
from data_finish import FINISH
from data_conflict import CONFLICT, RULES
from data_regions import REGIONS
from i18n import I18N
from zh_hant import to_hant, to_hans

OUT = os.path.dirname(os.path.abspath(__file__))

GROUPS = {
    "mat": MAT_FINISH,
    "obj": MAT_FF_E,
    "light": LIGHT,
    "finish": FINISH,
}
GROUP_KEYS = ("mat", "obj", "light", "finish")
LOOKUP = {(g, e["code"]): e for g, items in GROUPS.items() for e in items}


def resolve_ref(ref):
    """把 ("ref", group, code) 解析成 5 语言文本；字面量原样返回。"""
    if ref[0] == "lit":
        return dict(ref[1])
    _, group, code = ref
    entry = LOOKUP[(group, code)]
    out = {}
    for lg in LANGS:
        name = entry["loc"][lg]["name"]
        full = entry["full"]
        if name == full:
            out[lg] = full
        else:
            sep = "（" if lg in ("zh", "ja", "ko") else " ("
            close = "）" if lg in ("zh", "ja", "ko") else ")"
            out[lg] = "{}{}{}{}".format(name, sep, full, close)
    return out


def pick(region, table, group, code):
    """地区覆盖查表：先查「分组:代码」，再查「代码」。"""
    return table.get(group + ":" + code, table.get(code))


def _hant_all(d, rid):
    """把 5 语言字典中的中文槽转成繁体。"""
    return dict(d, zh=to_hant(d.get("zh", ""), rid))


def build_region_view(region):
    """把一个地区的惯例套用到 80 条基准条目上，生成该地区的完整视图。"""
    rid = region["id"]
    lg = region["local_lang"]
    script = region.get("script", "")
    hant = (script == "hant")

    groups, diff = {}, []
    for g in GROUP_KEYS:
        rows = []
        for e in GROUPS[g]:
            base = e["code"]
            rcode = pick(region, region["codes"], g, base) or base

            lname = pick(region, region["names"], g, base)
            if not lname:
                lname = to_hant(e["loc"]["zh"]["name"], rid) if hant else e["loc"][lg]["name"]

            full = pick(region, region["fulls"], g, base) or e["full"]

            loc = {}
            for l2 in LANGS:
                d, n = e["loc"][l2]["desc"], e["loc"][l2]["note"]
                if hant and l2 == "zh":
                    d, n = to_hant(d, rid), to_hant(n, rid)
                loc[l2] = {"desc": d, "note": n}

            rnote = pick(region, region["notes"], g, base) or ""
            if rnote and hant:
                rnote = to_hant(rnote, rid)

            # UI 语言下的名称（当地区语言 ≠ 界面语言时作为副标题）
            ui_name = e["loc"]["zh"]["name"]
            if hant and lg == "zh":
                ui_name = e["loc"]["zh"]["name"]

            s = " ".join([base, rcode, full, lname, rnote] + [
                loc[l2]["desc"] + " " + loc[l2]["note"] for l2 in LANGS]).lower()

            rows.append({
                "code": rcode, "base": base, "full": full, "name": lname,
                "loc": loc, "rnote": rnote, "s": s,
            })
            if rcode != base:
                diff.append({"base": base, "code": rcode, "name": lname,
                             "full": full, "group": g, "note": rnote})
        groups[g] = rows

    # 地区特有条目
    extras = []
    for e in region["extras"]:
        loc = {l2: {"desc": e["loc"][l2]["desc"], "note": e["loc"][l2]["note"]} for l2 in LANGS}
        if hant:
            for l2 in LANGS:
                if l2 == "zh":
                    loc[l2] = {"desc": to_hant(loc[l2]["desc"], rid),
                               "note": to_hant(loc[l2]["note"], rid)}
        name = e["loc"][lg]["name"]
        if hant and lg == "zh":
            name = to_hant(name, rid)
        s = " ".join([e["code"], e["full"], name] + [
            loc[l2]["desc"] + " " + loc[l2]["note"] for l2 in LANGS]).lower()
        extras.append({"code": e["code"], "base": e["code"], "full": e["full"],
                       "name": name, "loc": loc, "rnote": "", "s": s})

    # 易混代码：基准冲突 + 地区特有冲突
    conflicts = []
    for c in CONFLICT:
        a, b = resolve_ref(c["a"]), resolve_ref(c["b"])
        howto = c["howto"]
        if hant:
            a, b, howto = _hant_all(a, rid), _hant_all(b, rid), _hant_all(howto, rid)
        s = " ".join([c["code"]] + list(a.values()) + list(b.values()) + list(howto.values())).lower()
        conflicts.append({"code": c["code"], "a": a, "b": b, "howto": howto,
                          "s": s, "is_extra": False})
    for c in region["conflicts"]:
        a, b = resolve_ref(c["a"]), resolve_ref(c["b"])
        howto = c["howto"]
        if hant:
            a, b, howto = _hant_all(a, rid), _hant_all(b, rid), _hant_all(howto, rid)
        s = " ".join([c["code"]] + list(a.values()) + list(b.values()) + list(howto.values())).lower()
        conflicts.append({"code": c["code"], "a": a, "b": b, "howto": howto,
                          "s": s, "is_extra": True})

    # 编号规则
    rules = []
    for r in RULES:
        title, detail = dict(r["title"]), dict(r["detail"])
        ex = r["example"]
        if isinstance(ex, dict):
            ex = dict(ex)
        if hant:
            title, detail = _hant_all(title, rid), _hant_all(detail, rid)
            if isinstance(ex, dict):
                ex = _hant_all(ex, rid)
        ex_text = ex if isinstance(ex, str) else " ".join(ex.values())
        s = " ".join([ex_text] + list(title.values()) + list(detail.values())).lower()
        rules.append({"title": title, "example": ex, "detail": detail, "s": s})

    # 速查索引
    index = []
    for g in GROUP_KEYS:
        for row in groups[g]:
            index.append({"code": row["code"], "base": row["base"], "full": row["full"],
                          "group": g, "name": row["name"], "s": row["s"]})
    for row in extras:
        index.append({"code": row["code"], "base": row["code"], "full": row["full"],
                      "group": "extra", "name": row["name"], "s": row["s"]})

    label = _hant_all(region["label"], rid) if hant else region["label"]
    intro = _hant_all(region["intro"], rid) if hant else region["intro"]
    warn = region.get("warn")
    if warn:
        warn = _hant_all(warn, rid) if hant else dict(warn)

    # 体系依据（接在简介之前）与权威资料清单
    basis = region.get("basis")
    if basis:
        basis = _hant_all(basis, rid) if hant else {lg: basis[lg] for lg in LANGS}
        if not hant:
            basis["zh"] = to_hans(basis["zh"])
        intro = {lg: (basis[lg] + " " + intro[lg]).strip() for lg in LANGS}

    sources = region.get("sources")
    if sources:
        sources = {lg: list(sources[lg]) for lg in LANGS}
        if hant:
            sources = {lg: [to_hant(s, rid) for s in v] for lg, v in sources.items()}
        else:
            sources["zh"] = [to_hans(s) for s in sources["zh"]]

    foot_src = region.get("foot_src")
    if foot_src:
        foot_src = _hant_all(foot_src, rid) if hant else {lg: foot_src[lg] for lg in LANGS}
        if not hant:
            foot_src["zh"] = to_hans(foot_src["zh"])

    i18n_zh = {k: to_hant(v["zh"], rid) for k, v in I18N.items()} if hant else None

    return {
        "id": rid,
        "flag": region["flag"],
        "label": label,
        "local_lang": lg,
        "intro": intro,
        "warn": warn,
        "sources": sources,
        "foot_src": foot_src,
        "i18n_zh": i18n_zh,
        "groups": groups,
        "extras": extras,
        "conflicts": conflicts,
        "rules": rules,
        "diff": diff,
        "index": index,
    }


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


def build_payload():
    regions = {}
    for r in REGIONS:
        regions[r["id"]] = build_region_view(r)
    return {
        "regions": regions,
        "regionOrder": [r["id"] for r in REGIONS],
        "sections": SECTIONS,
        "tabs": TABS,
        "i18n": I18N,
        "langs": [{"id": lg, **LANG_META[lg]} for lg in LANGS],
    }


PAYLOAD = build_payload()

# ---------------------------------------------------------------- Logo
# 标识：施工蓝图网格底板 + 代码标签 + 材料饰面叠层
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


# ---------------------------------------------------------------- 网页模板
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark" data-lang="zh" data-region="cn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>施工图材料代码多语对照表</title>
<meta name="description" content="施工图材料大类代码 · 按地区划分的缩写与全称对照 · 中日英韩西多语言 · Material Legend">
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
.hero-top{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;justify-content:space-between}
.brand{display:flex;gap:14px;align-items:center;min-width:280px}
.logo{
  width:46px;height:46px;flex:0 0 46px;border-radius:13px;overflow:hidden;line-height:0;
  box-shadow:0 4px 14px rgba(10,58,102,.28)
}
.logo svg{width:100%;height:100%;display:block}
h1{font-size:24px;font-weight:700;letter-spacing:.4px;line-height:1.25}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--muted);font-size:12.8px;margin-top:5px}
.hero-tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.langs{display:flex;gap:4px;padding:4px;border-radius:999px;background:var(--panel2);border:1px solid var(--line)}
.lang{
  border:0;background:transparent;color:var(--muted);cursor:pointer;border-radius:999px;
  padding:5px 12px;font-size:12.5px;font-family:inherit;transition:.16s;white-space:nowrap
}
.lang:hover{color:var(--ink)}
.lang.on{background:var(--accent);color:#fff;font-weight:600}
html[data-theme="light"] .lang.on{color:#fff}
.icon-btn{
  border:1px solid var(--line);background:var(--panel2);color:var(--ink2);cursor:pointer;
  width:38px;height:38px;border-radius:10px;display:grid;place-items:center;transition:.16s
}
.icon-btn:hover{border-color:var(--accent-line);color:var(--accent)}
.icon-btn svg{width:18px;height:18px}
.region-pick{display:flex;flex-direction:column;gap:4px}
.region-pick span{font-size:10.5px;color:var(--faint);letter-spacing:.5px;padding-left:3px}
.region-pick select{
  border:1px solid var(--line);background:var(--panel2);color:var(--ink);border-radius:10px;
  padding:8px 30px 8px 12px;font-size:13px;font-family:inherit;cursor:pointer;outline:none;
  appearance:none;-webkit-appearance:none;
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
<body>
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
        <div class="langs" id="langs"></div>
        <button class="icon-btn" id="themeBtn" title="theme"></button>
        <button class="icon-btn" id="printBtn" title="print">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 9V3h12v6"/><path d="M6 18H4v-6h16v6h-2"/><path d="M8 14h8v7H8z"/>
          </svg>
        </button>
      </div>
    </div>
    <div class="stats" id="stats"></div>
  </header>

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
var PAYLOAD = __PAYLOAD__;

var DATA = PAYLOAD, SECTIONS = PAYLOAD.sections, TABS = PAYLOAD.tabs;
var I18N = PAYLOAD.i18n, LANGS = PAYLOAD.langs, REGIONS = PAYLOAD.regions;

var state = { lang: "zh", region: "cn", group: "all", view: "table", q: "" };

try{
  var sv = localStorage.getItem("mcl.lang");
  if(sv && LANGS.some(function(l){return l.id===sv})) state.lang = sv;
  var sr = localStorage.getItem("mcl.region");
  if(sr && REGIONS[sr]) state.region = sr;
  var st = localStorage.getItem("mcl.theme");
  if(st === "light" || st === "dark") document.documentElement.setAttribute("data-theme", st);
}catch(e){}

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
    '<div class="stat"><b>5</b><span>'+esc(t("languages"))+'</span></div>' +
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

  $("#langs").innerHTML = LANGS.map(function(l){
    return '<button class="lang'+(l.id===state.lang?" on":"")+'" data-lang="'+l.id+'">'+esc(l.label)+'</button>';
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
    state.group = "all";
    try{ localStorage.setItem("mcl.region", state.region); }catch(err){}
    renderHeader(); renderMain();
  });
  $("#langs").addEventListener("click", function(e){
    var b = e.target.closest(".lang"); if(!b) return;
    state.lang = b.dataset.lang;
    try{ localStorage.setItem("mcl.lang", state.lang); }catch(err){}
    renderHeader(); renderMain();
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

renderHeader();
renderMain();
bind();
</script>
</body>
</html>
"""


def build_html():
    payload = json.dumps(PAYLOAD, ensure_ascii=False, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__PAYLOAD__", payload)
    html = html.replace("__FAVICON__", FAVICON_URI)
    html = html.replace("__LOGO__", LOGO_SVG)
    path = os.path.join(OUT, "施工图材料代码多语对照表.html")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)
    # 同步输出独立的 logo 文件（供仓库、PPT、提案复用）
    logo_path = os.path.join(OUT, "logo.svg")
    with io.open(logo_path, "w", encoding="utf-8") as f:
        f.write(LOGO_SVG)
    return path, len(html)


# ---------------------------------------------------------------- XLSX（可选）
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

    used = set()

    def sheet(wb, name, headers, rows, widths, row_h=30):
        safe = re.sub(r"[\/\?\*\[\]:]", "·", str(name))[:31]
        base = safe
        k = 2
        while safe in used:
            suf = "·%d" % k
            safe = base[:31 - len(suf)] + suf
            k += 1
        used.add(safe)
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
                cell.alignment = Alignment(horizontal="center", vertical="center") if c == 1 \
                    else Alignment(vertical="center", wrap_text=True)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = "A1:" + get_column_letter(len(headers)) + str(ws.max_row)
        return ws

    wb = Workbook()
    wb.remove(wb.active)
    for region in REGIONS:
        view = build_region_view(region)
        label = region["label"]["zh"]
        for lg in LANGS:
            rows = []
            for g in GROUP_KEYS:
                for r in view["groups"][g]:
                    rows.append((r["code"], r["base"], r["full"], r["name"],
                                 r["loc"][lg]["desc"], r["loc"][lg]["note"]))
            for r in view["extras"]:
                rows.append((r["code"], r["code"], r["full"], r["name"],
                             r["loc"][lg]["desc"], r["loc"][lg]["note"]))
            sheet(wb, "{}·{}·{}".format(region["id"].upper(), label, LANG_META[lg]["label"][:3]),
                  ["代码", "通用代码", "Full name (EN)", "名称 / Name",
                   "说明 / Description", "备注 / Notes"],
                  rows, [11, 11, 32, 26, 46, 42])
        crows = []
        for c in view["conflicts"]:
            crows.append((c["code"], c["a"][lg], c["b"][lg], c["howto"][lg]))
        sheet(wb, "{}·{}·易混".format(region["id"].upper(), label), ["代码", "含义 A", "含义 B / C", "区分方法"],
              crows, [14, 38, 42, 54])

        # 地区提示：把该地区的资料出处与跨项目提醒按 5 语言落到表里
        nrows = []
        for l2 in LANGS:
            nrows.append((
                region["id"].upper(),
                region["label"].get(l2, label),
                LANG_META[l2]["label"],
                view["intro"][l2],
                (view["warn"] or {}).get(l2, ""),
            ))
        sheet(wb, "{}·{}·提示".format(region["id"].upper(), label),
              ["地区", "Region", "语言", "先读这句 / Read this first", "跨项目提示 / Before reuse"],
              nrows, [12, 22, 10, 88, 88], row_h=96)
    path = os.path.join(OUT, "施工图材料代码多语对照表.xlsx")
    try:
        wb.save(path)
    except PermissionError:
        path = os.path.join(OUT, "施工图材料代码多语对照表(多地区).xlsx")
        wb.save(path)
        print("note: 原 xlsx 正被占用，已另存为", os.path.basename(path))
    return path


if __name__ == "__main__":
    p, n = build_html()
    print("html ok:", p, n, "bytes")
    for rid in PAYLOAD["regionOrder"]:
        v = PAYLOAD["regions"][rid]
        print("  region {:6s} entries={:3d} diff={:3d} extras={:2d} conflicts={:2d}".format(
            rid, len(v["index"]), len(v["diff"]), len(v["extras"]), len(v["conflicts"])))
    x = build_xlsx()
    if x:
        print("xlsx ok:", x)
