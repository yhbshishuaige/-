from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

WIDTH = 336
HEIGHT = 480
ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "micreate_project"
OUT = PROJECT_DIR / "images"
PROJECT = PROJECT_DIR / "BOOTFACE.fprj"

GREEN = (66, 245, 141, 255)
DIM_GREEN = (19, 115, 62, 255)
TEXT_GREEN = (223, 255, 233, 255)
MUTED_GREEN = (103, 155, 120, 255)
SCAN_GREEN = (3, 14, 8, 255)
BLACK = (0, 0, 0, 255)

GLYPHS = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    "%": ["11001", "11010", "00100", "01000", "10110", "00110", "00000"],
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
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "a": ["00000", "01110", "00001", "01111", "10001", "10011", "01101"],
    "b": ["10000", "10000", "10110", "11001", "10001", "10001", "11110"],
    "e": ["00000", "01110", "10001", "11111", "10000", "10000", "01111"],
    "h": ["10000", "10000", "10110", "11001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "p": ["00000", "00000", "11110", "10001", "11110", "10000", "10000"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11110", "01000", "01000", "01001", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "w": ["00000", "00000", "10001", "10001", "10101", "10101", "01010"],
}


def font(size):
    for name in ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/arial.ttf"]:
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


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


def pixel_width(text, size, gap=1):
    width = 0
    for char in text:
        glyph = GLYPHS.get(char, GLYPHS[" "])
        width += len(glyph[0]) * size + gap * size
    return max(0, width - gap * size)


def save_pixel_asset(text, filename, size, color=GREEN, gap=1):
    w = pixel_width(text, size, gap) + 4
    h = 7 * size + 4
    image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_pixel_text(draw, text, 2, 2, size=size, fill=color, gap=gap)
    image.save(OUT / filename)
    return image.size


def draw_text(draw, xy, text, size, fill, anchor="la"):
    draw.text(xy, text, font=font(size), fill=fill, anchor=anchor)


def make_background():
    image = Image.new("RGBA", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(image, "RGBA")
    for y in range(0, HEIGHT, 6):
        draw.rectangle([0, y, WIDTH, y], fill=SCAN_GREEN)

    draw_pixel_text(draw, "BOOTFACE", 34, 42, size=3, fill=DIM_GREEN)
    draw.line([34, 244, 302, 244], fill=(66, 245, 141, 40), width=1)

    lines = [("steps", "8234"), ("heart", "72 bpm"), ("weather", "26C"), ("batt", "")]
    for index, (label, value) in enumerate(lines):
        y = 270 + index * 34
        draw_text(draw, (34, y), ">", 14, GREEN)
        draw_text(draw, (54, y), label, 14, MUTED_GREEN)
        if value:
            draw_text(draw, (300, y), value, 14, TEXT_GREEN, anchor="ra")

    draw.rectangle([34, 420, 66, 434], outline=GREEN, width=2)
    draw.rectangle([68, 424, 71, 430], fill=GREEN)
    draw.rectangle([37, 423, 62, 431], fill=GREEN)
    draw_text(draw, (302, 433), "/usr/time/live", 12, MUTED_GREEN, anchor="ra")
    draw_text(draw, (34, 461), "$", 16, GREEN)
    draw.rectangle([54, 447, 63, 461], fill=GREEN)
    image.convert("RGB").save(OUT / "0000.png")


def make_digit_sets():
    for index, char in enumerate("0123456789", start=1):
        save_pixel_asset(char, f"{index:04d}.png", size=12, color=TEXT_GREEN, gap=1)
    save_pixel_asset(":", "0011.png", size=12, color=TEXT_GREEN, gap=1)
    for offset, char in enumerate("0123456789", start=12):
        save_pixel_asset(char, f"{offset:04d}.png", size=3, color=GREEN, gap=1)
    save_pixel_asset(".", "0022.png", size=3, color=GREEN, gap=1)
    save_pixel_asset("%", "0023.png", size=3, color=TEXT_GREEN, gap=1)
    blank = Image.new("RGBA", (8, 22), (0, 0, 0, 0))
    blank.save(OUT / "0024.png")


def bitmap_list(start, end, blank="0024.png"):
    files = [f"{index:04d}.png" for index in range(start, end + 1)]
    files.append(blank)
    return "|".join(files)


def widget(parent, **attrs):
    ET.SubElement(parent, "Widget", {key: str(value) for key, value in attrs.items()})


def make_project():
    project = ET.Element("FaceProject", {"DeviceType": "11", "Id": "BOOTFACE"})
    screen = ET.SubElement(project, "Screen", {"Title": "BOOTFACE", "Bitmap": "0000.png"})
    widget(screen, Shape=30, Name="Background", X=0, Y=0, Width=336, Height=480, Alpha=255, Visible_Src=0, Bitmap="0000.png")
    widget(screen, Shape=32, Name="Hours", X=49, Y=116, Width=112, Height=88, Alpha=255, Digits=2, Alignment=1, Spacing=4, Blanking=0, Visible_Src=0, Value_Src=811, BitmapList=bitmap_list(1, 10))
    widget(screen, Shape=30, Name="Colon", X=151, Y=116, Width=64, Height=88, Alpha=255, Visible_Src=0, Bitmap="0011.png")
    widget(screen, Shape=32, Name="Minutes", X=181, Y=116, Width=112, Height=88, Alpha=255, Digits=2, Alignment=1, Spacing=4, Blanking=0, Visible_Src=0, Value_Src=1011, BitmapList=bitmap_list(1, 10))
    widget(screen, Shape=32, Name="Month", X=139, Y=202, Width=36, Height=25, Alpha=255, Digits=2, Alignment=1, Spacing=1, Blanking=0, Visible_Src=0, Value_Src=1012, BitmapList=bitmap_list(12, 21))
    widget(screen, Shape=30, Name="DateDot", X=170, Y=202, Width=19, Height=25, Alpha=255, Visible_Src=0, Bitmap="0022.png")
    widget(screen, Shape=32, Name="Day", X=188, Y=202, Width=36, Height=25, Alpha=255, Digits=2, Alignment=1, Spacing=1, Blanking=0, Visible_Src=0, Value_Src=1812, BitmapList=bitmap_list(12, 21))
    widget(screen, Shape=32, Name="BatteryPercent", X=261, Y=372, Width=36, Height=25, Alpha=255, Digits=2, Alignment=2, Spacing=1, Blanking=0, Visible_Src=0, Value_Src=2031, BitmapList=bitmap_list(12, 21))
    widget(screen, Shape=30, Name="PercentSign", X=301, Y=372, Width=19, Height=25, Alpha=255, Visible_Src=0, Bitmap="0023.png")

    ET.indent(project, space="\t")
    tree = ET.ElementTree(project)
    tree.write(PROJECT, encoding="utf-8", xml_declaration=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_background()
    make_digit_sets()
    make_project()
    print(f"Exported flat Mi Create assets to {OUT}")
    print(f"Exported draft project to {PROJECT}")


if __name__ == "__main__":
    main()
