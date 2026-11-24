#!/usr/bin/env python3
"""Draw the front page for news-image-20261124 (rebuild r2).

A one-page newspaper summing up Tuesday 24 November 2026: masthead,
one dominant lead (Nvidia / Huang), four features, a dotted world map
with 12 numbered pins, region briefs, and an honest date-check box.

Written from scratch in this session. Run: python3 generate_image.py
writes entry.png next to this file (override with OUT=/path).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 244, 236)
INK = (18, 18, 18)
RED = (178, 32, 44)
BLUE = (31, 73, 125)
GREY = (105, 102, 94)
FAINT = (233, 229, 218)
ORANGE = (204, 102, 0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, width):
    """Greedy word wrap; returns a list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, s, f, width, fill=INK, leading=4):
    """Draw a wrapped paragraph; return the y just below it."""
    lh = f.size + leading
    for line in wrap(draw, s, f, width):
        draw.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, s, fill=RED):
    f = font(SANS_B, 13)
    draw.text((x, y), s, font=f, fill=fill)
    return y + 19


# ---------------------------------------------------------------- map
# Coarse world map, 48 columns x 22 rows, '#' = land. Drawn as dots.
MAP_ROWS = [
    ".........................######.................",
    "....######......##......##################......",
    "...##########...###...######################....",
    "..############..###..#########################..",
    "..#############.###..#####.##################.#.",
    "...############.....#####..########.############",
    "....##########......######.######..########.####",
    "....##########......#######.#####...######..###.",
    ".....#########......################.#####..##..",
    ".....########.......#################.####..#...",
    "......######.........###############..###......",
    ".......####..##.......#############...##.......",
    "........#########......##########..............",
    ".........########.......########...............",
    ".........########.......#######.....####.......",
    "..........######........######....########.....",
    "..........#####..........####....##########....",
    "...........####..........###.....########......",
    "...........###....................######......",
    "............##.....................####.......",
    "............#..................................",
    "...............................................",
]
MAP_COLS = max(len(r) for r in MAP_ROWS)


def draw_map(draw, x0, y0, cell, pins):
    """Dotted land map with numbered red pins. pins: [(col,row,label)]"""
    dot = max(1, cell // 2 - 1)
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx = x0 + c * cell + cell // 2
                cy = y0 + r * cell + cell // 2
                draw.ellipse([cx - dot, cy - dot, cx + dot, cy + dot],
                             fill=(70, 70, 66))
    pf = font(SANS_B, 11)
    for col, row, label in pins:
        cx = x0 + col * cell + cell // 2
        cy = y0 + row * cell + cell // 2
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                     outline=PAPER, width=2)
        tw = text_w(draw, label, pf)
        draw.text((cx - tw / 2, cy - 7), label, font=pf, fill=(255, 255, 255))


def icon_globe_crack(draw, x, y, s):
    draw.ellipse([x, y, x + s, y + s], outline=INK, width=3)
    draw.arc([x + 6, y + 6, x + s - 6, y + s - 6], 200, 330, fill=INK, width=2)
    draw.line([(x + s * 0.55, y + 2), (x + s * 0.42, y + s * 0.4),
               (x + s * 0.6, y + s * 0.62), (x + s * 0.45, y + s - 2)],
              fill=RED, width=3)


def icon_ship(draw, x, y, s):
    draw.polygon([(x + 2, y + s * 0.55), (x + s - 2, y + s * 0.55),
                  (x + s * 0.78, y + s - 4), (x + s * 0.22, y + s - 4)],
                 fill=BLUE)
    draw.line([(x + s * 0.5, y + s * 0.55), (x + s * 0.5, y + 4)],
              fill=INK, width=3)
    draw.polygon([(x + s * 0.5, y + 4), (x + s * 0.82, y + s * 0.3),
                  (x + s * 0.5, y + s * 0.3)], fill=RED)
    for i in range(3):
        yy = y + s - 2 + i * 0  # waterline ticks below hull
        draw.line([(x + 4 + i * 12, y + s + 2), (x + 12 + i * 12, y + s + 2)],
                  fill=BLUE, width=2)


def icon_flame(draw, x, y, s):
    draw.polygon([(x + s * 0.5, y + 2), (x + s * 0.82, y + s * 0.45),
                  (x + s * 0.68, y + s * 0.62), (x + s * 0.78, y + s - 4),
                  (x + s * 0.22, y + s - 4), (x + s * 0.32, y + s * 0.62),
                  (x + s * 0.18, y + s * 0.45)], fill=ORANGE)
    draw.polygon([(x + s * 0.5, y + s * 0.45), (x + s * 0.64, y + s * 0.7),
                  (x + s * 0.5, y + s - 6), (x + s * 0.36, y + s * 0.7)],
                 fill=(255, 214, 64))


def icon_drop(draw, x, y, s):
    draw.polygon([(x + s * 0.5, y + 2), (x + s * 0.8, y + s * 0.55),
                  (x + s * 0.2, y + s * 0.55)], fill=INK)
    draw.ellipse([x + s * 0.2, y + s * 0.42, x + s * 0.8, y + s - 2],
                 fill=INK)
    draw.text((x + s * 0.5 - 6, y + s * 0.55), "$",
              font=font(SANS_B, 16), fill=PAPER)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28                      # side margin
    rx = W - mx                  # right edge of text block

    # ---- masthead ----
    name_f = font(SERIF_B, 46)
    name = "THE WORLD IN ONE PAGE"
    d.text(((W - text_w(d, name, name_f)) / 2, 24), name, font=name_f,
           fill=INK)
    date_f = font(SANS_B, 21)
    date_s = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - text_w(d, date_s, date_f)) / 2, 78), date_s, font=date_f,
           fill=RED)
    sub_f = font(SANS, 13)
    sub = "One day's world news  ·  Every region, every field  ·  Read it in one image"
    d.text(((W - text_w(d, sub, sub_f)) / 2, 106), sub, font=sub_f,
           fill=GREY)
    rule(d, mx, 126, rx, 3)
    rule(d, mx, 131, rx, 1)

    # ---- lead ----
    y = 142
    y = kicker(d, mx, y, "MARKETS  ·  TECHNOLOGY  ·  THE DAY'S BIGGEST STORY")
    head_f = font(SERIF_B, 62)
    d.text((mx, y), "HUANG IS BACK", font=head_f, fill=INK)
    y += 70
    deck_f = font(SERIF, 19)
    deck = ("Nvidia reinstates Jensen Huang as chief executive, 11 days after "
            "he resigned — and Wall Street roars back.")
    y = para(d, mx, y, deck, deck_f, 640, leading=3)
    y += 4
    body_f = font(SANS, 14)
    body = ("The board voted unanimously on Monday after talks with senior US "
            "officials; President Trump said he \"convinced\" the board. "
            "Hours later the Commerce Department blacklisted Megaspeed, the "
            "Singapore chip firm at the centre of the espionage scandal.")
    y = para(d, mx, y, body, body_f, 640, leading=4)
    # lead chart, right side
    cx0, cy0 = 716, 168
    d.rectangle([cx0 - 10, cy0 - 12, rx + 2, cy0 + 132], outline=GREY,
                width=1)
    d.text((cx0, cy0 - 6), "MONDAY'S REBOUND", font=font(SANS_B, 12),
           fill=INK)
    bars = [("NVDA", "+31%", 1.00), ("NASDAQ", "+6.4%", 0.42),
            ("S&P 500", "+5.0%", 0.35)]
    by = cy0 + 16
    for name_b, val, frac in bars:
        d.text((cx0, by), name_b, font=font(SANS_B, 12), fill=INK)
        d.text((cx0 + 168, by), val, font=font(SANS_B, 12), fill=BLUE)
        d.rectangle([cx0, by + 16, cx0 + 230, by + 24], fill=FAINT)
        d.rectangle([cx0, by + 16, cx0 + int(230 * frac), by + 24],
                    fill=BLUE)
        by += 32
    d.text((cx0, by + 2), "Nvidia's best day in 23 years",
           font=font(SANS, 11), fill=GREY)
    rule(d, mx, 340, rx, 1, fill=GREY)

    # ---- features, 2 x 2 ----
    feats = [
        ("CLIMATE  ·  ANTALYA", "COP31 COLLAPSES",
         "No deal after the longest climate talks in history. The EU and "
         "island states refused a pact that never mentions fossil fuels; "
         "petrostates blocked it. First COP breakdown since Copenhagen 2009.",
         icon_globe_crack),
        ("WAR  ·  UKRAINE", "UKRAINE'S SEA WAR SPREADS",
         "Kyiv claims a Russian warship sunk off Libya; a Russian cargo "
         "ship burns off Finland. A drone strike on Dymer, in the Kyiv "
         "region, kills 11 — a boy is pulled alive from the rubble.",
         icon_ship),
        ("DISASTER  ·  INDONESIA", "BANTEN FIRE: 24 DEAD",
         "Rescuers resume the search at the burnt-out Milkita candy "
         "factory in Serang; about 30 workers are still missing. DNA "
         "identification of the victims will take weeks.",
         icon_flame),
        ("MIDDLE EAST  ·  ENERGY", "IRAN HITS BACK, SUES FOR $290BN",
         "Tehran steps up strikes on Gulf sites as a US naval blockade "
         "and new sanctions squeeze the country; Washington targets "
         "Iran's \"shadow banking\" networks.",
         icon_drop),
    ]
    fx = [mx, 524]
    fy = [352, 468]
    for i, (kick, head, text, icon) in enumerate(feats):
        x0 = fx[i % 2]
        y0 = fy[i // 2]
        d.rectangle([x0, y0, x0 + 472, y0 + 108], outline=GREY, width=1)
        icon(d, x0 + 12, y0 + 12, 44)
        kicker(d, x0 + 68, y0 + 10, kick)
        d.text((x0 + 68, y0 + 30), head, font=font(SERIF_B, 19), fill=INK)
        para(d, x0 + 12, y0 + 58, text, font(SANS, 12), 448, leading=2)

    # ---- world map + pins ----
    y = 590
    rule(d, mx, y - 6, rx, 1, fill=GREY)
    y = kicker(d, mx, y, "THE WORLD AT A GLANCE  ·  12 STORIES ON THE MAP")
    map_x, map_y, cell = mx, y + 4, 6
    pins = [
        (21, 6, "1"), (24, 4, "2"), (28, 3, "3"), (25, 8, "4"),
        (28, 7, "5"), (27, 13, "6"), (21, 10, "7"), (42, 6, "8"),
        (34, 8, "9"), (38, 9, "10"), (10, 12, "11"), (7, 10, "12"),
    ]
    draw_map(d, map_x, map_y, cell, pins)
    pin_text = [
        ("1", "LISBON — Thousands march over living costs."),
        ("2", "BRUSSELS — EU proposes 22nd Russia sanctions."),
        ("3", "KYIV REGION — Drone strike kills 11 in Dymer."),
        ("4", "BENGHAZI — Russian corvette ablaze in port."),
        ("5", "GAZA — Oxfam: war poisons air, soil, water."),
        ("6", "ZANZIBAR — Fire engulfs beachfront hotels."),
        ("7", "SENEGAL — Migrant boat capsizes; dozens lost."),
        ("8", "SEOUL — Russian jets enter air defence zone."),
        ("9", "AYODHYA–JANAKPUR — India–Nepal rail link opens."),
        ("10", "YANGON — 14 nations back ICJ genocide ruling."),
        ("11", "COLOMBIA — Drone hits police base; infant hurt."),
        ("12", "PANAMA — Talks to reopen Cobre mine resume."),
    ]
    lx = 340
    ly = y + 2
    pf = font(SANS, 11)
    for j, (num, txt) in enumerate(pin_text):
        xx = lx + (j // 6) * 328
        yy = ly + (j % 6) * 22
        d.text((xx, yy), num + ".", font=font(SANS_B, 11), fill=RED)
        d.text((xx + 24, yy), txt, font=pf, fill=INK)

    # ---- region briefs ----
    y = 764
    rule(d, mx, y - 6, rx, 1, fill=GREY)
    cols = [
        ("EUROPE", [
            "NATO: Putin could strike before Europe responds.",
            "Spain: right ahead in polls before Sunday's vote.",
            "Germans reject choosing between the US and China.",
        ]),
        ("ASIA-PACIFIC", [
            "Taliban erase women's names from papers in Balkh.",
            "India's oil import bill jumps ~60% on dearer crude.",
            "Ferrari unveils two new 296 models in Spain.",
        ]),
        ("AMERICAS", [
            "Trump assails Newsom and Democrats in crime speech.",
            "Virginia & Oregon sue SpaceX over Grok imagery.",
            "Trump halts Army explosives detonation in Iowa.",
        ]),
        ("AFRICA & MIDDLE EAST", [
            "West Bank settler arson called \"Jewish terrorism\".",
            "Sudan says it downed drones aimed at Khartoum.",
            "Israel rivals clash over the Iran threat.",
        ]),
        ("SPORT", [
            "Pant hits 128 as India bat v New Zealand.",
            "Verstappen wins the Las Vegas Grand Prix.",
        ]),
        ("MARKETS & TECH", [
            "SK hynix US shares surge 20% on Huang's return.",
            "Waymo pulls driverless taxis off US freeways.",
            "SpiceJet crisis deepens; pilots demand action.",
        ]),
    ]
    cw = 312
    for i, (title, items) in enumerate(cols):
        x0 = mx + (i % 3) * (cw + 12)
        y0 = y + (i // 3) * 76
        d.text((x0, y0), title, font=font(SANS_B, 12), fill=BLUE)
        yy = y0 + 16
        for it in items:
            for line in wrap(d, "• " + it, font(SANS, 11), cw):
                d.text((x0, yy), line, font=font(SANS, 11), fill=INK)
                yy += 14

    # ---- date check + footer ----
    y = 912
    d.rectangle([mx, y, rx, y + 44], outline=RED, width=1)
    d.text((mx + 8, y + 5), "DATE CHECK",
           font=font(SANS_B, 11), fill=RED)
    dc = ("Checked against reporting of Tue 24 Nov 2026. COP31's collapse was Sunday's closing "
          "plenary; the Banten fire began Saturday (24 deaths confirmed Monday). Excluded as older "
          "news: ICJ Myanmar ruling (19 Nov), Kerch Bridge strike (17 Nov), APEC Shenzhen (21 Nov).")
    para(d, mx + 96, y + 5, dc, font(SANS, 11), rx - mx - 104, leading=1)
    foot = ("Sources: CNN · Reuters · AP · BBC · Bloomberg · Barron's · The Times · NY Post · BusinessWorld · "
            "Jagran Josh  —  Drawn by an AI agent for make.fun's news-image-20261124")
    d.text((mx, 968), foot, font=font(SANS, 10), fill=GREY)
    return img


def main():
    out = os.environ.get("OUT") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
