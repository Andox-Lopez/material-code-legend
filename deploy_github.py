# -*- coding: utf-8 -*-
"""发布到 GitHub：建仓 → 推送 → 开启 Pages。

用法（令牌只从环境变量读取，不落盘、不打印）：
    GH_TOKEN=ghp_xxx python deploy_github.py

仓库：https://github.com/Andox-Lopez/material-code-legend
页面：https://Andox-Lopez.github.io/material-code-legend/
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO = "material-code-legend"
DESCRIPTION = ("施工图材料代码多语多地区对照表 · Material Code Legend "
               "(Multilingual, by region) — 单文件网页，8 个地区体系 × 5 种语言")
HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.github.com"


def api(method, path, token, data=None, accept="application/vnd.github+json"):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", accept)
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "material-code-legend-deploy")
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, body, timeout=60) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw[:400]}


def git(args, cwd=HERE, env=None):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True,
                       env=env, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def main():
    token = (os.environ.get("GH_TOKEN") or "").strip()
    if not token:
        print("请先设置环境变量 GH_TOKEN")
        return 2

    st, me = api("GET", "/user", token)
    if st != 200:
        print("令牌无效或权限不足：", me.get("message"))
        return 1
    owner = me["login"]
    print("账号：", owner)

    # 1) 建仓
    st, res = api("POST", "/user/repos", token, {
        "name": REPO, "description": DESCRIPTION, "private": False, "auto_init": False,
    })
    if st in (201, 422):
        print("仓库：", "已创建" if st == 201 else "已存在（复用）", REPO)
    else:
        print("建仓失败：", st, res.get("message"))
        return 1

    # 2) 提交并推送（令牌只用于这一次 push，随后把 remote 换回干净地址）
    rc, out, err = git(["init", "-b", "main"])
    git(["add", "-A"])
    git(["-c", "user.name=Karandox Lopez", "-c", "user.email=karandox@example.com",
         "commit", "-m", "feat: 施工图材料代码多语多地区对照表（含单文件网页与构建脚本）"])
    url_with_token = "https://%s:%s@github.com/%s/%s.git" % (owner, token, owner, REPO)
    git(["remote", "remove", "origin"])
    git(["remote", "add", "origin", url_with_token])
    rc, out, err = git(["push", "-u", "origin", "main"])
    if rc != 0:
        print("推送失败：\n", err[-1200:])
        return 1
    print("推送完成")
    git(["remote", "set-url", "origin", "https://github.com/%s/%s.git" % (owner, REPO)])

    # 3) 开启 Pages（Actions 路线为兜底）
    st, res = api("POST", "/repos/%s/%s/pages" % (owner, REPO),
                  token, {"source": {"branch": "main", "path": "/"}})
    if st in (201, 409, 422):
        print("Pages：已开启（分支来源）")
    elif st == 403:
        print("Pages：令牌无 Pages 权限，改由 GitHub Actions workflow 自动开启")
    else:
        print("Pages：", st, res.get("message"))

    page = "https://%s.github.io/%s/" % (owner, REPO)
    print("页面地址：", page)

    # 4) 等待部署（Actions 构建 + Pages 上线）
    for i in range(24):
        try:
            req = urllib.request.Request(page, headers={"User-Agent": "check"})
            with urllib.request.urlopen(req, timeout=20) as r:
                html = r.read(4000).decode("utf-8", "replace")
                if "Material Code" in html or "材料代码" in html or "LEGEND" in html.upper():
                    print("第 %d 次检查：页面已上线 ✓" % (i + 1))
                    return 0
                print("第 %d 次检查：站点可访问，等待构建完成…" % (i + 1))
        except Exception as e:
            print("第 %d 次检查：%s" % (i + 1, str(e)[:80]))
        time.sleep(15)
    print("等待超时，请查看 Actions 运行记录：https://github.com/%s/%s/actions" % (owner, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
