"""Render entry.png for news-image-20261123 v2 (builder A, magazine/atlas).

Draws a 1024x1024 picture-led atlas of Monday 23 November 2026 with
Pillow. Every illustration is an original drawing made of shapes here;
no photographs, no downloaded images. Run: python3 render.py
Writes entry.png next to this file (mode 0644).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (20, 50, 79)
TEAL = (15, 118, 110)
GOLD = (150, 105, 10)
SEA = (178, 214, 226)
LAND = (196, 214, 178)
LINE = (120, 110, 95)
GREY = (90, 86, 78)
CARD = (255, 253, 247)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y after the last line."""
    lh = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def halo_text(draw, x, y, text, fnt, fill, halo=(255, 255, 255)):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), text, font=fnt, fill=halo)
    draw.text((x, y), text, font=fnt, fill=fill)


def panel(draw, x, y, w, h, fill=CARD, outline=LINE, width=1):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- illustrations
def ill_chart(d, x, y, w, h):
    """Rising market bars + arrow (Nvidia / Wall Street)."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 42, 67))
    bars = [0.25, 0.38, 0.32, 0.55, 0.48, 0.72, 0.95]
    bw = w / (len(bars) * 1.6)
    for i, v in enumerate(bars):
        bx = x + 10 + i * (w - 20) / len(bars)
        bh = v * (h - 34)
        col = (46, 160, 67) if i < len(bars) - 1 else (255, 196, 0)
        d.rectangle([bx, y + h - 16 - bh, bx + bw, y + h - 16], fill=col)
    d.line([(x + 8, y + h - 22 - 0.95 * (h - 34)), (x + w - 8, y + 14)],
           fill=(255, 255, 255), width=4)
    d.polygon([(x + w - 8, y + 14), (x + w - 26, y + 12), (x + w - 10, y + 28)],
              fill=(255, 255, 255))
    d.text((x + 8, y + 6), "+31.48%", font=font(F_BOLD, 20), fill=(255, 196, 0))


def ill_seadrone(d, x, y, w, h):
    """Sea, warship silhouette, drone boats, blast (Libya)."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(24, 68, 110))
    d.rectangle([x, y + h - 34, x + w - 1, y + h - 1], fill=(14, 48, 80))
    for wy in (y + h - 30, y + h - 20, y + h - 10):
        for wx in range(x + 4, x + w - 10, 26):
            d.arc([wx, wy, wx + 22, wy + 8], 0, 180, fill=(140, 190, 220), width=2)
    # warship (grey silhouette, listing)
    d.polygon([(x + 90, y + 78), (x + 260, y + 78), (x + 250, y + 96),
               (x + 100, y + 96)], fill=(70, 74, 78))
    d.rectangle([x + 130, y + 58, x + 190, y + 78], fill=(70, 74, 78))
    d.rectangle([x + 155, y + 38, x + 162, y + 58], fill=(70, 74, 78))
    d.rectangle([x + 200, y + 66, x + 214, y + 78], fill=(70, 74, 78))
    # blast (starburst)
    cx, cy = x + 268, y + 62
    pts = []
    import math
    for k in range(16):
        ang = math.pi * k / 8
        rr = 30 if k % 2 == 0 else 12
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 196, 0))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))
    # two drone boats
    for dx in (x + 20, x + 300):
        d.polygon([(dx, y + h - 44), (dx + 34, y + h - 44), (dx + 28, y + h - 34),
                   (dx + 6, y + h - 34)], fill=(230, 230, 230))
        d.line([(dx + 17, y + h - 44), (dx + 17, y + h - 52)], fill=(230, 230, 230), width=2)
    d.text((x + 10, y + 6), "7 SEA DRONES", font=font(F_BOLD, 16), fill=(255, 255, 255))


def ill_cop(d, x, y, w, h):
    """Cracked globe over empty chairs (COP31 collapse). Scales with h."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(43, 24, 18))
    cx, cy = x + w // 2, y + h // 2 - 2
    r = max(14, int(h * 0.44))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 90),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - r, cy - r, cx - r // 3, cy + r // 2], fill=(70, 110, 70))
    d.ellipse([cx + r // 4, cy - r // 2, cx + r - 4, cy + r // 3], fill=(70, 110, 70))
    d.line([(cx - 4, cy - r), (cx + 6, cy - r // 2), (cx - 3, cy + 4),
            (cx + 8, cy + r // 2), (cx - 1, cy + r)], fill=(255, 255, 255), width=2)
    for sx in (x + 10, x + w - 40):
        d.rectangle([sx, y + h - 14, sx + 30, y + h - 4], fill=(150, 115, 75))
    d.rectangle([x + 6, y + 4, x + 84, y + 20], fill=RED)
    d.text((x + 10, y + 6), "NO DEAL", font=font(F_BOLD, 12), fill=(255, 255, 255))


def ill_dymer(d, x, y, w, h):
    """Broken apartment block, rescue crane, drones (Ukraine). Scales with h."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(38, 44, 66))
    for sx, sy in ((x + 30, y + 8), (x + 90, y + 6), (x + 150, y + 10), (x + 210, y + 7)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    bx, by = x + w // 4, y + int(h * 0.32)
    bw, bh = w // 3, h - int(h * 0.32) - 8
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 110, 100))
    d.polygon([(bx, by), (bx + 24, by - 8), (bx + 60, by + 2), (bx + bw, by),
               (bx + bw, by + 6), (bx, by + 6)], fill=(90, 82, 74))
    for row in range(2):
        for col in range(4):
            wx, wy = bx + 10 + col * 34, by + 12 + row * 18
            d.rectangle([wx, wy, wx + 20, wy + 11],
                        fill=(255, 196, 0) if (row, col) == (1, 1) else (60, 66, 80))
    d.line([(x + w - 30, y + 4), (x + w - 30, y + 22)], fill=(255, 196, 0), width=3)
    d.line([(x + w - 30, y + 4), (x + 24, y + 4)], fill=(255, 196, 0), width=3)
    d.line([(x + 28, y + 4), (x + 28, y + 16)], fill=(255, 196, 0), width=2)
    d.rectangle([x + 23, y + 16, x + 33, y + 24], fill=(255, 196, 0))
    d.text((x + 8, y + h - 16), "DYMER  •  11 KILLED", font=font(F_BOLD, 11),
           fill=(255, 255, 255))


def icon(d, x, y, kind):
    """40x40 original glyph for a tier-2 card."""
    d.rectangle([x, y, x + 39, y + 39], fill=(232, 238, 240), outline=LINE)
    c = NAVY
    if kind == "shield":  # Saudi
        d.polygon([(x + 20, y + 6), (x + 32, y + 11), (x + 32, y + 22),
                   (x + 20, y + 34), (x + 8, y + 22), (x + 8, y + 11)], fill=c)
        d.line([(x + 14, y + 20), (x + 19, y + 25), (x + 27, y + 15)], fill=(255, 255, 255), width=2)
    elif kind == "crystal":  # Congo cobalt
        d.polygon([(x + 20, y + 5), (x + 30, y + 16), (x + 26, y + 33),
                   (x + 14, y + 33), (x + 10, y + 16)], fill=(30, 90, 160))
        d.line([(x + 20, y + 5), (x + 20, y + 33)], fill=(255, 255, 255), width=1)
    elif kind == "deal":  # CrowdStrike
        d.rectangle([x + 7, y + 12, x + 18, y + 28], fill=c)
        d.rectangle([x + 22, y + 12, x + 33, y + 28], fill=TEAL)
        d.text((x + 9, y + 15), "$", font=font(F_BOLD, 12), fill=(255, 255, 255))
    elif kind == "gauge":  # PMI
        d.arc([x + 7, y + 10, x + 33, y + 34], 180, 360, fill=c, width=3)
        d.line([(x + 20, y + 24), (x + 29, y + 14)], fill=RED, width=3)
        d.ellipse([x + 17, y + 21, x + 23, y + 27], fill=c)
    elif kind == "ship":  # Sparta II
        d.polygon([(x + 5, y + 24), (x + 35, y + 24), (x + 30, y + 32), (x + 10, y + 32)], fill=c)
        d.rectangle([x + 14, y + 14, x + 24, y + 24], fill=c)
        d.line([(x + 5, y + 34), (x + 35, y + 34)], fill=TEAL, width=2)
    elif kind == "badge":  # FBI
        d.ellipse([x + 8, y + 8, x + 26, y + 26], outline=c, width=3)
        d.line([(x + 23, y + 23), (x + 32, y + 32)], fill=c, width=3)
        d.text((x + 14, y + 13), "?", font=font(F_BOLD, 12), fill=c)
    elif kind == "film":  # Kate documentary
        d.rectangle([x + 6, y + 12, x + 34, y + 28], fill=c)
        d.polygon([(x + 16, y + 16), (x + 16, y + 24), (x + 24, y + 20)], fill=(255, 255, 255))
        d.rectangle([x + 6, y + 6, x + 34, y + 11], fill=TEAL)
    elif kind == "plane":  # Thanksgiving travel
        d.polygon([(x + 6, y + 20), (x + 30, y + 12), (x + 34, y + 15),
                   (x + 16, y + 24), (x + 12, y + 30), (x + 9, y + 24)], fill=c)
        d.line([(x + 6, y + 32), (x + 34, y + 32)], fill=TEAL, width=2)
    elif kind == "flame":  # Novoshakhtinsk refinery
        d.polygon([(x + 20, y + 5), (x + 28, y + 18), (x + 31, y + 28),
                   (x + 20, y + 34), (x + 9, y + 28), (x + 12, y + 18)], fill=(220, 90, 20))
        d.ellipse([x + 15, y + 20, x + 25, y + 30], fill=(255, 196, 0))

# ---------------------------------------------------------------- world map
# Simplified continent outlines (lon, lat) in equirectangular projection.
CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 73), (-75, 72), (-65, 60), (-55, 52), (-60, 45),
                 (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 21),
                 (-95, 19), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
                 (-140, 60), (-155, 58), (-165, 60)],
    "samerica": [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10),
                 (-35, -20), (-45, -30), (-55, -35), (-65, -45), (-70, -55),
                 (-75, -40), (-80, -20), (-80, -5)],
    "africa": [(-15, 35), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 28),
               (43, 12), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (12, -18), (8, -5), (0, 5),
               (-8, 5), (-15, 15)],
    "europe": [(-10, 36), (-5, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
               (10, 59), (18, 56), (21, 55), (28, 59), (30, 60), (25, 65),
               (18, 69), (12, 70), (5, 62), (0, 55), (-5, 50), (-9, 43)],
    "asia": [(30, 60), (40, 68), (60, 70), (90, 75), (120, 73), (150, 70),
             (170, 66), (160, 60), (155, 50), (140, 45), (130, 42), (127, 38),
             (120, 32), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
             (80, 15), (75, 8), (70, 20), (60, 25), (55, 28), (48, 30),
             (43, 35), (35, 36)],
    "oceania": [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22),
                (153, -28), (150, -37), (140, -38), (130, -32), (120, -34),
                (113, -26)],
}

# (name, lon, lat, dot dx, dot dy, label dx, label dy, leader?)
# Label offsets are relative to the DRAWN dot; dot offsets (for pins whose
# true positions are <12px apart) are drawn with a short leader to the true spot.
PINS = [
    ("SEATTLE", -122, 48, 0, 0, -52, -14, True),
    ("NEW YORK", -74, 41, 0, 0, 10, -16, True),
    ("WASHINGTON", -77, 39, -10, 8, -68, 4, True),
    ("ANTALYA", 31, 37, 0, 0, -78, 8, True),
    ("BENGHAZI", 20, 32, 0, 0, -40, 14, True),
    ("KYIV", 30.5, 50.4, 0, 0, -58, -4, True),
    ("ST PETERSBURG", 30.3, 59.9, 8, -6, 6, -4, True),
    ("RIYADH", 47, 24.6, 0, 0, 10, -6, False),
    ("TEHRAN", 51.4, 35.7, 0, 0, 10, -14, True),
    ("MANAMA", 50.6, 26.2, 10, 8, -18, 6, True),
    ("GAZA", 34.5, 31.5, -12, 12, 18, 12, True),
    ("KINSHASA", 15.3, -4.3, 0, 0, -70, 6, True),
    ("MANILA", 121, 14.6, 0, 0, 10, -6, False),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(214, 232, 240), outline=LINE)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 170) / 360 * w
        d.line([(gx, y), (gx, y + h)], fill=(190, 210, 222), width=1)
    for lat in (60, 30, 0, -30):
        gy = y + (75 - lat) / 130 * h
        d.line([(x, gy), (x + w, gy)], fill=(190, 210, 222), width=1)
    for pts in CONTINENTS.values():
        xy = [(x + (lon + 170) / 360 * w, y + (75 - lat) / 130 * h) for lon, lat in pts]
        d.polygon(xy, fill=LAND, outline=(120, 140, 110))
    title = "THE WORLD — WHERE IT HAPPENED"
    tw = d.textlength(title, font=font(F_BOLD, 12))
    d.text((x + w - 8 - tw, y + 4), title, font=font(F_BOLD, 12), fill=NAVY)
    for i, (name, lon, lat, odx, ody, dx, dy, leader) in enumerate(PINS, 1):
        px = x + (lon + 170) / 360 * w
        py = y + (75 - lat) / 130 * h
        qx, qy = px + odx, py + ody
        if odx or ody:
            d.line([(px, py), (qx, qy)], fill=GREY, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        lx, ly = qx + dx, qy + dy
        if leader:
            d.line([(qx, qy), (lx + 4, ly + 5)], fill=GREY, width=1)
        d.ellipse([qx - 5, qy - 5, qx + 5, qy + 5], fill=RED, outline=(255, 255, 255), width=1)
        d.text((qx - 2, qy - 4), str(i), font=font(F_BOLD, 7), fill=(255, 255, 255))
        halo_text(d, lx, ly, name, font(F_BOLD, 9), INK)
    # region bar along the bottom of the map
    d.rectangle([x, y + h - 16, x + w - 1, y + h - 1], fill=(20, 50, 79))
    d.text((x + 8, y + h - 14),
           "NORTH AMERICA 11  ·  EUROPE 7  ·  MIDDLE EAST 6  ·  AFRICA 3  ·  ASIA 2  ·  GLOBAL 1",
           font=font(F_BOLD, 11), fill=(255, 255, 255))


# ---------------------------------------------------------------- content
LEADS_TOP = [
    ("MARKETS • NEW YORK", "HUANG IS BACK — WALL ST ROARS",
     "Nvidia's board reinstates Jensen Huang as CEO, effective immediately, "
     "after Trump called for his return. Nvidia +31.48% — its best day since "
     "2003. Nasdaq +6.51%, S&P 500 +4.73%, Dow +3.01%; the S&P exits correction.",
     ill_chart),
    ("MEDITERRANEAN • BENGHAZI", "KYIV CLAIMS WARSHIP SUNK OFF LIBYA",
     "[CLAIM: sunk] Zelensky says 7 Ukrainian sea drones hit the corvette "
     "Merkury and the cargo ship Angara at Benghazi. Satellite images show "
     "most of the Merkury capsized, bow above water. Libya condemns the attack.",
     ill_seadrone),
]
LEADS_BOT = [
    ("CLIMATE • ANTALYA", "COP31 COLLAPSES — NO DEAL",
     "Talks end Sun 22 Nov with no pact — the longest COP ever, the first "
     "collapse since COP15 in 2009. Fossil-fuel language is stripped from the "
     "text. About 90 countries back a pledge to lift electricity to 35% of "
     "energy by 2035. UNFCCC: 198 Parties.",
     ill_cop),
    ("UKRAINE • DYMER", "153 DRONES IN ONE NIGHT",
     "Russia launches 153 drones overnight; Ukraine downs 134, but 11 sites "
     "are hit. In Dymer 11 are killed; a boy, David, is pulled alive from the "
     "rubble after about 14 hours; 14 were reported missing.",
     ill_dymer),
]

TIER2 = [
    ("shield", "SAUDI SHIELD UP",
     "Coalition stops a Houthi drone aimed at the south; a missile too."),
    ("crystal", "CONGO STOPS COBALT",
     "DR Congo halts cobalt exports from 30 Nov, citing oversupply."),
    ("deal", "$43.9B CYBER DEAL",
     "CrowdStrike to buy Zscaler for $43.9B in stock; 34% premium."),
    ("gauge", "EUROZONE HOLDS 51.7",
     "Flash PMI steady at 51.7, a 5th month of growth; Germany up."),
    ("gauge", "US GROWTH COOLS",
     "Flash PMI eases to 54.6, a 4-month low, as prices bite."),
    ("ship", "SPARTA II COMES HOME",
     "Hit by drones in the Baltic, it reaches St Petersburg; crew safe."),
    ("badge", "FBI PROBES HACK",
     "FBI probes an apparent hack of its crime database."),
    ("film", "KATE'S CANCER FILM",
     "Princess Kate films life with cancer in a documentary."),
    ("plane", "THANKSGIVING RUSH",
     "Holiday travel begins amid delays and severe weather."),
    ("flame", "REFINERY HIT",
     "Ukraine hits the Novoshakhtinsk oil plant in Rostov."),
]

ALSO = [
    ("EUROPE", "KHARKIV: 2 hurt as drones hit homes Mon morning"),
    ("AFRICA", "LIBYA condemns the Benghazi attack"),
    ("M EAST", "IRGC claims it hit US Patriot radars in Bahrain"),
    ("M EAST", "US weighs training Syrian troops in demining"),
    ("M EAST", "QATAR holds talks in Tehran on ending the war"),
    ("M EAST", "IRAN signals openness to a US deal"),
    ("M EAST", "GAZA: 1,671 killed since the ceasefire — Gaza Health Min."),
    ("GLOBAL", "OIL falls on surplus fears and Gulf attacks"),
    ("N AM", "LAWMAKERS criticise Nvidia's Huang reinstatement"),
    ("N AM", "CROWDSTRIKE −9%, ZSCALER +17.7% on deal day"),
    ("N AM", "DELL +20%, MICRON +19% lead S&P gainers"),
    ("ASIA", "MANILA: transport strike starts; free rides offered"),
    ("ASIA", "BANGLADESH all out for 99 vs South Africa"),
    ("N AM", "SEATTLE: ICE arrests 2 boarding a flight"),
    ("N AM", "NVIDIA adds $952B of value in a single day"),
    ("N AM", "417 of the S&P 500's stocks rise"),
]

NUMBERS = [
    ("198", "UNFCCC Parties at COP31"),
    ("153", "drones launched · 134 downed"),
    ("+31.48%", "Nvidia in one day"),
    ("11", "killed in Dymer"),
    ("$43.9B", "CrowdStrike–Zscaler"),
    ("7", "sea drones off Libya"),
]

DATECHECK = [
    ("WIRES CUT", "23 NOV 23:59 UTC — anything later is not in this picture."),
    ("DATED ANOTHER DAY — NOT 23 NOV",
     "Mexico cartel capture 20–21 Nov · Nigeria boat 20 Nov · Gaza aid strike "
     "21 Nov · Bahrain strike 21 Nov · Hormuz tankers 22 Nov · Brazil storm "
     "21 Nov · France protests 21 Nov"),
    ("LEFT OUT — AFTER THE CUT-OFF",
     "German Ifo Tue 24 Nov · Japan flash PMIs Tue 24 Nov · US $70B 5-year "
     "note auction Tue 24 Nov"),
]


def lead_panel(d, x, y, w, h, kicker, headline, body, ill, ill_h):
    panel(d, x, y, w, h)
    d.rectangle([x, y, x + w - 1, y + 20], fill=NAVY)
    d.text((x + 8, y + 3), kicker, font=font(F_BOLD, 11), fill=(255, 255, 255))
    ill(d, x + 8, y + 26, w - 16, ill_h)
    hy = y + 26 + ill_h + 6
    hy = text_block(d, x + 8, hy, headline, font(F_BOLD, 19), w - 16, fill=RED, leading=22)
    text_block(d, x + 8, hy + 2, body, font(F_REG, 12), w - 16, leading=15)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W - 1, 92], fill=INK)
    d.text((12, 8), "THE WORLD IN ONE DAY  —  A PICTURE-LED ATLAS",
           font=font(F_BOLD, 13), fill=(255, 196, 0))
    d.text((12, 26), "MONDAY 23 NOVEMBER 2026", font=font(F_BOLD, 40), fill=(255, 255, 255))
    d.text((12, 72), "30 STORIES  •  6 REGIONS  •  14 ILLUSTRATED  •  ALL EVENTS OF 23 NOVEMBER 2026",
           font=font(F_BOLD, 11), fill=(200, 200, 200))
    d.text((W - 118, 10), "No. 2", font=font(F_BOLD, 13), fill=(255, 196, 0))
    d.text((W - 118, 28), "ROUND 4", font=font(F_BOLD, 13), fill=(255, 255, 255))
    d.text((W - 118, 46), "make.fun", font=font(F_REG, 11), fill=(200, 200, 200))
    # hero leads
    for i, (k, htxt, b, ill) in enumerate(LEADS_TOP):
        lead_panel(d, 12 + i * 504, 96, 496, 204, k, htxt, b, ill, 100)
    # second leads
    for i, (k, htxt, b, ill) in enumerate(LEADS_BOT):
        lead_panel(d, 12 + i * 504, 304, 496, 180, k, htxt, b, ill, 56)
    # map
    draw_map(d, 12, 488, 1000, 128)
    # BY THE NUMBERS (labelled)
    y = 618
    d.rectangle([12, y, 1011, y + 50], fill=(255, 253, 247), outline=LINE)
    d.rectangle([12, y, 1011, y + 18], fill=GOLD)
    d.text((20, y + 2), "BY THE NUMBERS", font=font(F_BOLD, 12), fill=(255, 255, 255))
    cw = 1000 / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 12 + i * cw
        if i:
            d.line([(cx, y + 20), (cx, y + 48)], fill=LINE, width=1)
        d.text((cx + 8, y + 19), num, font=font(F_BOLD, 17), fill=RED)
        d.text((cx + 8, y + 38), lab, font=font(F_REG, 9), fill=GREY)
    # tier-2 grid 5 x 2
    y0 = 672
    cw2, ch2 = 196, 76
    for i, (kind, head, body) in enumerate(TIER2):
        col, row = i % 5, i // 5
        x = 12 + col * (cw2 + 5)
        yy = y0 + row * (ch2 + 4)
        panel(d, x, yy, cw2, ch2)
        icon(d, x + 6, yy + 6, kind)
        text_block(d, x + 52, yy + 5, head, font(F_BOLD, 11), cw2 - 58, leading=13)
        text_block(d, x + 6, yy + 48, body, font(F_REG, 9), cw2 - 12, leading=11, max_lines=2)
    # ALSO TODAY
    y = 832
    d.rectangle([12, y, 1011, y + 74], fill=(255, 253, 247), outline=LINE)
    d.text((20, y + 3), "ALSO TODAY", font=font(F_BOLD, 11), fill=RED)
    colw = 1000 / 3
    for i, (tag, txt) in enumerate(ALSO):
        col, row = i % 3, i // 3
        x = 20 + col * colw
        yy = y + 16 + row * 9
        d.text((x, yy), tag, font=font(F_BOLD, 8), fill=NAVY)
        d.text((x + 52, yy), txt, font=font(F_REG, 9), fill=INK)
    # DATE CHECK (3 rows)
    y = 910
    d.rectangle([12, y, 1011, y + 60], fill=(20, 50, 79), outline=LINE)
    d.text((20, y + 3), "DATE CHECK", font=font(F_BOLD, 11), fill=(255, 196, 0))
    for i, (lab, txt) in enumerate(DATECHECK):
        yy = y + 17 + i * 14
        d.text((20, yy), lab + ":", font=font(F_BOLD, 9), fill=(255, 196, 0))
        lw = d.textlength(lab + ": ", font=font(F_BOLD, 9))
        d.text((20 + lw, yy), txt, font=font(F_REG, 9), fill=(255, 255, 255))
    # footer
    d.text((12, 976),
           "SOURCES: Reuters · AP · CNN · Xinhua · UNFCCC · Ukrainian Air Force · Saudi Press Agency · "
           "S&P Global · NBC TODAY · UKMTO",
           font=font(F_REG, 9), fill=GREY)
    d.text((12, 988),
           "All stories happened or were first reported 23 Nov 2026. Drawn by hand in code; no photographs. "
           "make.fun / news-image-20261123",
           font=font(F_REG, 9), fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    os.chmod(out, 0o644)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
