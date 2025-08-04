#!/usr/bin/env python3
import fontforge
import os
import random

# 設定
FONT_PATH = "font/hotal-sans2.ttf"
PRON_FILE = "pronunciation.txt"

# 音素定義
initials = ["k", "g", "s", "z", "t", "d", "n", "m", "h", "y", "w", "r", "x", "j", "b", "p"]
vowels = ["a", "i", "u", "e", "o"]
dipthongs = ["ua", "uo", "ao", "ai"]
finals = ["s", "l", "ng", "n", "m"]
accents = ["1", "2", "3"]

def generate_pronunciation(existing_prons):
    while True:
        onset = "" if random.random() < 0.12 else random.choice(initials)
        vowel = random.choice(dipthongs) if random.random() < 0.25 else random.choice(vowels)

        if vowel == "uo" and random.random() < 0.40:
            base = onset + "uom"
        else:
            base = onset + vowel
            if random.random() < 0.33:
                base += random.choice(finals)

        accent = random.choice(accents)
        full = base + accent
        if full not in existing_prons:
            return full

def load_existing(path):
    mapping = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if " - " in line:
                    k, v = line.strip().split(" - ", 1)
                    mapping[k] = v
    return mapping

def extract_glyph_chars(font_path):
    font = fontforge.open(font_path)
    chars = {}
    for g in font.glyphs():
        if g.unicode != -1:
            try:
                ch = chr(g.unicode)
                chars[ch] = g.glyphname
            except ValueError:
                continue
    font.close()
    return chars  # {文字: グリフ名}

def main():
    existing = load_existing(PRON_FILE)
    used_prons = set(existing.values())

    chars = extract_glyph_chars(FONT_PATH)

    updated = {}
    for ch in sorted(chars):
        if ch not in existing:
            pron = generate_pronunciation(used_prons)
            existing[ch] = pron
            used_prons.add(pron)
            updated[ch] = pron

    if not updated:
        print("🔁 新規発音はありません")
        return

    with open(PRON_FILE, "w", encoding="utf-8") as f:
        for ch in sorted(existing):
            f.write(f"{ch} - {existing[ch]}\n")

    print(f"✅ {len(updated)} 件の新規発音を追加しました")

if __name__ == "__main__":
    main()
