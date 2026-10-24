# -*- coding: utf-8 -*-
"""数据结构定义：施工图材料代码多语言对照表

设计要点
--------
* 每条记录 = 一个缩写代码 + 英文全称 + 5 种语言的「名称 / 说明 / 备注」。
* 语言：中文(zh) / 英语(en) / 日语(ja) / 韩语(ko) / 西班牙语(es)。
* E()  每个语言传 (名称, 说明, 备注) 三元组，缺项用 "" 占位。
* C()  用于「同码多义」：含义可用 ref 引用已有条目（自动带出各语言名称），
       也可用 lit 直接写字面文本。
"""

LANGS = ["zh", "en", "ja", "ko", "es"]

LANG_META = {
    "zh": {"label": "中文", "en_label": "Chinese", "html": "zh-CN", "flag": "🇨🇳"},
    "en": {"label": "English", "en_label": "English", "html": "en", "flag": "🇬🇧"},
    "ja": {"label": "日本語", "en_label": "Japanese", "html": "ja", "flag": "🇯🇵"},
    "ko": {"label": "한국어", "en_label": "Korean", "html": "ko", "flag": "🇰🇷"},
    "es": {"label": "Español", "en_label": "Spanish", "html": "es", "flag": "🇪🇸"},
}

# 分组：代码 -> (数据键, i18n 键)
GROUPS = [
    ("mat", "g_mat"),
    ("obj", "g_obj"),
    ("light", "g_light"),
    ("finish", "g_finish"),
    ("conflict", "g_conflict"),
]


def E(code, en, zh, ja, ko, es):
    """构造一条多语言对照记录。每个语言参数为 (名称, 说明, 备注)。"""
    def pack(t):
        t = list(t) + ["", "", ""]
        return {"name": t[0], "desc": t[1], "note": t[2]}

    return {
        "code": code,
        "full": en[0],
        "loc": {
            "zh": pack(zh),
            "en": pack(en),
            "ja": pack(ja),
            "ko": pack(ko),
            "es": pack(es),
        },
    }


def C(code, a, b, howto):
    """同码多义条目。

    a / b 可以是:
        ("ref", 分组键, 代码)  -> 引用已有条目，自动解析为对应语言的名称
        ("lit", {lang: 文本})  -> 直接写字面文本
    howto 为 5 语言字典。
    """
    return {"code": code, "a": a, "b": b, "howto": howto}


def R(title, example, detail):
    """编号规则：标题 / 示例 / 要点，5 语言字典。

    example 可以是字符串（各语言通用）或 5 语言字典。
    """
    return {"title": title, "example": example, "detail": detail}
