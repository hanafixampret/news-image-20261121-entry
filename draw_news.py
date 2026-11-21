#!/usr/bin/env python3
"""Draw the front page of Saturday 21 November 2026's world news as one image.

A 1024x1024 newspaper front page: a masthead naming the day, a strip of
the day's big numbers, one illustrated lead story, two more illustrated
leads, ten feature cards and sixteen one-line stories -- 29 stories in all,
every one of them first reported on Saturday 21 November 2026, with its
source named in the footer.

Everything is drawn with PIL primitives: no external images, no network,
no timestamps, no randomness. Running this file twice writes byte-identical
PNGs. Run:  python3 draw_news.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

LIB = "/usr/share/fonts/truetype/liberation/"
DEJ = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    for base in (LIB, DEJ):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_I = lambda s: font("LiberationSans-Italic.ttf", s)

PAPER = (246, 241, 229)
INK = (18, 18, 18)
NAVY = (20, 38, 77)
NAVY_DK = (13, 25, 52)
GOLD = (233, 196, 88)
GOLD_DK = (198, 158, 52)
RED = (178, 34, 34)
GREY = (96, 96, 90)
RULE = (150, 140, 120)
WHITE = (255, 255, 255)
SKY = (168, 200, 228)
TEAL = (24, 96, 88)
PLUM = (96, 44, 84)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(d, text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, wdt=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def kicker(d, x, y, text, fill=RED, size=17):
    f = SANS_B(size)
    d.text((x, y), text, font=f, fill=fill)
    return y + size + 6


def scales(d, cx, cy, s, ink=NAVY, gold=GOLD):
    """Scales of justice, drawn from lines and arcs, centred at (cx, cy)."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=gold)
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=ink, width=4)
    top = cy - s * 0.62
    d.line([(cx, top), (cx, cy + s * 0.55)], fill=ink, width=6)
    d.line([(cx - s * 0.55, top + s * 0.12), (cx + s * 0.55, top + s * 0.12)],
           fill=ink, width=6)
    d.ellipse([cx - 7, top - 14, cx + 7, top], fill=ink)
    for side in (-1, 1):
        px = cx + side * s * 0.55
        py = top + s * 0.12
        d.line([(px, py), (px - s * 0.16, py + s * 0.42)], fill=ink, width=4)
        d.line([(px, py), (px + s * 0.16, py + s * 0.42)], fill=ink, width=4)
        d.arc([px - s * 0.22, py + s * 0.30, px + s * 0.22, py + s * 0.62],
              start=0, end=180, fill=ink, width=5)
    d.line([(cx - s * 0.30, cy + s * 0.55), (cx + s * 0.30, cy + s * 0.55)],
           fill=ink, width=6)


def burst(d, cx, cy, r, fill=RED):
    """Explosion burst: a spiked star."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=GOLD)


def trend_down(d, x0, y0, x1, y1, fill=RED):
    """A falling chart arrow inside a box."""
    d.line([(x0, y0), (x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.25),
            (x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.1),
            (x0 + (x1 - x0) * 0.8, y0 + (y1 - y0) * 0.55),
            (x1, y1)], fill=fill, width=6)
    d.polygon([(x1 - 14, y1 - 2), (x1 + 2, y1 - 2), (x1 - 4, y1 + 14)],
              fill=fill)


def chip(d, x, y, s, color, letters):
    d.rounded_rectangle([x, y, x + s, y + s], radius=6, fill=color)
    f = SANS_B(20)
    tw = d.textlength(letters, font=f)
    th = f.size
    d.text((x + (s - tw) / 2, y + (s - th) / 2 - 1), letters, font=f,
           fill=WHITE)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # page margin

    # ---- masthead ------------------------------------------------------
    rule(d, mx, W - mx, 10, 3)
    f = SERIF_B(76)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 16), title, font=f, fill=INK)
    f = SANS_B(21)
    sub = "SATURDAY 21 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS IN ONE IMAGE"
    tw = d.textlength(sub, font=f)
    d.text(((W - tw) / 2, 100), sub, font=f, fill=NAVY)
    rule(d, mx, W - mx, 132, 2)

    # ---- big numbers ---------------------------------------------------
    nums = [
        ("$3.79BN", "GTA VI day-one sales, a record"),
        ("–9%", "Anthropic shares fall after record IPO"),
        ("€1BN", "EU military aid for Ukraine"),
        ("42", "hurt in the Kryvyi Rih strike"),
    ]
    bw = (W - 2 * mx - 3 * 12) / 4
    y = 142
    for i, (big, label) in enumerate(nums):
        x = mx + i * (bw + 12)
        d.rectangle([x, y, x + bw, y + 66], outline=RULE, width=1)
        d.rectangle([x, y, x + bw, y + 5], fill=NAVY)
        f = SERIF_B(28)
        d.text((x + 10, y + 10), big, font=f, fill=RED)
        para(d, x + 10, y + 42, label, SANS(12), GREY, bw - 20, 13)
    # ---- hero lead: the world court ------------------------------------
    y = 222
    rule(d, mx, W - mx, y, 2)
    y += 12
    kicker(d, mx, y, "THE HAGUE  ·  WORLD COURT")
    f = SERIF_B(46)
    head = ["Myanmar guilty", "of genocide"]
    yy = y + 26
    for ln in head:
        d.text((mx, yy), ln, font=f, fill=NAVY)
        yy += 50
    yy += 2
    yy = para(d, mx, yy,
              "The International Court of Justice rules 9–6 that Myanmar "
              "committed genocide against the Rohingya — the first time a "
              "state has ever been found guilty by a world court.",
              SANS(18), INK, 560, 24)
    scales(d, 830, 318, 95)
    d.text((700, 420), "The court in session: nine judges to six.",
           font=SANS_I(14), fill=GREY)
    rule(d, mx, W - mx, 448, 2)

    # ---- second and third leads ----------------------------------------
    y = 464
    # lead 2: Ukraine
    x = mx
    kicker(d, x, y, "UKRAINE  ·  WAR")
    f = SERIF_B(30)
    yy = para(d, x, y + 26,
              "Russia's huge missile barrage hits Kyiv and the west",
              f, INK, 440, 34)
    para(d, x, yy + 4,
         "Overnight strikes kill two and wound 42 in Kryvyi Rih; missiles "
         "cross into Poland, which asks NATO for help.",
         SANS(16), INK, 420, 21)
    burst(d, 490, 545, 30)
    # lead 3: markets
    x = 540
    kicker(d, x, y, "MARKETS  ·  TECH")
    yy = para(d, x, y + 26,
              "Anthropic sinks 9% a day after its record IPO",
              f, INK, 440, 34)
    para(d, x, yy + 4,
         "Shares of the AI lab fall sharply the morning after its "
         "blockbuster listing; GTA VI takes $3.79bn on day one.",
         SANS(16), INK, 360, 21)
    trend_down(d, 925, 560, 985, 608)
    rule(d, mx, W - mx, 618, 2)

    # ---- feature cards --------------------------------------------------
    cards = [
        ("SA", NAVY, "SAUDI ARABIA", "Houthi missile shot down over Riyadh",
         "Debris falls on the capital after the interception."),
        ("UA", TEAL, "UKRAINE TALKS", "US floats NATO entry for Kyiv for land",
         "Membership traded for territory, a report says."),
        ("IN", RED, "INDIA", "Cyclone Akvan slams the Odisha coast",
         "Strong winds and heavy rain as the storm crosses land."),
        ("CY", PLUM, "CYBER", "Hackers hit JPMorgan, Visa, Mastercard",
         "Banks say their payment networks were not affected."),
        ("CL", TEAL, "CLIMATE", "COP31 talks reach their final stage",
         "Fossil fuels and climate cash still divide nations."),
        ("US", NAVY, "UNITED STATES", "Trump pardons baseball's Pete Rose",
         "A posthumous pardon for the late hit king."),
        ("US", RED, "UNITED STATES", "Senate rejects Iran war-powers vote",
         "The bid to curb strikes fails 51–48."),
        ("EU", NAVY, "EUROPE", "EU gives €1bn more arms aid to Kyiv",
         "Britain adds 1,000-plus drones in a £260m package."),
        ("SP", TEAL, "SPORT", "Rahul's ton puts India on top in Wellington",
         "India 247 for 1 on day three against New Zealand."),
        ("EU", PLUM, "EUROPE", "EU and UK agree a youth mobility deal",
         "Ages 18 to 31, capped places, in a new pact."),
    ]
    y = 634
    col_w = (W - 2 * mx - 20) / 2
    row_h = 40
    for i, (tag, color, place, head, body) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = mx + col * (col_w + 20)
        yy = y + row * row_h
        chip(d, x, yy, 34, color, tag)
        f = SANS_B(17)
        d.text((x + 44, yy - 2), head, font=f, fill=INK)
        d.text((x + 44, yy + 18), body, font=SANS(14), fill=GREY)
    rule(d, mx, W - mx, y + 5 * row_h + 4, 2)

    # ---- one-liners ------------------------------------------------------
    y = 848
    f = SANS_B(17)
    d.text((mx, y), "ALSO TODAY", font=f, fill=RED)
    rule(d, mx + 130, W - mx, y + 10, 1, RULE)
    ones = [
        "US sanctions four Iranians over oil money.",
        "US clears ~900,000 AI chips for China in six months.",
        "Trump: close to a Mexico deal; Canada work remains.",
        "Trump threatens a ban on AI data centres abroad.",
        "Tanker struck and ablaze in the Strait of Hormuz.",
        "Argentina backs a disability law, 71–0 in the Senate.",
        "Two Danes charged in a Russian plot to kill a rapper.",
        "Iraq retakes Jurf al-Sakhar after 12 years.",
        "Indian man jailed 19 years in a Sikh leader plot.",
        "South Africa murders fall — still 60 a day.",
        "ECB board race: Boone and Brunnermeier in line.",
        "Hyundai shows the 2027 Elantra at the LA Auto Show.",
        "Sensex rallies nearly 900 points.",
        "Firouzja wins the chess world tour pilot event.",
        "Europe's youth rally over living costs.",
        "India court allows the Deepathoon lamp lighting.",
    ]
    y = 872
    col_w = (W - 2 * mx - 20) / 2
    for i, line in enumerate(ones):
        col = i % 2
        row = i // 2
        x = mx + col * (col_w + 20)
        yy = y + row * 15
        d.text((x, yy), "▪  " + line, font=SANS(14), fill=INK)

    # ---- footer ----------------------------------------------------------
    rule(d, mx, W - mx, 998, 2)
    f = SANS_B(14)
    d.text((mx, 1006),
           "21 NOVEMBER 2026 — first reported today, from the ICJ, NDTV, "
           "BBC, Reuters, AP and PTI · The World Today",
           font=f, fill=NAVY)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    draw()
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
