# -*- coding: utf-8 -*-
"""把新语种内容与新地区合并进 CSV 数据集。

用法：python tools_apply_translations.py
数据源：
  seed_lang_entries.py    条目级翻译（名称/说明/备注 × fr/it/pt/ru）
  seed_lang_i18n.py       界面文案（fr/it/pt/ru）
  seed_region_existing.py 既有 8 个地区的四语资料
  seed_regions_new.py     新增 4 个地区（9 语种）
  本文件内的 CONFLICT_TR / RULE_TR  冲突说明与编号规则的四语翻译
"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed_lang_entries import ENTRY_TR, SHORT_TR
from seed_lang_i18n import I18N_TR
from seed_region_existing import EXISTING_TR
from seed_regions_new import NEW_REGIONS


# 跨分组重复代码的分组限定翻译
GROUP_TR = {
("finish", "PC"): {
    "fr": ("Poudrage", "Application électrostatique de poudre sur profilés aluminium",
           "En conflit avec le sol vinyl (PC) : la légende tranche."),
    "it": ("Verniciatura a polvere", "Verniciatura elettrostatica a polvere su profili in alluminio",
           "In conflitto con il pavimento in vinile (PC): decide la legenda."),
    "pt": ("Pintura em pó", "Aplicação eletrostática de pó em perfis de alumínio",
           "Em conflito com o piso vinílico (PC): a legenda decide."),
    "ru": ("Порошковая окраска", "Электростатическая порошковая окраска алюминиевых профилей",
           "Конфликт с виниловым полом (PC) — решает легенда.")},
("light", "TL"): {
    "fr": ("Projecteur sur rail", "Projecteurs sur rail à 1, 2 ou 3 circuits, avec accessoires de suspension",
           "En conflit avec le carrelage (TL) : la légende tranche."),
    "it": ("Binario", "Binari a 1, 2 o 3 circuiti con accessori di sospensione",
           "In conflitto con la ceramica (TL): decide la legenda."),
    "pt": ("Trilho", "Trilhos de 1, 2 ou 3 circuitos com acessórios de suspensão",
           "Em conflito com o azulejo (TL): a legenda decide."),
    "ru": ("Трековый светильник", "Треки на 1, 2 или 3 цепи с подвесными аксессуарами",
           "Конфликт с плиткой (TL) — решает легенда.")},
("light", "DL"): {
    "fr": ("Downlight", "Encastrés ronds, ≤ Φ50 mm ; certains bureaux créent DS pour les petits diamètres", ""),
    "it": ("Downlight", "Incassati rotondi, ≤ Φ50 mm; alcuni studi prevedono DS per i piccoli diametri", ""),
    "pt": ("Downlight", "Embutidos redondos, ≤ Φ50 mm; alguns escritórios criam DS para pequenos diâmetros", ""),
    "ru": ("Точечный светильник", "Встраиваемые круглые, ≤ Φ50 мм; в некоторых бюро для малых диаметров вводят DS", "")},
("light", "PL"): {
    "fr": ("Suspension", "Luminaires suspendus décoratifs et linéaires",
           "PL peut aussi désigner un panneau lumineux (Panel Light)."),
    "it": ("Sospensione", "Sospensioni decorative e lineari",
           "PL può indicare anche il pannello luminoso (Panel Light)."),
    "pt": ("Pendente", "Luminárias pendentes decorativas e lineares",
           "PL também pode designar o painel de luz (Panel Light)."),
    "ru": ("Подвесной светильник", "Декоративные и линейные подвесные светильники",
           "PL может означать и светодиодный панель (Panel Light).")},
("finish", "CL"): {
    "fr": ("Vernis brillant", "Couche de vernis transparent protectrice",
           "À ne pas confondre avec le plafonnier (CL)."),
    "it": ("Vernice lucida", "Strato protettivo di vernice trasparente",
           "Da non confondere con il plafoniera (CL)."),
    "pt": ("Verniz brilhante", "Camada protetora de verniz transparente",
           "Não confundir com a luminária de teto (CL)."),
    "ru": ("Блестящий лак", "Защитный слой прозрачного лака",
           "Не путать с потолочным светильником (CL).")},
("finish", "FL"): {
    "fr": ("Flammé", "Traitement thermique du granit ( flammé)",
           "À ne pas confondre avec le projecteur (FL)."),
    "it": ("Fiammato", "Trattamento termico del granito (fiammato)",
           "Da non confondere con il floodlight (FL)."),
    "pt": ("Flamado", "Tratamento térmico do granito (flamado)",
           "Não confundir com o floodlight (FL)."),
    "ru": ("Огненная обработка", "Термообработка гранита (огненная)",
           "Не путать с прожектором (FL).")},
}

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
LANGS = ["zh", "en", "ja", "ko", "es", "fr", "it", "pt", "ru"]
NEW = ["fr", "it", "pt", "ru"]
COLLIDE = {"CL", "DL", "FL", "PL", "TL"}  # 跨分组重复代码，需按分组限定
# 跨分组代码中，继续沿用通用译表的分组（其余分组在 GROUP_TR 中单独给出）
COLLIDE_OK = {("light", "CL"), ("light", "FL"), ("mat", "TL"), ("mat", "PL"), ("obj", "DL")}

# ---------------------------------------------------------------- 冲突说明四语
CONFLICT_TR = {
"DL": ("Dans le tableau des matériaux = catégorie ; dans les légendes et références de luminaire = downlight.",
       "Nel quadro dei materiali = categoria; nelle legende e nei codici dei luminaire = downlight.",
       "No quadro de materiais = categoria; nas legendas e referências de luminária = downlight.",
       "В таблице материалов — категория; в легендах и моделях светильников — точечный светильник."),
"SL": ("Selon la présence de paramètres électriques : sur les plans électriques, SL désigne la bande LED ou le spot.",
       "In base alla presenza di parametri elettrici: sui disegni elettrici SL indica la strip LED o lo spot.",
       "Conforme a presença de parâmetros elétricos: nos projetos elétricos, SL designa a fita de LED ou o spot.",
       "По наличию электрических параметров: на электрических чертежах SL — это LED-лента или спот."),
"SF": ("Si SF-01 est suivi de « feuille d'or / feuille d'argent », c'est la catégorie des feuilles métalliques.",
       "Se SF-01 è seguito da « foglia d'oro / foglia d'argento », è la categoria dei foil metallici.",
       "Se SF-01 for seguido de «folha de ouro / folha de prata», é a categoria dos folhados metálicos.",
       "Если после SF-01 идёт «золотая фольга / серебряная фольга» — это категория фольги."),
"SP": ("Dans le tableau des matériaux SP = peinture ; dans les plans électriques, SP = spot.",
       "Nel quadro dei materiali SP = vernice; nei disegni elettrici SP = spot.",
       "No quadro de materiais SP = tinta; nos projetos elétricos SP = spot.",
       "В таблице материалов SP = краска; на электрических чертежах SP = спот."),
"PL": ("Selon la version de la légende (ancienne ou récente) : vérifier systématiquement le présent document.",
       "A seconda della versione della legenda (vecchia o recente): verificare sempre il presente documento.",
       "Conforme a versão da legenda (antiga ou recente): confirme sempre neste documento.",
       "Зависит от версии легенды (старой или новой) — всегда сверяйтесь с настоящей таблицей."),
"CT / TL": ("Deux écritures de la même chose : en choisir une pour l'ensemble et ne pas les mélanger.",
            "Due modi di scrivere la stessa cosa: sceglierne uno per tutto e non mescolarli.",
            "Duas formas de escrever a mesma coisa: escolha uma para todo o conjunto e não as misture.",
            "Две формы записи одного и того же: выберите одну на весь комплект и не смешивайте."),
"AC": ("Si AC-01 est suivi d'« acrylique / diffuseur », c'est de l'acrylique.",
       "Se AC-01 è seguito da « acrilico / diffusore », è acrilico.",
       "Se AC-01 for seguido de «acrílico / difusor», é acrílico.",
       "Если после AC-01 идёт «акрил / рассеиватель» — это акрил."),
"AR": ("Dans les listes FF&E, AR = œuvre d'art ; dans un tableau de matériaux, AR peut désigner la pierre artificielle.",
       "Nelle liste FF&E AR = opera d'arte; in un quadro di materiali AR può valere pietra artificiale.",
       "Nas listas de FF&E AR = obra de arte; num quadro de materiais AR pode designar pedra artificial.",
       "В списках FF&E AR — произведение искусства; в ведомости материалов AR может означать искусственный камень."),
"CU": ("Dans les tableaux de matériaux CU = rideau ; dans un sous-tableau des métaux, CU = cuivre.",
       "Nei quadri dei materiali CU = tenda; in un sotto-quadro dei metalli CU = rame.",
       "Nos quadros de materiais CU = cortina; num subquadro de metais CU = cobre.",
       "В ведомостях материалов CU — шторы; в подразделе металлов CU — медь."),
"MT": ("MT est la catégorie générale ; SS est le code spécifique de l'inox.",
       "MT è la categoria generale; SS è il codice specifico dell'inox.",
       "MT é a categoria geral; SS é o código específico do inox.",
       "MT — общая категория; SS — конкретный код нержавейки."),
"HW": ("Vérifier si le tableau comporte une entrée distincte SW/SAN pour les sanitaires.",
       "Verificare se il quadro prevede una voce separata SW/SAN per i sanitari.",
       "Verificar se o quadro tem uma entrada separada SW/SAN para os sanitários.",
       "Проверьте, есть ли в ведомости отдельная строка SW/SAN на сантехнику."),
"PC": ("Sol = revêtement de sol ; traitement de surface des profilés =.application de poudre.",
       "Pavimento = rivestimento di pavimento; trattamento di superficie dei profili = verniciatura a polvere.",
       "Piso = revestimento de piso; tratamento de superfície dos perfis = pintura em pó.",
       "Пол — покрытие пола; обработка поверхности профилей — порошковая окраска."),
"SS": ("Si SS-01 est suivi de « brossé / miroir », il s'agit de l'inox.",
       "Se SS-01 è seguito da « spazzolato / specchio », si tratta di inox.",
       "Se SS-01 for seguido de «escovado / espelho», trata-se de inox.",
       "Если после SS-01 идёт «шлифованный / зеркальный» — это нержавейка."),
"MC": ("Selon qu'il apparaît ou non parmi les finitions de peinture murale.",
       "A seconda che compaia o meno tra le finiture per pitture murali.",
       "Conforme apareça ou não entre os acabamentos de pintura de parede.",
       "В зависимости от того, указан ли он среди отделки стен краской."),
"SC": ("Sur le plan de plafond = membrane tendue ; sur un élévation = cloisonnement.",
       "Nel disegno del soffitto = membrana elastica; in un prospetto = divisoria.",
       "No desenho do teto = membrana tensionada; num alçado = divisória.",
       "На плане потолка — натяжное полотно; на разрезе — перегородка."),
"WC / WP": ("Synonymes : WC couvre aussi le tissu mural, WP uniquement le papier peint.",
            "Sinonimi: WC comprende anche il rivestimento tessile, WP solo la carta da parati.",
            "Sinônimos: WC inclui o revestimento em tecido, WP apenas o papel de parede.",
            "Синонимы: WC включает и тканевые покрытия, WP — только обои."),
"L": ("Il s'agit d'un code de division dans l'index des plans, pas d'un numéro de matériau.",
       "È un codice di divisione nell'indice dei disegni, non un numero di materiale.",
       "É um código de divisão no índice dos projetos, não um número de material.",
       "Это обозначение раздела в перечне чертежей, а не номер материала."),
}

RULE_TR = {
"R1": (("Deux lettres de code + deux chiffres de série",
        "ST-01, WD-03, DL-07",
        "Numérotation dans l'ordre d'apparition, complété de zéros ; un numéro = un matériau (chaque couleur a son numéro)."),
       ("Due lettere di codice + due cifre di serie",
        "ST-01, WD-03, DL-07",
        "Numerazione secondo l'ordine di comparsa, con zeri; un numero = un materiale (ogni colore ha il suo)."),
       ("Duas letras de código + dois algarismos de série",
        "ST-01, WD-03, DL-07",
        "Numeração pela ordem de aparecimento, completada com zeros; um número = um material (cada cor tem o seu)."),
       ("Две буквы кода + две цифры порядкового номера",
        "ST-01, WD-03, DL-07",
        "Нумерация по порядку появления с дополнением нулями; один номер — один материал (каждый цвет отдельно).")),
"R2": (("Code – numéro – nom du matériau",
        "ST-01 Pierre beige / GL-01 Verre artistique",
        "Méthode de dénomination recommandée par les référentiels BIM et de décoration : correspondance directe avec les composants du modèle."),
       ("Codice – numero – nome del materiale",
        "ST-01 Pietra beige / GL-01 Vetro artistico",
        "Metodo di denominazione raccomandato dai riferimenti BIM e di decorazione: corrispondenza diretta con i componenti del modello."),
       ("Código – número – nome do material",
        "ST-01 Pedra bege / GL-01 Vidro artístico",
        "Método de nomenclatura recomendado pelas normas de BIM e decoração: correspondência direta com os componentes do modelo."),
       ("Код – номер – наименование материала",
        "ST-01 Бежевый камень / GL-01 Художественное стекло",
        "Способ наименования, рекомендованный нормативами по BIM и отделке: прямое соответствие элементам модели.")),
"R3": (("Numéro + spécification + classement au feu + emplacement",
        "WD-01 Placage chêne blanc 0,6 mm Placage naturel B1 Mur du hall",
        "Les cinq éléments d'une ligne de tableau ; le classement au feu suit GB 8624 (A / B1 / B2)."),
       ("Numero + specifica + classe di reazione al fuoco + posizione",
        "WD-01 Impiallacciato di rovere 0,6 mm Impiallacciato naturale B1 Parete del lobby",
        "I cinque elementi di una voce di capitolato; la classe al fuoco segue GB 8624 (A / B1 / B2)."),
       ("Número + especificação + classe de reação ao fogo + localização",
        "WD-01 Revestimento de carvalho 0,6 mm Folheado natural B1 Parede do átrio",
        "Os cinco elementos de uma linha de quadro; a classe ao fogo segue GB 8624 (A / B1 / B2)."),
       ("Номер + спецификация + класс пожарной опасности + местоположение",
        "WD-01 Шпон белого дуба 0,6 мм Натуральный шпон B1 Стена лобби",
        "Пять обязательных элементов строки ведомости; класс пожарной опасности — по GB 8624 (A / B1 / B2).")),
"R4": (("Nouveaux numéros à la suite, numéros retirés non réutilisés",
        "—",
        "En révision, les nouveaux matériaux continuent la série ; les numéros retirés restent vides pour éviter toute confusion entre anciens et nouveaux plans."),
       ("Nuovi numeri in sequenza, numeri annullati non riutilizzati",
        "—",
        "In revisione i nuovi materiali proseguono la serie; i numeri annullati restano vuoti per non confondere i disegni vecchi con i nuovi."),
       ("Novos números em sequência, números revogados não reutilizados",
        "—",
        "Na revisão, os novos materiais continuam a série; os números revogados ficam vazios para não confundir projetos antigos e novos."),
       ("Новые номера продолжают ряд, отменённые номера не переиспользуются",
        "—",
        "При пересмотре новые материалы продолжают ряд; отменённые номера остаются пустыми, чтобы старые и новые чертежи не путались.")),
}


def lookup(group, code, lg):
    """按 分组+代码 取某个语言的 (名称, 说明, 备注)。"""
    key = (group, code)
    if key in GROUP_TR:
        return GROUP_TR[key][lg]
    if code in COLLIDE and key not in COLLIDE_OK:
        return None
    if code in SHORT_TR:
        return SHORT_TR[code][lg]
    if code in ENTRY_TR:
        i = NEW.index(lg)
        t = ENTRY_TR[code]
        return (t[i * 3], t[i * 3 + 1], t[i * 3 + 2])
    return None


# ---------------------------------------------------------------- CSV 读写
def read(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, header, rows):
    with io.open(os.path.join(DATA, name), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    # ---------------- entries：名称 ----------------
    rows = read("entries.csv")
    header = ["code", "group", "full_en"] + ["name_%s" % lg for lg in LANGS]
    for r in rows:
        code, grp_ = r["code"], r["group"]
        for lg in NEW:
            r["name_%s" % lg] = ""
        for lg in NEW:
            tr = lookup(grp_, code, lg)
            r["name_%s" % lg] = tr[0] if tr else ""
    write("entries.csv", header, [[r[c] for c in header] for r in rows])
    print("entries.csv  :", len(rows), "行 ×", len(header), "列")

    # ---------------- entry_text：说明与备注 ----------------
    rows = read("entry_text.csv")
    header = ["group", "code", "lang", "desc", "note"]
    have = {(r["group"], r["code"], r["lang"]) for r in rows}
    for r in rows:
        code, lg, grp_ = r["code"], r["lang"], r["group"]
        if lg not in NEW:
            continue
        tr = lookup(grp_, code, lg)
        if tr:
            r["desc"], r["note"] = tr[1], tr[2]
    for r in list(rows):
        for lg in NEW:
            key = (r["group"], r["code"], lg)
            if key in have:
                continue
            tr = lookup(r["group"], r["code"], lg)
            if not tr:
                continue
            rows.append({"group": r["group"], "code": r["code"], "lang": lg,
                         "desc": tr[1], "note": tr[2]})
            have.add(key)
    write("entry_text.csv", header, [[r[c] for c in header] for r in rows])
    print("entry_text.csv:", len(rows), "行")

    # ---------------- i18n ----------------
    rows = read("i18n.csv")
    header = ["key"] + LANGS
    for r in rows:
        for lg in NEW:
            r[lg] = I18N_TR.get(r["key"], {}).get(lg, "")
    write("i18n.csv", header, [[r[c] for c in header] for r in rows])
    print("i18n.csv     :", len(rows), "行 ×", len(header), "列")

    # ---------------- regions / region_text ----------------
    regions = read("regions.csv")
    rtext = read("region_text.csv")
    have = {r["id"] for r in regions}
    for nr in NEW_REGIONS:
        if nr["id"] not in have:
            regions.append({"id": nr["id"], "flag": nr["flag"],
                            "local_lang": nr["local_lang"], "script": nr["script"]})
        for lg in LANGS:
            label, intro, warn, basis, sources, foot = nr["text"][lg]
            rtext.append({"region_id": nr["id"], "lang": lg, "label": label, "intro": intro,
                          "warn": warn, "basis": basis,
                          "sources": " ; ".join(sources), "foot_src": foot})
    for rid, trs in EXISTING_TR.items():
        for lg in NEW:
            label, intro, warn, basis, sources, foot = trs[lg]
            hit = None
            for r in rtext:
                if r["region_id"] == rid and r["lang"] == lg:
                    hit = r
                    break
            if hit is None:
                hit = {"region_id": rid, "lang": lg, "label": "", "intro": "", "warn": "",
                       "basis": "", "sources": "", "foot_src": ""}
                rtext.append(hit)
            hit["label"], hit["intro"], hit["warn"] = label, intro, warn
            hit["basis"], hit["sources"], hit["foot_src"] = basis, " ; ".join(sources), foot
    write("regions.csv", ["id", "flag", "local_lang", "script"],
          [[r[c] for c in ["id", "flag", "local_lang", "script"]] for r in regions])
    write("region_text.csv", ["region_id", "lang", "label", "intro", "warn", "basis", "sources", "foot_src"],
          [[r[c] for c in ["region_id", "lang", "label", "intro", "warn", "basis", "sources", "foot_src"]]
           for r in rtext])
    print("regions.csv  :", len(regions), "个地区；region_text.csv:", len(rtext), "行")

    # ---------------- 地区代码覆盖 / 特有条目 / 特有冲突 ----------------
    rcodes = read("region_codes.csv")
    rextras = read("region_extras.csv")
    rconf = read("region_conflicts.csv")
    for nr in NEW_REGIONS:
        rid = nr["id"]
        for key, code in nr["codes"].items():
            group, _, base = key.rpartition(":")
            if not group:
                group, base = "", key
            rcodes.append({"region_id": rid, "group": group, "base_code": base, "code": code,
                           "name": nr["names"].get(key, ""), "full": "", "note": ""})
        for e in nr["extras"]:
            rextras.append({"region_id": rid, "code": e["code"], "full": e["full"], "name": e["name"],
                            "desc": e["desc"], "note": e["note"]})
        for c in nr["conflicts"]:
            rconf.append({"region_id": rid, "code": c["code"], "a_text": c["a"], "b_text": c["b"],
                          "howto": c["howto"]})
    write("region_codes.csv", ["region_id", "group", "base_code", "code", "name", "full", "note"],
          [[r[c] for c in ["region_id", "group", "base_code", "code", "name", "full", "note"]] for r in rcodes])
    write("region_extras.csv", ["region_id", "code", "full", "name", "desc", "note"],
          [[r[c] for c in ["region_id", "code", "full", "name", "desc", "note"]] for r in rextras])
    write("region_conflicts.csv", ["region_id", "code", "a_text", "b_text", "howto"],
          [[r[c] for c in ["region_id", "code", "a_text", "b_text", "howto"]] for r in rconf])
    print("region_codes/extras/conflicts:", len(rcodes), len(rextras), len(rconf))

    # ---------------- 冲突说明四语 ----------------
    rows = read("conflict_text.csv")
    have = {(r["code"], r["lang"]) for r in rows}
    for r in rows:
        if r["code"] in CONFLICT_TR:
            for i, lg in enumerate(NEW):
                r[lg] = CONFLICT_TR[r["code"]][i]
    for r in list(rows):
        if r["code"] not in CONFLICT_TR:
            continue
        for i, lg in enumerate(NEW):
            key = (r["code"], lg)
            if key in have:
                continue
            rows.append({"code": r["code"], "lang": lg, "zh": r.get("zh", ""),
                         "en": r.get("en", ""), "ja": r.get("ja", ""),
                         "ko": r.get("ko", ""), "es": r.get("es", ""),
                         lg: CONFLICT_TR[r["code"]][i]})
            have.add(key)
    write("conflict_text.csv", ["code", "lang"] + LANGS,
          [[r["code"], r["lang"]] + [r.get(lg, "") for lg in LANGS] for r in rows])
    print("conflict_text.csv:", len(rows), "行")

    # ---------------- 编号规则四语 ----------------
    rows = read("rule_text.csv")
    have = {(r["rule_id"], r["lang"]) for r in rows}
    for r in rows:
        rid, lg = r["rule_id"], r["lang"]
        if rid in RULE_TR and lg in NEW:
            i = NEW.index(lg)
            title, ex, detail = RULE_TR[rid][i]
            r["title"], r["detail"], r["example"] = title, detail, ex
    for r in list(rows):
        rid = r["rule_id"]
        if rid not in RULE_TR:
            continue
        for i, lg in enumerate(NEW):
            key = (rid, lg)
            if key in have:
                continue
            title, ex, detail = RULE_TR[rid][i]
            rows.append({"rule_id": rid, "lang": lg, "title": title,
                         "detail": detail, "example": ex})
            have.add(key)
    write("rule_text.csv", ["rule_id", "lang", "title", "detail", "example"],
          [[r.get(c, "") for c in ["rule_id", "lang", "title", "detail", "example"]] for r in rows])
    print("rule_text.csv :", len(rows), "行")


if __name__ == "__main__":
    main()
