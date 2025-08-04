#!/usr/bin/env python3
import fontforge
import requests
import os

PHUN_URL = "https://kaeru2193.github.io/Phun-Resources/font/PhunDot-latest.ttf"
HOTAL_PATH = "font/hotal-sans.ttf"
OUTPUT_PATH = "font/hotal-sans2.ttf"
PHUN_TEMP = "phundot-temp.ttf"

# 1. PhunDot フォントを一時ダウンロード
def download_phundot():
    print("Downloading PhunDot...")
    r = requests.get(PHUN_URL)
    r.raise_for_status()
    with open(PHUN_TEMP, "wb") as f:
        f.write(r.content)

# 2. フォントをマージ（競合時はhotalを優先）
def merge_fonts():
    print("Opening hotal-sans...")
    hotal = fontforge.open(HOTAL_PATH)

    print("Opening phundot-temp...")
    phun = fontforge.open(PHUN_TEMP)

    hotal_encoding = {g.unicode for g in hotal.glyphs() if g.unicode != -1}

    for glyph in phun.glyphs():
        if glyph.unicode == -1 or glyph.unicode in hotal_encoding:
            continue  # Skip duplicate or undefined unicode
        glyph_name = glyph.glyphname
        phun.selection.select(glyph_name)
        phun.copy()
        hotal.createChar(glyph.unicode, glyph_name)
        hotal.selection.select(glyph_name)
        hotal.paste()
    
    print(f"Saving merged font to {OUTPUT_PATH}")
    hotal.generate(OUTPUT_PATH)
    hotal.close()
    phun.close()
    os.remove(PHUN_TEMP)

if __name__ == "__main__":
    download_phundot()
    merge_fonts()
