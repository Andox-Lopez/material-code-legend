# 施工图材料代码 · 多语多地区对照表
# Material Code Legend — Multilingual & Multi-Region

<p align="center">
  <img src="logo.svg" width="96" alt="施工图材料代码对照表 logo">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/regions-12-blue.svg" alt="Regions">
  <img src="https://img.shields.io/badge/languages-9-blue.svg" alt="Languages">
  <img src="https://img.shields.io/badge/data-CSV-brightgreen.svg" alt="CSV data">
  <img src="https://img.shields.io/badge/offline-single--file-brightgreen.svg" alt="Offline single file">
</p>

> 施工图材料大类代码的 **缩写 ↔ 全称** 对照工具：先选**地区**，再看那个市场真正在用的写法；界面与说明支持 **9 种语言**。
> A lookup for construction-drawing material codes: pick the **region** first, then read the codes as that market actually writes them, in 9 languages.

| | |
|---|---|
| **在线浏览 / Live** | https://andox-lopez.github.io/material-code-legend/ （运行时读取 `data/*.csv`） |
| **离线单文件 / Offline** | [`施工图材料代码多语对照表.html`](施工图材料代码多语对照表.html) — 所有 CSV 已内嵌，零外部依赖，可直接发给同事 |
| **Excel** | [`施工图材料代码多语对照表.xlsx`](施工图材料代码多语对照表.xlsx) — 12 地区 × 9 语言 × 3 张表 |

支持分享链接：`?lang=fr&region=fr`（语言与地区会写进 URL，便于直接甩给同事）。

---

## 为什么按地区划分

同一条材料，不同市场的缩写与全称并不相同：

| 材料 | 中国内地 | 中国香港 | 中国台湾 | 日本 | 法国 | 意大利 | 葡萄牙 | 俄罗斯 | 欧美 |
|---|---|---|---|---|---|---|---|---|---|
| 瓷砖 | CT / TL | TIL | TL | TI | CAR | CER | CER | KER | TL |
| 木地板 | WF | TF | PIS | PAR | PAR | PAR | PIS | PAK | — |
| 灯具大类 | DL | LT ⚠ | LT | LT | LUM | ILL | ILU | SVE | LGT |
| 石膏板 | PB | GYB | GES | GBP | PLQ | CG | GES | GKL | GB / GYP |
| 金属复合板 | MC | MC | — | — | — | — | — | — | ACP |

⚠ 港式图纸里 `LT` 既可能是照明、也可能是燈槽；台湾 `MR` 可能是大理石也可能是鏡面。**代码本身没有对错，错的是拿错了体系**——它会一路错到采购单、样板间和现场收口。

## 覆盖范围

- **12 个地区体系**：中国大陆、中国香港、中国澳门、中国台湾、日本、韩国、欧美（美/英/欧）、西班牙·拉丁美洲、中东·东南亚、法国·法语区、意大利、葡萄牙·巴西、俄罗斯·东欧
- **9 种语言**：中文 / English / 日本語 / 한국어 / Español / Français / Italiano / Português / Русский
  中国香港、中国澳门、中国台湾的中文自动转繁体并使用当地惯用词（亞加力、傢俬、膠片、壓克力、美耐板…）
- **80 条基准代码**（饰面 30 / 物料软装 10 / 灯具 16 / 表面处理 24）+ 各地区特有条目 + **17 条同码多义**专表 + 4 条编号规则
- 每个地区都给出**当地权威资料依据**（标准号与文件名称）、**体系说明**与**跨项目套用提醒**，页脚「资料口径」也按地区改写
- 实时搜索（可跨语种命中）、速查卡视图、点击代码即复制、深/浅色主题、打印为 A4；手机端地区 / 语言 / (主题+打印) 三栏排布

---

## 数据即 CSV：改数据，不用改代码

**`data/*.csv` 是唯一真相源**，`build.py` 只读 CSV，不含任何硬编码数据。

| 文件 | 内容 | 主键 |
|---|---|---|
| `data/entries.csv` | 每个材料一行：代码、分组、英文全称、9 种语言的名称 | (group, code) |
| `data/entry_text.csv` | 每条材料每种语言的「说明」「备注」 | (group, code, lang) |
| `data/regions.csv` | 地区清单：id、国旗、惯用语言、是否繁体 | id |
| `data/region_text.csv` | 地区级文案：名称、简介、提醒、依据、资料来源、页脚口径 | (region_id, lang) |
| `data/region_codes.csv` | 地区代码覆盖：通用代码 → 当地代码、当地名称 | (region_id, group, base_code) |
| `data/region_extras.csv` | 地区特有条目（如法国的 PLACO、俄国的 PLIN） | (region_id, code) |
| `data/region_conflicts.csv` | 地区特有的同码多义 | (region_id, code) |
| `data/conflicts.csv` / `data/conflict_text.csv` | 基准同码多义及其多语言区分方法 | code |
| `data/rules.csv` / `data/rule_text.csv` | 编号规则 | rule_id |
| `data/i18n.csv` | 界面文案（key + 9 语言） | key |
| `data/meta.csv` | 内容元信息：`updated_at` = 内容最后更新日期（页脚「更新日期」取自此处）、`source_note` = 出处概述 | key |

> ⚠ `DL`、`PL`、`TL`、`CL`、`FL` 五个代码在多个分组重复出现（既是「灯具大类」又是「筒灯」），定位时必须用 **group + code** 一起看。

### 构建

```bash
pip install openpyxl zhconv     # zhconv 仅用于繁体转换，缺失时自动回退内置逐字表
python build.py
```

产出 `index.html`（在线版）、`施工图材料代码多语对照表.html`（离线单文件）、`施工图材料代码多语对照表.xlsx`、`logo.svg`。

页脚的「更新日期」不是构建日期，而是 `data/meta.csv` 里 `updated_at` 的值——每次更新内容时改一次，这样它反映的是**内容**何时更新，而不是页面何时重新生成。

### 两个版本怎么来的

| | 在线版 `index.html` | 离线版 `施工图材料代码多语对照表.html` |
|---|---|---|
| 数据来源 | 运行时 `fetch('data/*.csv')` | 构建时把 12 个 CSV 全文内嵌进 HTML |
| 部署 | 与 `data/` 目录一起上传（GitHub Pages 直接可用） | 单文件，随手发人 |
| 外部依赖 | 仅同目录的 CSV | **零** |

两端共用同一套前端装配逻辑（`parseCSV` → `assemble`），所以两个版本内容完全一致。

## 每周更新

`prompts/weekly_update_prompt.md` 是一份**可在全新会话中独立执行**的定时任务提示词，包含：任务目标、全部 CSV 数据源路径与列说明、更新规则（含各地区权威资料清单）、输出格式、以及 8 项校验要求与交付报告模板。把它作为每周定时任务的提示词即可。

## 目录

```
index.html                 在线版页面
施工图材料代码多语对照表.html   离线版页面（单文件）
data/*.csv                 数据集（唯一真相源）
build.py                   构建脚本：读 CSV → 在线版 / 离线版 / Excel
zh_hant.py                 简体→繁体（港/台用词）转换
logo.svg                   站点标识
prompts/weekly_update_prompt.md   每周更新提示词
seed_*.py / tools_*.py     一次性数据迁移与多语内容生成脚本（留档，日常不必动）
seed/                      旧版 Python 数据源留档（已不参与构建）
```

## 资料口径与免责

各地区条目整理自**公开标准与法规**（如 GB、BS、JIS、KS、NF DTU、UNI、NP、СП、CTE、SBC 等）及行业实务惯例，属事实性信息汇编，不涉及第三方版权材料；具体项目的材料表图例仍受各设计单位版权约束，引用时请注明出处。

同一代码在不同设计公司、不同项目仍可能含义不同，**跨项目套用前务必先读该项目的 Material Legend**。

## 开源许可

本项目以 **MIT License** 开源——允许任何人自由使用、复制、修改、合并、发布、分发、再许可乃至商业销售，只需保留版权声明与许可声明。代码、构建脚本与页面模板均适用 MIT。

Copyright © 2026 Karandox Lopez. Released under the MIT License.
