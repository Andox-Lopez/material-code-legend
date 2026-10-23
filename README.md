# 施工图材料代码 · 多语多地区对照表
# Material Code Legend — Multilingual & Multi-Region

> 施工图材料大类代码的 **缩写 ↔ 全称** 对照工具：按地区切换当地惯用写法，界面与说明支持 中 / 英文 / 日本語 / 한국어 / Español。
> An offline-first lookup for construction-drawing material codes: switch **region** to see local abbreviations and full names, in 5 languages.

**在线浏览 / Live site：** https://Andox-Lopez.github.io/material-code-legend/

---

## 这个工具解决什么问题 / What it solves

同一条材料在不同国家/地区的缩写与全称并不相同：

| 材料 | 中国内地 | 中国香港 | 中国台湾 | 日本 | 欧美 |
|---|---|---|---|---|---|
| 木地板 | WF | TF | WF | WF | — |
| 瓷砖 | CT / TL | TIL | TL | TI | TL |
| 石材金属 | MT | MTL | — | — | — |
| 灯具大类 | DL | LT（也可能指燈槽） | LT | LT | LGT |
| 防火板 | LP | LAM | 美耐板 | 化粧ボード | LAM |

So a code copied from another project can be wrong. This tool lets you pick the region first, then read the code, the local name, the contents, the notes and the traps for that market.

## 功能 / Features

- **8 个地区体系**：中国大陆、中国香港、中国台湾、日本、韩国、欧美（美/英/欧）、西班牙/拉丁美洲、中东与东南亚
  每个地区有自己的代码映射、当地名称、地区特有条目与地区特有易混代码。
- **5 种界面语言**：中文 / English / 日本語 / 한국어 / Español；中国香港、中国台湾自动转繁体并使用当地惯用词（亞加力、傢俬、膠片、壓克力、美耐板…）。
- **「先读这句」随地区切换**：每个地区显示自己的资料出处与跨项目套用提醒（例如香港 LT 的照明/燈槽歧义、台湾 MR 的 Marble/Mirror 歧义）。
- 实时搜索（可跨语种命中）、速查卡视图、点击代码即复制、深/浅色主题、打印为 A4。
- Excel 版：每个地区、每种语言各一张表，另附「地区提示」表。

## 资料口径 / Sources

国内没有统一强制的材料代码国标。基准表取自深圳《居住建筑室内装饰装修工程建筑信息模型设计交付标准》表 4.2.4 装饰材料代码表、多地精装施工图材料表实例，以及设计公司通用的中英文对照缩写。各地区条目为当地实务常见惯例的整理，**实际出图必须以本项目材料表图例（Material Legend / Cuadro de Materiales / 材料表）为准**。

## 目录 / Repository layout

| 路径 | 说明 |
|---|---|
| `index.html` | 成品页面（由 CI 从源码构建后回写） |
| `build.py` | 构建脚本：生成单文件 HTML + 多地区 Excel |
| `data_common.py` | 数据结构与语言定义 |
| `data_mat.py` | 饰面材料 / 物料软装（40 条） |
| `data_light.py` | 灯具类型（16 条） |
| `data_finish.py` | 表面处理 / 终饰（24 条） |
| `data_conflict.py` | 同码多义（17 条）与编号规则（4 条） |
| `data_regions.py` `data_regions_a.py` `data_regions_b.py` | 8 个地区的惯例数据（代码 / 名称 / 说明 / 特有条目 / 特有冲突） |
| `i18n.py` | 界面文案（5 语言） |
| `zh_hant.py` | 简体→繁体（港/台用词）转换 |
| `.github/workflows/pages.yml` | 构建并发布到 GitHub Pages |

## 本地构建 / Build locally

```bash
pip install openpyxl zhconv     # zhconv 可选：缺失时回退到内置逐字表
python build.py                 # 生成 施工图材料代码多语对照表.html / .xlsx
```

打开生成的 `施工图材料代码多语对照表.html` 即可（单文件、离线可用）。

## 说明 / Disclaimer

各地区条目整理自公开标准与行业惯例，用于出图前的**快速核对**；同一代码在不同设计公司、不同项目仍可能含义不同，跨项目套用前务必先读该项目的 Material Legend。
