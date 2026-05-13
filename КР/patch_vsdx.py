#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Открывает оригинальные .vsdx-шаблоны преподавателя, патчит:
  - поле «Выполнил» (****** → Воробьев Е. А.);
  - группу (ИУ5-41Б → ИУ5-42Б) — только для Алгоритмов;
  - клавиши (F1?→F8?, F2?→F9?, F3?→F1?, F4?→F2?) — только для Алгоритмов,
    под вариант №5 ИУ5-42Б.
Сохраняет под новыми именами в КР/, затем конвертирует в PDF через LibreOffice.
"""
import io
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path("/Users/EV/Desktop/BMSTU/СП/Курсач СП")
SRC = ROOT / "Материалы"
DST = ROOT / "КР"

SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"

# (исходный .vsdx, имя нового .vsdx, имя итогового pdf)
JOBS = [
    (
        "Модульная структура_01_ОБР_2025.vsdx",
        "Стр_КР_СП_ИУ5-42Б_Воробьев_СП_2026.vsdx",
        "Стр_КР_СП_ИУ5-42Б_Воробьев_СП_2026.pdf",
        "mod",
    ),
    (
        "Схема взаимодействия_01_ОБР_2025.vsdx",
        "Схема_КР_СП_ИУ5-42Б_Воробьев_СП_2026.vsdx",
        "Схема_КР_СП_ИУ5-42Б_Воробьев_СП_2026.pdf",
        "sch",
    ),
    (
        "Алгоритмы_КР_СП_ОБР_СП_2025.vsdx",
        "Блок_КР_СП_ИУ5-42Б_Воробьев_СП_2026.vsdx",
        "Блок_КР_СП_ИУ5-42Б_Воробьев_СП_2026.pdf",
        "alg",
    ),
]

NAME = "Воробьев Е. А."


def patch_text(xml: str, kind: str) -> str:
    """Применяет замены к строке XML страницы Visio."""
    # 1) поле «Выполнил» — заменяем последовательность звёздочек (>= 4) на ФИО.
    xml = re.sub(r"\*{4,}", NAME, xml)

    # 1a) Цвет ФИО — чёрный вместо плейсхолдерного красного.
    # В шаблоне у текста-плейсхолдера задан THEMEGUARD(RGB(255,0,0)).
    xml = xml.replace("#ff0000", "#000000")
    xml = xml.replace("THEMEGUARD(RGB(255,0,0))", "THEMEGUARD(RGB(0,0,0))")

    # 2) группа в Алгоритмах
    if kind == "alg":
        xml = xml.replace("ИУ5-41Б", "ИУ5-42Б")

        # 3) клавиши под вариант №5: F1→F8, F2→F9, F3→F1, F4→F2.
        # Делаем через временные плейсхолдеры, чтобы не было каскада.
        placeholders = [
            ("F1?", "\x00K8\x00"),
            ("F2?", "\x00K9\x00"),
            ("F3?", "\x00K1\x00"),
            ("F4?", "\x00K2\x00"),
        ]
        for src, dst in placeholders:
            xml = xml.replace(src, dst)
        replacements = [
            ("\x00K8\x00", "F8?"),
            ("\x00K9\x00", "F9?"),
            ("\x00K1\x00", "F1?"),
            ("\x00K2\x00", "F2?"),
        ]
        for src, dst in replacements:
            xml = xml.replace(src, dst)

    return xml


def patch_vsdx(src_path: Path, dst_path: Path, kind: str):
    """Распаковать .vsdx, патчить XML страницы и подменить шрифт на узкий вариант."""
    with zipfile.ZipFile(src_path, "r") as zin:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                # Патчим только page1.xml (содержимое страницы).
                if item.filename.endswith("visio/pages/page1.xml"):
                    text = data.decode("utf-8")
                    new_text = patch_text(text, kind)
                    data = new_text.encode("utf-8")
                # На странице — уменьшаем размер шрифта на 15%.
                # Visio задаёт Size в дюймах (например, 0.1666 ≈ 12pt).
                # macOS-Calibri рендерится шире, чем Visio ожидает, поэтому
                # текст вылезает за рамки шейпов. Компенсируем уменьшением.
                if item.filename.endswith("visio/pages/page1.xml"):
                    text = data.decode("utf-8")
                    def shrink(m):
                        try:
                            v = float(m.group(1))
                        except ValueError:
                            return m.group(0)
                        return f'<Cell N=\'Size\' V=\'{v * 0.85:.10f}\''
                    text = re.sub(
                        r"<Cell N=['\"]Size['\"] V=['\"]([0-9.]+)['\"]",
                        shrink, text,
                    )
                    data = text.encode("utf-8")
                # Сохраняем атрибуты файла (важно для OPC-структуры).
                new_info = zipfile.ZipInfo(filename=item.filename,
                                           date_time=item.date_time)
                new_info.compress_type = item.compress_type
                new_info.external_attr = item.external_attr
                zout.writestr(new_info, data)
        dst_path.write_bytes(buf.getvalue())


def vsdx_to_pdf(vsdx: Path, pdf_name: str):
    """Конвертирует .vsdx → .pdf через LibreOffice headless."""
    out_dir = vsdx.parent
    res = subprocess.run(
        [SOFFICE, "--headless", "--convert-to", "pdf",
         "--outdir", str(out_dir), str(vsdx)],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr, file=sys.stderr)
        raise SystemExit(f"LibreOffice failed for {vsdx}")
    produced = out_dir / (vsdx.stem + ".pdf")
    target = out_dir / pdf_name
    if produced != target:
        shutil.move(str(produced), str(target))


def main():
    for src_name, vsdx_name, pdf_name, kind in JOBS:
        src = SRC / src_name
        dst_vsdx = DST / vsdx_name
        print(f"→ Патчим {src_name}")
        patch_vsdx(src, dst_vsdx, kind)
        print(f"  Сохранено: {dst_vsdx.name}")
        print(f"→ Конвертируем в PDF: {pdf_name}")
        vsdx_to_pdf(dst_vsdx, pdf_name)
        print(f"  Готово: {pdf_name}")
        print()


if __name__ == "__main__":
    main()
