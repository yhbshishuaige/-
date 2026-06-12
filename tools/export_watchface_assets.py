from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 336
HEIGHT = 480
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "watchface"

GREEN = (66, 245, 141, 255)
DIM_GREEN = (19, 115, 62, 255)
TEXT_GREEN = (223, 255, 233, 255)
MUTED_GREEN = (103, 155, 120, 255)
SCAN_GREEN = (66, 245, 141, 14)

RED = (255, 70, 85, 255)
DIM_RED = (123, 24, 34, 255)
TEXT_RED = (255, 228, 231, 255)
MUTED_RED = (182, 111, 120, 255)
SCAN_RED = (255, 70, 85, 13)

BLACK = (0, 0, 0, 255)

GLYPHS = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "10000", "11110", "10000", "10000"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "a": ["00000", "01110", "00001", "01111", "10001", "10011", "01101"],
    "b": ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01111", "10000", "10000", "10000", "01111"],
    "d": ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
    "e": ["00000", "01110", "10001", "11111", "10000", "10000", "01111"],
    "h": ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "n": ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
    "o": ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11110", "01000", "01000", "01001", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "v": ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
}


def ensure_dirs():
    for path in [
        OUT,
        OUT / "background",
        OUT / "digits" / "green",
        OUT / "digits" / "red",
        OUT / "icons" / "green",
        OUT / "icons" / "red",
        OUT / "labels" / "green",
        OUT / "labels" / "red",
        OUT / "preview",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def draw_scanlines(draw, color):
    for y in range(0, HEIGHT, 6):
        draw.rectangle([0, y, WIDTH, y], fill=color)


def draw_pixel_text(draw, text, x, y, size=4, fill=GREEN, gap=1):
    cursor = x
    for char in text:
        glyph = GLYPHS.get(char, GLYPHS[" "])
        for row, line in enumerate(glyph):
            for col, bit in enumerate(line):
                if bit == "1":
                    draw.rectangle(
                        [
                            round(cursor + col * size),
                            round(y + row * size),
                            round(cursor + col * size + max(1, size - 2)),
                            round(y + row * size + max(1, size - 2)),
                        ],
                        fill=fill,
                    )
        cursor += len(glyph[0]) * size + gap * size


def text_width(text, size, gap=1):
    width = 0
    for char in text:
        glyph = GLYPHS.get(char, GLYPHS[" "])
        width += len(glyph[0]) * size + gap * size
    return max(0, width - gap * size)


def font(size):
    for name in [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/consolab.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]:
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_text(draw, xy, text, size, fill, anchor="la"):
    draw.text(xy, text, font=font(size), fill=fill, anchor=anchor)


def make_static_screen(mode):
    if mode == "root":
        accent, dim, text, muted, scan = RED, DIM_RED, TEXT_RED, MUTED_RED, SCAN_RED
        header = "ROOTFACE"
        lines = [("uid", "0(root)"), ("shell", "/bin/su"), ("secure", "off"), ("batt", "86%")]
        path = "/root/time/live"
        prompt = "#"
    else:
        accent, dim, text, muted, scan = GREEN, DIM_GREEN, TEXT_GREEN, MUTED_GREEN, SCAN_GREEN
        header = "BOOTFACE"
        lines = [("steps", "8234"), ("heart", "72 bpm"), ("weather", "26C"), ("batt", "86%")]
        path = "/usr/time/live"
        prompt = "$"

    image = Image.new("RGBA", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_scanlines(draw, scan)
    draw_pixel_text(draw, header, 34, 42, size=3, fill=dim)
    draw_text(draw, (WIDTH // 2, 118), "14:08", 70, text, anchor="ma")
    draw_text(draw, (WIDTH // 2, 221), "FRI 06.12", 17, accent, anchor="ma")
    draw.line([34, 244, 302, 244], fill=(*accent[:3], 40), width=1)

    for index, (label, value) in enumerate(lines):
        y = 270 + index * 34
        draw_text(draw, (34, y), ">", 14, accent)
        draw_text(draw, (54, y), label, 14, muted)
        draw_text(draw, (300, y), value, 14, text, anchor="ra")

    draw.rectangle([34, 420, 66, 434], outline=accent, width=2)
    draw.rectangle([68, 424, 71, 430], fill=accent)
    draw.rectangle([37, 423, 62, 431], fill=accent)
    draw_text(draw, (302, 433), path, 12, muted, anchor="ra")
    draw_text(draw, (34, 461), prompt, 16, accent)
    draw.rectangle([54, 447, 63, 461], fill=accent)
    return image.convert("RGB")


def transparent_text_asset(text, name, color, subdir, size=4, scale_font=False):
    if scale_font:
        fnt = font(size)
        bbox = fnt.getbbox(text)
        w = bbox[2] - bbox[0] + 4
        h = bbox[3] - bbox[1] + 4
        image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((2 - bbox[0], 2 - bbox[1]), text, font=fnt, fill=color)
    else:
        w = text_width(text, size) + 4
        h = 7 * size + 4
        image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw_pixel_text(draw, text, 2, 2, size=size, fill=color)
    image.save(subdir / f"{name}.png")


def make_digit_assets(color, out_dir):
    for char in "0123456789":
        transparent_text_asset(char, f"digit_{char}", color, out_dir, size=12)
    transparent_text_asset(":", "colon", color, out_dir, size=12)


def make_icon_assets(color, out_dir):
    image = Image.new("RGBA", (42, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle([0, 2, 32, 16], outline=color, width=2)
    draw.rectangle([34, 6, 37, 12], fill=color)
    draw.rectangle([4, 5, 28, 13], fill=color)
    image.save(out_dir / "battery_86.png")

    for prompt in ["$", "#", ">"]:
        transparent_text_asset(prompt, f"prompt_{ord(prompt)}", color, out_dir, size=3)
    image = Image.new("RGBA", (9, 15), (0, 0, 0, 0))
    ImageDraw.Draw(image).rectangle([0, 0, 8, 14], fill=color)
    image.save(out_dir / "cursor_block.png")


def make_label_assets(color, muted, out_dir):
    labels = [
        "BOOTFACE",
        "ROOTFACE",
        "FRI",
        "MON",
        "TUE",
        "WED",
        "THU",
        "SAT",
        "SUN",
        "steps",
        "heart",
        "weather",
        "batt",
        "uid",
        "shell",
        "secure",
        "off",
        "/usr/time/live",
        "/root/time/live",
        "0(root)",
        "/bin/su",
        "86%",
        "72 bpm",
    ]
    for label in labels:
        safe = label.replace("/", "_").replace("(", "").replace(")", "").replace(" ", "_").replace("%", "pct")
        transparent_text_asset(label, safe, color if label.isupper() else muted, out_dir, size=3 if label.isupper() else 14, scale_font=not label.isupper())


def write_notes():
    notes = """# BOOTFACE watchface assets

These files are prepared for Xiaomi Smart Band 8 Pro watchface authoring.

Recommended Mi Create setup:

- Device: Xiaomi Smart Band 8 Pro / 336 x 480
- Base background: `background/user_static.png`
- Optional root preview background: `background/root_static.png`
- Boot animation frames: `../boot/boot_000.png` ... `../boot/boot_036.png`
- Time digits: `digits/green/digit_0.png` ... `digit_9.png` plus `colon.png`

Important limitation:

The web demo's triple-tap + `su` state machine is JavaScript. Real Xiaomi band watchfaces generally support static layers, system data, animations, and tap actions, but not arbitrary JavaScript logic. For the real band, use `root_static.png` as an alternate preview/page if your editor supports tap actions, or keep it as a visual variant.

Suggested layout coordinates:

- Time: x=168, y=116, centered
- Date: x=168, y=202, centered
- Divider: x=34..302, y=244
- Data rows: y=270, 304, 338, 372
- Battery icon: x=34, y=420
- Prompt: x=34, y=446
"""
    (OUT / "README.md").write_text(notes, encoding="utf-8")


def main():
    ensure_dirs()
    make_static_screen("user").save(OUT / "background" / "user_static.png")
    make_static_screen("root").save(OUT / "background" / "root_static.png")
    make_static_screen("user").save(OUT / "preview" / "preview_user.png")
    make_static_screen("root").save(OUT / "preview" / "preview_root.png")
    make_digit_assets(GREEN, OUT / "digits" / "green")
    make_digit_assets(RED, OUT / "digits" / "red")
    make_icon_assets(GREEN, OUT / "icons" / "green")
    make_icon_assets(RED, OUT / "icons" / "red")
    make_label_assets(GREEN, MUTED_GREEN, OUT / "labels" / "green")
    make_label_assets(RED, MUTED_RED, OUT / "labels" / "red")
    write_notes()
    print(f"Exported BOOTFACE assets to {OUT}")


if __name__ == "__main__":
    main()
