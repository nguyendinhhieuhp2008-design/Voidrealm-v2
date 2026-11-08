#!/usr/bin/env python3
"""Icon 32x32 theo phong cach bo 'Void Steel Tools' cua nguoi choi:
- void_steel_{sword,shovel,pickaxe,hoe,axe}: cat truc tiep tu anh nguoi choi (da lam sach) -> da nam trong textures/item.
- Con lai ve moi: void_reaper, voidpiercer, gravity_staff, dream_sword, dream_battle_axe, dream_drill, dream_crossbow.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402
from gen_art import hash2  # noqa: E402
from gen_tools32 import OUT, N, ramp, render, seg_dist  # noqa: E402
from gen_dream import to_blue  # noqa: E402

PUR = [(14, 7, 28), (36, 20, 66), (64, 36, 112), (100, 60, 164), (144, 98, 212), (192, 152, 250)]
BLU = [(6, 14, 40), (16, 44, 110), (36, 92, 190), (80, 160, 245), (150, 215, 255), (232, 248, 255)]
OUTLINE_P = (12, 6, 24)
OUTLINE_B = (4, 10, 30)


def shade_line(P, t, dist, w, seed, x, y):
    """Mau cho than hinh tru: sang o gan tam tren, toi o ria."""
    base = 0.62 - 0.45 * (dist / w) ** 1.3
    base += 0.12 * math.sin(t * 9.0)
    if hash2(x, y, seed) > 0.95:
        base += 0.16
    return ramp(P, base)


def poly_width(px, py, pts):
    """pts: [(x,y,w)]. Tra ve (rel, t, side, seg) tot nhat hoac None."""
    best = None
    for (ax, ay, aw), (bx, by, bw) in zip(pts, pts[1:]):
        dd, tt = seg_dist(px, py, ax, ay, bx, by)
        w = aw + (bw - aw) * tt
        if dd <= w and (best is None or dd / max(w, 1e-6) < best[0]):
            nx, ny = (by - ay), -(bx - ax)
            ln = math.hypot(nx, ny) or 1
            cx, cy = ax + (bx - ax) * tt, ay + (by - ay) * tt
            side = ((px - cx) * nx + (py - cy) * ny) / ln
            best = (dd / max(w, 1e-6), tt, side, w)
    return best


def part_color(P, hit, x, y, seed):
    rel, tt, side, w = hit
    base = 0.5 + 0.22 * side / max(w, 1.0) - 0.08 * rel
    if side > 0.35 * w:
        base = 0.88
    elif side < -0.45 * w:
        base = 0.16
    if hash2(x, y, seed) > 0.95:
        base += 0.14
    return ramp(P, base)


def handle(P, px, py, a, b, w, x, y, seed=11):
    dist, t = seg_dist(px, py, a[0], a[1], b[0], b[1])
    if dist <= w:
        return ramp(P, 0.2 + 0.26 * (0.5 + 0.5 * math.sin(t * 11.0)) + 0.2 * (1 - dist / w))
    return None


# ------------------------------------------------------------------ Void Reaper (luoi hai)
def reaper(P=PUR, out=OUTLINE_P, name="void_reaper"):
    BLADE = [(21.5, 9.0, 1.4), (19.0, 5.2, 2.5), (14.0, 3.0, 3.0), (8.5, 3.8, 2.6), (4.5, 7.0, 1.6), (2.0, 12.0, 0.7)]

    def fn(s, d, x, y):
        px, py = x + 0.5, y + 0.5
        # chop nhan
        if ((px - 22.5) / 2.4) ** 2 + ((py - 8.0) / 2.4) ** 2 <= 1:
            return ramp(P, 0.82 if (x + y) % 2 else 0.6)
        h = handle(P, px, py, (3.0, 29.0), (21.5, 9.5), 1.7, x, y)
        if h:
            return h
        hit = poly_width(px, py, BLADE)
        if hit:
            return part_color(P, hit, x, y, 13)
        return None
    im = render(fn, out)
    for (x, y) in ((21, 9), (22, 8)):
        im.putpixel((x, y), (255, 130, 225, 255) if P is PUR else (170, 255, 255, 255))
    im.save(os.path.join(OUT, name + ".png"))


# ------------------------------------------------------------------ Voidpiercer (giao)
def piercer():
    P = PUR

    def fn(s, d, x, y):
        px, py = x + 0.5, y + 0.5
        if 2 <= s <= 4 and abs(d) <= 2.2:                                        # dot cat
            return ramp(P, 0.6)
        if 4 < s <= 40 and abs(d) <= 1.7:                                         # can
            wrap = 14 <= s <= 26 and (s // 2) % 2 == 0
            return ramp(P, 0.24 + 0.14 * (1 if wrap else 0) + 0.24 * (1 - (d + 1.7) / 3.4))
        if 38 <= s <= 42 and abs(d) <= 3.2:                                       # co
            return ramp(P, 0.7 - 0.12 * d / 3.2 + (0.2 if s == 39 else 0))
        if 42 < s <= 61:                                                          # muoi giao hinh la
            hw = 4.7 * math.sin(math.pi * (s - 41.5) / 20.0) ** 0.75
            if abs(d) <= hw:
                u = (d + hw) / max(2 * hw, 0.1)
                base = 0.7 - 0.5 * u
                if abs(d) <= 0.5 and s > 46:
                    base = 0.2
                if u < 0.22:
                    base = 0.95
                elif u > 0.8:
                    base = 0.12
                if hash2(x, y, 17) > 0.95:
                    base += 0.14
                return ramp(P, base)
        return None
    im = render(fn, OUTLINE_P)
    im.putpixel((20, 11), (255, 130, 225, 255))
    im.putpixel((19, 12), (255, 130, 225, 255))
    im.save(os.path.join(OUT, "voidpiercer.png"))


# ------------------------------------------------------------------ Gravity Staff
def staff():
    P = PUR

    def fn(s, d, x, y):
        px, py = x + 0.5, y + 0.5
        cx, cy = 24.0, 8.0
        r = math.hypot(px - cx, py - cy)
        if r <= 2.7:                                                              # loi
            return ramp([(120, 40, 160), (220, 90, 220), (255, 190, 245), (255, 255, 255)], 1 - r / 2.7)
        if r <= 4.5:                                                              # cau nang luong
            return ramp(P, 0.32 + 0.5 * (1 - r / 4.5) + (0.12 if hash2(x, y, 3) > 0.9 else 0))
        if r <= 6.1:                                                              # vong thep
            ang = math.atan2(py - cy, px - cx)
            gap = abs(math.sin(ang * 2.0)) < 0.16 and r > 5.1
            if not gap:
                return ramp(P, 0.62 - 0.24 * (r - 4.5) / 1.6 + 0.2 * math.cos(ang + 2.2))
        if 6 <= s <= 36 and abs(d) <= 1.6 and r > 5.0:                            # can
            wrap = 14 <= s <= 24 and (s // 2) % 2 == 0
            return ramp(P, 0.22 + 0.14 * (1 if wrap else 0) + 0.24 * (1 - (d + 1.6) / 3.2))
        if 2 <= s < 6 and abs(d) <= 2.2:
            return ramp(P, 0.6)
        return None
    im = render(fn, OUTLINE_P)
    im.save(os.path.join(OUT, "gravity_staff.png"))


# ------------------------------------------------------------------ Dream: kiem + riu tu bo giap moi, doi mau xanh
def dream_from_void():
    for src, dst, gem in (("void_steel_sword", "dream_sword", (232, 250, 255)), ("void_steel_axe", "dream_battle_axe", (232, 250, 255))):
        im = to_blue(Image.open(os.path.join(OUT, src + ".png")), 1.7)
        # canh gioi chu: vien sang
        px = im.load()
        for y in range(N):
            for x in range(N):
                r, g, b, a = px[x, y]
                if a and (r + g + b) / 3 < 40:
                    px[x, y] = (4, 10, 30, 255)
        im.save(os.path.join(OUT, dst + ".png"))
    # tinh the sang tren kiem + rieu
    sw = Image.open(os.path.join(OUT, "dream_sword.png"))
    for (x, y) in ((4, 27), (5, 27), (4, 28)):
        if sw.getpixel((x, y))[3]:
            sw.putpixel((x, y), (200, 245, 255, 255))
    sw.save(os.path.join(OUT, "dream_sword.png"))


# ------------------------------------------------------------------ Dream drill
def drill():
    P = BLU
    BIT = [(21.0, 11.0, 3.4), (25.0, 7.0, 2.6), (29.5, 2.5, 0.9)]

    def fn(s, d, x, y):
        px, py = x + 0.5, y + 0.5
        # than may
        dist, t = seg_dist(px, py, 13.0, 19.0, 21.0, 11.0)
        if dist <= 3.4 and t <= 1.0:
            band = (int(t * 5.0) % 2 == 0)
            base = 0.52 - 0.3 * (dist / 3.4) + (0.12 if band else 0)
            if hash2(x, y, 5) > 0.95:
                base += 0.2
            if dist < 1.1 and 0.35 < t < 0.65:
                return (225, 250, 255)
            return ramp(P, base)
        hit = poly_width(px, py, BIT)
        if hit:
            rel, tt, side, w = hit
            spiral = math.sin((tt * 14.0) + (side / max(w, 0.5)) * 2.0)
            return ramp(P, 0.9 if spiral > 0.35 else (0.55 if spiral > -0.4 else 0.25))
        h = handle(P, px, py, (3.0, 29.0), (14.0, 18.0), 1.7, x, y)
        if h:
            return h
        return None
    im = render(fn, OUTLINE_B)
    im.save(os.path.join(OUT, "dream_drill.png"))


# ------------------------------------------------------------------ Dream crossbow
def crossbow():
    P = BLU
    PROD = [(11.5, 4.0, 1.0), (17.5, 4.2, 1.7), (23.0, 7.5, 2.0), (26.8, 12.8, 1.8), (28.2, 19.5, 1.0)]

    def fn(s, d, x, y):
        px, py = x + 0.5, y + 0.5
        # day cung (nhat)
        dist, t = seg_dist(px, py, 11.5, 4.0, 28.2, 19.5)
        if dist <= 0.55:
            return (210, 242, 255)
        # mui ten
        dist, t = seg_dist(px, py, 12.5, 18.5, 25.5, 5.5)
        if dist <= 0.75 or (t > 0.9 and dist <= 1.5 - (t - 0.9) * 15):
            return ramp(P, 0.95 if t > 0.8 else 0.75)
        hit = poly_width(px, py, PROD)
        if hit:
            return part_color(P, hit, x, y, 21)
        dist, t = seg_dist(px, py, 3.0, 29.0, 20.5, 11.5)
        if dist <= 2.0 and t <= 1.0:
            return ramp(P, 0.18 + 0.28 * (0.5 + 0.5 * math.sin(t * 8.0)) + 0.2 * (1 - dist / 2.0))
        return None
    im = render(fn, OUTLINE_B)
    im.save(os.path.join(OUT, "dream_crossbow.png"))


if __name__ == "__main__":
    reaper()
    piercer()
    staff()
    dream_from_void()
    drill()
    crossbow()
    print("gen_tools_style xong")
