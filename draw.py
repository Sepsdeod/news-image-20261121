#!/usr/bin/env python3
"""Draw the news-image-20261121 poster: six stories from Saturday 21 November 2026.

Renders a 1024x1024 PNG with PIL and the system DejaVu fonts. Deterministic:
no timestamps, no randomness, no network. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (245, 240, 230)
INK = (26, 26, 26)
NAVY = (21, 42, 69)
GOLD = (224, 170, 62)
CARD = (255, 255, 255)
CARD_EDGE = (205, 196, 175)
MUTED = (90, 84, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
def pic_globe(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=col, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=col, width=3)


def pic_scales(d, cx, cy, r, col):
    d.line([cx, cy - r, cx, cy + r], fill=col, width=4)
    d.line([cx - r * 0.85, cy - r * 0.55, cx + r * 0.85, cy - r * 0.55],
           fill=col, width=4)
    d.ellipse([cx - 5, cy - r - 5, cx + 5, cy - r + 5], fill=col)
    for sx in (-r * 0.85, r * 0.85):
        d.line([cx + sx, cy - r * 0.55, cx + sx, cy + r * 0.1], fill=col, width=3)
        d.polygon([(cx + sx - r * 0.42, cy + r * 0.1), (cx + sx + r * 0.42, cy + r * 0.1),
                   (cx + sx, cy + r * 0.75)], outline=col, width=3)
    d.line([cx - r * 0.7, cy + r, cx + r * 0.7, cy + r], fill=col, width=4)


def pic_chart(d, cx, cy, r, col):
    # descending bars
    bw = r * 0.34
    heights = [r * 1.15, r * 0.8, r * 0.45]
    for i, h in enumerate(heights):
        x0 = cx - r + i * (bw + 6)
        d.rectangle([x0, cy + r * 0.7 - h, x0 + bw, cy + r * 0.7], fill=col)
    # falling arrow over the bars
    d.line([(cx - r, cy - r * 0.85), (cx - r * 0.2, cy - r * 0.15),
            (cx + r * 0.25, cy - r * 0.45), (cx + r, cy + r * 0.45)],
           fill=col, width=5)
    d.polygon([(cx + r, cy + r * 0.45), (cx + r * 0.55, cy + r * 0.28),
               (cx + r * 0.72, cy + r * 0.85)], fill=col)


def pic_cuffs(d, cx, cy, r, col):
    for sx in (-r * 0.5, r * 0.5):
        d.ellipse([cx + sx - r * 0.42, cy - r * 0.42, cx + sx + r * 0.42,
                   cy + r * 0.42], outline=col, width=5)
    d.line([cx - r * 0.18, cy - r * 0.12, cx + r * 0.18, cy + r * 0.12],
           fill=col, width=4)
    d.line([cx - r * 0.18, cy + r * 0.12, cx + r * 0.18, cy - r * 0.12],
           fill=col, width=4)


def pic_shield(d, cx, cy, r, col):
    pts = [(cx, cy - r), (cx + r * 0.85, cy - r * 0.6), (cx + r * 0.85, cy + r * 0.1),
           (cx, cy + r), (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.85, cy - r * 0.6)]
    d.polygon(pts, outline=col, width=4)
    d.line([(cx - r * 0.4, cy), (cx - r * 0.08, cy + r * 0.35),
            (cx + r * 0.5, cy - r * 0.4)], fill=col, width=5)


def pic_quake(d, cx, cy, r, col):
    pts = [(cx - r, cy + r * 0.25), (cx - r * 0.6, cy + r * 0.25),
           (cx - r * 0.4, cy - r * 0.5), (cx - r * 0.15, cy + r * 0.5),
           (cx + r * 0.1, cy - r * 0.6), (cx + r * 0.3, cy + r * 0.25),
           (cx + r, cy + r * 0.25)]
    d.line(pts, fill=col, width=4, joint="curve")
    for rr in (r * 0.55, r * 0.85):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 340, fill=col, width=3)


# ------------------------------------------------------------------- stories
# Headlines and decks verified against Reuters / AP reporting of 21 Nov 2026.
STORIES = [
    dict(kicker="DIPLOMACY  ·  SHENZHEN", color=(31, 78, 121),
         pic=pic_globe,
         headline="Trump, Xi and Putin sign peace declaration",
         deck="First three-way leaders' summit ends with a four-point pact "
              "\u2014 silent on Ukraine. Zelensky calls it \u201cvery "
              "unsuccessful\u201d for Russia."),
    dict(kicker="JUSTICE  ·  THE HAGUE", color=(122, 31, 47),
         pic=pic_scales,
         headline="World Court: Myanmar guilty of Rohingya genocide",
         deck="The International Court of Justice finds Myanmar responsible "
              "for genocide \u2014 the first state ever convicted of it."),
    dict(kicker="MARKETS  ·  NEW YORK", color=(27, 94, 70),
         pic=pic_chart,
         headline="Stocks plunge in worst week since Covid",
         deck="S&P 500 falls 3.7% and Nasdaq 5.3% on Friday; Nvidia drops "
              "14% after reports of an SEC accounting inquiry."),
    dict(kicker="CRIME  ·  MEXICO", color=(146, 96, 20),
         pic=pic_cuffs,
         headline="Mexico captures \u201cEl Chapo Isidro\u201d",
         deck="Troops seize FBI most-wanted cartel boss Fausto Isidro Meza "
              "Flores in Sinaloa, in a major operation."),
    dict(kicker="SECURITY  ·  EUROPE", color=(74, 52, 110),
         pic=pic_shield,
         headline="Russian missiles land in Poland",
         deck="Two missiles and a drone come down during a strike on "
              "Ukraine; NATO vows to defend \u201cevery inch\u201d of "
              "Polish soil."),
    dict(kicker="DISASTER  ·  BANDA SEA", color=(14, 92, 110),
         pic=pic_quake,
         headline="Magnitude 6.8 quake strikes off Timor-Leste",
         deck="The quake hits the Banda Sea on Saturday, 226 km from Dili; "
              "felt in Darwin, no casualties reported."),
]


def draw_card(img, x, y, w, h, story):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                        outline=CARD_EDGE, width=2)
    col = story["color"]
    # colour spine
    d.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=col)
    # pictogram disc
    cx, cy, r = x + 70, y + 62, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    story["pic"](d, cx, cy, 26, (255, 255, 255))
    # kicker + headline, right of the disc
    tx = x + 132
    d.text((tx, y + 20), story["kicker"], font=SANS_B(15), fill=col)
    hl = wrap(d, story["headline"], SANS_B(25), w - 132 - 18)
    draw_text_block(d, tx, y + 46, hl[:3], SANS_B(25), INK, 30)
    # deck, full width below
    dk = wrap(d, story["deck"], SANS(18), w - 48)
    draw_text_block(d, x + 24, y + 136, dk[:3], SANS(18), (58, 54, 46), 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=SERIF_B(52))
    d.text(((W - tw) / 2, 18), title, font=SERIF_B(52), fill=(255, 255, 255))
    date = "Saturday 21 November 2026"
    dw = d.textlength(date, font=SANS_B(34))
    d.text(((W - dw) / 2, 92), date, font=SANS_B(34), fill=GOLD)

    # six cards, 2 x 3
    cw, ch, gap, mx = 480, 256, 16, 24
    top = 168
    for i, story in enumerate(STORIES):
        row, col_i = divmod(i, 2)
        x = mx + col_i * (cw + gap)
        y = top + row * (ch + 14)
        draw_card(img, x, y, cw, ch, story)

    # footer
    foot = "Sources: Reuters \u00b7 Associated Press \u00b7 GFZ  \u2014  Saturday 21 November 2026"
    fw = d.textlength(foot, font=SANS(17))
    d.text(((W - fw) / 2, 982), foot, font=SANS(17), fill=MUTED)

    img.save(OUT, format="PNG", compress_level=9)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
