from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "promo-climatcomfort39.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

slides = [
    {
        "image": ROOT / "assets/images/hero-premium-home.png",
        "kicker": "КАЛИНИНГРАД · ИНЖЕНЕРНЫЙ КОМФОРТ",
        "title": "Комфорт,\nкоторый не видно.",
        "copy": "Системы для интерьеров, где важна каждая линия.",
        "align": "left",
    },
    {
        "image": ROOT / "assets/images/ventilation-plenum.png",
        "kicker": "ВОЗДУХ · ТИШИНА · ЛОГИКА",
        "title": "Свежий воздух\nбез лишнего шума.",
        "copy": "Вентиляция и распределение воздуха — под планировку дома.",
        "align": "left",
    },
    {
        "image": ROOT / "assets/images/clean-installation.png",
        "kicker": "АККУРАТНАЯ РЕАЛИЗАЦИЯ",
        "title": "Инженерия,\nкоторая бережёт интерьер.",
        "copy": "Согласовываем трассы до отделки и защищаем готовое пространство.",
        "align": "left",
    },
    {
        "image": ROOT / "assets/images/designer-partnership.png",
        "kicker": "ДИЗАЙНЕР · ИНЖЕНЕР · ВЛАДЕЛЕЦ",
        "title": "Одна идея.\nОдин понятный результат.",
        "copy": "Проектирование ОВКВ, монтаж и сервис — в согласованном контуре.",
        "align": "left",
    },
    {
        "image": ROOT / "assets/images/hero-premium-home.png",
        "kicker": "КЛИМАТКОМФОРТ39",
        "title": "Ваш объект —\nследующий.",
        "copy": "Кондиционирование · вентиляция · отопление · автоматика\nclimatcomfort39.ru",
        "align": "left",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, progress, direction=1):
    """Ken Burns crop to 16:9 canvas."""
    target_ratio = W / H
    iw, ih = img.size
    base_scale = max(W / iw, H / ih)
    scale = base_scale * (1.02 + progress * 0.10)
    rw, rh = int(iw * scale), int(ih * scale)
    im = img.resize((rw, rh), Image.Resampling.LANCZOS)
    extra_x = max(0, rw - W)
    extra_y = max(0, rh - H)
    if direction == 1:
        x = int(extra_x * (.30 + .25 * progress))
    else:
        x = int(extra_x * (.58 - .25 * progress))
    y = int(extra_y * (.48 + .08 * math.sin(progress * math.pi)))
    return im.crop((x, y, x + W, y + H))


def wrap_text(draw, text, fnt, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_slide(slide, t, idx):
    # 0..1 slide movement, with 0.35 sec fade in/out
    img = Image.open(slide["image"]).convert("RGB")
    canvas = cover(img, t, 1 if idx % 2 == 0 else -1).convert("RGBA")
    # dark editorial gradient left; light fade over first/last margins
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = overlay.load()
    for x in range(W):
        # left remains readable even on brightest frames
        alpha = int(180 * max(0, 1 - x / (W * .72))) + 18
        for y in range(H):
            px[x, y] = (7, 28, 24, min(alpha, 210))
    canvas = Image.alpha_composite(canvas, overlay)
    d = ImageDraw.Draw(canvas)
    sans = font(FONT_BOLD, 16)
    title_font = font(FONT_SERIF, 58)
    copy_font = font(FONT_SANS, 23)
    brand_font = font(FONT_BOLD, 14)
    x, y = 85, 140
    # animation rise + fade
    alpha = int(255 * min(1, t / .12, (1-t) / .12))
    rise = int((1 - min(1, t/.16)) * 22)
    text_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    td = ImageDraw.Draw(text_layer)
    td.text((x, y-rise), slide["kicker"], font=sans, fill=(230, 195, 142, alpha), stroke_width=0)
    yy = y + 46 - rise
    for line in slide["title"].split("\n"):
        td.text((x, yy), line, font=title_font, fill=(255, 250, 242, alpha))
        yy += 67
    yy += 20
    for line in slide["copy"].split("\n"):
        for wrapped in wrap_text(td, line, copy_font, 570):
            td.text((x, yy), wrapped, font=copy_font, fill=(218, 232, 222, alpha))
            yy += 32
    # top brand and frame line
    td.text((85, 55), "КЛИМАТКОМФОРТ39", font=brand_font, fill=(242, 242, 234, 210))
    td.line((85, 82, 170, 82), fill=(215, 161, 93, 220), width=2)
    # progress 
    td.rectangle((85, 665, 85 + int(1110 * t), 669), fill=(232, 191, 130, alpha))
    td.rectangle((85 + int(1110 * t), 665, 1195, 669), fill=(255,255,255,60))
    canvas = Image.alpha_composite(canvas, text_layer)
    return np.asarray(canvas.convert("RGB"))

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
writer = imageio_ffmpeg.write_frames(
    str(OUT), (W, H), fps=FPS, codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p",
    quality=7, ffmpeg_log_level="error", output_params=["-movflags", "+faststart", "-preset", "medium"]
)
writer.send(None)
frames_per_slide = FPS * 4
for idx, slide in enumerate(slides):
    for i in range(frames_per_slide):
        frame = draw_slide(slide, i / max(1, frames_per_slide-1), idx)
        writer.send(frame)
writer.close()
print(OUT)
