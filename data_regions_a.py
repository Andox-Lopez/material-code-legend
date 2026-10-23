# -*- coding: utf-8 -*-
"""地区体系 A：中国大陆（基准）、中国香港、中国台湾

每个地区描述「本地惯用什么代码、叫什么名字」：
  codes   通用代码 → 本地区常用代码
  names   通用名称 → 本地区惯用名称（本地语言）
  descs   说明文字的地区用语替换
  fulls   英文全称的地区写法
  notes   该条目的地区备注（本地语言）
  extras  本地区特有条目
  conflicts 本地区特有易混代码
键写法："代码" 或 "分组:代码"（同一代码在不同分组含义不同时用后者）
"""

from data_common import E, C


def G(**kw):
    kw.setdefault("script", "")
    kw.setdefault("codes", {})
    kw.setdefault("names", {})
    kw.setdefault("descs", {})
    kw.setdefault("fulls", {})
    kw.setdefault("notes", {})
    kw.setdefault("extras", [])
    kw.setdefault("conflicts", [])
    return kw


REGIONS_A = [
    # ============================================================ 中国大陆
    G(
        id="cn", flag="🇨🇳",
        label={"zh": "中国大陆", "en": "Mainland China", "ja": "中国大陸", "ko": "중국 본토", "es": "China continental"},
        local_lang="zh", script="",
        intro={
            "zh": "国内没有强制的材料代码国标，实际出图以本项目材料表图例（Material Legend）为唯一准绳。本表基准取自深圳《居住建筑室内装饰装修工程建筑信息模型设计交付标准》表 4.2.4 与各地精装施工图实例；DL、SP、SL、PL 是跨专业最易出错的四个代码。",
            "en": "China has no mandatory material-code standard: the project's own Material Legend governs. This baseline follows Table 4.2.4 of the Shenzhen BIM delivery standard for residential interior fit-out plus material schedules from fit-out drawings nationwide. DL, SP, SL and PL are the four codes most often mixed up across disciplines.",
            "ja": "中国には強制される材料コード国標はなく、実際の出図は当該プロジェクトの材料表凡例（Material Legend）が基準。深圳の「居住建築室内装飾装修工程建築情報モデル設計交付標準」表 4.2.4 と各地域の施工図事例を基準とし、DL・SP・SL・PL は職種をまたいで最も混同されやすいコード。",
            "ko": "중국에는 강제되는 재료 코드 국표가 없어 실제 출도는 해당 프로젝트의 Material Legend를 기준으로 합니다. 본 표는 선전시 「주거 건축 실내 장식 샹싱 건축정보모델 설계납품표준」 표 4.2.4와 각지精装施工도 사례를 기준으로 하며, DL·SP·SL·PL은 직군을 넘나들며 가장 자주 혼동되는 코드입니다.",
            "es": "China no tiene norma obligatoria de códigos de material: rige la leyenda de materiales del proyecto. Esta referencia sigue la tabla 4.2.4 del estándar de entrega BIM de Shenzhen y cuadros de materiales de planos de decoración de distintas ciudades. DL, SP, SL y PL son los códigos que más se confunden entre disciplinas.",
        },
        warn={
            "zh": "同一代码在不同设计公司/项目可能含义不同，跨项目套用前必须先读该项目的 Material Legend。",
            "en": "The same code may mean different things in different practices or projects: always read the project's own Material Legend before reusing it.",
            "ja": "同じコードでも設計事務所・プロジェクトで意味が異なる場合があります。転用前に必ず当該プロジェクトの Material Legend を確認してください。",
            "ko": "동일한 코드라도 설계사무소·프로젝트에 따라 의미가 다를 수 있으므로, 다른 프로젝트에 적용하기 전 반드시 해당 프로젝트의 Material Legend를 확인하세요.",
            "es": "El mismo código puede significar cosas distintas según el estudio o el proyecto: lea siempre la leyenda de materiales del proyecto antes de reutilizarlo.",
        },
        notes={
            "obj:DL": "材料表／物料清单＝灯具大类；灯位图与型号（DL-Φ100-12W）＝筒灯。国内项目若把两类混用，必须在图例中写明。",
            "mat:SP": "SP 在材料表＝特殊涂料；在电气图例＝射灯（Spot Light）。",
            "mat:SL": "SL 在材料表＝特殊饰面；在电气图例＝灯带／射灯。",
        },
    ),

    # ============================================================ 中国香港
    G(
        id="hk", flag="🇭🇰",
        label={"zh": "中国香港", "en": "Hong Kong, China", "ja": "中国香港", "ko": "중국 홍콩", "es": "Hong Kong (China)"},
        local_lang="zh", script="hant",
        intro={
            "zh": "香港工程图例多用英式英文与粤语习惯术语：亚加力（Acrylic）、傢俬、地胶、胶片、髮纹；石材金属常用 MTL／ALU／GYB／TIL 等较长缩写，假天花（False Ceiling）与防火门（Fire Door）亦属常见项目。以本项目 Material Legend 为准。",
            "en": "Hong Kong drawings lean on British English and Cantonese trade terms: acrylic (亞加力), furniture (傢俬), vinyl flooring (地膠), light diffusers (膠片) and hairline (髮紋). Longer abbreviations such as MTL, ALU, GYB and TIL are common, and false ceilings (假天花) and fire doors (防火門) appear as standard items. The project's Material Legend still rules.",
            "ja": "香港の図面はイギリス英語と広東語の商用語を好む：アクリル（亞加力）、傢俬、塩ビ床材（地膠）、ライトパネル（膠片）、ヘアライン（髮紋）。MTL／ALU／GYB／TIL といった長め，略称が一般的で、假天花（False Ceiling）や防火門（防火門）も通常の項目。基準は当該プロジェクトの Material Legend。",
            "ko": "홍콩 도면은 영국식 영어와 광둥어 관용어를 즐겨 씁니다: 아크릴(亞加力), 가구(傢俬), 비닐 바닥재(地膠), 조명 디퓨저(膠片), 헤어라인(髮紋). MTL·ALU·GYB·TIL 처럼 긴 약어가 흔하며, 천장(假天花)·방화문(防火門)도 흔한 항목입니다. 기준은 해당 프로젝트의 Material Legend입니다.",
            "es": "Los planos de Hong Kong apuntan al inglés británico y a los términos de oficio de Cantón: acrílico (亞加力), mobiliario (傢俬), suelo de vinilo (地膠), difusores (膠片) y cepillado (髮紋). Son habituales las abreviaturas largas (MTL, ALU, GYB, TIL) y el falso techo (假天花) y las puertas cortafuegos (防火門). Mandará la leyenda de materiales del proyecto.",
        },
        warn={
            "zh": "香港項目多用較長的英式縮寫與粵語行話，同一字母在不同顧問公司之間含義可不同（LT 既可指照明，也可指燈槽）。跨項目套用前，必須先讀該項目的 Material Legend。",
            "en": "Hong Kong drawings favour longer British abbreviations and Cantonese trade terms, and the same letters can differ between consultants (LT may mean luminaires or light trunk). Read the project's own Material Legend before reusing any code.",
            "ja": "香港の図面は長い英式略称と広東語の行語を好み、同じ英字が設計顾问社ごとに意味が異なること（LT は照明器具にも燈槽にもあたる）があります。転用前に必ず当該プロジェクトの Material Legend を確認してください。",
            "ko": "홍콩 도면은 긴 영식 약어와 광둥어 관용어를 선호하며 같은 영문이 컨설턴트마다 의미가 다를 수 있습니다(LT는 조명기구이자 燈槽). 적용 전 반드시 해당 Material Legend를 확인하세요.",
            "es": "Los planos de Hong Kong prefieren abreviaturas británicas largas y términos de Cantón, y las mismas letras cambian entre consultores (LT puede ser luminarias o light trunk). Lea la leyenda de materiales del proyecto antes de reutilizar.",
        },
        codes={
            "MT": "MTL", "AL": "ALU", "AC": "ACR", "PB": "GYB", "CT": "TIL", "mat:TL": "TIL",
            "MO": "MOS", "CA": "CAR", "WC": "WAL", "PT": "PNT", "PL": "PLA", "LP": "LAM",
            "SF": "SPF", "WR": "WPF", "VF": "VNL", "SC": "SCF", "AP": "ACU",
            "obj:DL": "LT", "obj:FR": "FUR", "obj:HW": "HDW", "obj:SW": "SAN", "obj:KIT": "KTE",
            "obj:AR": "ART", "obj:BDG": "BED", "obj:SSP": "SWP", "obj:EA": "ELE",
            "light:SL": "SP", "light:TL": "TRK", "light:UL": "UCB", "light:ML": "MAG",
            "light:WW": "WWL", "light:IL": "IGL", "light:UW": "UWL", "light:EL": "EMG",
            "light:EXIT": "EXI", "finish:H": "HL",
        },
        names={
            "AC": "亞加力（有機玻璃）", "PL": "塑膠（亞加力／膠片／塑膠板）",
            "UP": "軟硬包（皮革／布藝）", "WC": "牆面飾材（牆紙／牆布）",
            "obj:FR": "傢俬·家具", "obj:SW": "潔具", "obj:BDG": "寢具用品",
            "obj:SSP": "開關插座面板", "obj:EA": "電器設備", "obj:DL": "燈具",
            "MC": "金屬複合板", "WR": "防水捲材", "VF": "地膠板（PVC 地板）",
            "finish:H": "拉絲／髮紋飾面", "finish:MA": "毛光·啞光飾面",
            "finish:CL": "亮漆罩面", "finish:PC": "粉體噴塗", "finish:FL": "火燒面",
            "light:TL": "軌道燈", "light:EXIT": "疏散指示燈",
        },
        descs={
            "PL": "亞加力板、PC 耐力板、膠片、塑膠飾條",
            "AC": "亞加力透光板、燈箱面板、立體雕刻字",
            "UP": "皮革硬包、布藝軟包、吸音軟包",
            "MC": "鋁塑複合板、鋁蜂窩板、鈦鋅複合板",
            "WR": "SBS 捲材、自黏防水膜、防水塗膜捲材",
            "WC": "牆紙、牆布、無紡布牆布、稻草紋／木紋壁紙",
            "obj:FR": "活動傢俬、固定傢俬、櫃體、檯面",
            "obj:SSP": "開關面板、插座面板、智能控制面板",
            "finish:H": "不鏽鋼／鋁板長髮紋",
        },
        fulls={
            "PB": "Gypsum Board", "WC": "Wallpaper", "CA": "Carpet", "LP": "Laminate",
            "AC": "Acrylic", "MT": "Metal", "AL": "Aluminium", "CT": "Ceramic Tile",
            "obj:FR": "Furniture", "obj:HW": "Hardware", "obj:SW": "Sanitary Ware",
            "obj:EA": "Electrical Appliances", "light:EXIT": "Exit Sign",
        },
        notes={
            "obj:DL": "港式常把燈具大類寫成 LT，DL 留給筒燈；材料表與燈位圖要用同一套寫法。",
            "mat:TL": "港式瓷磚多用 TIL；TIL 與 TL 同義，全冊須統一。",
            "AC": "ACR 為亞加力，但港式亦有 ACR 指 Acoustic（吸音）材料，看 AC-01 後接字判斷。",
            "PB": "GYB = Gypsum Board（石膏板），與 GR（玻璃鋼）、MF（夾板）不同。",
            "finish:CL": "CL 在港式既可指 Clear Lacquer，也可在燈具圖例指 Ceiling Light，按圖層判斷。",
        },
        extras=[
            E("FC",
              ("False Ceiling", "Mineral fibre board, calcium silicate board, aluminium tile and grid ceiling",
               "Very common in Hong Kong fit-out drawings"),
              ("假天花", "礦棉板、硅酸鈣板、鋁扣板天花、輕鋼龍骨天花",
               "香港工程常見項目；與表面處理的 FC（氟碳塗層）同碼，需按圖層判斷"),
              ("False Ceiling", "岩綿板、珪酸カルシウム板、アルミ化粧板、軽鉄骨下地天井",
               "香港の工事では一般的。表面仕上げの FC（フッ素塗装）と同コードのため図層で判断"),
              ("천장", "미네랄울纤维板, 칼슘실리케이트 보드, 알루미늄 타일 천장",
               "홍콩 공사에서 흔한 항목. 표면 마감 FC(플루오로카본)와 코드가 같아 도면 계층으로 구분"),
              ("Falso techo", "Placa de lana mineral, placa de calcio-silicato, placa de aluminio y techo raso",
               "Muy habitual en la decoración de Hong Kong; comparte código con el acabado FC")),
        ],
        conflicts=[
            C("FC",
              ("lit", {"zh": "假天花（False Ceiling）", "en": "False ceiling", "ja": "仮天井（False Ceiling）",
                       "ko": "천장（False Ceiling）", "es": "Falso techo (False Ceiling)"}),
              ("lit", {"zh": "氟碳喷涂饰面（Fluorine Coat）", "en": "Fluorocarbon coating", "ja": "フッ素樹脂塗装",
                       "ko": "플루오로카본 코팅", "es": "Recubrimiento de fluorocarbono"}),
              {"zh": "天花图／顶棚标注＝假天花；型材表面处理表＝氟碳涂层。看是否出现在铝型材表面处理表。",
               "en": "Ceiling plans = false ceiling; profile finish schedules = fluorocarbon coating.",
               "ja": "天井図＝仮天井、型材の表面処理表＝フッ素塗装。表のどちらに現れるかで判別",
               "ko": "천장도=천장, 프로파일 마감표=플루오로카본. 어느 표에 나오는지로 구분",
               "es": "Planos de techo = falso techo; cuadros de acabado de perfiles = fluorocarbono."}),
            C("DL",
              ("lit", {"zh": "灯具大类（LT）", "en": "Lighting fixtures (LT)", "ja": "照明器具（LT）",
                       "ko": "조명기구（LT）", "es": "Luminarias (LT)"}),
              ("lit", {"zh": "筒灯（Downlight）", "en": "Downlight", "ja": "ダウンライト",
                       "ko": "다운라이트", "es": "Downlight"}),
              {"zh": "港式 LT＝灯具大类、DL＝筒灯；与国内 DL 双重含义的写法相反。",
               "en": "In Hong Kong practice LT = fixtures and DL = downlight, the reverse of the mainland convention.",
               "ja": "香港式では LT＝照明器具、DL＝ダウンライトで、中国本土とは逆の扱い。",
               "ko": "홍콩식 표기는 LT=조명기구, DL=다운라이트로 중국 본토와 반대입니다.",
               "es": "En Hong Kong LT = luminarias y DL = downlight, al contrario de la convención del continente chino."}),
        ],
    ),

    # ============================================================ 中国台湾
    G(
        id="tw", flag="🇹🇼",
        label={"zh": "中国台湾", "en": "Taiwan, China", "ja": "中国台湾", "ko": "중국 대만", "es": "Taiwán (China)"},
        local_lang="zh", script="hant",
        intro={
            "zh": "台湾图例以繁体中文搭配行业英文缩写为主：壓克力、人造石、石英磚、美耐板、系統櫥櫃、燈具 LT／筒燈 DL 分工明确，防火板常写 FP、壁纸壁布常写 WC。以本项目 Material Legend 为准。",
            "en": "Taiwanese drawings pair traditional Chinese with trade abbreviations: 壓克力, 人造石, 石英磚, 美耐板 and 系統櫥櫃. Lighting is split as LT for fixtures and DL for downlights, laminate is often FP, and wall coverings WC. The project's Material Legend still rules.",
            "ja": "台湾の図例は繁体字中国語と業界略称の組み合わせ：壓克力、人造石、石英磚、美耐板、系統櫥櫃。照明は LT＝照明器具、DL＝ダウンライトと明確に分担し、化粧ボードは FP、壁紙・壁布は WC。基準は当該プロジェクトの Material Legend。",
            "ko": "대만 도면은 번체 중국어와 업계 약칭의 결합입니다: 壓克力, 人造石, 石英磚, 美耐板, 系統櫥櫃. 조명은 LT=조명기구, DL=다운라이트로 명확히 나뉘며, 합판은 FP, 벽지는 WC로 표기합니다. 기준은 해당 프로젝트의 Material Legend입니다.",
            "es": "Los planos de Taiwán combinan chino tradicional con abreviaturas del sector: 壓克力, 人造石, 石英磚, 美耐板, 系統櫥櫃. La iluminación se reparte como LT (luminarias) y DL (downlights); el laminado suele ser FP y el revestimiento mural WC.",
        },
        warn={
            "zh": "台灣地區同一縮寫常見不同義（MR 可指大理石 Marble，也可指鏡面 Mirror）；跨項目套用前，必須先讀該項目的 Material Legend。",
            "en": "In Taiwan, China the same abbreviation often carries two meanings (MR may be Marble or Mirror); always read the project's own Material Legend before reusing a code.",
            "ja": "台湾地区では同じ略称が二つの意味を持つことが多い（MR は Marble にも Mirror にも当たります）。転用前に必ず当該プロジェクトの Material Legend を確認してください。",
            "ko": "대만(중국)에서는 같은 약어가 두 가지 의미로 쓰이는 경우가 많습니다(MR이 Marble일 수도 Mirror일 수도). 적용 전 반드시 해당 Material Legend를 확인하세요.",
            "es": "En Taiwán (China) la misma abreviatura suele tener dos significados (MR puede ser Marble o Mirror); lea la leyenda de materiales del proyecto antes de reutilizar.",
        },
        codes={
            "LP": "FP", "AC": "AC", "WC": "WC", "PT": "PT", "CA": "CA",
            "obj:DL": "LT", "obj:FR": "FR", "obj:SW": "SAN", "obj:KIT": "KTE",
            "obj:AR": "ART", "obj:EA": "ELE",
            "light:PL": "PD", "light:PN": "PL", "light:SL": "SP", "light:EXIT": "EX",
            "finish:H": "HL",
        },
        names={
            "AC": "壓克力（有機玻璃）", "PL": "塑膠（壓克力／燈片／塑膠板）",
            "UP": "皮革硬包／軟包", "WC": "壁布／壁紙（牆面飾材）", "LP": "美耐板（防火板）",
            "obj:FR": "傢俱", "obj:SW": "衛浴設備", "obj:KIT": "廚具設備", "obj:BDG": "寢具",
            "obj:EA": "家電／電器設備", "obj:PLT": "綠植／盆栽", "obj:DL": "燈具",
            "light:PL": "吊燈", "light:PN": "平板燈", "light:SL": "射燈",
            "finish:H": "拉絲飾面", "finish:PC": "粉體烤漆", "finish:FL": "火燒面",
        },
        descs={
            "AC": "壓克力透光板、燈箱面板、立體雕刻字",
            "PL": "壓克力板、PC 耐力板、燈片、塑膠飾條",
            "UP": "皮革硬包、軟包、吸音軟包",
            "WC": "壁紙、壁布、非織布壁布、稻草紋／木紋壁紙",
            "obj:FR": "活動傢俱、固定傢俱、櫃體、檯面",
            "obj:SSP": "開關面板、插座面板、智能控制面板",
            "finish:PC": "鋁型材靜電粉體烤漆",
        },
        fulls={
            "AC": "Acrylic (PMMA)", "LP": "Fire Proof Laminate", "WC": "Wall Covering",
            "obj:SW": "Sanitary Ware", "obj:EA": "Electrical Appliances",
            "light:PN": "Panel Light", "light:PL": "Pendant Light",
        },
        notes={
            "obj:DL": "台灣常見 LT＝燈具大類、DL＝筒燈；PD＝吊燈、PL＝平板燈，與大陸的 PL 寫法相反。",
            "AC": "AC 可指壓克力，也可指礦棉吸音板（Acoustic Ceiling），看 AC-01 後接字。",
            "LP": "美耐板常寫 FP；部分工程仍沿用 LP。",
        },
        extras=[
            E("AS",
              ("Engineered Stone", "Quartz-based engineered stone, sintered stone and artificial stone panels",
               "A major category in Taiwanese fit-outs; in Mainland drawings it is usually AR"),
              ("人造石", "石英石、燒結石、人造石板材",
               "台灣精裝常用大類；大陸多以 AR（人造石）表示，注意區分"),
              ("Engineered Stone", "人造石、石英石、燒結石",
               "台湾精装の主要カテゴリ。大陸では AR（人工石）で表すことが多い"),
              ("인조석", "엔지니어드 스톤, 시마스톤, 인공석 판",
               "대만 마감에서 흔한 분류, 중국 본토에서는 AR(인공석)로 표기"),
              ("Piedra artificial", "Piedra reconstituida, terrazo y cuarcita de nueva generación",
               "Categoría habitual en decoración taiwanesa; en China continental suele ser AR")),
            E("QT",
              ("Quartz Tile", "Engineered quartz floor and wall tiles, 600×600 and 800×800 formats",
               "Commonly separated from ceramic tile in Taiwanese schedules"),
              ("石英磚", "石英磚地磚／牆磚、600×600、800×800 規格",
               "台灣常與陶瓷磚分列；大陸多併入 CT 瓷磚"),
              ("Quartz Tile", "石英タイル（床・壁）、600×600、800×800 規格",
               "台湾では磁器タイルと分けて記載することが多い"),
              ("쿼츠 타일", "엔지니어드 쿼artz 바닥·벽 타일, 600×600·800×800",
               "대만에서는 세라믹 타일과 분리 표기, 중국 본토는 CT에 통합"),
              ("Baldosa de cuarzo", "Baldosas de cuarzo de 600×600 y 800×800",
               "En Taiwán se listan aparte del gres cerámico")),
        ],
        conflicts=[
            C("LT / DL",
              ("lit", {"zh": "燈具大類（LT）", "en": "Lighting fixtures (LT)", "ja": "照明器具（LT）",
                       "ko": "조명기구（LT）", "es": "Luminarias (LT)"}),
              ("lit", {"zh": "筒燈（DL）", "en": "Downlight (DL)", "ja": "ダウンライト（DL）",
                       "ko": "다운라이트（DL）", "es": "Downlight (DL)"}),
              {"zh": "台灣分工明確：LT＝燈具類、DL＝筒燈。跨地區套用圖例時最易出錯。",
               "en": "Taiwanese practice splits them cleanly: LT for fixtures, DL for downlights — the usual error when reusing another region's legend.",
               "ja": "台湾では LT＝照明器具、DL＝ダウンライトと明確に分かれる。他地域の凡例をそのまま流用すると最も間違えやすい。",
               "ko": "대만은 LT=조명기구, DL=다운라이트로 명확히 구분하며, 다른 지역 凡例의 그대로 쓰면 가장 자주 틀립니다.",
               "es": "En Taiwán se separan con claridad (LT y DL); es el error más común al reutilizar la leyenda de otra región."}),
            C("AC",
              ("lit", {"zh": "壓克力（Acrylic）", "en": "Acrylic", "ja": "アクリル",
                       "ko": "아크릴", "es": "Acrílico"}),
              ("lit", {"zh": "礦棉吸音板（Acoustic Ceiling）", "en": "Acoustic ceiling", "ja": "吸音天井",
                       "ko": "흡음 천장", "es": "Techo acústico"}),
              {"zh": "AC-01 後接「壓克力／燈片」＝壓克力；出現在天花圖＝礦棉吸音板。",
               "en": "If AC-01 is followed by acrylic or diffuser, it is acrylic; in ceiling plans it means acoustic ceiling.",
               "ja": "AC-01 の後に「壓克力／燈片」なら壓克力、天井図に現れるなら吸音天井。",
               "ko": "AC-01 뒤에 압크릴/조명판이 오면 압크릴, 천장도에 나타나면 흡음 천장.",
               "es": "Si tras AC-01 aparece acrílico o difusor, es acrílico; en planos de techo, techo acústico."}),
        ],
    ),
]
