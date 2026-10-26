# -*- coding: utf-8 -*-
"""把离线单文件版发布到 Gitee（作为 GitHub Release 的镜像与兜底下载源）。

用法：
    export GITEE_TOKEN=<Gitee 私人令牌>
    export GITEE_OWNER=<你的 Gitee 账号或组织>
    export GITEE_REPO=<Gitee 仓库名，默认 material-code-legend>
    python tools/publish_gitee.py            # 上传（不重新构建）
    python tools/publish_gitee.py --build    # 先按当日标签重新构建再上传

说明：
* 标签规则与 GitHub 一致：<yymmdd>-v<major>.<minor>，每日首个 release 为 v1.0，
  同日再次发布自动递增修订号。
* 仓库不存在时会自动创建（公开仓库）。
* 令牌从环境变量读取，不写入任何文件。
"""
import csv
import io
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = "https://gitee.com/api/v5"


def meta_map():
    path = os.path.join(ROOT, "data", "meta.csv")
    out = {}
    if not os.path.exists(path):
        return out
    for r in csv.DictReader(io.open(path, encoding="utf-8-sig")):
        out[r.get("key", "")] = r.get("value", "")
    return out


def set_meta(key, value):
    path = os.path.join(ROOT, "data", "meta.csv")
    rows = list(csv.DictReader(io.open(path, encoding="utf-8-sig")))
    header = list(rows[0].keys())
    hit = False
    for r in rows:
        if r.get("key") == key:
            r["value"] = value
            hit = True
    if not hit:
        rows.append({"key": key, "value": value, "note": ""})
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def api(method, path, token, data=None, files=None):
    url = API + path
    if files is None:
        if data is not None:
            body = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request(url, method=method, data=body)
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
        else:
            req = urllib.request.Request(url, method=method)
    else:
        boundary = "----wbform" + str(int(time.time() * 1000))
        buf = io.BytesIO()
        for k, v in (data or {}).items():
            buf.write(("--%s\r\n" % boundary).encode())
            buf.write(('Content-Disposition: form-data; name="%s"\r\n\r\n' % k).encode())
            buf.write(("%s\r\n" % v).encode())
        for k, (fname, content) in files.items():
            buf.write(("--%s\r\n" % boundary).encode())
            buf.write(('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (k, fname)).encode())
            buf.write(b"Content-Type: application/octet-stream\r\n\r\n")
            buf.write(content)
            buf.write(b"\r\n")
        buf.write(("--%s--\r\n" % boundary).encode())
        body = buf.getvalue()
        req = urllib.request.Request(url, method=method, data=body)
        req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    req.add_header("User-Agent", "material-code-legend-publisher")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"message": raw[:300]}


def next_tag(owner, repo, token):
    st, rels = api("GET", "/repos/%s/%s/releases?access_token=%s&per_page=100" % (owner, repo, token), token)
    prefix = time.strftime("%y%m%d") + "-v"
    best = ""
    if st == 200 and isinstance(rels, list):
        for r in rels:
            tag = r.get("tag_name", "")
            if tag.startswith(prefix):
                if tag > best:
                    best = tag
    if not best:
        return prefix + "1.0"
    cur = best[len(prefix):]
    maj = cur.split(".")[0]
    try:
        minor = int(cur.split(".")[1])
    except Exception:
        minor = 0
    return "%s%d.%d" % (prefix, int(maj), minor + 1)


def main():
    token = (os.environ.get("GITEE_TOKEN") or "").strip()
    m = meta_map()
    owner = (os.environ.get("GITEE_OWNER") or m.get("gitee_owner") or "").strip()
    repo = (os.environ.get("GITEE_REPO") or m.get("gitee_repo") or "material-code-legend").strip()
    if not token:
        print("缺少环境变量 GITEE_TOKEN（Gitee 私人令牌），已跳过 Gitee 发布。")
        return 2
    if not owner:
        print("缺少 Gitee 账号：设置环境变量 GITEE_OWNER 或在 data/meta.csv 填 gitee_owner。")
        return 2

    # 1) 确保仓库存在
    st, _ = api("GET", "/repos/%s/%s?access_token=%s" % (owner, repo, token), token)
    if st == 404:
        st, res = api("POST", "/user/repos?access_token=%s" % token, token, {
            "name": repo, "path": repo,
            "description": "施工图材料代码 · 多语多地区对照表（GitHub 镜像）",
            "private": False, "auto_init": True, "default_branch": "master",
        })
        print("创建 Gitee 仓库 %s/%s：%s" % (owner, repo, "成功" if st in (200, 201) else res))
        time.sleep(2)
    elif st != 200:
        print("访问 Gitee 仓库失败：%s" % st)
        return 1

    # 2) 标签（与 GitHub 同规则）
    tag = next_tag(owner, repo, token)
    print("本次 Gitee 标签：%s" % tag)

    # 3) 重新构建（注入标签，使文件知道自己��版本）
    if "--build" in sys.argv:
        env = dict(os.environ)
        env["RELEASE_TAG"] = tag
        r = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env=env)
        if r.returncode != 0:
            return r.returncode

    # 4) 创建 release
    notes = ("离线单文件版（全部 CSV 已内嵌，零外部依赖）：\n\n"
             "- material-code-legend-offline.html = 施工图材料代码多语对照表.html\n"
             "- material-code-legend.xlsx = 施工图材料代码多语对照表.xlsx\n\n"
             "- GitHub 源仓库：https://github.com/Andox-Lopez/material-code-legend\n"
             "- 标签规则：yymmdd-v major.minor（每日首个 release 为 v1.0）\n")
    st, rel = api("POST", "/repos/%s/%s/releases?access_token=%s" % (owner, repo, token), token, {
        "tag_name": tag, "name": "施工图材料代码 多语对照表 · %s" % tag,
        "body": notes, "target_commitish": "master", "prerelease": False,
    })
    if st not in (200, 201):
        print("创建 Gitee release 失败：%s %s" % (st, rel))
        return 1
    rid = rel.get("id")
    print("release 已创建：%s" % rel.get("html_url"))

    # 5) 上传附件（中文文件名不被 Gitee 接受，用 ASCII 名）
    for src, dst in (("施工图材料代码多语对照表.html", "material-code-legend-offline.html"),
                     ("施工图材料代码多语对照表.xlsx", "material-code-legend.xlsx")):
        path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            continue
        content = io.open(path, "rb").read()
        st, res = api("POST", "/repos/%s/%s/releases/%s/attach_files?access_token=%s"
                      % (owner, repo, rid, token), token, {}, {"file": (dst, content)})
        print("  上传 %s：%s" % (dst, "成功" if st in (200, 201) else "%s %s" % (st, res)))

    # 6) 记录坐标与标签，供页面读取（更新检查的 Gitee 兜底）
    set_meta("gitee_owner", owner)
    set_meta("gitee_repo", repo)
    set_meta("release_tag", tag)
    print("已把 gitee_owner / gitee_repo / release_tag 写入 data/meta.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
