#!/usr/bin/env python3
import fontforge

# 入力フォント
ORIGINAL_FONT = "font/hotal-sans.ttf"
MERGED_FONT = "font/hotal-sans2.ttf"

# 出力ファイル
ALL_GLYPHS_TXT = "glyphs_all.txt"
DIFF_GLYPHS_TXT = "glyphs_added.txt"

def extract_chars(font_path):
    font = fontforge.open(font_path)
    chars = set()
    for g in font.glyphs():
        if g.unicode != -1:
            try:
                chars.add(chr(g.unicode))
            except ValueError:
                continue  # skip invalid unicode
    font.close()
    return chars

def main():
    merged_chars = extract_chars(MERGED_FONT)
    original_chars = extract_chars(ORIGINAL_FONT)

    # 保存: すべてのグリフ
    with open(ALL_GLYPHS_TXT, "w", encoding="utf-8") as f:
        f.write("".join(sorted(merged_chars)))
    print(f"All glyphs written to {ALL_GLYPHS_TXT}")

    # 保存: 差分（追加されたグリフ）
    added = merged_chars - original_chars
    with open(DIFF_GLYPHS_TXT, "w", encoding="utf-8") as f:
        f.write("".join(sorted(added)))
    print(f"Added glyphs written to {DIFF_GLYPHS_TXT}")

if __name__ == "__main__":
    main()
