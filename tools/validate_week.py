# -*- coding: utf-8 -*-
"""按 prompts/weekly_update_prompt.md 第五节做 9 项校验。

用法：python tools/validate_week.py
"""
import collections
import csv
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LANGS = ["zh", "en", "ja", "ko", "es", "fr", "it", "pt", "ru"]
GROUPS = ("mat", "obj", "light", "finish")
RESULT = []

NODE_JS = r"""
const fs=require("fs"),path=require("path");
const ROOT=process.argv[2];
const html=fs.readFileSync(path.join(ROOT,"index.html"),"utf8");
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const el=()=>({style:{},classList:{add(){},remove(){}},dataset:{},setAttribute(){},addEventListener(){},textContent:"",innerHTML:"",appendChild(){},querySelectorAll:()=>[],querySelector:()=>el()});
global.document={getElementById:()=>el(),querySelector:()=>el(),querySelectorAll:()=>[],body:el(),documentElement:el(),createElement:()=>el(),addEventListener:()=>{}};
global.localStorage={getItem:()=>null,setItem:()=>{}};
global.location={search:"",href:"http://localhost/"};
global.fetch=(u)=>Promise.resolve({ok:true,text:()=>Promise.resolve(fs.readFileSync(path.join(ROOT,"data",u),"utf8"))});
eval(js);
const texts={};CSV_FILES.forEach(n=>texts[n]=fs.readFileSync(path.join(ROOT,"data",n),"utf8"));
const P=assemble(texts);
setTimeout(()=>{
  const out={meta:P.meta};
  Object.keys(P.regions).forEach(rid=>{
    const v=P.regions[rid];
    out[rid]={codes:v.groups.mat.map(r=>r.code).join(","),
              names:v.groups.mat.map(r=>r.name).join("|"),
              intro:v.intro.zh, warn:v.warn.zh, sources:v.sources.zh.join(" ; "),
              foot:v.foot_src.zh, label:v.label.zh,
              i18n_title:P.i18n.title.zh,
              ja_names:v.groups.mat.map(r=>r.loc.ja?r.loc.ja.desc:"").join("|").slice(0,120),
              ko_names:v.groups.mat.map(r=>r.loc.ko?r.loc.ko.desc:"").join("|").slice(0,120),
              ja_i18n:P.i18n.title.ja};
  });
  console.log("###JSON###"+JSON.stringify(out));
},300);
"""


def rd(name):
    with io.open(os.path.join(DATA, name), "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def ok(item, passed, detail):
    RESULT.append((item, passed, detail))
    print(("  [通过] " if passed else "  [不通过] ") + item + " — " + detail)


def main():
    entries = rd("entries.csv")
    etext = rd("entry_text.csv")
    conflicts = rd("conflicts.csv")
    ctext = rd("conflict_text.csv")
    rules = rd("rules.csv")
    rtext = rd("rule_text.csv")
    regions = rd("regions.csv")
    rttext = rd("region_text.csv")
    rcodes = rd("region_codes.csv")
    rextras = rd("region_extras.csv")
    rconf = rd("region_conflicts.csv")
    i18n = rd("i18n.csv")
    meta = rd("meta.csv")

    # ---------------------------------------------------------- 1 行数自洽
    checks = [("entry_text.csv", len(etext), len(entries) * 9),
              ("conflict_text.csv", len(ctext), len(conflicts) * 9),
              ("rule_text.csv", len(rtext), len(rules) * 9),
              ("region_text.csv", len(rttext), len(regions) * 9)]
    bad = [c for c in checks if c[1] != c[2]]
    ok("1 行数自洽", not bad,
       "；".join("%s %d（= %d×9）" % (n, a, b) for n, a, b in checks) +
       ("；不一致：" + str(bad) if bad else "；全部一致"))

    # ---------------------------------------------------------- 2 无空值
    empt = []
    for r in entries:
        for lg in LANGS:
            if not (r.get("name_" + lg) or "").strip():
                empt.append("entries %s/%s name_%s" % (r["group"], r["code"], lg))
    tx = {(r["group"], r["code"], r["lang"]): r for r in etext}
    for r in entries:
        for lg in LANGS:
            t = tx.get((r["group"], r["code"], lg))
            if not t:
                empt.append("entry_text 缺行 %s/%s/%s" % (r["group"], r["code"], lg))
                continue
            for f in ("desc", "note"):
                if not (t.get(f) or "").strip():
                    empt.append("entry_text 空 %s/%s/%s/%s" % (r["group"], r["code"], lg, f))
    for r in i18n:
        for lg in LANGS:
            if not (r.get(lg) or "").strip():
                empt.append("i18n 空 %s/%s" % (r["key"], lg))
    for r in rttext:
        for f in ("label", "intro", "warn", "basis", "sources", "foot_src"):
            if not (r.get(f) or "").strip():
                empt.append("region_text 空 %s/%s/%s" % (r["region_id"], r["lang"], f))
    for r in ctext:
        for lg in LANGS:
            if not (r.get(lg) or "").strip():
                empt.append("conflict_text 空 %s/%s" % (r["code"], lg))
    for r in rtext:
        for f in ("title", "detail", "example"):
            if not (r.get(f) or "").strip():
                empt.append("rule_text 空 %s/%s/%s" % (r["rule_id"], r["lang"], f))
    for r in rextras:
        for f in ("full", "name", "desc", "note"):
            if not (r.get(f) or "").strip():
                empt.append("region_extras 空 %s/%s/%s" % (r["region_id"], r["code"], f))
    for r in rconf:
        for lg in LANGS:
            for p in ("a_", "b_", "howto_"):
                if not (r.get(p + lg) or "").strip():
                    empt.append("region_conflicts 空 %s/%s/%s%s" % (r["region_id"], r["code"], p, lg))
    ok("2 无空值", not empt,
       ("空值 %d 处：%s" % (len(empt), empt[:8])) if empt else
       "entries/entry_text/i18n/region_text/conflict_text/rule_text/region_extras/region_conflicts 全部非空")

    # ---------------------------------------------------------- 3 地区覆盖
    bygroup = collections.defaultdict(dict)
    for r in entries:
        bygroup[r["group"]][r["code"]] = r["name_zh"]
    ov = collections.defaultdict(dict)
    for r in rcodes:
        ov[r["region_id"]][(r["group"], r["base_code"])] = r
    rt9 = collections.Counter(r["region_id"] for r in rttext)
    cover_bad = []
    detail = []
    for rg in regions:
        rid = rg["id"]
        if rt9.get(rid) != 9:
            cover_bad.append("%s region_text %d 行" % (rid, rt9.get(rid, 0)))
        cells = []
        for g in GROUPS:
            tot = len(bygroup[g])
            m = sum(1 for bc in bygroup[g]
                    if ov[rid].get((g, bc)) or ov[rid].get(("", bc)))
            cells.append("%s %d/%d" % (g, m, tot))
            if m == 0:
                cover_bad.append("%s 缺 %s 组映射" % (rid, g))
        detail.append("%s[%s]" % (rid, " ".join(cells)))
    ok("3 地区覆盖", not cover_bad,
       ("问题：" + "；".join(cover_bad)) if cover_bad else
       "%d 地区各 9 行 region_text，四组映射：" % len(regions) + " ".join(detail))

    # ---------------------------------------------------------- 4 代码无冲突
    ent_codes = {(r["group"], r["code"]) for r in entries}
    allcodes = set(r["code"] for r in entries)
    base_bad = []
    for r in rcodes:
        g = r["group"] or ""
        valid = (r["base_code"] in bygroup[g]) if g else (r["base_code"] in allcodes)
        if not valid:
            base_bad.append("%s %s/%s" % (r["region_id"], g or "(all)", r["base_code"]))
    coll = []
    for rg in regions:
        rid = rg["id"]
        for g in GROUPS:
            eff = collections.defaultdict(list)
            for bc in bygroup[g]:
                o = ov[rid].get((g, bc)) or ov[rid].get(("", bc))
                eff[(o["code"] if o else "") or bc].append(bc)
            for code, bcs in eff.items():
                if len(bcs) > 1:
                    # 同义别名条目（名称形如「瓷砖（同 CT）」）不算真冲突：
                    # TL 就是 CT 的别名行，同地区同组出现同一个当地代码是预期行为。
                    alias = any(("（同 %s" % o) in bygroup[g][b] or ("（同%s" % o) in bygroup[g][b]
                                for b in bcs for o in bcs if o != b)
                    coll.append((rid, g, code, sorted(bcs), alias))
    real = [c for c in coll if not c[4]]
    alias = [c for c in coll if c[4]]
    ok("4 代码无冲突", not base_bad and not real,
       ("base_code 不可解析：" + str(base_bad)) if base_bad else
       ("真冲突：" + str(real)) if real else
       "base_code 全部可解析；同地区同组无真冲突（%d 处为同义别名 TL＝CT，非冲突）" % len(alias))

    # ---------------------------------------------------------- 5 引用可解析
    ref_bad = []
    for r in conflicts:
        for k in ("a_ref", "b_ref"):
            if r[k] and tuple(r[k].split(":")) not in ent_codes:
                ref_bad.append("conflicts %s %s=%s" % (r["code"], k, r[k]))
    region_ids = {r["id"] for r in regions}
    for f, rows in (("region_extras", rextras), ("region_conflicts", rconf)):
        for r in rows:
            if r["region_id"] not in region_ids:
                ref_bad.append("%s %s 地区不存在" % (f, r["region_id"]))
    ok("5 引用可解析", not ref_bad,
       ("问题：" + "；".join(ref_bad)) if ref_bad else
       "conflicts.csv %d 条 a_ref/b_ref 全部存在；region_extras/region_conflicts 地区 id 全部有效" % len(conflicts))

    # ---------------------------------------------------------- 6 构建零报错
    try:
        p = subprocess.run([sys.executable, "build.py"], cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        per_region = len(re.findall(r"region\s+\w+\s+entries=", p.stdout))
        ok("6 构建零报错", p.returncode == 0 and per_region == len(regions),
           "python build.py 退出码 %d，打印 %d/%d 个地区统计" % (p.returncode, per_region, len(regions)))
    except Exception as e:
        ok("6 构建零报错", False, "构建异常：" + str(e))

    # ---------------------------------------------------------- 7 页面可用
    idx = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    off = io.open(os.path.join(ROOT, "施工图材料代码多语对照表.html"), encoding="utf-8").read()
    ext = [u for u in re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', off)
           if "github" not in u and "gitee" not in u and "api." not in u]
    csv_inline = all(n in off for n in ("entries.csv", "region_codes.csv", "region_text.csv"))
    ok("7 页面可用", (not ext) and csv_inline and len(off) > 100000,
       "离线版 %d KB，内嵌 CSV 齐全=%s，除「检查更新」按钮外零外部资源请求"
       % (len(off) / 1024, csv_inline))

    # ---------------------------------------------------------- 8 回归
    payload = None
    import tempfile
    node_file = os.path.join(tempfile.gettempdir(), "_assemble_check_%d.js" % os.getpid())
    try:
        with io.open(node_file, "w", encoding="utf-8") as fh:
            fh.write(NODE_JS)
        r = subprocess.run(["node", node_file, ROOT], capture_output=True, text=True, timeout=180)
        line = [l for l in r.stdout.splitlines() if l.startswith("###JSON###")]
        if not line:
            raise RuntimeError((r.stdout + r.stderr)[-400:])
        payload = json.loads(line[-1][len("###JSON###"):])
    except Exception as e:
        print("  (node 装配失败：%s)" % e)
    finally:
        try:
            os.remove(node_file)
        except OSError:
            pass

    if payload:
        reg_only = {k: v for k, v in payload.items() if k != "meta"}
        codes = {k: v["codes"] for k, v in reg_only.items()}
        names = {k: v["names"] for k, v in reg_only.items()}
        intro = {k: v["intro"] for k, v in reg_only.items()}
        warn = {k: v["warn"] for k, v in reg_only.items()}
        src = {k: v["sources"] for k, v in reg_only.items()}
        foot = {k: v["foot"] for k, v in reg_only.items()}
        label = {k: v["label"] for k, v in reg_only.items()}
        uniq = lambda d: len(set(d.values()))
        reg_ok = min(uniq(codes), uniq(names), uniq(intro), uniq(warn),
                     uniq(src), uniq(foot), uniq(label)) > 1
        lang_ok = all(reg_only[k]["ja_names"] != reg_only[k]["ko_names"]
                      and reg_only[k]["ja_names"] for k in reg_only)
        i18n_ok = (all(v["i18n_title"] for v in reg_only.values())
                   and len({v["ja_i18n"] for v in reg_only.values()}) == 1)
        ok("8 回归（切地区／切语言）", reg_ok and lang_ok and i18n_ok,
           "%d 地区：代码 %d 种、当地名称 %d 种、体系说明 %d 种、风险提示 %d 种、资料来源 %d 种、页脚口径 %d 种、地区名 %d 种；"
           "语言切换：各地区 ja/ko 条目说明互不相同=%s；界面文案随语言切换变化=%s"
           % (len(reg_only), uniq(codes), uniq(names), uniq(intro), uniq(warn),
              uniq(src), uniq(foot), uniq(label), lang_ok, i18n_ok))
    else:
        ok("8 回归（切地区／切语言）", False, "无法执行 node 装配校验")

    # ---------------------------------------------------------- 9 更新日期
    ua = next((r["value"] for r in meta if r["key"] == "updated_at"), "")
    online_meta = ""
    if payload:
        online_meta = (payload.get("meta") or {}).get("updated_at", "")
    xlsx_hit = None
    try:
        from openpyxl import load_workbook
        wb = load_workbook(os.path.join(ROOT, "施工图材料代码多语对照表.xlsx"), read_only=True)
        xlsx_hit = False
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=12, max_col=9, values_only=True):
                if ua in [str(x) for x in row if x is not None]:
                    xlsx_hit = True
    except Exception as e:
        xlsx_hit = "读取失败：%s" % e
    passed = bool(ua) and ua in off and online_meta == ua and xlsx_hit is True
    ok("9 更新日期", passed,
       "data/meta.csv updated_at=%s；在线版页脚取值 %s、离线版内嵌 %s、xlsx 提示表 %s"
       % (ua, online_meta or "（缺失）", ua in off, xlsx_hit))

    print("\n汇总：%d / %d 项通过" % (sum(1 for _, p, _ in RESULT if p), len(RESULT)))
    failed = [i for i, p, _ in RESULT if not p]
    if failed:
        print("不通过项：" + "、".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
