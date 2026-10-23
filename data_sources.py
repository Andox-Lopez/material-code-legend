# -*- coding: utf-8 -*-
"""各地区的权威资料依据（标准/法规/行业惯例）与页脚资料口径

设计说明
--------
* LOCAL_BASIS：该地区"体系依据"的一句话，接在地区简介之前——回答"这个体系由谁定的"。
* SOURCES：该地区可查证的权威资料清单（标准号、文件名称），页面单独成块展示。
* FOOT_SRC：页脚"资料口径"一句话，按地区改写（原先只有内地那套）。
* 香港/澳门/台湾地区的 zh 字段写成繁体，与 zh_hant.py 的转换结果保持一致。

内容为公开标准与实务惯例的整理，用于出图前核对；实际出图仍以本项目
Material Legend（材料表图例）为唯一准绳。
"""

LOCAL_BASIS = {
    "cn": {
        "zh": "中国内地没有强制的装饰材料代码国标，这套代码体系由各地住建标准、行业协会与设计单位在实务中逐步约定形成。",
        "en": "Mainland China has no mandatory national code for decoration material codes; the system accretes from local housing standards, trade associations and drawing-office practice.",
        "ja": "中国本土には装飾材料コードの強制国標がなく、地域の建設基準・業界団体・設計事務所の实务運用で成り立っている。",
        "ko": "중국 본토에는 장식 재료 코드의 강제 국표가 없고, 지역 건설 기준·업계 단체·설계事务所 실무의 운용으로 형성되었다.",
        "es": "China continental no tiene norma nacional obligatoria de códigos de material de decoración: el sistema se forma por normas locales, asociaciones sectoriales y práctica de los estudios.",
    },
    "hk": {
        "zh": "香港沒有統一的裝飾材料代碼規範，材料表圖例由發展商、總承建商與設計顧問按屋宇署裝修工程指引與消防條例的實務要求自行編製。",
        "en": "Hong Kong has no unified decoration-code standard: material legends are drawn up by developers, main contractors and consultants against the Buildings Department renovation codes and fire-safety ordinances.",
        "ja": "香港には統一された装飾材料コードの規範がなく、材料表図例は開発者・ゼネコン・設計顾问が屋宇署の改修工事指针と消防条例の实务要求に沿って自行作成する。",
        "ko": "홍콩에는 통일된 장식 재료 코드 규범이 없으며, 재료표 범례는 발주사·총承包·설계 컨설턴트가屋宇署의 보수 공사 지침과 화재 안전 조례 실무 요건에 따라 자체 작성한다.",
        "es": "Hong Kong no tiene norma unificada de códigos de decoración: cada promotor, contratista y consultor redacta su leyenda según las directrices de reforma del Buildings Department y las ordenanzas de seguridad contra incendios.",
    },
    "mo": {
        "zh": "澳門的裝飾工程做法以第 85/85/M 號法令《建築技術條例》及市政署規範為技術依據，圖例與材料名稱常中葡雙語並置。",
        "en": "In Macao the technical basis is Decree-Law no. 85/85/M (Building Technical Regulations) together with IAM municipal requirements, and drawings often carry Chinese and Portuguese in parallel.",
        "ja": "マカオの装飾工事は第 85/85/M 号法令「建築技術条例」と市政署の規範を技術的根拠とし、図例と材料名は中国語・ポルトガル語併記が多い。",
        "ko": "마카오의 장식 공사는 제 85/85/M 号法令 「建築技術条例」와市政署 규범을 기술 근거로 삼고, 도예와 재료명은 중국어·포르투갈어가 병기되는 경우가 많다.",
        "es": "En Macao la base técnica es el Decreto-LEY n.º 85/85/M (Reglamento Técnico de la Edificación) junto con los requisitos municipales de IAM, y los planos suelen rotular en chino y portugués.",
    },
    "tw": {
        "zh": "台灣地區的材料代碼由建築與室內設計事務所自行訂定，技術依據以內政部建築法規與 CNS 國家標準為準。",
        "en": "In Taiwan, China the codes are set by each architecture and interior practice, with the Ministry of the Interior's building regulations and CNS national standards as the technical basis.",
        "ja": "台湾地区では建築・インテリア事務所が個々に略称を設定し、技術的根拠は内政部の建築法規と CNS 国家標準による。",
        "ko": "대만(중국)에서는 건축·인테리어 사무소가 각자의 코드를 정하며, 기술 근거는 내정부 건축 법규와 CNS 국가 표준이다.",
        "es": "En Taiwán (China) cada estudio de arquitectura e interior fija sus códigos, con los reglamentos de construcción del Ministerio del Interior y las normas CNS como base técnica.",
    },
    "jp": {
        "zh": "日本無統一的裝飾材料代碼國標，圖面多以日文建材名為主、羅馬字縮寫為輔，並廣泛採用 Integrated-CAD（建築 BIM）統一建材記法。",
        "en": "Japan has no national code for decoration materials: drawings lean on Japanese trade names with roman abbreviations as support, and the Integrated-CAD (building BIM) material naming is widely adopted.",
        "ja": "日本には装飾材料コードの国家規範がなく、図面は和文の建材名を主、ローマ字略称を従とする。またIntegrated-CAD（建築 BIM）の建材情報標準化も普及している。",
        "ko": "일본에는 장식 재료 코드의 국가 규범이 없고, 도면은 일본어 시공재 명칭을 중심으로 로마자 약어를 보조적으로 쓰며, Integrated-CAD(건축 BIM)建材 정보 표준화도 널리 쓰인다.",
        "es": "Japón no tiene norma nacional de materiales: los planos usan nombres japoneses de material con abreviaturas romanas de apoyo, y la normalización Integrated-CAD (BIM de construcción) está extendida.",
    },
    "kr": {
        "zh": "韓國無強制的裝飾材料代碼規範，材料表以設計事務所與施工方自訂為主，技術依據為 KS 韓國標準與國家建設標準（KCS/ECS）。",
        "en": "South Korea has no mandatory decoration-code rule: schedules are mostly drawn up by studios and contractors, against KS Korean standards and the national construction standards (KCS/ECS).",
        "ja": "韓国には強制的な装飾材料コードの規範がなく、材料表は設計事務所と施工側の自訂が主で、技術的根拠は KS 韓国標準と国家建設標準（KCS/ECS）。",
        "ko": "한국에는 강제되는 장식 재료 코드 규범이 없어 재료표는 설계사무소와 시공 측의 자체 정의가 중심이며, 기술 근거는 KS 한국 표준과 국가건설기준(KCS/ECS)이다.",
        "es": "Corea del Sur no tiene norma obligatoria de códigos: los cuadros los redactan estudios y contratistas, con las normas KS y los estándares nacionales de construcción (KCS/ECS) como base.",
    },
    "west": {
        "zh": "歐美沒有跨國統一的材料代碼體系，材料表由建築師按項目編寫，主要依據是分區規格書體系（美國 MasterFormat 09、英國 NBS Work Section 05/06、歐洲 Eurocodes 與各國國家標準）。",
        "en": "The West has no cross-border material-code system: schedules are written per project by the architect, drawing on division-based specifications (US MasterFormat 09, UK NBS Work Sections 05/06, European Eurocodes and national standards).",
        "ja": "欧米には国をまたぐ材料コード体系がなく、材料表は建築士が個別に作成する。根拠は区分仕様書体系（米国 MasterFormat 09、英国 NBS Work Section 05/06、欧州 Eurocodes と各国国家标准）。",
        "ko": "서방에는 국경을 넘는 재료 코드 체계가 없어 재료표는 건축사가 프로젝트별로 작성하며, 근거는 구역별 시방서 체계(미국 MasterFormat 09, 영국 NBS Work Section 05/06, 유럽 Eurocodes와 각국 국가 표준)이다.",
        "es": "Occidente no tiene un sistema de códigos transnacional: los cuadros los redacta el arquitecto proyecto a proyecto, con las especificaciones por división (MasterFormat 09 en EE. UU., NBS Work Sections 05/06 en Reino Unido, Eurocodes y normas nacionales en Europa).",
    },
    "latam": {
        "zh": "西班牙與拉丁美洲的裝飾材料代碼多源自各國技術規範與建築製圖傳統（CTE、NBE、NCh），並在顧問公司的材料表（Cuadro de Materiales）中統一。",
        "en": "Codes in Spain and Latin America come mostly from each country's technical rules and drafting tradition (CTE, NBE, NCh), unified inside the consultant's Cuadro de Materiales.",
        "ja": "スペイン語圏のコードは各国の技術規範と製図伝統（CTE、NBE、NCh）に由来し、顾问会社の材料表（Cuadro de Materiales）で統一される。",
        "ko": "스페인어권 코드는 각국의 기술 규범과 도법 전통(CTE, NBE, NCh)에서 나와 컨설턴트의 재료표(Cuadro de Materiales)로 통일된다.",
        "es": "Los códigos en España y Latinoamérica provienen de las normas técnicas y la tradición de dibujo de cada país (CTE, NBE, NCh), unificados en el Cuadro de Materiales del consultor.",
    },
    "mena": {
        "zh": "中東與東南亞沒有本地國標，實務以總包／顧問圖例與送審（Submittal）制度為主，技術依據參照海灣通用規範與新加坡、迪拜的本地法規。",
        "en": "The Middle East and Southeast Asia have no local standard: practice runs on consultant and contractor legends plus the submittal regime, technically referring to the GCC codes and the Singapore/Dubai regulations.",
        "ja": "中東・東南アジアには本地国標がなく、実務はゼネコン／顾问の図例と送審制度が主で、技術的根拠は GCC 共通規範とシンガポール・ドバイの法規を参照する。",
        "ko": "중동·동남아에는本地 국표가 없어 실무는 총承包·컨설턴트 범례와 승인(Submittal) 제도가 중심이며, 기술 근거는 GCC 공통 규범과 싱가포르·두바이 규정을 참조한다.",
        "es": "Oriente Medio y el Sudeste Asiático no tienen norma local: la práctica se apoya en las leyendas de consultor y contratista y en el régimen de aprobaciones, remitiendo a los códigos del GCC y a los reglamentos de Singapur y Dubái.",
    },
}

SOURCES = {
    "cn": {
        "zh": [
            "《居住建筑室内装饰装修工程建筑信息模型设计交付标准》（深圳）表 4.2.4 装饰材料代码表",
            "GB/T 50325《住宅装饰装修工程施工规范》",
            "GB 50210《建筑装饰装修工程质量验收标准》",
            "粤建质〔2009〕41号《住宅室内装饰装修工程质量验收规范》（广东省）",
            "JGJ/T 331《建筑室内装饰装修工程制图标准》；GB 8624《建筑材料及制品燃烧性能分级》",
        ],
        "en": [
            "Shenzhen BIM Delivery Standard for Residential Interior Fit-out, Table 4.2.4 — Finish Material Codes",
            "GB/T 50325 Code for Construction of Residential Interior Decoration",
            "GB 50210 Acceptance Standard for Quality of Architectural Decoration and Construction",
            "Guangdong Notice 粤建质〔2009〕41号 — Quality Acceptance of Residential Interior Decoration",
            "JGJ/T 331 Standard for Architectural Interior Decoration Drawing; GB 8624 Classification of Combustion Performance of Building Materials",
        ],
        "ja": [
            "深圳「居住建築室内装飾装修工程建築情報モデル設計交付標準」表 4.2.4 装飾材料コード表",
            "GB/T 50325《住宅装飾装修工程施工規範》",
            "GB 50210《建築装飾装修工程質量驗收標準》",
            "粤建质〔2009〕41号《住宅室内装飾装修工程質量驗收規範》（広東省）",
            "JGJ/T 331《建築室内装飾装修工程製図標準》；GB 8624《建築材料及び製品の燃焼性能分级》",
        ],
        "ko": [
            "선전시 「주거 건축 실내 장식 샹싱 건축정보모델 설계납품표준」 표 4.2.4 장식 재료 코드표",
            "GB/T 50325 주거 실내 장식装修공사 시공규범",
            "GB 50210 건축 장식装修工程质量 검수표준",
            "粤建质〔2009〕41号 주거 실내 장식装修工程质量 검수규범(광동성)",
            "JGJ/T 331 건축 실내 장식装修제도표준; GB 8624 건축 재료 및 제품 연소 성능 등급",
        ],
        "es": [
            "Norma de entrega BIM de decoración de interiores residenciales (Shenzhen), tabla 4.2.4 — códigos de material de acabado",
            "GB/T 50325 Norma para la ejecución de trabajos de decoración interior residencial",
            "GB 50210 Norma de aceptación de calidad de decoración arquitectónica y construcción",
            "Aviso de Guangdong 粤建质〔2009〕41号 — aceptación de calidad de decoración interior residencial",
            "JGJ/T 331 Norma de dibujo de decoración interior de arquitectura; GB 8624 Clasificación del comportamiento al fuego de materiales de construcción",
        ],
    },
    "hk": {
        "zh": [
            "屋宇署《住宅装修工程指引》（Code of Practice for Renovation of Residential Premises）",
            "屋宇署《办公室装修工程实务指引》（Code of Practice for Office Renovation）",
            "《消防安全（商业处所）规例》（Cap. 502F）及《防火（处所）规例》",
            "BS EN 14411《陶瓷砖——定义、规格与标记》、BS 8300《住宅装修工程实务与性能》",
            "香港测量师学会与香港室内设计协会的图则及材料表惯例（粤语术语：亞加力、傢俬、地膠、膠片、髮紋）",
        ],
        "en": [
            "Buildings Department — Code of Practice for Renovation of Residential Premises",
            "Buildings Department — Code of Practice for Office Renovation",
            "Fire Safety (Commercial Premises) Ordinance (Cap. 502F) and Fire Safety (Places) Regulations",
            "BS EN 14411 Ceramic tiles — Definitions, specifications and marking; BS 8300 Code of practice for renovation of residential dwellings",
            "Common practice of HK surveyors' and HKIDA drawing offices (Cantonese terms: 亞加力 acrylic, 傢俬 furniture, 地膠 vinyl, 膠片 diffuser, 髮紋 hairline)",
        ],
        "ja": [
            "屋宇署《住宅改装工事指针》（Code of Practice for Renovation of Residential Premises）",
            "屋宇署《事务室改装工事实务指针》（Code of Practice for Office Renovation）",
            "《火災安全（商業場所）規例》（Cap. 502F）、《火災安全（場所）規例》",
            "BS EN 14411《セラミックタイル―定義・規格・表示》、BS 8300《住宅改装工事の实务と性能》",
            "香港測量師学会と香港インテリアデザイン協会、図則・材料表の慣行（広東語用語：亞加力、傢俬、地膠、膠片、髮紋）",
        ],
        "ko": [
            "屋宇署 《주거裝修工事 지침》(Code of Practice for Renovation of Residential Premises)",
            "屋宇署 《업소裝修工事 실무지침》(Code of Practice for Office Renovation)",
            "《화재안전(상업적 장소) 조례》(Cap. 502F) 및 《소방(장소) 규칙》",
            "BS EN 14411 세라믹 타일 — 정의·규격·표시, BS 8300 주거 개축 공사 실무와 성능",
            "홍콩 측량사 학회와 HKIDA의 도면·재료표 관행(광둥어 용어: 亞加力, 傢俬, 地膠, 膠片, 髮紋)",
        ],
        "es": [
            "Buildings Department — Código de práctica para reforma de viviendas",
            "Buildings Department — Código de práctica para reforma de locales de oficina",
            "Ordenanza de Seguridad contra Incendios (Locales Comerciales) Cap. 502F y Reglamentos de Seguridad contra Incendios (Recintos de Stromidad)",
            "BS EN 14411 Baldosas cerámicas — Definiciones, especificaciones y marcado; BS 8300 Código de práctica para reforma de viviendas",
            "Práctica habitual de los estudios de Hong Kong (topógrafos) y HKIDA, con términos de Cantón: 亞加力 acrílico, 傢俬 mobiliario, 地膠 vinilo, 膠片 difusor, 髮紋 cepillado",
        ],
    },
    "mo": {
        "zh": [
            "第 85/85/M 号法令《建筑技术条例》（Decreto-Lei n.º 85/85/M）",
            "第 8/2005 号法律《城市规划与土地使用法》",
            "澳门市政署（IAM）工程规范与验收要求",
            "中葡双语材料表惯例（材料名称附葡语，承港式做法）",
        ],
        "en": [
            "Decreto-Lei n.º 85/85/M — Regulamento Técnico de la Edificação",
            "Lei n.º 8/2005 — Lei do Ordenamento Territorial e do Uso do Solo",
            "Instituto para os Assuntos Municipais (IAM) — requisitos de execução e aceitação",
            "Practice of bilingual (Chinese–Portuguese) material schedules, with Cantonese-influenced conventions",
        ],
        "ja": [
            "第 85/85/M 号法令《建築技術条例》（Decreto-Lei n.º 85/85/M）",
            "第 8/2005 号法律《都市計画及土地使用法》",
            "市政署（IAM）工事規範及驗收要求",
            "中国語・ポルトガル語併記の材料表の慣行（広東語的な慣習を含む）",
        ],
        "ko": [
            "제 85/85/M 号法令 「建築技術条例」(Decreto-Lei n.º 85/85/M)",
            "제 8/2005 号法律 「都市計劃 및 토지사용법」",
            "市政署(IAM) 공사 규범 및 검사 요구사항",
            "중국어·포르투갈어 병기 재료표 관행(광둥어 영향 관행 포함)",
        ],
        "es": [
            "Decreto-Ley n.º 85/85/M — Reglamento Técnico de la Edificación",
            "Ley n.º 8/2005 — Ley del Ordenamiento Territorial y Uso del Suelo",
            "Instituto para los AsuntosMunicipais (IAM) — requisitos de ejecución y recepción",
            "Práctica de cuadros de materiales bilingües (chino-portugués), con influencia de las convenciones de Cantón",
        ],
    },
    "tw": {
        "zh": [
            "內政部《建築技術規則》",
            "內政部《建築物室內設計與裝修規範》",
            "CNS 國家標準：CNS 1527《陶瓷磚》、CNS 6475《塑膠地板》、CNS 4299《玻璃》相關標準",
            "台灣室內設計協會與建材廠商的材料表格式慣例（美耐板、系統櫥櫃、輕鋼龍骨等）",
        ],
        "en": [
            "Ministry of the Interior — Code for Construction Standards (建築技術規則)",
            "Ministry of the Interior — Code Governing Interior Design and Decoration of Buildings",
            "CNS national standards: CNS 1527 Ceramic tiles, CNS 6475 Plastic floor coverings, CNS 4299 Glass",
            "Practice of Taiwan interior design associations and material suppliers (美耐板 compact laminate, 系統櫥櫃 fitted joinery, 輕鋼龍骨 light-gauge steel studs)",
        ],
        "ja": [
            "内政部《建築技術規則》",
            "内政部《建築物室內設計與裝修規範》",
            "CNS 国家標準：CNS 1527《セラミックタイル》、CNS 6475《プラスチック床材》、CNS 4299《ガラス》",
            "台湾のインテリアデザイン協会と建材メーカーの材料表の慣行（美耐板、系統櫥櫃、輕鋼龍骨など）",
        ],
        "ko": [
            "내정부 《建築技術規則》",
            "내정부 《建築物室內設計與裝修規範》",
            "CNS 국가 표준: CNS 1527 세라믹 타일, CNS 6475 플라스틱 바닥재, CNS 4299 유리",
            "대만(중국) 인테리어 디자인 협회와 자재 업체의 재료표 관행(美耐板, 系統櫥櫃, 輕鋼龍骨 등)",
        ],
        "es": [
            "Ministerio del Interior — Código de estándares de construcción (建築技術規則)",
            "Ministerio del Interior — Norma de diseño interior y decoración de edificios",
            "Normas nacionales CNS: CNS 1527 Baldosas cerámicas, CNS 6475 Revestimientos de suelo plásticos, CNS 4299 Vidrio",
            "Práctica de las asociaciones de diseño interior y proveedores de materiales (美耐板 compacto, 系統櫥櫃 carpintería a medida, 輕鋼龍骨 perfiles de acero ligero)",
        ],
    },
    "jp": {
        "zh": [
            "JIS A 5905《内装用合成树脂板及塑胶地板》、JIS A 5908",
            "国土交通省「住宅性能表示制度」与《建筑基准法》相关告示",
            "Integrated-CAD（建筑 BIM 推进会议）建材信息标准化：同一建材在各专业图纸上的记法统一",
            "日本建筑学会 標準設計書（JASS）与《建筑施工标准图》",
        ],
        "en": [
            "JIS A 5905 Decorative polymer boards and PVC floor sheets for interior use; JIS A 5908",
            "MLIT — Housing Performance Indicator System and Building Standards Act notifications",
            "Integrated-CAD (building BIM council) — standardisation of material information so the same product is named alike across disciplines",
            "Architectural Institute of Japan — Standard Design Documents (JASS) and Architectural Construction Standard Drawings",
        ],
        "ja": [
            "JIS A 5905《内装用合成樹脂ボード・塩ビシート》、JIS A 5908",
            "国土交通省「住宅性能表示制度」及び《建築基準法》関連告示",
            "Integrated-CAD（建築 BIM 推進会議）建材情報の標準化：同じ建材を各専門図で同じ呼び方にする",
            "日本建築学会 標準設計書（JASS）、建築施工標準図",
        ],
        "ko": [
            "JIS A 5905 내장용 합성수지 보드·염비 시트, JIS A 5908",
            "국토교통부 「주택성능 표시제도」 및 「건축기준법」 관련 고시",
            "Integrated-CAD(건축 BIM 추진 회의)建材 정보 표준화: 동일 부재를 전공 도면에서 동일하게 표기",
            "일본건축학회 표준 설계서(JASS)와 건축 시공 표준도",
        ],
        "es": [
            "JIS A 5905 Tableros decorativos de polímero y pavimentos de PVC para interior; JIS A 5908",
            "MLIT — Sistema de Indicadores de Rendimiento de la Vivienda y notificaciones de la Ley de Estándares de Construcción",
            "Integrated-CAD (consejo de BIM de construcción) — normalización de la información de materiales para nombrar igual el mismo producto en todas las specialties",
            "Architectural Institute of Japan — Documentos de Diseño Estándar (JASS) y planos estándar de construcción",
        ],
    },
    "kr": {
        "zh": [
            "KS 韩国产业标准：KS F 2271《建筑材料试验方法》、KS M 3802《弹性地板》、KS F 3200《地板材料》",
            "KCS / ECS《建筑工事标准规格书》（国家建设标准中心）",
            "国土交通部《建筑标准规范》建筑工事篇（内线/配管/精装各章）",
            "韩国室内建筑学会与施工企业的材料表惯例（以英文缩写为主，辅以韩文材料名）",
        ],
        "en": [
            "KS Korean standards: KS F 2271 Test methods for building materials, KS M 3802 Rubber floor coverings, KS F 3200 Floor coverings",
            "KCS / ECS Standard Specifications for Construction Works (National Construction Standards Center)",
            "MOLIT Building Code — construction chapters (interior, electrical, plumbing)",
            "Practice of Korean interior institutes and contractors: English abbreviations with Korean material names alongside",
        ],
        "ja": [
            "KS 韓国産業標準：KS F 2271《建築材料試験方法》、KS M 3802《弾性床材》、KS F 3200《床材》",
            "KCS / ECS《建築工事標準仕様書》（国家建設基準センター）",
            "国土交通部《建築基準規範》建築工事編（内装・電気・配管）",
            "韓国のインテリア建築学会と施工企業の材料表の慣行（英字略称を主とし、韩文材料名を併記）",
        ],
        "ko": [
            "KS 한국 산업표준: KS F 2271 건축 재료 시험방법, KS M 3802 탄성 바닥재, KS F 3200 바닥재",
            "KCS / ECS 「건축공사 표준시방서」(국가건설기준센터)",
            "국토교통부 「건축기준규범」 건축공사 편(내장·전기·배관)",
            "한국 인테리어 건축학회와施工企业의 재료표 관행(영문 약어를 중심으로 한글 재료명을 병기)",
        ],
        "es": [
            "Normas coreanas KS: KS F 2271 Métodos de ensayo de materiales de construcción, KS M 3802 Revestimientos de suelo elásticos, KS F 3200 Revestimientos de suelo",
            "KCS / ECS Especificaciones Estándar de Obras (Centro Nacional de Estándares de Construcción)",
            "MOLIT Código de Construcción — capítulos de ejecución (interiores, electricidad, fontanería)",
            "Práctica de los institutos de arquitectura de interiores y contratistas coreanos: abreviaturas en inglés con nombres de material en coreano",
        ],
    },
    "west": {
        "zh": [
            "美国：CSI MasterFormat（09 22 00 石材、09 63 00 木饰面、09 96 00 特殊表面处理）与 ASTM / AWI 产品标准",
            "英国：NBS Source Work Section 05、06 与 BS 8300、BS EN 14411",
            "欧洲：EN 1991–1995 Eurocodes、DIN 18202《干式内墙》、EN 12004《瓷砖粘结剂》",
            "建筑师自订的 Finish Schedule 与产品样板（Cut Sheet）惯例（美国缩写较长且项目自定）",
        ],
        "en": [
            "United States: CSI MasterFormat (09 22 00 Stone, 09 63 00 Wood Trim, 09 96 00 Special Finishes) plus ASTM and AWI product standards",
            "United Kingdom: NBS Source Work Sections 05 and 06, with BS 8300 and BS EN 14411",
            "Europe: EN 1991–1995 Eurocodes, DIN 18202 Drylining, EN 12004 Adhesives for tiling",
            "Practice of the architect's own Finish Schedule and product cut sheets (US abbreviations are longer and project-specific)",
        ],
        "ja": [
            "米国：CSI MasterFormat（09 22 00 Stone、09 63 00 Wood Trim、09 96 00 Special Finishes）と ASTM / AWI 製品規格",
            "英国：NBS Source Work Section 05、06、および BS 8300、BS EN 14411",
            "欧州：EN 1991–1995 Eurocodes、DIN 18202《乾式内装》、EN 12004《タイル用接着剤》",
            "建築士が自ら定める Finish Schedule と製品カットシートの慣行（米国の略称は長くプロジェクトごと）",
        ],
        "ko": [
            "미국: CSI MasterFormat(09 22 00 Stone, 09 63 00 Wood Trim, 09 96 00 Special Finishes)와 ASTM/AWI 제품 표준",
            "영국: NBS Source Work Section 05, 06 및 BS 8300, BS EN 14411",
            "유럽: EN 1991–1995 Eurocodes, DIN 18202 건식 내장, EN 12004 타일용 접착제",
            "건축사가 스스로 정하는 Finish Schedule과 제품 카트시트 관행(미국 약어는 길고 프로젝트별)",
        ],
        "es": [
            "Estados Unidos: CSI MasterFormat (09 22 00 Stone, 09 63 00 Wood Trim, 09 96 00 Special Finishes) y normas de producto ASTM y AWI",
            "Reino Unido: NBS Source Work Sections 05 y 06, con BS 8300 y BS EN 14411",
            "Europa: Eurocodes EN 1991–1995, DIN 18202 Tabiquería en seco, EN 12004 Adhesivos para baldosas",
            "Práctica del Finish Schedule del arquitecto y de las hojas de producto (cut sheets): en EE. UU. las abreviaturas son largas y propias de cada proyecto",
        ],
    },
    "latam": {
        "zh": [
            "西班牙 CTE《建筑技术规范》（CTE DB-SI 消防、DB-HS 卫生、DB-HR 声学）",
            "墨西哥 NBE《基本建筑规范》、智利 NCh 系列标准",
            "UNE（西班牙）/ NMX（墨西哥）产品标准系列",
            "Cuadro de Materiales / Leyenda de acabados 的编制惯例：多以石材、瓷砖、涂装三大类缩写起头（如 PIED／MAR／CT／PINT）",
        ],
        "en": [
            "Spain: CTE Código Técnico de la Edificación (DB-SI fire, DB-HS health, DB-HR acoustics)",
            "Mexico: NBE Normas Básicas de Edificación; Chile: NCh standards",
            "UNE (Spain) / NMX (Mexico) product standard series",
            "Practice of the Cuadro de Materiales / leyenda de acabados: usually headed by three families — stone, tile and paint (e.g. PIED / MAR / CT / PINT)",
        ],
        "ja": [
            "スペイン：CTE《建築技術規範》（DB-SI 火災、DB-HS 衛生、DB-HR 音響）",
            "メキシコ：NBE《基本建築規範》、チリ：NCh 規格",
            "UNE（スペイン）/ NMX（メキシコ）製品規格シリーズ",
            "Cuadro de Materiales / leyenda de acabados の慣行：石材・タイル・塗装の三大分類で始めることが多い（PIED／MAR／CT／PINT など）",
        ],
        "ko": [
            "스페인: CTE 「건축기술규범」(DB-SI 소방, DB-HS 위생, DB-HR 음향)",
            "멕시코: NBE 「기본건축규범\", 칠레: NCh 표준",
            "UNE(스페인)/NMX(멕시코) 제품 표준 시리즈",
            "Cuadro de Materiales / leyenda de acabados 관행: 석재·타일·도장 세大类으로 시작하는 경우가 많다(PIED／MAR／CT／PINT 등)",
        ],
        "es": [
            "España: CTE Código Técnico de la Edificación (DB-SI incendio, DB-HS salud, DB-HR acústica)",
            "México: NBE Normas Básicas de Edificación; Chile: normas NCh",
            "Series de producto UNE (España) y NMX (México)",
            "Práctica del Cuadro de Materiales: suele organizarse por las familias piedra, baldosa y pintura (p. ej. PIED / MAR / CT / PINT)",
        ],
    },
    "mena": {
        "zh": [
            "沙特 SBC《沙特建筑规范》、GCC 海湾通用规范（ESMA / GSO）",
            "迪拜 Municipality《Manual of Building Regulations》、阿布扎比 Estidama 绿色建筑评级体系",
            "新加坡 BCA《Code on Accessibility》与 SS 563《消防安全》、MS ISO 系列",
            "Submittal（送审）标注惯例：TBC 待确认、TBA 待定、MOQ 起订量、GP 通用产品、MFG 矿棉天花",
        ],
        "en": [
            "Saudi Building Code (SBC); GCC general codes (ESMA / GSO)",
            "Dubai Municipality Manual of Building Regulations; Abu Dhabi Estidama Pearl Rating System",
            "Singapore BCA Code on Accessibility and SS 563 Code of Practice for Fire Safety; MS ISO series",
            "Submittal notation in practice: TBC to be confirmed, TBA to be advised, MOQ minimum order quantity, GP general purpose, MFG mineral-fibre grid",
        ],
        "ja": [
            "サウジ・ビルディングコード（SBC）、GCC 共通規範（ESMA / GSO）",
            "ドバイ Municipality《Manual of Building Regulations》、アブダビ Estidama 評価制度",
            "シンガポール BCA《Code on Accessibility》と SS 563《火災安全》、MS ISO シリーズ",
            "送審（Submittal）での注記慣行：TBC 要確認、TBA 別途通知、MOQ 最低発注数量、GP 一般品、MFG 鉱維系天井",
        ],
        "ko": [
            "사우디 건축코드(SBC), GCC 공통 규범(ESMA/GSO)",
            "두바이 Municipality 「Manual of Building Regulations», 아부다비 Estidama 등급 체계",
            "싱가포르 BCA 「Code on Accessibility」와 SS 563 「소방안전」, MS ISO 시리즈",
            "Submittal 표기 관행: TBC 확인 필요, TBA 별도 통보, MOQ 최소 발주량, GP 일반 제품, MFG 미네랄 파이버 천장",
        ],
        "es": [
            "Saudi Building Code (SBC); códigos generales del GCC (ESMA / GSO)",
            "Manual of Building Regulations de Dubai Municipality; sistema de pearls Estidama de Abu Dhabi",
            "Code on Accessibility de BCA de Singapur y SS 563 Código de Práctica para la Seguridad contra Incendios; serie MS ISO",
            "Notación habitual en los submittals: TBC por confirmar, TBA pendiente de advise, MOQ cantidad mínima, GP producto genérico, MFG techo de fibra mineral",
        ],
    },
}

FOOT_SRC = {
    "cn": {
        "zh": "资料口径：基准取自深圳《居住建筑室内装饰装修工程建筑信息模型设计交付标准》表 4.2.4，并参照 GB/T 50325、GB 50210、粤建质〔2009〕41号、JGJ/T 331、GB 8624 等国内规范与多地精装施工图实例整理。",
        "en": "Sources: Table 4.2.4 of the Shenzhen BIM delivery standard, read with GB/T 50325, GB 50210, Guangdong Notice 〔2009〕41号, JGJ/T 331 and GB 8624, plus material schedules from fit-out drawings nationwide.",
        "ja": "資料の口径：深圳「居住建築室内装飾装修工程建築情報モデル設計交付標準」表 4.2.4 を基準とし、GB/T 50325、GB 50210、粤建质〔2009〕41号、JGJ/T 331、GB 8624 等の国内規範と各地域の施工図事例から整理。",
        "ko": "자료 근거: 선전시 「주거 건축 실내 장식 샹싱 건축정보모델 설계납품표준」 표 4.2.4 를 기준으로 GB/T 50325, GB 50210, 粤建质〔2009〕41号, JGJ/T 331, GB 8624 등 국내 규범과 각지施工도 사례를 정리했다.",
        "es": "Fuentes: tabla 4.2.4 de la norma de entrega BIM de Shenzhen, junto con GB/T 50325, GB 50210, el aviso de Guangdong 〔2009〕41号, JGJ/T 331 y GB 8624, y cuadros de materiales de planos de decoración de distintas ciudades.",
    },
    "hk": {
        "zh": "資料口徑：按屋宇署《住宅裝修工程指引》《辦公室裝修工程實務指引》、Cap. 502F《消防安全（商業處所）規例》，以及 BS EN 14411、BS 8300 等英式標準與港式材料表慣例整理。",
        "en": "Sources: the Buildings Department renovation codes (residential and office), the Fire Safety (Commercial Premises) Ordinance Cap. 502F, plus BS EN 14411, BS 8300 and common HK schedule practice.",
        "ja": "資料の口径：屋宇署《住宅改装工事指针》《事務室改装工事实务指针》、Cap. 502F《火災安全（商業場所）規例》、および BS EN 14411、BS 8300 等の英式標準と香港の材料表慣行に基づき整理。",
        "ko": "자료 근거:屋宇署 《주거裝修工事 지침》《업소裝修工事 실무지침》, Cap. 502F 「화재안전(상업적 장소) 조례」, 그리고 BS EN 14411, BS 8300 등 영식 표준과홍콩식 재료표 관행에 따라 정리했다.",
        "es": "Fuentes: las directrices de reforma del Buildings Department (residencial y oficinas), la Ordenanza de Seguridad contra Incendios Cap. 502F, además de BS EN 14411, BS 8300 y la práctica habitual de Hong Kong.",
    },
    "mo": {
        "zh": "資料口徑：按第 85/85/M 號法令《建築技術條例》、第 8/2005 號法律《都市規劃及土地使用法》與市政署工程規範，並按中葡雙語材料表慣例整理。",
        "en": "Sources: Decree-Law 85/85/M on Building Technical Regulations, Law 8/2005 on land use, IAM municipal requirements, and bilingual material-schedule practice.",
        "ja": "資料の口径：第 85/85/M 号法令《建築技術条例》、第 8/2005 号法律《都市計画及土地使用法》、市政署の工事規範、および中国語・ポルトガル語併記の材料表慣行に基づき整理。",
        "ko": "자료 근거: 제 85/85/M 号法令 「建築技術条例」, 제 8/2005 号法律 「都市計劃 및 토지사용법」,市政署 공사 규범, 그리고 중 포 병기 재료표 관행에 따라 정리했다.",
        "es": "Fuentes: Decreto-Ley 85/85/M, Ley 8/2005 de uso del suelo, requisitos municipales del IAM y la práctica de cuadros de materiales bilingües.",
    },
    "tw": {
        "zh": "資料口徑：按內政部《建築技術規則》《建築物室內設計與裝修規範》、CNS 1527／6475／4299 等國家標準，並按台灣設計事務所材料表慣例整理。",
        "en": "Sources: the Ministry of the Interior's Building Code and interior-decoration rules, CNS standards (1527, 6475, 4299) and Taiwan practice for material schedules.",
        "ja": "資料の口径：内政部《建築技術規則》《建築物室內設計與裝修規範》、CNS 1527／6475／4299 等の国家標準、および台湾の設計事務所における材料表の慣行に基づき整理。",
        "ko": "자료 근거: 내정부 「建築技術規則」「建築物室內設計與裝修規範」, CNS 1527·6475·4299 등 국가 표준, 그리고 대만(중국) 설계사무소 재료표 관행에 따라 정리했다.",
        "es": "Fuentes: el Código de construcción y la norma de decoración de interiores del Ministerio del Interior, las normas CNS (1527, 6475, 4299) y la práctica de los cuadros de materiales en Taiwán (China).",
    },
    "jp": {
        "zh": "資料口徑：按 JIS A 5905／5908 等日本標準、國土交通省「住宅性能表示制度」與建築基準法告示、Integrated-CAD 建材信息標準化，以及日本建築學會標準設計書（JASS）與建築施工標準圖整理。",
        "en": "Sources: Japanese Standards such as JIS A 5905/5908, MLIT's Housing Performance Indicator System and Building Standards Act notices, Integrated-CAD material-information standardisation, and the AIJ Standard Design Documents (JASS).",
        "ja": "資料の口径：JIS A 5905／5908 等の日本標準、国土交通省「住宅性能表示制度」及び建築基準法の告示、Integrated-CAD の建材情報標準化、日本建築学会の標準設計書（JASS）と建築施工標準図に基づき整理。",
        "ko": "자료 근거: JIS A 5905·5908 등 일본 표준, 국토교통부 「주택성능 표시제도」와 건축기준법 고시, Integrated-CAD 建材 정보 표준화, 일본건축학회 표준 설계서(JASS)와 건축 시공 표준도에 따라 정리했다.",
        "es": "Fuentes: normas japonesas como JIS A 5905/5908, el Sistema de Indicadores de Rendimiento de la Vivienda del MLIT y sus notificaciones, la normalización Integrated-CAD y los Documentos de Diseño Estándar (JASS) del AIJ.",
    },
    "kr": {
        "zh": "資料口徑：按 KS 韓國產業標準（KS F 2271、KS M 3802、KS F 3200）、KCS／ECS《建築工事標準規格書》、國土交通部《建築標準規範》，以及韓國設計事務所與施工方材料表慣例整理。",
        "en": "Sources: KS Korean standards (KS F 2271, KS M 3802, KS F 3200), the KCS/ECS Standard Specifications for Construction Works, the MOLIT Building Code and Korean studio/contractor schedule practice.",
        "ja": "資料の口径：KS 韓国産業標準（KS F 2271、KS M 3802、KS F 3200）、KCS／ECS《建築工事標準仕様書》、国土交通部《建築基準規範》、および韓国の設計事務所・施工側の材料表慣行に基づき整理。",
        "ko": "자료 근거: KS 한국 산업표준(KS F 2271, KS M 3802, KS F 3200), KCS·ECS 「건축공사 표준시방서」, 국토교통부 「건축기준규범」, 그리고 한국 설계사무소·시공 측 재료표 관행에 따라 정리했다.",
        "es": "Fuentes: normas coreanas KS (KS F 2271, KS M 3802, KS F 3200), las Especificaciones Estándar KCS/ECS, el Código de Construcción del MOLIT y la práctica coreana de cuadros de materiales.",
    },
    "west": {
        "zh": "資料口徑：按美國 CSI MasterFormat（09 章）與 ASTM／AWI 標準、英國 NBS Source Work Section 05／06 與 BS 8300、BS EN 14411，以及歐洲 Eurocodes、DIN 18202、EN 12004，並結合建築師自訂 Finish Schedule 的慣例整理。",
        "en": "Sources: US CSI MasterFormat division 09 with ASTM/AWI standards, UK NBS Source Work Sections 05/06 with BS 8300 and BS EN 14411, European Eurocodes, DIN 18202 and EN 12004, plus the architect's own Finish Schedule practice.",
        "ja": "資料の口径：米国 CSI MasterFormat 第 09 章と ASTM／AWI 標準、英国 NBS Source Work Section 05／06 と BS 8300、BS EN 14411、欧州 Eurocodes、DIN 18202、EN 12004、および建築士自訂の Finish Schedule の慣行に基づき整理。",
        "ko": "자료 근거: 미국 CSI MasterFormat 09 장과 ASTM·AWI 표준, 영국 NBS Source Work Section 05·06과 BS 8300·BS EN 14411, 유럽 Eurocodes·DIN 18202·EN 12004, 그리고 건축사 자체 Finish Schedule 관행에 따라 정리했다.",
        "es": "Fuentes: CSI MasterFormat división 09 con normas ASTM/AWI, NBS Source Work Sections 05/06 con BS 8300 y BS EN 14411, Eurocodes, DIN 18202 y EN 12004, más la práctica del Finish Schedule del arquitecto.",
    },
    "latam": {
        "zh": "資料口徑：按西班牙 CTE《建築技術規範》、墨西哥 NBE《基本建築規範》、智利 NCh 標準與 UNE／NMX 產品標準系列，並按顧問公司 Cuadro de Materiales 的編製慣例整理。",
        "en": "Sources: the Spanish CTE, Mexico's NBE, Chilean NCh standards, the UNE/NMX product-standard series, and the practice of the consultant's Cuadro de Materiales.",
        "ja": "資料の口径：スペイン CTE《建築技術規範》、メキシコ NBE《基本建築規範》、チリ NCh 標準、UNE／NMX 製品規格シリーズ、および顾问会社の Cuadro de Materiales の作成慣行に基づき整理。",
        "ko": "자료 근거: 스페인 CTE 「건축기술규범」, 멕시코 NBE 「기본건축규범」, 칠레 NCh 표준, UNE·NMX 제품 표준 시리즈, 그리고 컨설턴트 Cuadro de Materiales 작성 관행에 따라 정리했다.",
        "es": "Fuentes: el CTE español, las NBE mexicanas, las normas NCh chilenas, las series UNE/NMX de producto y la práctica de redacción del Cuadro de Materiales del consultor.",
    },
    "mena": {
        "zh": "資料口徑：按沙特 SBC、GCC 通用規範、迪拜 Municipality《Manual of Building Regulations》、阿布扎比 Estidama 體系、新加坡 BCA 與 SS 563，並按 Submittal（送審）制度下的圖例與標註慣例整理。",
        "en": "Sources: the Saudi Building Code, GCC general codes, the Dubai Municipality Manual of Building Regulations, Abu Dhabi's Estidama system, Singapore BCA and SS 563, read together with submittal-stage legend and notation practice.",
        "ja": "資料の口径：サウジ SBC、GCC 共通規範、ドバイ Municipality《Manual of Building Regulations》、アブダビ Estidama、シンガポール BCA と SS 563、および送審段階の図例・注記慣行に基づき整理。",
        "ko": "자료 근거: 사우디 SBC, GCC 공통 규범, 두바이 Municipality 「Manual of Building Regulations」, 아부다비 Estidama, 싱가포르 BCA와 SS 563, 그리고 승인(Submittal) 단계의 범례·표기 관행에 따라 정리했다.",
        "es": "Fuentes: el Saudi Building Code, los códigos del GCC, el Manual of Building Regulations de Dubai, el sistema Estidama de Abu Dhabi, BCA y SS 563 de Singapur, junto con la práctica de leyendas y notación en la etapa de submittal.",
    },
}
