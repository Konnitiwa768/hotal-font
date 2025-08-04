import os
import requests
from fontTools.ttLib import TTFont
from io import BytesIO

def download_font(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

def merge_fonts(primary_path, secondary_url, output_path):
    # Load primary (base) font: hotal-sans
    primary_font = TTFont(primary_path)

    # Load secondary font (remote): PhunDot
    secondary_stream = download_font(secondary_url)
    secondary_font = TTFont(secondary_stream)

    # Glyphs already in primary
    existing_glyphs = set(primary_font.getGlyphOrder())
    existing_codepoints = {
        cmap.get('cmap', {})
        for cmap in primary_font['cmap'].tables
    }

    # Merge glyphs from secondary that don't conflict
    for table in secondary_font['cmap'].tables:
        for codepoint, name in table.cmap.items():
            if codepoint in existing_codepoints:
                continue
            if name in existing_glyphs:
                continue
            glyph = secondary_font['glyf'].glyphs.get(name)
            if glyph:
                primary_font['glyf'].glyphs[name] = glyph
                primary_font['cmap'].tables[0].cmap[codepoint] = name
                primary_font['hmtx'].metrics[name] = secondary_font['hmtx'].metrics[name]
                existing_glyphs.add(name)

    # Save merged font
    primary_font.save(output_path)
    print(f"Merged font saved to: {output_path}")

if __name__ == "__main__":
    primary_path = "font/hotal-sans.ttf"
    secondary_url = "https://kaeru2193.github.io/Phun-Resources/font/PhunDot-latest.ttf"
    output_path = "font/hotal-sans2.ttf"
    merge_fonts(primary_path, secondary_url, output_path)
