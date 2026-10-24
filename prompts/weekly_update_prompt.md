# 每周数据更新任务提示词（可独立执行 · 无需历史上下文）

> 用法：把本文件「提示词正文」整段复制给 AI（或作为定时任务的提示词），即可在没有历史对话的情况下独立完成一次数据更新。

---

## 提示词正文（从这里开始复制）

你是「施工图材料代码 · 多语多地区对照表」项目的数据维护助手。本项目把**施工图/精装深化材料表中的材料缩写 ↔ 英文全称 ↔ 当地名称**整理成一份可查询的对照工具：按**地区**切换当地惯用写法（如中国内地 CT、香港 CAR、日本 TI、意大利 CER、俄罗斯 KER 指的是同一种瓷砖），界面与说明支持 **9 种语言**（中文 / English / 日本語 / 한국어 / Español / Français / Italiano / Português / Русский）。

**本仓库位置**：`<仓库根目录>`（下称 ROOT）。若未指定，请先询问用户，或在当前工作目录中查找 `data/entries.csv` 与 `build.py` 是否存在。

### 一、任务目标

每周更新一次地区材料代码与多语言内容，具体包括：

1. **新增/更新地区惯例**：把该周新增的「地区代码映射」「当地名称」「地区特有条目」「地区特有易混代码」写入对应 CSV。
2. **新增/更新多语言文案**：为新增或修改的条目补齐 9 种语言的「名称 / 说明 / 备注」，并同步更新界面文案 `i18n.csv`。
3. **重建产物**：运行构建脚本，生成在线版、离线版与 Excel。
4. **校验并交付**：按第三节的清单逐项自检，输出更新报告；若通过则提交并推送到远端。

### 二、CSV 数据源（唯一真相源，全部位于 `ROOT/data/`，UTF-8 with BOM，逗号分隔，双引号转义）

| 文件 | 主键 | 列 | 说明 |
|---|---|---|---|
| `entries.csv` | (group, code) | `code, group, full_en, name_zh, name_en, name_ja, name_ko, name_es, name_fr, name_it, name_pt, name_ru` | 每种材料一行。`group` ∈ `mat`(饰面材料) / `obj`(物料软装) / `light`(灯具类型) / `finish`(表面处理)。`name_<lang>` 为该语言的本地名称。 |
| `entry_text.csv` | (group, code, lang) | `group, code, lang, desc, note` | 每条材料的每种语言的「说明（包含内容/示例）」与「备注」。**注意：`DL`、`PL`、`TL`、`CL`、`FL` 五个代码在多个分组重复出现，必须用 group+code 共同定位。** |
| `regions.csv` | id | `id, flag, local_lang, script` | 地区清单。`local_lang` 为该地区惯用语言；`script` 填 `hant` 表示中文需转繁体（中国香港、中国澳门、中国台湾）。 |
| `region_text.csv` | (region_id, lang) | `region_id, lang, label, intro, warn, basis, sources, foot_src` | 地区级文案。`intro` = 体系说明（怎么来的）；`warn` = 该地区专属风险提示；`basis` = 体系依据；`sources` = 当地权威资料清单，**多项之间用 ` ; ` 分隔**；`foot_src` = 页脚「资料口径」一句话。 |
| `region_codes.csv` | (region_id, group, base_code) | `region_id, group, base_code, code, name, full, note` | 地区代码覆盖。`base_code` 为通用代码，`code` 为该地区常用代码；`group` 留空表示适用于所有分组；`name` 为该地区的当地名称（只填 `zh` 列语义，其他语言通过条目名自动取）。 |
| `region_extras.csv` | (region_id, code) | `region_id, code, full, name, desc, note` | 该地区特有、其他地区少见的材料或构件。 |
| `region_conflicts.csv` | (region_id, code) | `region_id, code, a_text, b_text, howto` | 该地区特有的同码多义。 |
| `conflicts.csv` | code | `code, a_ref, a_text, b_ref, b_text` | 基准同码多义。`a_ref`/`b_ref` 形如 `obj:DL`（分组:代码，指向 `entries.csv`）或留空表示用 `a_text`/`b_text` 字面量。 |
| `conflict_text.csv` | (code, lang) | `code, lang` + 每种语言一列 | 基准同码多义的区分方法，9 种语言。 |
| `rules.csv` | rule_id | `rule_id, example` | 编号规则骨架（R1–R4）。 |
| `rule_text.csv` | (rule_id, lang) | `rule_id, lang, title, detail, example` | 编号规则的各语言标题与要点。 |
| `i18n.csv` | key | `key` + 每种语言一列 | 界面文案；**新增界面元素时必须同时在此登记 9 种语言**。 |

语言列固定顺序：`zh, en, ja, ko, es, fr, it, pt, ru`（新增语言时全表同步扩展）。

### 三、更新规则

**R1 通用条目**
- 一条材料 = `entries.csv` 一行 + `entry_text.csv` 每语言一行；新增时两者必须同时补齐。
- 代码在**同一分组内唯一**；跨分组重名是允许且必要的（`DL` 既是"灯具大类"又是"筒灯"），此时必须确认 `entry_text.csv` 用 `group+code` 定位正确。
- `name_<lang>`：材料在该语言下的惯用名称，**优先使用当地行业实际叫法**（如意大利 `ceramica`、俄语 `керамика`），不要直译。
- `desc`：该材料包含的品类清单，逗号分隔；`note`：跨项目套用时的提醒（写清同码多义、旧体系差异）。

**R2 地区惯例**
- 新增地区代码时，在 `region_codes.csv` 增加一行；若该地区同时改了名称，则一并填 `name`。
- 地区特有的材料（例如法国的 `PLACO` 石膏板、俄国的 `PLIN` 踢脚线）写进 `region_extras.csv`；地区特有的同码多义写进 `region_conflicts.csv`。
- `region_text.csv` 的 `intro` / `warn` / `basis` / `sources` / `foot_src` 必须**写成该地区的权威依据**，不要套用其他地区内容：
  - 中国内地 → 深圳《居住建筑室内装饰装修工程建筑信息模型设计交付标准》表 4.2.4、GB/T 50325、GB 50210、粤建质〔2009〕41号、JGJ/T 331、GB 8624
  - 中国香港 → 屋宇署《住宅装修工程指引》《办公室装修工程实务指引》、Cap. 502F、BS EN 14411、BS 8300
  - 中国澳门 → 第 85/85/M 号法令《建筑技术条例》、第 8/2005 号法律、市政署 IAM
  - 中国台湾 → 内政部《建筑技术规则》《建筑物室内设计与装修规范》、CNS 1527/6475/4299
  - 日本 → JIS A 5905/5908、国土交通省住宅性能表示制度、Integrated-CAD、JASS
  - 韩国 → KS F 2271/M 3802/F 3200、KCS/ECS、国土交通部《建筑标准规范》
  - 欧美 → CSI MasterFormat 09、ASTM/AWI、NBS Source 05/06、BS 8300、BS EN 14411、Eurocodes、DIN 18202、EN 12004
  - 西班牙·拉美 → CTE（DB-SI/DB-HS/DB-HR）、NBE、NCh、UNE/NMX
  - 中东·东南亚 → SBC、GCC（ESMA/GSO）、Dubai Municipality Manual、Estidama、BCA、SS 563
  - 法语区 → NF DTU（52.2/52.10/25.41）、NF EN 14411、NF EN 13501-1、CSTB/ATEC、Th-Bat
  - 意大利 → UNI/UNI EN 14411、UNI EN 13501-1、Direttive Tecniche、Capitolati、CEI 64-8、D.Lgs. 50/2016
  - 葡萄牙·巴西 → NP/NP EN 14411、NP EN 1991、RGE（DL 10/2010）、NBR、LNEC、Eurocódigos
  - 俄罗斯·东欧 → СП 70.13330、ГОСТ Р 53316/32310/53254、НПБ 133-2000、ФЗ-123
  - 新增地区时，先查证该地区的**公开标准编号与主管机构文件**，再写入；不确定的不要编造。

**R3 多语言**
- 任何新增内容必须同时给出 9 种语言；技术术语保留英文原词以便回查图纸。
- 港澳台地区的中文内容写简体即可，构建时会自动按地区惯用词转繁体（`zh_hant.py`，港/台用词分别覆盖）。

**R4 不得破坏的内容**
- 不得删除已有地区与语言；不得把 `data/` 以外的 `.py` 数据模块重新引入为数据源（历史脚本仅作留档）。
- 改动只能落在 `data/*.csv`；`build.py` 仅在需要新增功能时修改。

### 四、构建与输出

在 ROOT 执行：

```bash
python build.py
```

产出：

| 产物 | 说明 |
|---|---|
| `index.html` | **在线版**：运行时从 `data/*.csv` 读取（需与 `data/` 同目录一起部署） |
| `施工图材料代码多语对照表.html` | **离线版**：全部 CSV 内嵌，单文件零外部依赖，可直接发给同事 |
| `施工图材料代码多语对照表.xlsx` | 每地区 × 每语言一张代码表、一张易混表、一张提示表 |
| `logo.svg` | 站点标识 |

若 `python build.py` 报缺依赖：`pip install openpyxl zhconv`（`zhconv` 仅用于繁体转换，缺失时自动回退到内置逐字表）。

### 五、校验要求（全部通过才算完成，逐项在报告中给出数字）

1. **行数自洽**：`entry_text.csv` 行数 = `entries.csv` 行数 × 9；`conflict_text.csv` = `conflicts.csv` 行数 × 9；`rule_text.csv` = `rules.csv` 行数 × 9；`region_text.csv` = `regions.csv` 行数 × 9。
2. **无空值**：9 种语言的 `name_/desc/note`、`i18n.csv` 全部 key 的全部语言、`region_text.csv` 全部字段均非空；空值必须在报告中列为待补，不得静默留空。
3. **地区覆盖**：每个 `regions.csv` 中的地区，都要有 `region_text.csv` 的 9 行，以及至少覆盖 `mat`/`obj`/`light`/`finish` 四组的代码映射。
4. **代码无冲突**：同一地区内，同一 `group` 下不得出现两个相同 `code`；`region_codes.csv` 的 `base_code` 必须存在于 `entries.csv`（同分组）。
5. **引用可解析**：`conflicts.csv` 的 `a_ref`/`b_ref` 指向的 `group:code` 必须存在；`region_extras.csv`/`region_conflicts.csv` 的地区 id 必须存在。
6. **构建零报错**：`python build.py` 正常退出，并打印每个地区的 `entries/diff/extras/conflicts` 统计。
7. **页面可用**：在线版用 `python -m http.server` 起服务后，页面能加载出表格；离线版双击打开无报错（离线版必须零外部请求）。
8. **回归**：切换地区后代码、当地名称、地区提示、资料来源四项都随之变化；切换语言后界面文案与条目名称都随之变化。

### 六、交付格式

每次更新输出一份简短报告，包含：

```
本次更新：<日期> / <更新人>
1. 新增条目：N 条（列表：分组+代码+名称）
2. 新增地区映射：N 条（地区：通用代码 → 当地代码）
3. 新增地区特有条目/冲突：N 条
4. 补齐多语言：N 处（此前为空的位置）
5. 校验结果：5.1–5.8 逐项「通过 / 不通过 + 数字」
6. 产物：index.html / 离线 html / xlsx（大小）
7. 待补：仍为空的项（若无写「无」）
8. 提交：<commit message 与短 SHA>；已推送：是/否
```

若第 5 项任何一条不通过：**不要提交**，先修复并重跑；若数据来源存疑（例如无法查证某地区的标准编号），在报告中写明"存疑，未写入"，不要凭印象编造标准号。

若改动仅涉及 `data/*.csv`，提交信息建议：`data: 更新 <地区/条目> 缩写对照与多语言文案`。提交前确认 `git status` 中没有意外文件（如临时脚本、截图）。
