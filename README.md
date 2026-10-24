# 施工图材料代码 · 多语多地区对照表
# Material Code Legend — Multilingual & Multi-Region

<p align="center">
  <img src="logo.svg" width="96" alt="施工图材料代码对照表 logo">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/language-zh%20%7C%20en%20%7C%20ja%20%7C%20ko%20%7C%20es-blue.svg" alt="Languages">
  <img src="https://img.shields.io/badge/regions-8-blue.svg" alt="Regions">
  <img src="https://img.shields.io/badge/离线-offline%20usable-brightgreen.svg" alt="Offline usable">
</p>

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
- **「先读这句」随地区切换**：每个地区显示自己的资料出处与跨项目套用提醒（例如香港 LT 的照明/燈槽歧义、台湾 MR 的 Marble/Mirror 歧义）。
- **本地区资料依据**：按地区列出当地可查证的权威依据——中国内地引深圳 BIM 交付标准表 4.2.4、GB/T 50325、GB 50210、粤建质〔2009〕41号、JGJ/T 331、GB 8624；中国香港引屋宇署《住宅装修工程指引》《办公室装修工程实务指引》、Cap. 502F、BS EN 14411、BS 8300；中国澳门引第 85/85/M 号法令《建筑技术条例》；中国台湾引内政部《建筑技术规则》与 CNS 1527/6475/4299；日本引 JIS A 5905、国土交通省住宅性能表示制度、Integrated-CAD 建材信息标准化、JASS；韩国引 KS 与 KCS/ECS、国家建设标准；欧美引 CSI MasterFormat 09、NBS Work Section 05/06、Eurocodes、DIN 18202；西语区引 CTE、NBE、NCh、UNE/NMX；中东与东南亚引 SBC、GCC 通用规范、迪拜 Municipality 手册、Estidama、新加坡 BCA 与 SS 563。页脚「资料口径」同样按地区改写。
- **5 种界面语言**：中文 / English / 日本語 / 한국어 / Español；中国香港、中国台湾自动转繁体并使用当地惯用词（亞加力、傢俬、膠片、壓克力、美耐板…）。
- 实时搜索（可跨语种命中）、速查卡视图、点击代码即复制、深/浅色主题、打印为 A4。
- Excel 版：每个地区、每种语言各一张表，另附「地区提示」表（含资料依据与跨项目提醒）。

## 资料口径 / Sources

国内没有统一强制的材料代码国标。基准表取自深圳《居住建筑室内装饰装修工程建筑信息模型设计交付标准》表 4.2.4 装饰材料代码表、多地精装施工图材料表实例，以及设计公司通用的中英文对照缩写。各地区条目为当地实务常见惯例的整理，**实际出图必须以本项目材料表图例（Material Legend / Cuadro de Materiales / 材料表）为准**。

## 目录 / Repository layout

| 路径 | 说明 |
|---|---|
| `index.html` | 成品页面（由 CI 从源码构建后回写） |
| `logo.svg` | 站点标识：施工蓝图网格 + 代码标签 + 材料饰面叠层（页面页头与浏览器图标共用） |
| `build.py` | 构建脚本：生成单文件 HTML + 多地区 Excel |
| `data_common.py` | 数据结构与语言定义 |
| `data_mat.py` | 饰面材料 / 物料软装（40 条） |
| `data_light.py` | 灯具类型（16 条） |
| `data_finish.py` | 表面处理 / 终饰（24 条） |
| `data_conflict.py` | 同码多义（17 条）与编号规则（4 条） |
| `data_regions.py` `data_regions_a.py` `data_regions_b.py` | 8 个地区的惯例数据（代码 / 名称 / 说明 / 特有条目 / 特有冲突） |
| `data_sources.py` | 各地区的权威资料依据、体系依据说明与页脚资料口径（5 语言） |
| `i18n.py` | 界面文案（5 语言） |
| `zh_hant.py` | 简体→繁体（港/台用词）转换 |
| `.github/workflows/pages.yml` | 构建并发布到 GitHub Pages |

## 本地构建 / Build locally

```bash
pip install openpyxl zhconv     # zhconv 可选：缺失时回退到内置逐字表
python build.py                 # 生成 施工图材料代码多语对照表.html / .xlsx
```

打开生成的 `施工图材料代码多语对照表.html` 即可（单文件、离线可用）。

## 开源许可 / License

本项目以 **MIT License** 开源——这是最宽松的常用开源授权：允许任何人自由使用、复制、修改、合并、发布、分发、再许可乃至销售本项目，只需保留版权声明与许可声明。

代码、构建脚本与页面模板均适用 MIT；可直接 fork、二次开发、嵌入你自己的项目或商业项目使用，无需额外申请授权。

各地区材料代码条目整理自**公开标准与法规**（如 GB、BS、JIS、KS、CTE、SBC 等）及行业实务惯例，属于事实性信息的汇编，不涉及第三方版权材料；但具体项目的材料表图例仍受各设计单位版权约束，引用时请注明出处。

各地区条目整理自公开标准与实务惯例，用于出图前的**快速核对**；同一代码在不同设计公司、不同项目仍可能含义不同，跨项目套用前务必先读该项目的 Material Legend。

Copyright © 2026 Karandox Lopez. Released under the MIT License.
