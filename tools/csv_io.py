# -*- coding: utf-8 -*-
"""本地一次性数据维护脚本：读写 data/*.csv，保持 BOM / 换行 / 引号风格不变。

仅供本次每周更新使用，不参与构建（build.py）。
"""
import csv
import io
import os

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def read(name):
    """读 CSV -> (fieldnames, rows)。rows 为 dict 列表，保留原始列顺序。"""
    path = os.path.join(DATA, name)
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = list(rd.fieldnames)
        rows = [dict(r) for r in rd]
    return fields, rows


def write(name, fields, rows):
    """写 CSV：UTF-8 with BOM，沿用原文件的换行符，QUOTE_MINIMAL。"""
    path = os.path.join(DATA, name)
    raw = open(path, "rb").read()
    terminator = "\r\n" if b"\r\n" in raw else "\n"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=terminator,
                       extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})
    with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def row_index(rows, keyfn):
    return {keyfn(r): i for i, r in enumerate(rows)}
