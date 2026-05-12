# Makefile для сборки документации курсовой работы
# Воробьев Е. А., ИУ5-42Б, вариант №5
#
# Цели:
#   make            — собрать все .docx из .md
#   make pdf        — собрать все .pdf из .docx (требует LibreOffice или Word)
#   make zip        — упаковать комплект для отправки преподавателю
#   make clean      — удалить сборочные артефакты
#   make help       — показать список целей

# ─── Настройки ─────────────────────────────────────────────────────────────

# Префикс/суффикс имён выходных файлов по шаблону кафедры
PREFIX  := КР_СП_ИУ5-42Б_Воробьев_СП_2026
SUFFIX  := .docx

# Шаблон оформления — кастомный reference.docx со стилями ГОСТ:
# Times New Roman 14pt, межстрочный 1.5, поля 30/15/20/20 мм,
# tab leaders для TOC, page-break-before для разделов.
REF_DOC := reference.docx

# Pandoc, LibreOffice и rsvg-convert
PANDOC  := pandoc
SOFFICE := /Applications/LibreOffice.app/Contents/MacOS/soffice
RSVG    := rsvg-convert

# Список логических документов и их markdown-источников
DOCS := ТЗ ОП ТО РП РСП ПМИ ЛИТ

# Полные имена .docx-файлов
DOCX_FILES := $(foreach d,$(DOCS),$(d)_$(PREFIX).docx)
PDF_FILES  := $(DOCX_FILES:.docx=.pdf)

# Листы формата А1 (генерируются из SVG в подкаталоге листы/)
SHEETS      := Стр Схема Блок
SHEET_PDFS  := $(foreach s,$(SHEETS),$(s)_$(PREFIX).pdf)

# Опции pandoc.
# Содержание делается вручную внутри md (через стили TOC1/TOC2 с tab leader).
# Номера разделов уже прописаны в заголовках md.
PANDOC_OPTS := \
    --from markdown \
    --to docx \
    --reference-doc="$(REF_DOC)"

# ─── Главные цели ───────────────────────────────────────────────────────────

.PHONY: all docx pdf листы zip clean help

all: docx листы

docx: $(DOCX_FILES)
	@echo ""
	@echo "✓ Все 7 docx-документов готовы в текущем каталоге."
	@echo "  Открой их в Word и подправь рамку/штамп по шаблону кафедры."

pdf: $(PDF_FILES)
	@echo ""
	@echo "✓ Все 7 PDF готовы."

листы: $(SHEET_PDFS)
	@echo ""
	@echo "✓ Все 3 листа А1 готовы (Стр, Схема, Блок)."

# ─── Правила трансляции ─────────────────────────────────────────────────────

# Каждый <тип>_…2026.docx собирается из <тип>.md
ТЗ_$(PREFIX).docx: ТЗ.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

ОП_$(PREFIX).docx: ОП.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

ТО_$(PREFIX).docx: ТО.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

РП_$(PREFIX).docx: РП.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

РСП_$(PREFIX).docx: РСП.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

ПМИ_$(PREFIX).docx: ПМИ.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

# Листинг — те же опции
ЛИТ_$(PREFIX).docx: ЛИТ.md
	@echo "→ pandoc: $< → $@"
	@$(PANDOC) $(PANDOC_OPTS) "$<" -o "$@"

# Листы А1: SVG → PDF (формат A1 = 841×594 мм, рамка и штамп по ГОСТ 2.104)
Стр_$(PREFIX).pdf: листы/Стр.svg
	@echo "→ rsvg-convert: $< → $@"
	@$(RSVG) -f pdf -o "$@" "$<"

Схема_$(PREFIX).pdf: листы/Схема.svg
	@echo "→ rsvg-convert: $< → $@"
	@$(RSVG) -f pdf -o "$@" "$<"

Блок_$(PREFIX).pdf: листы/Блок.svg
	@echo "→ rsvg-convert: $< → $@"
	@$(RSVG) -f pdf -o "$@" "$<"

# docx → pdf через LibreOffice (если установлен)
%.pdf: %.docx
	@if [ -x "$(SOFFICE)" ]; then \
	    echo "→ LibreOffice: $< → $@"; \
	    "$(SOFFICE)" --headless --convert-to pdf --outdir "$(dir $@)" "$<" >/dev/null; \
	else \
	    echo "⚠ LibreOffice не найден по пути $(SOFFICE)"; \
	    echo "  Установи его или открой $< в Word и сохрани как PDF вручную."; \
	    exit 1; \
	fi

# ─── Упаковка ────────────────────────────────────────────────────────────────

zip: docx листы
	@ZIP_NAME="Воробьев_КР_СП_ИУ5-42Б_СП_2026.zip"; \
	rm -f "$$ZIP_NAME"; \
	zip -q "$$ZIP_NAME" $(DOCX_FILES) $(SHEET_PDFS) tsr.asm tsr.com 2>/dev/null || \
	zip -q "$$ZIP_NAME" $(DOCX_FILES) $(SHEET_PDFS) tsr.asm; \
	echo "✓ Архив для отправки: $$ZIP_NAME"; \
	ls -lh "$$ZIP_NAME"

# ─── Уборка ──────────────────────────────────────────────────────────────────

clean:
	@rm -f $(DOCX_FILES) $(PDF_FILES) $(SHEET_PDFS)
	@rm -f Воробьев_КР_СП_ИУ5-42Б_СП_2026.zip
	@echo "✓ Удалены: docx, pdf, листы А1, zip"

# Артефакты сборки tsr.com можно удалить отдельно
clean-asm:
	@rm -f tsr.com tsr.lst tsr.obj tsr.map
	@echo "✓ Удалены: tsr.com, tsr.lst, tsr.obj, tsr.map"

# ─── Помощь ──────────────────────────────────────────────────────────────────

help:
	@echo "Makefile для курсовой работы ИУ5-42Б Воробьев Вариант №5"
	@echo ""
	@echo "Цели:"
	@echo "  make           Собрать .docx + листы А1 (по умолчанию)"
	@echo "  make docx      Собрать только 7 .docx из .md"
	@echo "  make pdf       Собрать все 7 .pdf из .docx (нужен LibreOffice)"
	@echo "  make листы     Собрать 3 листа А1 (PDF) из SVG"
	@echo "  make zip       Упаковать комплект для отправки преподавателю"
	@echo "  make clean     Удалить собранные .docx/.pdf/листы/.zip"
	@echo "  make clean-asm Удалить артефакты компиляции tsr.com"
	@echo "  make help      Показать эту справку"
	@echo ""
	@echo "Зависимости:"
	@echo "  pandoc         $$(command -v pandoc || echo 'НЕ УСТАНОВЛЕН — brew install pandoc')"
	@echo "  rsvg-convert   $$(command -v rsvg-convert || echo 'НЕ УСТАНОВЛЕН — brew install librsvg')"
	@echo "  LibreOffice    для pdf-цели: $(SOFFICE)"
	@echo ""
	@echo "Шаблон оформления:"
	@echo "  $(REF_DOC)"
