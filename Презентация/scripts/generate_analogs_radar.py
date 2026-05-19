from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "img" / "analogs-radar.png"

SIZE = (2200, 1400)
CENTER = (760, 720)
RADIUS = 420
LEVELS = 5

AXES = [
    ("Киров", 90, 1.18),
    ("GPS-\nгеолокация", 18, 1.34),
    ("Дедупликация", -54, 1.24),
    ("Карта\nобращений", -126, 1.26),
    ("Уведомления", -198, 1.24),
]

SERIES = [
    ("ПОС\n(Госуслуги)", [5, 2, 1, 4, 3], (84, 145, 204)),
    ("Наш город\n(Москва)", [1, 5, 2, 3, 5], (230, 151, 67)),
    ("Добродел", [1, 4, 3, 4, 5], (96, 167, 112)),
    ("FixMyStreet", [1, 5, 3, 5, 1], (200, 120, 80)),
    ("Разрабатываемая\nсистема", [5, 5, 5, 5, 4], (181, 103, 181)),
]


def polar_point(angle_deg: float, radius: float) -> tuple[float, float]:
    angle = pi * angle_deg / 180.0
    x = CENTER[0] + radius * cos(angle)
    y = CENTER[1] - radius * sin(angle)
    return x, y


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    font_path = Path("C:/Windows/Fonts") / font_name
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def draw_centered_multiline(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font, fill) -> None:
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=4)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.multiline_text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill, align="center", spacing=4)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGBA", SIZE, "white")
    draw = ImageDraw.Draw(image, "RGBA")

    title_font = load_font(56, bold=True)
    label_font = load_font(34, bold=True)
    small_font = load_font(28)
    legend_font = load_font(30)

    grid_color = (210, 214, 220, 255)
    axis_color = (160, 165, 172, 255)
    text_color = (40, 40, 40, 255)

    for level in range(1, LEVELS + 1):
        radius = RADIUS * level / LEVELS
        points = [polar_point(angle, radius) for _, angle, _ in AXES]
        draw.line(points + [points[0]], fill=grid_color, width=2)

    for label, angle, radius_mult in AXES:
        end = polar_point(angle, RADIUS * 1.05)
        draw.line([CENTER, end], fill=axis_color, width=2)

        label_radius = RADIUS * radius_mult
        label_point = polar_point(angle, label_radius)
        draw_centered_multiline(draw, label_point, label, label_font, text_color)

    for level in range(1, LEVELS + 1):
        point = polar_point(0, RADIUS * level / LEVELS)
        draw.text((point[0] + 8, point[1] - 10), str(level), font=small_font, fill=(120, 120, 120, 255))

    for name, values, color in SERIES:
        points = [polar_point(angle, RADIUS * value / LEVELS) for value, (_, angle, _) in zip(values, AXES)]
        fill_alpha = 18 if "Разрабатываемая" in name else 36
        draw.polygon(points, fill=(*color, fill_alpha))

    for name, values, color in SERIES:
        points = [polar_point(angle, RADIUS * value / LEVELS) for value, (_, angle, _) in zip(values, AXES)]
        draw.line(points + [points[0]], fill=(*color, 255), width=5)
        for point in points:
            draw.ellipse((point[0] - 7, point[1] - 7, point[0] + 7, point[1] + 7), fill=(*color, 255))

    title = "Сравнение существующих решений"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((SIZE[0] - 520 - title_width / 2, 80), title, font=title_font, fill=text_color)

    legend_x = 1400
    legend_y = 240
    legend_gap = 88
    for index, (name, _, color) in enumerate(SERIES):
        y = legend_y + index * legend_gap
        draw.line([(legend_x, y), (legend_x + 80, y)], fill=(*color, 255), width=8)
        draw.ellipse((legend_x + 31, y - 8, legend_x + 49, y + 8), fill=(*color, 255))
        draw_centered_multiline(draw, (legend_x + 220, y), name, legend_font, text_color)

    note = "Шкала: от 1 (минимум) до 5 (максимум)"
    note_bbox = draw.textbbox((0, 0), note, font=small_font)
    note_w = note_bbox[2] - note_bbox[0]
    draw.text((CENTER[0] - note_w / 2, 1260), note, font=small_font, fill=(90, 90, 90, 255))

    image.save(OUTPUT_PATH)
    print(f"OK: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
