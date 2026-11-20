#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The Global Edition — Friday 20 November 2026, in one 1024x1024 poster.

Renders a one-page world-news broadsheet with PIL: a masthead, three lead
stories, a dot-matrix world map with one pin per region, sixteen small
illustrated scenes, all 56 numbered stories in seven region columns with
their outlet tags, a UTC timeline, a by-the-numbers strip, a weather strip
and a "left out & why" date-check box.  Every story was published or
reported on 20 November 2026; SOURCES.md in this repository lists each one
with its outlet and verification page.

Deterministic: no clock, no randomness, no network.  Two runs write a
byte-identical entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 243, 234)
INK = (20, 26, 38)
FAINT = (90, 96, 110)
RULE = (20, 26, 38)
RED = (178, 34, 52)
BLUE = (30, 78, 150)
TEAL = (16, 110, 104)
GOLD = (196, 138, 30)
SKY = (214, 228, 240)
PANEL_BG = (238, 233, 220)
CARD = (255, 253, 247)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REGIONS = [
    ("NORTH AMERICA", 1),
    ("LATIN AMERICA", 9),
    ("EUROPE", 17),
    ("MIDDLE EAST", 25),
    ("AFRICA", 33),
    ("ASIA", 41),
    ("OCEANIA", 49),
]

# (number, headline, outlet) — headlines shortened only where the column
# width forces it; wording otherwise follows the day's reports.
STORIES = [
    (1, "Senate rejects Iran war-powers bill, 51-48", "AP"),
    (2, "Trump pardons baseball legend Pete Rose", "AP"),
    (3, "Judge: USDA chief's emails unconstitutional", "AP"),
    (4, "California probes Nvidia over China AI chips", "Guardian"),
    (5, "Florida's record 20th execution of 2026", "AP"),
    (6, "Anthropic soars 17% after record $81.3bn IPO", "Reuters"),
    (7, "Trump back from China; briefing today", "Reuters"),
    (8, "Blood test can spot CTE in living players", "NY Post"),
    (9, "US-Venezuela deal restores military ties", "Reuters"),
    (10, "US details $12bn Venezuelan oil revenue", "AP"),
    (11, "Copa: Venezuela flights 90% full, 47 a week", "Rio Times"),
    (12, "Tesla opens orders in Argentina from today", "Rio Times"),
    (13, "Brazil real hits 19-month low near R$5.93", "Rio Times"),
    (14, "Lima mayor urges Peru election overhaul", "Rio Times"),
    (15, "Haiti: 34 gang suspects killed in Martissant", "Rio Times"),
    (16, "CAF backs Panama journalist after arson", "Rio Times"),
    (17, "Kyiv hit by four ballistic missiles overnight", "Daily Baku"),
    (18, "Genoa airport halts flights over drone", "Daily Baku"),
    (19, "UK-Norway GBP100m+ for Ukraine naval craft", "AP"),
    (20, "Europe ready for Russia talks on war", "Reuters"),
    (21, "Denmark approves Greenland defence deal, 109-0", "AP"),
    (22, "Serbia elects Cupic speaker, 140 votes to 97", "AP"),
    (23, "France braces for 4th weekend of cost protests", "Paris Eye"),
    (24, "Millions strike in Spain over housing", "CBC"),
    (25, "Trump: US to 'see what happens' in Iran war", "Just Security"),
    (26, "US strikes Iranian island in Hormuz", "Inquirer"),
    (27, "Houthis claim strikes on four Saudi targets", "Daily Baku"),
    (28, "Saudi: rebel attack damaged Riyadh tower", "Reuters"),
    (29, "Tanker ablaze after mine hit near Hormuz", "Daily Baku"),
    (30, "Aid groups rate Gaza peace plan 4 out of 26", "AppiSToS"),
    (31, "Four nations urge open Gaza aid routes", "Paris Eye"),
    (32, "Israeli strike hits Hezbollah site in E. Lebanon", "Daily Baku"),
    (33, "Two Sudan forces claim same Blue Nile town", "Rio Times"),
    (34, "Somalia orders UAE envoy out within 72 hours", "Rio Times"),
    (35, "Senegal budget forced through by decree", "Rio Times"),
    (36, "Gabon MPs cut budget by US$376 million", "Rio Times"),
    (37, "Fidelity Bank names Amuchie as next CEO", "Rio Times"),
    (38, "Soweto floods kill one; girl missing", "Rio Times"),
    (39, "S. Africa holds rate as fuel lifts prices", "Rio Times"),
    (40, "Bandits kill one, abduct five in Zamfara raid", "Punch"),
    (41, "Trump-Xi-Putin sign peace declaration", "Reuters"),
    (42, "World Court: Myanmar genocide ruling", "AP"),
    (43, "APEC adopts Shenzhen Outlook on trade, AI", "AppiSToS"),
    (44, "Takaichi dodges Taiwan contingency question", "SimpleLife"),
    (45, "N. Korea expanding Yongbyon plant - IAEA", "AP"),
    (46, "S. Korea court clears ex-PM Han Duck-soo", "AP"),
    (47, "Cyclone Akvan nears Odisha coast", "Times of India"),
    (48, "Indonesia passes asset-forfeiture bill", "AppiSToS"),
    (49, "Nicholls 113* as NZ reach 243/5 vs India", "AP"),
    (50, "Ash Barty picked for Tennis Hall of Fame", "Jagran Josh"),
    (51, "Fiji declares drought disaster, El Nino", "AP"),
    (52, "Cyclone Xavier: alerts for Cook Islands", "AppiSToS"),
    (53, "Monitor: faith reference shows 'fed bias'", "Guardian"),
    (54, "AUKUS: could Australian ships be compelled?", "Guardian"),
    (55, "Physicists beam 'gravity' through brick wall", "Guardian"),
    (56, "PNG-Fiji join wildlife-climate pact", "EIN Presswire"),
]

LEADS = [
    {
        "num": 41,
        "kicker": "SHENZHEN SUMMIT · REUTERS",
        "head": "Trump, Xi and Putin sign a 'peace declaration'",
        "sub": "The three presidents close the APEC summit in Shenzhen with a "
               "joint text; the bloc also adopts its Shenzhen Outlook on "
               "trade and AI.",
        "scene": "flags",
    },
    {
        "num": 42,
        "kicker": "THE HAGUE · AP",
        "head": "World Court: Myanmar committed genocide",
        "sub": "Judges rule 9-6 in Gambia v. Myanmar that the Rohingya "
               "crackdown was genocide, in the court's judgment on the "
               "2017 campaign.",
        "scene": "gavel",
    },
    {
        "num": 6,
        "kicker": "WALL STREET · REUTERS",
        "head": "Anthropic soars 17% after record $81.3bn IPO",
        "sub": "Shares jump 17% in the AI lab's first session after the "
               "largest listing of 2026, a record $81.3bn offering.",
        "scene": "chart",
    },
]

TIMELINE = [
    ("02:00", "Kyiv struck by four ballistic missiles overnight (17)"),
    ("08:00", "World Court delivers its genocide judgment (42)"),
    ("10:00", "'Peace declaration' signed in Shenzhen (41)"),
    ("11:30", "APEC adopts the Shenzhen Outlook (43)"),
    ("14:30", "Anthropic shares open on Wall Street (6)"),
    ("19:00", "White House briefing on the China trip (7)"),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's record IPO"),
    ("9-6", "World Court genocide split"),
    ("51-48", "Senate war-powers vote"),
    ("$12bn", "Venezuelan oil revenue"),
    ("109-0", "Denmark's Greenland vote"),
    ("4 of 26", "Gaza plan, aid groups say"),
]

WEATHER = [
    ("Dubai", "31"), ("Sao Paulo", "32"), ("Singapore", "30"),
    ("Cairo", "29"), ("Sydney", "27"), ("New York", "18"),
    ("Tokyo", "14"), ("London", "9"), ("Seoul", "3"),
]
WATCHES = "Watches: Cyclone Akvan -> Odisha · Cyclone Xavier -> Cook Is. · Soweto floods · Fiji drought"

LEFTOUT = (
    "Date rule: every story was published or reported on 20 Nov 2026. "
    "Excluded: Windows 11 Patch Tuesday (10 Nov - stale); COP31 mangrove "
    "$1bn (18 Nov - outside the window); GTA 6 / Gemini 4 chatter "
    "(single-source roundups, unverified). The 19 Nov summit itself is "
    "kept only because its peace-declaration text landed on the 20th."
)


FONTS = {}


def font(path, size):
    key = (path, size)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(path, size)
    return FONTS[key]


def fit_font(draw, text, path, size, max_w, min_size=8):
    """Largest font at or below size that keeps text inside max_w."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns the list of lines."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# --- dot-matrix world map -------------------------------------------------
# Continent outlines as (lon, lat) polygons, rasterised onto a dot grid.

EURASIA = [
    (-9, 43), (-9, 48), (-2, 50), (3, 52), (8, 54), (8, 57), (5, 58),
    (5, 60), (10, 59), (18, 56), (21, 55), (24, 58), (29, 60), (30, 62),
    (25, 66), (20, 70), (32, 70), (45, 68), (58, 69), (70, 72), (85, 73),
    (100, 76), (112, 74), (125, 73), (140, 72), (152, 70), (165, 70),
    (178, 65), (178, 62), (162, 60), (157, 52), (150, 45), (142, 42),
    (140, 39), (134, 35), (129, 33), (126, 31), (121, 29), (120, 25),
    (114, 22), (108, 17), (106, 9), (103, 5), (100, 8), (98, 13),
    (94, 17), (91, 22), (88, 21), (85, 19), (80, 14), (77, 8), (72, 19),
    (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (50, 26), (55, 24),
    (59, 22), (55, 17), (52, 15), (45, 12), (43, 12), (39, 15), (36, 22),
    (34, 28), (36, 36), (30, 36), (26, 38), (22, 37), (19, 40), (15, 40),
    (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36), (-9, 37),
]
NORTH_AMERICA = [
    (-165, 60), (-150, 60), (-135, 57), (-128, 52), (-124, 46), (-124, 40),
    (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-92, 15),
    (-86, 13), (-83, 9), (-79, 9), (-81, 13), (-84, 16), (-88, 16),
    (-91, 19), (-97, 20), (-97, 24), (-93, 30), (-89, 30), (-84, 30),
    (-81, 26), (-80, 32), (-76, 35), (-74, 39), (-70, 42), (-66, 44),
    (-60, 46), (-65, 50), (-60, 52), (-64, 58), (-68, 58), (-78, 62),
    (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-141, 70),
    (-155, 71), (-165, 68),
]
SOUTH_AMERICA = [
    (-79, 9), (-75, 11), (-70, 12), (-62, 10), (-55, 6), (-50, 0),
    (-44, -3), (-35, -8), (-39, -14), (-40, -22), (-48, -27), (-53, -34),
    (-58, -39), (-63, -42), (-65, -46), (-67, -51), (-69, -54), (-71, -54),
    (-73, -50), (-73, -43), (-72, -36), (-71, -29), (-70, -19), (-75, -15),
    (-79, -8), (-80, -4), (-80, 1), (-77, 5),
]
AFRICA = [
    (-17, 15), (-11, 27), (-6, 35), (3, 37), (10, 37), (19, 32), (30, 31),
    (33, 27), (35, 23), (37, 20), (39, 15), (43, 12), (48, 11), (51, 11),
    (47, 4), (42, -3), (40, -11), (39, -19), (36, -23), (33, -27),
    (29, -32), (20, -35), (17, -32), (15, -27), (13, -19), (12, -14),
    (13, -9), (9, -4), (9, 1), (7, 4), (-2, 5), (-8, 5), (-13, 8),
]
MADAGASCAR = [(43, -12), (47, -14), (50, -18), (48, -23), (45, -25), (44, -19), (43, -15)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 55), (-7, 58), (-4, 58), (-2, 55), (-1, 52), (-4, 50)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44), (140, 42), (138, 37), (135, 34), (131, 32)]
SUMATRA = [(95, 5), (100, 1), (105, -5), (104, -6), (99, 0), (95, 4)]
BORNEO = [(109, 1), (113, 4), (118, 2), (117, -2), (112, -3), (109, -1)]
JAVA = [(106, -6), (114, -7), (114, -9), (106, -8)]
NEW_GUINEA = [(131, -1), (138, -2), (146, -6), (150, -9), (146, -8), (139, -6), (133, -3)]
AUSTRALIA = [
    (113, -22), (114, -29), (115, -34), (119, -35), (125, -33), (130, -32),
    (133, -32), (136, -35), (139, -37), (144, -38), (149, -37), (153, -31),
    (153, -26), (150, -23), (146, -19), (142, -15), (142, -11), (140, -17),
    (136, -15), (135, -12), (132, -11), (129, -13), (125, -15), (121, -18),
    (117, -20),
]
TASMANIA = [(145, -41), (148, -41), (147, -43), (145, -43)]
NEW_ZEALAND = [(167, -45), (170, -44), (172, -42), (174, -40), (176, -38), (174, -36), (172, -40), (169, -43), (167, -46)]

LAND = [
    EURASIA, NORTH_AMERICA, SOUTH_AMERICA, AFRICA, MADAGASCAR, BRITAIN,
    JAPAN, SUMATRA, BORNEO, JAVA, NEW_GUINEA, AUSTRALIA, TASMANIA, NEW_ZEALAND,
]

# (region index, lon, lat) for the seven numbered pins
PINS = [
    (1, -102, 42), (2, -60, -14), (3, 14, 51), (4, 44, 27),
    (5, 20, 4), (6, 96, 33), (7, 134, -27),
]


def draw_map(d, x0, y0, w, h):
    """Rasterise the continent polygons into a dot grid and stamp the pins."""
    grid_w, grid_h = 148, 62
    mask = Image.new("1", (grid_w, grid_h), 0)
    md = ImageDraw.Draw(mask)
    for poly in LAND:
        pts = [
            ((lon + 180) / 360.0 * grid_w, (82 - lat) / 140.0 * grid_h)
            for lon, lat in poly
        ]
        md.polygon(pts, fill=1)
    px = mask.load()
    step_x = w / grid_w
    step_y = h / grid_h
    r = max(1.6, min(step_x, step_y) * 0.30)
    for gy in range(grid_h):
        for gx in range(grid_w):
            if px[gx, gy]:
                cx = x0 + (gx + 0.5) * step_x
                cy = y0 + (gy + 0.5) * step_y
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 128, 145))
    for idx, lon, lat in PINS:
        cx = x0 + (lon + 180) / 360.0 * w
        cy = y0 + (82 - lat) / 140.0 * h
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED, outline=(255, 255, 255), width=2)
        label = str(idx)
        f = font(SANS_B, 13)
        tw = d.textlength(label, font=f)
        d.text((cx - tw / 2, cy - 8), label, font=f, fill=(255, 255, 255))


# --- sixteen illustrated scenes --------------------------------------------
# Each draws inside the box (x, y, w, h) with flat shapes only.

def scene_flags(d, x, y, w, h):
    for i, col in enumerate((RED, GOLD, BLUE)):
        px = x + w * (0.22 + 0.26 * i)
        d.line([px, y + 6, px, y + h - 4], fill=INK, width=2)
        d.polygon([(px, y + 6), (px + 16, y + 10), (px, y + 15)], fill=col)
    d.line([x + 6, y + h - 4, x + w - 6, y + h - 4], fill=INK, width=2)


def scene_gavel(d, x, y, w, h):
    d.polygon([(x + w * 0.30, y + h * 0.28), (x + w * 0.62, y + h * 0.60),
               (x + w * 0.52, y + h * 0.72), (x + w * 0.20, y + h * 0.40)], fill=GOLD)
    d.rectangle([x + w * 0.16, y + h * 0.16, x + w * 0.36, y + h * 0.30], fill=INK)
    d.rectangle([x + w * 0.52, y + h * 0.60, x + w * 0.72, y + h * 0.74], fill=INK)
    d.rectangle([x + w * 0.18, y + h * 0.84, x + w * 0.82, y + h * 0.90], fill=INK)


def scene_chart_up(d, x, y, w, h):
    pts = [(x + 8, y + h - 10), (x + w * 0.38, y + h * 0.58),
           (x + w * 0.58, y + h * 0.66), (x + w - 14, y + 12)]
    d.line(pts, fill=TEAL, width=3)
    d.polygon([(x + w - 14, y + 12), (x + w - 26, y + 14), (x + w - 15, y + 24)], fill=TEAL)
    for i in range(3):
        bx = x + 12 + i * (w * 0.24)
        d.rectangle([bx, y + h - 8 - (i + 1) * 7, bx + 10, y + h - 6], fill=SKY)


def scene_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 52))
    for sx, sy in ((0.15, 0.2), (0.4, 0.12), (0.68, 0.22), (0.85, 0.14), (0.55, 0.3)):
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(255, 255, 255))
    d.polygon([(x + w * 0.62, y + h * 0.66), (x + w * 0.78, y + h * 0.30),
               (x + w * 0.84, y + h * 0.36), (x + w * 0.70, y + h * 0.70)], fill=(230, 230, 235))
    d.polygon([(x + w * 0.60, y + h * 0.70), (x + w * 0.52, y + h * 0.84),
               (x + w * 0.66, y + h * 0.78)], fill=GOLD)
    d.rectangle([x, y + h - 9, x + w, y + h], fill=(10, 12, 20))
    for bx in range(4):
        d.rectangle([x + 6 + bx * (w // 4), y + h - 16, x + 16 + bx * (w // 4), y + h - 9], fill=(10, 12, 20))


def scene_cyclone(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    for rr, start in ((w * 0.36, 20), (w * 0.26, 140), (w * 0.16, 260)):
        d.arc([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8], start, start + 230, fill=BLUE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def scene_senate(d, x, y, w, h):
    d.polygon([(x + 8, y + 8), (x + w - 8, y + 8), (x + w / 2, y + 1)], fill=INK)
    for i in range(5):
        cx = x + 12 + i * ((w - 24) / 4)
        d.rectangle([cx - 2, y + 12, cx + 2, y + h - 12], fill=INK)
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 6], fill=INK)


def scene_car(d, x, y, w, h):
    d.polygon([(x + 8, y + h * 0.62), (x + w * 0.24, y + h * 0.60), (x + w * 0.38, y + h * 0.38),
               (x + w * 0.66, y + h * 0.38), (x + w * 0.80, y + h * 0.60), (x + w - 8, y + h * 0.64),
               (x + w - 8, y + h * 0.74), (x + 8, y + h * 0.74)], fill=RED)
    d.polygon([(x + w * 0.42, y + h * 0.44), (x + w * 0.62, y + h * 0.44),
               (x + w * 0.72, y + h * 0.58), (x + w * 0.40, y + h * 0.58)], fill=SKY)
    for wx in (0.28, 0.74):
        d.ellipse([x + w * wx - 7, y + h * 0.68, x + w * wx + 7, y + h * 0.68 + 14], fill=INK)
        d.ellipse([x + w * wx - 3, y + h * 0.68 + 4, x + w * wx + 3, y + h * 0.68 + 10], fill=(200, 200, 200))


def scene_tanker(d, x, y, w, h):
    d.polygon([(x + 8, y + h * 0.58), (x + w - 16, y + h * 0.58), (x + w - 26, y + h * 0.74),
               (x + 16, y + h * 0.74)], fill=INK)
    d.rectangle([x + w * 0.30, y + h * 0.44, x + w * 0.62, y + h * 0.58], fill=FAINT)
    d.polygon([(x + w * 0.44, y + h * 0.42), (x + w * 0.50, y + h * 0.18),
               (x + w * 0.56, y + h * 0.42)], fill=(232, 110, 30))
    d.polygon([(x + w * 0.47, y + h * 0.42), (x + w * 0.50, y + h * 0.28),
               (x + w * 0.53, y + h * 0.42)], fill=GOLD)
    for i in range(3):
        d.arc([x + 6 + i * (w // 3), y + h * 0.76, x + 26 + i * (w // 3), y + h * 0.92], 0, 180, fill=BLUE, width=2)


def scene_cricket(d, x, y, w, h):
    d.polygon([(x + w * 0.30, y + h - 8), (x + w * 0.40, y + h - 8),
               (x + w * 0.62, y + 10), (x + w * 0.54, y + 6)], fill=GOLD)
    d.ellipse([x + w * 0.68, y + h * 0.52, x + w * 0.68 + 13, y + h * 0.52 + 13], fill=RED)
    for i in range(3):
        sx = x + w * 0.14 + i * 6
        d.line([sx, y + h - 20, sx, y + h - 6], fill=INK, width=2)


def scene_island(d, x, y, w, h):
    d.ellipse([x + 8, y + h * 0.66, x + w - 8, y + h * 0.86], fill=(232, 205, 140))
    px = x + w / 2
    d.line([px, y + h * 0.70, px, y + h * 0.30], fill=(110, 74, 30), width=3)
    for ang in (-40, -12, 16, 42):
        import math as _m
        ex = px + 20 * _m.cos(_m.radians(ang - 90))
        ey = y + h * 0.30 + 15 * _m.sin(_m.radians(ang - 90))
        d.line([px, y + h * 0.30, ex, ey], fill=TEAL, width=3)
    d.arc([x + w * 0.66, y + 4, x + w * 0.66 + 22, y + 24], 90, 320, fill=BLUE, width=2)


def scene_shield(d, x, y, w, h):
    cx = x + w / 2
    d.polygon([(cx - 18, y + 6), (cx + 18, y + 6), (cx + 18, y + h * 0.5),
               (cx, y + h - 6), (cx - 18, y + h * 0.5)], fill=RED)
    d.rectangle([cx - 4, y + 10, cx + 4, y + h * 0.62], fill=(255, 255, 255))
    d.rectangle([cx - 14, y + h * 0.26, cx + 14, y + h * 0.26 + 7], fill=(255, 255, 255))


def scene_flood(d, x, y, w, h):
    d.polygon([(x + w * 0.32, y + 8), (x + w * 0.68, y + 8), (x + w / 2, y + 1)], fill=INK)
    d.rectangle([x + w * 0.36, y + 10, x + w * 0.64, y + h * 0.58], fill=PANEL_BG, outline=INK)
    for r in range(3):
        for i in range(3):
            d.arc([x + 6 + i * (w // 3), y + h * (0.60 + 0.12 * r), x + 26 + i * (w // 3),
                   y + h * (0.72 + 0.12 * r)], 180, 360, fill=BLUE, width=2)


def scene_beam(d, x, y, w, h):
    for r in range(3):
        for c in range(3):
            bx = x + w * 0.52 + c * 13
            by = y + 6 + r * ((h - 12) // 3)
            d.rectangle([bx, by, bx + 11, by + (h - 16) // 3], outline=INK)
    d.polygon([(x + 6, y + h * 0.42), (x + w * 0.56, y + h * 0.50), (x + w * 0.56, y + h * 0.58),
               (x + 6, y + h * 0.60)], fill=GOLD)
    d.ellipse([x + 2, y + h * 0.40, x + 12, y + h * 0.62], fill=RED)


def scene_baseball(d, x, y, w, h):
    cx, cy = x + w * 0.36, y + h * 0.48
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255), outline=INK, width=2)
    d.arc([cx - 12, cy - 13, cx + 2, cy + 13], 300, 60, fill=RED, width=2)
    d.arc([cx - 2, cy - 13, cx + 12, cy + 13], 120, 240, fill=RED, width=2)
    d.polygon([(x + w * 0.60, y + h - 8), (x + w * 0.68, y + h - 8),
               (x + w - 8, y + 8), (x + w - 14, y + 5)], fill=(150, 100, 50))


def scene_aid(d, x, y, w, h):
    d.rectangle([x + 8, y + h * 0.34, x + w * 0.62, y + h * 0.68], fill=TEAL)
    d.polygon([(x + w * 0.62, y + h * 0.46), (x + w * 0.80, y + h * 0.46),
               (x + w * 0.88, y + h * 0.68), (x + w * 0.62, y + h * 0.68)], fill=TEAL)
    cx, cy = x + w * 0.34, y + h * 0.51
    d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=(255, 255, 255))
    d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=(255, 255, 255))
    for wx in (0.24, 0.72):
        d.ellipse([x + w * wx - 6, y + h * 0.62, x + w * wx + 6, y + h * 0.62 + 12], fill=INK)


def scene_chart_down(d, x, y, w, h):
    pts = [(x + 8, y + 10), (x + w * 0.38, y + h * 0.36),
           (x + w * 0.58, y + h * 0.30), (x + w - 14, y + h - 12)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(x + w - 14, y + h - 12), (x + w - 26, y + h - 14), (x + w - 15, y + h - 24)], fill=RED)
    f = font(SANS_B, 13)
    d.text((x + 8, y + h - 18), "R$", font=f, fill=INK)


SCENES = {
    "flags": scene_flags, "gavel": scene_gavel, "chart": scene_chart_up,
    "missile": scene_missile, "cyclone": scene_cyclone, "senate": scene_senate,
    "car": scene_car, "tanker": scene_tanker, "cricket": scene_cricket,
    "island": scene_island, "shield": scene_shield, "flood": scene_flood,
    "beam": scene_beam, "baseball": scene_baseball, "aid": scene_aid,
    "chart_down": scene_chart_down,
}

# (story number, scene key, caption)
PANELS = [
    (41, "flags", "Shenzhen summit"), (42, "gavel", "World Court rules"),
    (6, "chart", "Anthropic IPO +17%"), (17, "missile", "Kyiv missile night"),
    (47, "cyclone", "Cyclone Akvan"), (1, "senate", "Senate 51-48"),
    (12, "car", "Tesla in Argentina"), (29, "tanker", "Hormuz tanker fire"),
    (49, "cricket", "Nicholls 113*"), (52, "island", "Cyclone Xavier"),
    (21, "shield", "Greenland deal"), (38, "flood", "Soweto floods"),
    (55, "beam", "'Gravity' beamed"), (2, "baseball", "Pete Rose pardoned"),
    (30, "aid", "Gaza plan: 4 of 26"), (13, "chart_down", "Real at 19-mo low"),
]


# --- page assembly ----------------------------------------------------------

MARGIN = 24
CONTENT_W = W - 2 * MARGIN


def masthead(d):
    d.text((MARGIN, 12), "ONE IMAGE · ONE DAY · EVERY STORY SOURCED",
           font=font(SANS_B, 10), fill=RED)
    d.text((MARGIN, 26), "THE GLOBAL EDITION", font=font(SERIF_B, 41), fill=INK)
    right1 = "FRIDAY 20 NOVEMBER 2026"
    f = font(SANS_B, 15)
    d.text((W - MARGIN - d.textlength(right1, font=f), 30), right1, font=f, fill=INK)
    right2 = "56 stories · 7 regions · 16 pictures"
    f2 = font(SANS, 11)
    d.text((W - MARGIN - d.textlength(right2, font=f2), 52), right2, font=f2, fill=FAINT)
    right3 = "The world in one day"
    d.text((W - MARGIN - d.textlength(right3, font=f2), 68), right3, font=f2, fill=FAINT)
    d.rectangle([MARGIN, 90, W - MARGIN, 93], fill=RED)
    d.rectangle([MARGIN, 96, W - MARGIN, 97], fill=INK)


def lead_cards(d):
    y0, h = 104, 188
    card_w = (CONTENT_W - 24) // 3
    for i, lead in enumerate(LEADS):
        x = MARGIN + i * (card_w + 12)
        d.rectangle([x, y0, x + card_w, y0 + h], fill=CARD, outline=INK, width=1)
        d.rectangle([x, y0, x + card_w, y0 + 4], fill=RED)
        d.text((x + 10, y0 + 10), lead["kicker"], font=font(SANS_B, 9), fill=RED)
        badge = str(lead["num"])
        bf = font(SANS_B, 12)
        bw = d.textlength(badge, font=bf)
        d.ellipse([x + card_w - 30, y0 + 8, x + card_w - 8, y0 + 30], fill=INK)
        d.text((x + card_w - 19 - bw / 2, y0 + 13), badge, font=bf, fill=(255, 255, 255))
        SCENES[lead["scene"]](d, x + 10, y0 + 30, card_w - 20, 52)
        head_f = font(SERIF_B, 16)
        lines = wrap(d, lead["head"], head_f, card_w - 20)[:3]
        ly = y0 + 88
        for line in lines:
            d.text((x + 10, ly), line, font=head_f, fill=INK)
            ly += 19
        sub_f = font(SANS, 10)
        for line in wrap(d, lead["sub"], sub_f, card_w - 20)[:4]:
            d.text((x + 10, ly + 2), line, font=sub_f, fill=FAINT)
            ly += 13


def map_band(d):
    y0, h = 300, 182
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + h], outline=INK, width=1)
    d.text((MARGIN + 10, y0 + 7), "WHERE IT HAPPENED — ONE PIN PER REGION",
           font=font(SANS_B, 10), fill=INK)
    draw_map(d, MARGIN + 12, y0 + 28, 606, 142)
    key_x = MARGIN + 646
    notes = [
        "Senate, Rose pardon, Anthropic",
        "Venezuela deals, Tesla, Haiti",
        "Kyiv missiles, Greenland 109-0",
        "Hormuz strikes, Gaza plan",
        "Sudan, Somalia envoy, Soweto",
        "Shenzhen summit, World Court",
        "Cricket, cyclones, Fiji drought",
    ]
    for i, (name, first) in enumerate(REGIONS):
        ry = y0 + 32 + i * 20
        d.ellipse([key_x, ry, key_x + 15, ry + 15], fill=RED)
        nf = font(SANS_B, 9)
        num = str(i + 1)
        d.text((key_x + 7.5 - d.textlength(num, font=nf) / 2, ry + 2), num,
               font=nf, fill=(255, 255, 255))
        d.text((key_x + 21, ry + 1), name, font=font(SANS_B, 10), fill=INK)
        rng = "%d-%d" % (first, first + 7)
        d.text((key_x + 128, ry + 1), rng, font=font(SANS, 9), fill=RED)
        d.text((key_x + 160, ry + 1), notes[i], font=font(SANS, 9), fill=FAINT)


def panel_grid(d):
    y0 = 492
    d.text((MARGIN, y0), "THE DAY IN PICTURES — SIXTEEN SCENES FROM THE STORIES",
           font=font(SANS_B, 10), fill=INK)
    cell_w = (CONTENT_W - 7 * 6) // 8
    for idx, (num, scene, caption) in enumerate(PANELS):
        row, col = divmod(idx, 8)
        x = MARGIN + col * (cell_w + 6)
        y = y0 + 16 + row * 58
        d.rectangle([x, y, x + cell_w, y + 38], fill=PANEL_BG, outline=(190, 184, 168))
        SCENES[scene](d, x + 4, y + 3, cell_w - 8, 32)
        nf = font(SANS_B, 9)
        d.text((x + 2, y + 41), str(num), font=nf, fill=RED)
        cap = fit_font(d, caption, SANS, 9, cell_w - 16)
        d.text((x + 15, y + 41), caption, font=cap, fill=INK)


def story_columns(d):
    y0 = 628
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 2], fill=INK)
    d.text((MARGIN, y0 + 5),
           "THE DAY IN 56 STORIES — EVERY ITEM PUBLISHED OR REPORTED ON 20 NOV 2026 · OUTLET AFTER EACH STORY",
           font=font(SANS_B, 10), fill=INK)
    col_w = (CONTENT_W - 3 * 8) // 4
    by_num = {n: (head, outlet) for n, head, outlet in STORIES}
    layout = [(0, 1), (2, 3), (4, 5), (6, None)]  # region indexes per column
    for c, pair in enumerate(layout):
        x = MARGIN + c * (col_w + 8)
        y = y0 + 24
        for region_idx in pair:
            if region_idx is None:
                # left-out box under Oceania in the last column
                d.rectangle([x, y, x + col_w, y + 112], fill=(243, 236, 222), outline=INK)
                d.text((x + 7, y + 5), "LEFT OUT — AND WHY", font=font(SANS_B, 10), fill=RED)
                lf = font(SANS, 9)
                ly = y + 20
                for line in wrap(d, LEFTOUT, lf, col_w - 14):
                    d.text((x + 7, ly), line, font=lf, fill=INK)
                    ly += 11.5
                continue
            name, first = REGIONS[region_idx]
            d.rectangle([x, y, x + col_w, y + 15], fill=INK)
            d.text((x + 6, y + 2), "%s   %d-%d" % (name, first, first + 7),
                   font=font(SANS_B, 9), fill=(255, 255, 255))
            ly = y + 19
            for n in range(first, first + 8):
                head, outlet = by_num[n]
                nf = font(SANS_B, 9)
                d.text((x, ly), str(n), font=nf, fill=RED)
                num_w = d.textlength(str(n), font=nf) + 4
                tag = " · " + outlet.upper()
                tf = font(SANS_B, 7)
                tag_w = d.textlength(tag, font=tf)
                hf = fit_font(d, head, SANS, 10, col_w - num_w - tag_w, min_size=7)
                d.text((x + num_w, ly), head, font=hf, fill=INK)
                head_w = d.textlength(head, font=hf)
                d.text((x + num_w + head_w, ly + 1), tag, font=tf, fill=FAINT)
                ly += 12
            y += 112 + 5


def bottom_strips(d):
    y0, h = 884, 86
    boxes = [(MARGIN, 400), (MARGIN + 412, 252), (MARGIN + 676, 300)]
    # timeline
    x, w = boxes[0]
    d.rectangle([x, y0, x + w, y0 + h], outline=INK)
    d.text((x + 8, y0 + 5), "THE DAY IN UTC", font=font(SANS_B, 10), fill=RED)
    ly = y0 + 20
    for stamp, what in TIMELINE:
        d.text((x + 8, ly), stamp, font=font(SANS_B, 9), fill=INK)
        wf = fit_font(d, what, SANS, 9, w - 52)
        d.text((x + 46, ly), what, font=wf, fill=INK)
        ly += 11
    # by the numbers
    x, w = boxes[1]
    d.rectangle([x, y0, x + w, y0 + h], outline=INK)
    d.text((x + 8, y0 + 5), "BY THE NUMBERS", font=font(SANS_B, 10), fill=RED)
    ly = y0 + 20
    for value, label in NUMBERS:
        d.text((x + 8, ly), value, font=font(SANS_B, 9), fill=BLUE)
        vw = d.textlength(value, font=font(SANS_B, 9))
        lf = fit_font(d, label, SANS, 9, w - 20 - vw)
        d.text((x + 14 + vw, ly), label, font=lf, fill=INK)
        ly += 11
    # weather
    x, w = boxes[2]
    d.rectangle([x, y0, x + w, y0 + h], outline=INK)
    d.text((x + 8, y0 + 5), "WEATHER — 20 NOV HIGHS °C", font=font(SANS_B, 10), fill=RED)
    ly = y0 + 20
    for r in range(3):
        for c in range(3):
            city, temp = WEATHER[r * 3 + c]
            cx = x + 8 + c * ((w - 16) // 3)
            d.text((cx, ly), city, font=font(SANS, 9), fill=INK)
            tw = d.textlength(city, font=font(SANS, 9))
            d.text((cx + tw + 4, ly), temp + "°", font=font(SANS_B, 9), fill=BLUE)
        ly += 12
    wf = font(SANS, 8)
    for line in wrap(d, WATCHES, wf, w - 16)[:2]:
        d.text((x + 8, ly + 1), line, font=wf, fill=FAINT)
        ly += 10


def footer(d):
    d.rectangle([MARGIN, 980, W - MARGIN, 981], fill=INK)
    line1 = "Sources: SOURCES.md in this repository lists every story with its outlet and verification page · Weather: Darwin-Prediction-Weather, issued 19 Nov 00:40 UTC"
    f1 = fit_font(d, line1, SANS, 9, CONTENT_W)
    d.text(((W - d.textlength(line1, font=f1)) / 2, 986), line1, font=f1, fill=FAINT)
    line2 = "THE GLOBAL EDITION — drawn by program, no photographs · Friday 20 November 2026"
    f2 = font(SANS_B, 9)
    d.text(((W - d.textlength(line2, font=f2)) / 2, 1000), line2, font=f2, fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead_cards(d)
    map_band(d)
    panel_grid(d)
    story_columns(d)
    bottom_strips(d)
    footer(d)
    return img


def main():
    import os
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    render().save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
