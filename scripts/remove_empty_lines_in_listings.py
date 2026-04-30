#!/usr/bin/env python3
"""
remove_empty_lines_in_listings.py — утилита для удаления пустых строк внутри окружений
\\begin{lstlisting} ... \\end{lstlisting} в файлах LaTeX.

Использование:
  python remove_empty_lines_in_listings.py input.tex                # выводит результат в STDOUT
  python remove_empty_lines_in_listings.py input.tex -o output.tex  # сохраняет в output.tex
  python remove_empty_lines_in_listings.py input1.tex input2.tex -i # изменяет файлы на месте
"""

import argparse
import sys
from pathlib import Path
from typing import List

def get_lines(path: Path) -> List[str]:
    """Читает файл и возвращает список строк (с символами перевода строки)."""
    try:
        return path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        # Попытка со стандартной кодировкой Windows-1251
        return path.read_text(encoding="cp1251").splitlines(keepends=True)

def remove_blank_lines_in_listings(lines: List[str]) -> List[str]:
    """Возвращает новый список строк без пустых строк внутри lstlisting."""
    in_listing = False
    processed: List[str] = []

    for line in lines:
        stripped = line.strip()

        # Определяем начало/конец окружения lstlisting
        if stripped.startswith(r"\begin{lstlisting"):
            in_listing = True
            processed.append(line)
            continue
        if stripped.startswith(r"\end{lstlisting"):
            in_listing = False
            processed.append(line)
            continue

        # Если внутри окружения и строка пустая или содержит только пробелы — пропускаем её
        if in_listing and stripped == "":
            continue

        processed.append(line)

    return processed

def process_file(path: Path, in_place: bool = False, output_path: Path | None = None) -> None:
    lines = get_lines(path)
    new_lines = remove_blank_lines_in_listings(lines)

    if in_place:
        path.write_text("".join(new_lines), encoding="utf-8")
    elif output_path is not None:
        output_path.write_text("".join(new_lines), encoding="utf-8")
    else:
        sys.stdout.write("".join(new_lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Удаляет пустые строки внутри окружений lstlisting в LaTeX-файлах."
    )
    parser.add_argument("input", nargs="+", help="Пути к входным LaTeX-файлам.")
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Перезаписывать файлы на месте без создания копии.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Путь к выходному файлу (допустимо только при обработке одного входного файла без --in-place).",
    )

    args = parser.parse_args()

    if len(args.input) > 1 and args.output:
        parser.error("Опция -o/--output несовместима с обработкой нескольких входных файлов.")

    for inp in args.input:
        in_path = Path(inp)
        if not in_path.exists():
            parser.error(f"Файл '{inp}' не найден.")

        if args.in_place:
            process_file(in_path, in_place=True)
        else:
            out_path = Path(args.output) if args.output else None
            process_file(in_path, output_path=out_path)

if __name__ == "__main__":
    main() 