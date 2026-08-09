"""Render compact contact sheets for the PDF pages used in the DX review."""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageOps, ImageDraw


PAGE_GROUPS = {
    "01_건축공학": [71, 72],
    "02_토목공학": [100, 102],
    "03_산업공학": [214, 215, 216],
    "04_수리빅데이터": [239, 241],
    "05_고분자공학": [256, 257],
    "06_신소재공학": [274, 275, 277],
    "07_소재디자인공학": [447, 451],
    "08_화학공학": [470, 471, 473],
    "09_화학생명소재": [489, 490, 491],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    pdf = fitz.open(args.pdf)
    zoom = 1.5
    matrix = fitz.Matrix(zoom, zoom)

    for label, page_numbers in PAGE_GROUPS.items():
        rendered: list[Image.Image] = []
        for page_number in page_numbers:
            pix = pdf[page_number - 1].get_pixmap(matrix=matrix, alpha=False)
            page = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page = ImageOps.expand(page, border=(4, 34, 4, 4), fill="white")
            draw = ImageDraw.Draw(page)
            draw.text((12, 8), f"PDF page {page_number}", fill="black")
            rendered.append(page)

        width = max(image.width for image in rendered)
        height = sum(image.height for image in rendered)
        sheet = Image.new("RGB", (width, height), "white")
        y = 0
        for image in rendered:
            sheet.paste(image, (0, y))
            y += image.height
        sheet.save(args.out_dir / f"{label}.png")


if __name__ == "__main__":
    main()
