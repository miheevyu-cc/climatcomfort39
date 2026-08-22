"""Apply user-supplied image revisions while preserving manually edited HTML text.
The HTML files are self-contained, so the selected assets are embedded as data URIs.
"""
from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = Path('/home/user/uploads')
ASSET_DIR = ROOT / 'assets' / 'images' / 'user-revisions-2026-08-18'
ASSET_DIR.mkdir(parents=True, exist_ok=True)
REF_DIR = ROOT / 'assets' / 'references' / 'user-images-2026-08-18'
REF_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    'hisense_warm_air': '2026_HISENSE_S-PRO_features_black__06_2.jpg',
    'hisense_wifi': '2026_HISENSE_S-PRO_features_black__12.jpg',
    'app_temperature': 'app_indoor_temperature-480x592.jpg',
    'clean_install': 'clean-installation1-2.png',
    'designer': 'designer-partnership-2.png',
    'heating': 'heating-manifold-valtec-2.jpg',
    'sensation_transparent': 'sensation-slider-pro-carbon-superior-dc-inverter-2.png',
    'utility_room': 'utility-room-720x716.jpg',
}


def copy_reference(filename: str) -> Path:
    src = UPLOADS / filename
    target = REF_DIR / filename
    target.write_bytes(src.read_bytes())
    return src


def optimize(key: str, filename: str, *, preserve_alpha: bool = False, max_px: int = 1100, warmth: float | None = None) -> tuple[Path, str]:
    src = copy_reference(filename)
    im = ImageOps.exif_transpose(Image.open(src))
    if preserve_alpha and im.mode in ('RGBA', 'LA'):
        # Keep transparent official product cut-out intact.
        if max(im.size) > max_px:
            im.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        out = ASSET_DIR / (Path(filename).stem + '.png')
        im.save(out, 'PNG', optimize=True)
        mime = 'image/png'
    else:
        if im.mode in ('RGBA', 'LA'):
            bg = Image.new('RGB', im.size, '#ffffff')
            bg.paste(im, mask=im.getchannel('A'))
            im = bg
        else:
            im = im.convert('RGB')
        if max(im.size) > max_px:
            im.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        # Keep the real heating assembly authentic; only a restrained colour/contrast normalisation.
        if warmth is not None:
            im = ImageEnhance.Color(im).enhance(warmth)
            im = ImageEnhance.Contrast(im).enhance(1.025)
        out = ASSET_DIR / (Path(filename).stem + '.jpg')
        im.save(out, 'JPEG', quality=87, optimize=True, progressive=True)
        mime = 'image/jpeg'
    encoded = base64.b64encode(out.read_bytes()).decode('ascii')
    print(f'{key}: {out.name} {out.stat().st_size // 1024} KB')
    return out, f'data:{mime};base64,{encoded}'


DATA: dict[str, str] = {}
for key, filename in SOURCES.items():
    DATA[key] = optimize(
        key,
        filename,
        preserve_alpha=(key == 'sensation_transparent'),
        max_px=1100,
        warmth=0.96 if key == 'heating' else None,
    )[1]


def load_html(name: str) -> str:
    return (ROOT / name).read_text(encoding='utf-8')


def save_html(name: str, html: str) -> None:
    (ROOT / name).write_text(html, encoding='utf-8')


def replace_tag_src(soup: BeautifulSoup, selector: str, data_uri: str, alt: str | None = None) -> None:
    tag = soup.select_one(selector)
    if not tag:
        raise RuntimeError(f'Missing target: {selector}')
    tag['src'] = data_uri
    if alt:
        tag['alt'] = alt


def serialize(soup: BeautifulSoup) -> str:
    # formatter=None keeps Russian text, inline scripts and URLs unescaped as entered by the user.
    return soup.decode(formatter=None)


# INDEX: preserve all user-edited text, modify just the requested visual targets.
index_soup = BeautifulSoup(load_html('index.html'), 'html.parser')
replace_tag_src(index_soup, '#content .cards a:nth-of-type(1) img', DATA['hisense_warm_air'], 'Hisense SENSATION SLIDER PRO CARBON — тёплый воздушный поток')
replace_tag_src(index_soup, '#content > section.section.blue .visual-stack img.mini', DATA['designer'], 'Дизайнер и инженер согласовывают проект')
replace_tag_src(index_soup, '#content > section.section.pink-bg .equipment article:nth-of-type(1) img', DATA['hisense_wifi'], 'Hisense SENSATION SLIDER PRO CARBON с Wi-Fi управлением')
index_html = serialize(index_soup)
# Requested hero cropping: same source, composition shifted to the right only for hero image.
index_html = index_html.replace('</style>', '.hero-photo{object-position:72% center!important}</style>', 1)
save_html('index.html', index_html)

# SERVICES: replace declared service visuals.
services_soup = BeautifulSoup(load_html('services.html'), 'html.parser')
replace_tag_src(services_soup, '#air > img.photo', DATA['clean_install'], 'Монтаж кондиционера в интерьере с высоким потолком')
replace_tag_src(services_soup, '#heat > img.photo', DATA['heating'], 'Смесительный узел и коллектор отопления')
replace_tag_src(services_soup, '#content > section.section.pink-bg .models article:nth-of-type(1) img', DATA['sensation_transparent'], 'Hisense SENSATION SLIDER PRO CARBON')

# The current services page did not contain the visual-stack named in the request.
# Add it as a direct child of its main second section so its intended CSS selectors work exactly.
main_section = services_soup.select_one('#content > section.section')
if not main_section:
    raise RuntimeError('Main services section not found')
wrap = main_section.select_one(':scope > .wrap')
if not wrap:
    raise RuntimeError('Services section wrapper not found')
old_stack = wrap.select_one(':scope > .visual-stack.services-visual-stack')
if not old_stack:
    stack = services_soup.new_tag('div', attrs={'class': 'visual-stack services-visual-stack', 'style': 'margin:30px 0 54px'})
    big = services_soup.new_tag('img', attrs={'class': 'big', 'src': DATA['utility_room'], 'alt': 'Техническое помещение с инженерным оборудованием'})
    mini = services_soup.new_tag('img', attrs={'class': 'mini', 'src': DATA['app_temperature'], 'alt': 'Управление температурой с мобильного приложения'})
    stack.append(big)
    stack.append(mini)
    # Position visual stack immediately after service navigation and heading, before service cards.
    head = wrap.select_one(':scope > .section-head')
    if head:
        head.insert_after(stack)
    else:
        wrap.insert(0, stack)
else:
    replace_tag_src(services_soup, '#content > section.section:nth-of-type(2) .visual-stack.services-visual-stack img.big', DATA['utility_room'])
    replace_tag_src(services_soup, '#content > section.section:nth-of-type(2) .visual-stack.services-visual-stack img.mini', DATA['app_temperature'])

save_html('services.html', serialize(services_soup))
print('HTML visual revisions applied.')
