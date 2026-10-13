"""Make favicon.png, apple-touch-icon.png, favicon.svg and og-image.jpg (link preview) from the logo and a screen.

    python make_assets.py      # after build.py --png w11
"""
import base64
import io
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
STATIC = os.path.join(HERE, "fonts", "static")

logo = Image.open(os.path.join(HERE, "assets", "idiu-logo.png")).convert("RGBA")
logo = logo.crop(logo.getbbox())


def icon(size, pad):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill="#F3F6F2")
    lg = logo.copy()
    lg.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
    im.alpha_composite(lg, ((size - lg.width) // 2, (size - lg.height) // 2))
    return im


icon(64, 6).save(os.path.join(OUT, "favicon.png"))
icon(180, 22).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
buf = io.BytesIO()
icon(64, 6).save(buf, "PNG")
with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><image width="64" height="64" '
            f'href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/></svg>\n')

# link preview, 1200 x 630
W, H = 1200, 630
og = Image.new("RGB", (W, H), "#F3F6F2")
d = ImageDraw.Draw(og)
d.rectangle([0, 0, 470, H], fill="#EAF6DD")
lg = logo.copy()
lg.thumbnail((74, 74), Image.LANCZOS)
og.paste(lg, (56, 56), lg)
bold = lambda s: ImageFont.truetype(os.path.join(STATIC, "Bricolage-700.ttf"), s)
body = lambda s, w=500: ImageFont.truetype(os.path.join(STATIC, f"Figtree-{w}.ttf"), s)
d.text((144, 58), "IDIU", font=bold(34), fill="#102A1E")
d.text((145, 100), "Procurement", font=body(18, 600), fill="#1A683F")
d.text((56, 200), "From budget to", font=bold(50), fill="#102A1E")
d.text((56, 258), "closed file.", font=bold(50), fill="#1A683F")
y = 346
for line in ["Requisitions, RFQs, evaluation, LPOs,", "delivery and payment, with maker-checker", "approvals and a full audit trail."]:
    d.text((58, y), line, font=body(21), fill="#3B5045")
    y += 31
pill = "Clickable mockup · illustrative data"
pw = d.textlength(pill, font=body(16, 700)) + 40
d.rounded_rectangle([56, 520, 56 + pw, 560], radius=20, fill="#D9F0B8")
d.text((76, 529), pill, font=body(16, 700), fill="#2F5A0F")
shot = Image.open(os.path.join(OUT, "_previews", "w11-11-file-pr-2026-0087-overview.png")).convert("RGB")
shot = shot.crop((276, 0, 1920, 1080)).resize((850, 558), Image.LANCZOS)
mask = Image.new("L", shot.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=16, fill=255)
shadow = Image.new("RGBA", (shot.width + 60, shot.height + 60), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle([30, 36, shot.width + 30, shot.height + 36], radius=18, fill=(16, 42, 30, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(14))
og.paste(shadow, (500 - 30, 60 - 30), shadow)
og.paste(shot, (500, 60), mask)
og.save(os.path.join(OUT, "og-image.jpg"), quality=88)
print("favicon.png, apple-touch-icon.png, favicon.svg, og-image.jpg")
