# -*- coding: utf-8 -*-
"""法语 / 意大利语 / 葡萄牙语 / 俄语 的界面文案（供 tools_apply_translations.py 合并进 i18n.csv）"""

I18N_TR = {
"title": {
 "fr": "Code <em>des matériaux · multilingue</em>",
 "it": "<em>Codici</em> dei materiali · multilingue",
 "pt": "<em>Códigos</em> de material · multilíngue",
 "ru": "<em>Коды</em> отделочных материалов · многоязычно"},
"subtitle": {
 "fr": "Abréviation · Nom complet · Nom local · Contenu",
 "it": "Abbreviazione · Nome completo · Nome locale · Contenuto",
 "pt": "Abreviatura · Nome completo · Nome local · Conteúdo",
 "ru": "Сокращение · Полное название · Местное название · Состав"},
"unit": {
 "fr": "entrées", "it": "voci", "pt": "entradas", "ru": "записей"},
"systems": {
 "fr": "catégories", "it": "categorie", "pt": "categorias", "ru": "категорий"},
"domain": {
 "fr": "Décoration intérieure / design d'intérieur · légende des matériaux",
 "it": "Arredamento / interior design · legenda dei materiali",
 "pt": "Decoração de interiores / design de interiores · legenda dos materiais",
 "ru": "Отделка интерьера / дизайн интерьера · легенда материалов"},
"note_label": {
 "fr": "À lire d'abord", "it": "Da leggere prima", "pt": "Leia primeiro", "ru": "Сначала прочитайте"},
"src_note": {
 "fr": "La Chine n'a pas de norme nationale obligatoire pour les codes de matériaux. Les codes ci-dessus proviennent du tableau 4.2.4 de la norme de livraison BIM de Shenzhen pour les logements, de tableaux de matériaux relevés sur des plans de décoration dans tout le pays, et des abréviations anglo-chinoises usuelles. Les plans doivent toujours être établis selon la légende des matériaux du projet.",
 "it": "In Cina non esiste una norma nazionale obbligatoria sui codici dei materiali. I codici riportati derivano dalla tabella 4.2.4 della norma di consegna BIM di Shenzhen per gli alloggi, dai quadri dei materiali dei progetti di decorazione e dalle abbreviazioni anglo-cinesi più comuni. I disegni vanno sempre redatti secondo la legenda dei materiali del progetto.",
 "pt": "A China não existe norma nacional obrigatória de códigos de material. Os códigos aqui vem da tabela 4.2.4 da norma de entrega BIM de Shenzhen para habitações, de quadros de materiais de projetos de decoração e das abreviaturas anglo-chinesas mais comuns. Os projetos devem seguir sempre a legenda de materiais do próprio projeto.",
 "ru": "В Китае нет обязательного национального стандарта кодов отделочных материалов. Коды приведены по таблице 4.2.4 стандарта передачи BIM-модели жилых помещений (Шэньчжэнь), по ведомостям материалов из проектов отделки и по распространённым англо-китайским сокращениям. Чертежи всегда выпускают по легенде материалов конкретного проекта."},
"warn_note": {
 "fr": "Un même code peut signifier des choses différentes selon les bureaux d'études et les projets : lisez toujours la légende des matériaux du projet avant de le reprendre.",
 "it": "Lo stesso codice può avere significati diversi da studio a studio e da progetto a progetto: prima di riutilizzarlo, leggere sempre la legenda dei materiali del progetto.",
 "pt": "Um mesmo código pode significar coisas diferentes conforme o escritório e o projeto: leia sempre a legenda de materiais do projeto antes de reaproveitar.",
 "ru": "Один и тот же код может означать разное в разных бюро и проектах: перед переносом всегда читайте легенду материалов конкретного проекта."},
"region_label": {
 "fr": "Région", "it": "Regione", "pt": "Região", "ru": "Регион"},
"region_hint": {
 "fr": "Un même matériau n'est pas abrégé de la même façon dans tous les pays. Changez de région pour voir la convention locale.",
 "it": "Lo stesso materiale non si abbrevia allo stesso modo in ogni paese: cambia regione per vedere la convenzione locale.",
 "pt": "Um mesmo material não é abreviado da mesma forma em todos os países. Troque de região para ver a convenção local.",
 "ru": "Один и тот же материал в разных странах сокращают по-разному: смените регион, чтобы увидеть местные соглашения."},
"region_summary": {
 "fr": "{n} codes ici · {d} différences avec la base · {e} entrées propres à la région",
 "it": "{n} codici qui · {d} differenze dalla base · {e} voci proprie della regione",
 "pt": "{n} códigos aqui · {d} diferenças da base · {e} itens exclusivos da região",
 "ru": "{n} кодов здесь · {d} отличий от базовых · {e} позиций только для региона"},
"g_sources_title": {
 "fr": "Références locales", "it": "Riferimenti locali", "pt": "Referências locais", "ru": "Местные источники"},
"g_sources_sub": {
 "fr": "Normes, réglementations et pratique locales",
 "it": "Norme, regolamentazioni e pratica locali",
 "pt": "Normas, regulamentos e prática locais",
 "ru": "Местные нормы, правила и практика"},
"g_region_title": {
 "fr": "Correspondance de codes par région", "it": "Corrispondenza dei codici per regione",
 "pt": "Correspondência de códigos por região", "ru": "Соответствие кодов по регионам"},
"g_region_sub": {
 "fr": "Code de base → code local", "it": "Codice base → codice locale",
 "pt": "Código base → código local", "ru": "Базовый код → местный код"},
"col_base_code": {
 "fr": "Code de base", "it": "Codice base", "pt": "Código base", "ru": "Базовый код"},
"col_region_code": {
 "fr": "Code local", "it": "Codice locale", "pt": "Código local", "ru": "Местный код"},
"col_region_name": {
 "fr": "Nom local", "it": "Nome locale", "pt": "Nome local", "ru": "Местное название"},
"g_extra_title": {
 "fr": "Éléments propres à la région", "it": "Voci proprie della regione",
 "pt": "Itens exclusivos da região", "ru": "Позиции, характерные для региона"},
"g_extra_sub": {
 "fr": "Matériaux et composants courants ici et ailleurs rares",
 "it": "Materiali e componenti diffusi qui e scarsi altrove",
 "pt": "Materiais e componentes comuns aqui e raros noutros lugares",
 "ru": "Материалы и элементы, обычные здесь и редкие в других регионах"},
"region_badge": {
 "fr": "régional", "it": "regionale", "pt": "regional", "ru": "региональный"},
"tab_extra": {
 "fr": "Exclusifs région", "it": "Solo regione", "pt": "Só região", "ru": "Только регион"},
"region_only_hint": {
 "fr": "Ces codes n'existent que dans la convention de cette région",
 "it": "Questi codici esistono solo nella convenzione di questa regione",
 "pt": "Estes códigos só existem na convenção desta região",
 "ru": "Эти коды существуют только в соглашениях данного региона"},
"tab_all": {
 "fr": "Tout", "it": "Tutto", "pt": "Tudo", "ru": "Все"},
"tab_mat": {
 "fr": "Finitions", "it": "Finiture", "pt": "Acabamentos", "ru": "Отделочные материалы"},
"tab_obj": {
 "fr": "Mobilier & FF&E", "it": "Arredi & FF&E", "pt": "Mobiliário e FF&E", "ru": "Мебель и FF&E"},
"tab_light": {
 "fr": "Types d'éclairage", "it": "Tipi di illuminazione", "pt": "Tipos de iluminação",
 "ru": "Типы освещения"},
"tab_finish": {
 "fr": "Finitions de surface", "it": "Finiture di superficie", "pt": "Acabamentos de superfície",
 "ru": "Отделка поверхностей"},
"tab_conflict": {
 "fr": "Codes ambigus", "it": "Codici ambigui", "pt": "Códigos ambíguos", "ru": "Неоднозначные коды"},
"tab_index": {
 "fr": "Index des codes", "it": "Indice dei codici", "pt": "Índice de códigos", "ru": "Указатель кодов"},
"tab_rules": {
 "fr": "Règles de numérotation", "it": "Regole di numerazione", "pt": "Regras de numeração",
 "ru": "Правила нумерации"},
"g_mat": {
 "fr": "1. Catégories de finitions", "it": "1. Categorie di finitura", "pt": "1. Categorias de acabamentos",
 "ru": "1. Категории отделочных материалов"},
"g_mat_sub": {
 "fr": "Mur / sol / plafond / formes", "it": "Parete / pavimento / soffitto / forme",
 "pt": "Parede / piso / teto / formas", "ru": "Стены / пол / потолок / формы"},
"g_obj": {
 "fr": "2. Équipement et décoration textile", "it": "2. Arredi e soft furnishing",
 "pt": "2. Equipamento e decoração têxtil", "ru": "2. Оборудование и мягкий декор"},
"g_obj_sub": {
 "fr": "Courant dans les listes FF&E", "it": "Comune nelle liste FF&E",
 "pt": "Comum nas listas de FF&E", "ru": "Часто в списках FF&E"},
"g_light": {
 "fr": "3. Codes de types d'éclairage", "it": "3. Codici dei tipi di illuminazione",
 "pt": "3. Códigos de tipos de iluminação", "ru": "3. Коды типов освещения"},
"g_light_sub": {
 "fr": "Plafonds réfléchis et plans d'éclairage", "it": "Plafondi riflessi e planimetrie illuminazione",
 "pt": "Tetos refletores e plantas de iluminação", "ru": "Потолочные планы и планы освещения"},
"g_finish": {
 "fr": "4. Codes de finition de surface", "it": "4. Codici di finitura superficiale",
 "pt": "4. Códigos de acabamento de superfície", "ru": "4. Коды отделки поверхностей"},
"g_finish_sub": {
 "fr": "Après le numéro de matériau, ex. MT-01 H", "it": "Dopo il numero del materiale, es. MT-01 H",
 "pt": "Após o número do material, ex. MT-01 H", "ru": "После номера материала, напр. MT-01 H"},
"g_conflict": {
 "fr": "5. Un code, plusieurs sens — à vérifier", "it": "5. Un codice, più significati — da verificare",
 "pt": "5. Um código, vários sentidos — a verificar", "ru": "5. Один код — несколько значений: проверяйте"},
"g_conflict_sub": {
 "fr": "Les mêmes lettres dans deux systèmes différents", "it": "Le stesse lettere in due sistemi diversi",
 "pt": "As mesmas letras em dois sistemas diferentes", "ru": "Одни и те же буквы в двух разных системах"},
"g_rules": {
 "fr": "6. Règles de numérotation", "it": "6. Regole di numerazione", "pt": "6. Regras de numeração",
 "ru": "6. Правила нумерации"},
"g_rules_sub": {
 "fr": "Comment composer et consigner", "it": "Come comporre e registrare",
 "pt": "Como compor e registrar", "ru": "Как составлять и записывать"},
"g_index": {
 "fr": "Index des codes", "it": "Indice dei codici", "pt": "Índice de códigos", "ru": "Указатель кодов"},
"g_index_sub": {
 "fr": "Code → nom complet en un coup d'œil", "it": "Codice → nome completo a colpo d'occhio",
 "pt": "Código → nome completo num relance", "ru": "Код → полное название сразу"},
"col_code": {
 "fr": "Code", "it": "Codice", "pt": "Código", "ru": "Код"},
"col_full": {
 "fr": "Nom complet (EN)", "it": "Nome completo (EN)", "pt": "Nome completo (EN)", "ru": "Полное название (EN)"},
"col_name": {
 "fr": "Nom", "it": "Nome", "pt": "Nome", "ru": "Название"},
"col_desc": {
 "fr": "Contenu / exemples", "it": "Contenuto / esempi", "pt": "Conteúdo / exemplos", "ru": "Состав / примеры"},
"col_note": {
 "fr": "Remarques", "it": "Note", "pt": "Observações", "ru": "Примечания"},
"col_desc2": {
 "fr": "Description", "it": "Descrizione", "pt": "Descrição", "ru": "Описание"},
"col_a": {
 "fr": "Sens A", "it": "Significato A", "pt": "Sentido A", "ru": "Значение A"},
"col_b": {
 "fr": "Sens B / C", "it": "Significato B / C", "pt": "Sentido B / C", "ru": "Значение B / C"},
"search_ph": {
 "fr": "Rechercher un code, un nom complet ou local — ex. ST / Stone / pierre / acier …",
 "it": "Cerca codice, nome completo o locale — es. ST / Stone / pietra / acciaio …",
 "pt": "Buscar código, nome completo ou local — ex. ST / Stone / pedra / aço …",
 "ru": "Поиск по коду, полному или местному названию — напр. ST / Stone / камень / сталь …"},
"showing": {
 "fr": "Affichage", "it": "Mostrati", "pt": "Exibindo", "ru": "Показано"},
"keyword": {
 "fr": "mot-clé", "it": "parola chiave", "pt": "palavra-chave", "ru": "ключевое слово"},
"no_result": {
 "fr": "Aucun résultat — essayez un autre mot-clé", "it": "Nessun risultato: prova un'altra parola chiave",
 "pt": "Sem resultados — tente outra palavra-chave", "ru": "Ничего не найдено — попробуйте другое слово"},
"reset": {
 "fr": "Effacer", "it": "Cancella", "pt": "Limpar", "ru": "Очистить"},
"copy_hint": {
 "fr": "Cliquez un code pour le copier", "it": "Clicca un codice per copiarlo",
 "pt": "Clique num código para copiar", "ru": "Нажмите на код, чтобы скопировать"},
"copied": {
 "fr": "Copié", "it": "Copiato", "pt": "Copiado", "ru": "Скопировано"},
"lang_label": {
 "fr": "Langue", "it": "Lingua", "pt": "Idioma", "ru": "Язык"},
"languages": {
 "fr": "langues", "it": "lingue", "pt": "idiomas", "ru": "языков"},
"theme_dark": {
 "fr": "Sombre", "it": "Scuro", "pt": "Escuro", "ru": "Тёмная"},
"theme_light": {
 "fr": "Clair", "it": "Chiaro", "pt": "Claro", "ru": "Светлая"},
"print_btn": {
 "fr": "Imprimer / PDF", "it": "Stampa / PDF", "pt": "Imprimir / PDF", "ru": "Печать / PDF"},
"print_title": {
 "fr": "Imprimer / PDF", "it": "Stampa / PDF", "pt": "Imprimir / PDF", "ru": "Печать / PDF"},
"clear_title": {
 "fr": "Effacer le mot-clé", "it": "Cancella la parola chiave", "pt": "Limpar palavra-chave",
 "ru": "Очистить ключевое слово"},
"view_label": {
 "fr": "Vue", "it": "Vista", "pt": "Vista", "ru": "Вид"},
"view_table": {
 "fr": "Tableau", "it": "Tabella", "pt": "Tabela", "ru": "Таблица"},
"view_index": {
 "fr": "Cartes", "it": "Schede", "pt": "Cartões", "ru": "Карточки"},
"expand_all": {
 "fr": "Tout déplier", "it": "Espandi tutto", "pt": "Expandir tudo", "ru": "Развернуть всё"},
"collapse_all": {
 "fr": "Tout replier", "it": "Comprimi tutto", "pt": "Recolher tudo", "ru": "Свернуть всё"},
"shortcut_hint": {
 "fr": "Raccourci : / pour rechercher, Échap pour effacer",
 "it": "Scorciatoia: / per cercare, Esc per cancellare",
 "pt": "Atalho: / para buscar, Esc para limpar", "ru": "Горячие клавиши: / — поиск, Esc — очистка"},
"badge_conflict": {
 "fr": "ambigu", "it": "ambiguo", "pt": "ambíguo", "ru": "конфликт"},
"foot_src": {
 "fr": "Sources : tableau 4.2.4 de la norme de livraison BIM de Shenzhen, lus avec GB/T 50325, GB 50210, l'avis du Guangdong 〔2009〕41号, JGJ/T 331 et GB 8624, plus les tableaux de matériaux relevés sur des plans de décoration dans tout le pays.",
 "it": "Fonti: tabella 4.2.4 della norma di consegna BIM di Shenzhen, con GB/T 50325, GB 50210, l'avviso del Guangdong 〔2009〕41号, JGJ/T 331 e GB 8624, più i quadri dei materiali dei progetti di decorazione.",
 "pt": "Fontes: tabela 4.2.4 da norma de entrega BIM de Shenzhen, com GB/T 50325, GB 50210, o aviso de Guangdong 〔2009〕41号, JGJ/T 331 e GB 8624, além de quadros de materiais de projetos de decoração.",
 "ru": "Источники: таблица 4.2.4 стандарта передачи BIM (Шэньчжэнь), а также GB/T 50325, GB 50210, постановление Гуандуна 〔2009〕41号, JGJ/T 331 и GB 8624, плюс ведомости материалов из проектов отделки."},
"foot_contact": {
 "fr": "Un problème ou une erreur ? Ouvrez une {issue} sur {gh}, ou écrivez à {mail}.",
 "it": "Hai trovato un problema o un errore? Apri una {issue} su {gh} o scrivi a {mail}.",
 "pt": "Encontrou um problema ou erro? Abra uma {issue} no {gh} ou escreva para {mail}.",
 "ru": "Нашли проблему или ошибку? Создайте {issue} на {gh} или напишите на {mail}.",
},
"foot_license": {
 "fr": "Code ouvert sous licence MIT (usage, modification et redistribution libres) · Copyright © 2026 Karandox Lopez",
 "it": "Open source con licenza MIT (uso, modifica e ridistribuzione liberi) · Copyright © 2026 Karandox Lopez",
 "pt": "Código aberto sob licença MIT (uso, modificação e redistribuição livres) · Copyright © 2026 Karandox Lopez",
 "ru": "Открытый код по лицензии MIT (свободное использование, изменение и распространение) · Copyright © 2026 Karandox Lopez"},
"foot_date": {
 "fr": "Dernière mise à jour {date} · fichier unique, utilisable hors ligne, impression A4 avec Ctrl+P",
 "it": "Ultimo aggiornamento {date} · file unico, utilizzabile offline, stampa A4 con Ctrl+P",
 "pt": "Última atualização {date} · arquivo único, funciona offline, impressão A4 com Ctrl+P",
 "ru": "Последнее обновление {date} · один файл, работает офлайн, печать A4 по Ctrl+P"},
"foot_lang": {
 "fr": "Traduit en chinois, anglais, japonais, coréen, espagnol, français, italien, portugais et russe ; les termes techniques conservent l'original anglais pour le recoupement avec les plans.",
 "it": "Tradotto in cinese, inglese, giapponese, coreano, spagnolo, francese, italiano, portoghese e russo; i termini tecnici mantengono l'originale inglese per il confronto con i disegni.",
 "pt": "Traduzido para chinês, inglês, japonês, coreano, espanhol, francês, italiano, português e russo; os termos técnicos mantêm o original em inglês para conferência com os projetos.",
 "ru": "Переведено на китайский, английский, японский, корейский, испанский, французский, итальянский, португальский и русский; технические термины оставлены на английском для сверки с чертежами."},
}
