from pathlib import Path
from PIL import Image, ImageDraw
import math

WIDTH = 336
HEIGHT = 480
BOOT_TEXT = "Hello world!"
BOOT_DURATION_MS = 3000
FPS = 12

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "boot"

GREEN = (66, 245, 141, 255)
DIM_GREEN = (19, 115, 62, 255)
SCAN = (3, 14, 8, 255)
BLACK = (0, 0, 0, 255)

GLYPHS = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "e": ["00000", "01110", "10001", "11111", "10000", "10000", "01111"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "o": ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    "w": ["00000", "00000", "10001", "10001", "10101", "10101", "01010"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "d": ["00001", "00001", "01101", "10011", "10001", "10001", "01111"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "a": ["00000", "01110", "00001", "01111", "10001", "10011", "01101"],
    "b": ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01111", "10000", "10000", "10000", "01111"],
    "f": ["00110", "01001", "01000", "11100", "01000", "01000", "01000"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "n": ["00000", "00000", "10110", "11001", "10001", "10001", "10001"],
    "p": ["00000", "00000", "11110", "10001", "11110", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11110", "01000", "01000", "01001", "00110"],
}


def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)


def text_width(text, size, gap=1):
    width = 0
    for char in text:
        glyph = GLYPHS.get(char, GLYPHS[" "])
        width += len(glyph[0]) * size + gap * size
    return max(0, width - gap * size)


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


def draw_scanlines(draw):
    for y in range(0, HEIGHT, 6):
        draw.rectangle([0, y, WIDTH, y], fill=SCAN)


def make_frame(ms):
    progress = min(max(ms / BOOT_DURATION_MS, 0), 1)
    chars = min(len(BOOT_TEXT), max(1, math.ceil(progress * len(BOOT_TEXT))))
    text = BOOT_TEXT[:chars]
    size = 5
    y = 214
    gap = 0
    final_width = text_width(BOOT_TEXT, size, gap=gap)
    current_width = text_width(text, size, gap=gap)
    target_x = (WIDTH - final_width) / 2
    center_x = (WIDTH - current_width) / 2
    x = center_x + (target_x - center_x) * ease_out_cubic(progress)

    image = Image.new("RGBA", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_scanlines(draw)

    draw_pixel_text(draw, "$ boot --face", 38, 48, size=3, fill=(19, 115, 62, 110))
    draw_pixel_text(draw, "init display...", 38, 70, size=3, fill=(19, 115, 62, 110))
    draw_pixel_text(draw, text, x, y, size=size, fill=GREEN, gap=gap)

    cursor_alpha = 255 if math.sin(ms / 95) > 0 else 85
    cursor_x = x + current_width + size * 2
    draw.rectangle([round(cursor_x), y, round(cursor_x + size - 2), y + size * 7 - 1], fill=(66, 245, 141, cursor_alpha))
    return image.convert("RGB")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frame_count = round(BOOT_DURATION_MS / 1000 * FPS) + 1
    for index in range(frame_count):
        ms = round(index * 1000 / FPS)
        frame = make_frame(ms)
        frame.save(OUT_DIR / f"boot_{index:03d}.png")
    print(f"Exported {frame_count} frames to {OUT_DIR}")


if __name__ == "__main__":
    main()
