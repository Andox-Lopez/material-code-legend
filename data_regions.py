# -*- coding: utf-8 -*-
"""地区体系汇总：把 A / B 两个分片合并成地区列表

分片说明
--------
data_regions_a.py —— 中国大陆（基准）、中国香港、中国台湾
data_regions_b.py —— 日本、韩国、欧美、西语区、中东与东南亚

每个地区可用的字段
------------------
id / flag / label      标识、旗帜、地区名称（5 语）
local_lang            该地区的惯用语言（用于本地名称列）
script                "" 或 "hant"（繁体转换）
intro                 地区体系的说明与资料出处（5 语）—— 页面顶部「先读这句」
warn                  地区特有的风险提示（5 语）—— 跨项目套用前必读
codes                 通用代码 → 本地区常用代码（可写 "分组:代码"）
names                 通用名称 → 本地区惯用名称（本地语言）
descs                 说明文字的地区用语替换（本地语言）
fulls                 英文全称的地区写法
notes                 该条目的地区备注（本地语言）
extras                本地区特有条目
conflicts             本地区特有易混代码
"""

from data_regions_a import REGIONS_A
from data_regions_b import REGIONS_B

REGIONS = REGIONS_A + REGIONS_B
