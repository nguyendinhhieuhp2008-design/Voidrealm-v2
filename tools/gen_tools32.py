#!/usr/bin/env python3
"""Ve lai 3 icon 32x32: rift_blade, void_steel_sword (dao), void_steel_pickaxe. Tham khao anh nguoi choi gui."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402
from gen_art import hash2  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "voidrealm", "textures", "item")
N = 32


def ramp(cols, t):
    t = max(0.0, min(1.0, t)) * (len(cols) - 1)
    i = int(t)
    if i >= len(cols) - 1:
        return tuple(cols[-1])
    f = t - i
    a, b = cols[i], cols[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))


def render(fn, outline):
    grid = [[None] * N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            s, d = x + 31 - y, x - 31 + y
            grid[y][x] = fn(s, d, x, y)
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for y in range(N):
        for x in range(N):
            c = grid[y][x]
            if c is not None:
                im.putpixel((x, y), tuple(c) + (255,))
            else:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < N and 0 <= yy < N and grid[yy][xx] is not None:
                        im.putpixel((x, y), tuple(outline) + (255,))
                        break
    return im


def sparkle(im, x, y, col):
    for dx, dy, k in ((0, 0, 1.0), (1, 0, 0.55), (-1, 0, 0.55), (0, 1, 0.55), (0, -1, 0.55)):
        if 0 <= x + dx < N and 0 <= y + dy < N and im.getpixel((x + dx, y + dy))[3] == 0:
            im.putpixel((x + dx, y + dy), tuple(int(c * k) for c in col) + (255,))


# ------------------------------------------------------------------ Rift Blade
PUR = [(22, 6, 52), (48, 18, 108), (82, 38, 158), (120, 68, 206), (172, 122, 242), (232, 200, 255)]
BLK = [(8, 6, 14), (22, 20, 34), (42, 40, 58), (72, 70, 96)]
GRN = [(8, 80, 44), (28, 168, 88), (90, 236, 142), (214, 255, 228)]


def rift_fn(s, d, x, y):
    # pommel
    if ((s - 3.8) / 3.2) ** 2 + (d / 3.8) ** 2 <= 1:
        if ((s - 3.8) / 1.6) ** 2 + (d / 1.9) ** 2 <= 1:
            return PUR[4]
        return ramp(BLK, 0.15 + 0.5 * (1 - (d + 3) / 6))
    # grip
    if 6 <= s <= 17 and abs(d) <= 1:
        band = s in (9, 10, 13, 14)
        return ramp(BLK, 0.55 if band else 0.2 + 0.25 * (1 - (d + 1) / 2))
    # gem
    if abs(s - 19.5) / 4.6 + abs(d) / 4.0 <= 1:
        t = 0.5 + (-(d) * 0.12) + (-(s - 19.5) * 0.06)
        if abs(s - 19.5) / 4.6 + abs(d) / 4.0 > 0.8:
            return GRN[0]
        return ramp(GRN, t + 0.15)
    # guard wings (cong len ve phia mui kiem)
    ad = abs(d)
    if 1 <= ad <= 13.5:
        c = 19.0 + 0.04 * ad * ad
        th = 3.6 - 0.22 * ad
        if abs(s - c) <= th:
            top = (s - c) / max(th, 0.5)
            return ramp(BLK, 0.62 - 0.4 * top - (0.12 if d > 0 else 0))
    # than kiem
    if 23 <= s <= 60:
        if s <= 28:
            hw = 3.2 + 0.4 * (s - 22)
        elif s <= 50:
            hw = 5.6
        else:
            hw = 5.6 * (60.5 - s) / 10.5
        if abs(d) <= hw:
            u = (d + hw) / (2 * hw)           # 0 = canh tren-trai, 1 = canh duoi-phai
            base = 0.62 - 0.55 * u
            if abs(d) <= 0.6 and 26 <= s <= 52:
                base = 0.12                    # ranh giua
            if u < 0.2:
                base = 0.92
            elif u > 0.82:
                base = 0.1
            h = hash2(x, y, 7)
            if h > 0.93:
                base += 0.3
            elif h < 0.04:
                base -= 0.1
            return ramp(PUR, base)
    return None


def rift_blade():
    im = render(rift_fn, (8, 4, 18))
    for (x, y, c) in ((5, 5, (255, 170, 255)), (11, 3, (150, 230, 255)), (2, 12, (255, 255, 255)), (26, 20, (255, 170, 255)),
                      (9, 19, (150, 230, 255))):
        sparkle(im, x, y, c)
    for (x, y, c) in ((17, 9, (230, 190, 255)), (13, 13, (150, 230, 255)), (24, 14, (255, 255, 255))):
        if im.getpixel((x, y))[3] == 0:
            im.putpixel((x, y), c + (255,))
    im.save(os.path.join(OUT, "rift_blade.png"))


# ------------------------------------------------------------------ Void Steel dao
STL = [(14, 8, 30), (34, 20, 62), (58, 36, 100), (88, 58, 142), (126, 92, 186), (178, 146, 232)]
BOT_PTS = [(22, 3), (30, 6), (39, 8.5), (48, 8.5), (54, 6), (58, -1)]


def lerp_pts(pts, s):
    for (s0, v0), (s1, v1) in zip(pts, pts[1:]):
        if s0 <= s <= s1:
            return v0 + (v1 - v0) * (s - s0) / (s1 - s0)
    return None


def dao_fn(s, d, x, y):
    if ((s - 3.4) / 3.0) ** 2 + (d / 3.4) ** 2 <= 1:                      # chuoi nut tron
        return ramp(STL, 0.5 - 0.1 * d + (0.15 if s > 3 else 0))
    if 6 <= s <= 16 and abs(d) <= 2.0:                                      # tay cam quan day
        return ramp(STL, 0.25 + 0.2 * ((s // 3) % 2) + 0.15 * (1 - (d + 1.6) / 3.2))
    if 16 <= s <= 21 and abs(d) <= 7.6 and not (abs(d) > 6.2 and (s in (16, 21))):   # tay ho
        return ramp(STL, 0.62 - 0.1 * (d / 7.6) + (0.2 if s == 17 else 0))
    if 22 <= s <= 58:
        top = -4.5 - 0.9 * (s - 22) / 36
        bot = lerp_pts(BOT_PTS, s)
        if bot is None:
            return None
        cut = 58.5 - (d + 6.0) * 0.28
        if top <= d <= bot and s <= cut:
            u = (d - top) / (bot - top)
            base = 0.6 - 0.2 * u
            if d <= top + 1.2:
                base = 0.92                                                  # song lung sang
            elif d >= bot - 1.6:
                base = 0.8 if d <= bot - 0.6 else 0.45                       # vat luoi
            h = hash2(x, y, 3)
            if h > 0.94:
                base += 0.18
            return ramp(STL, base)
    return None


def void_steel_sword():
    im = render(dao_fn, (8, 4, 18))
    im.save(os.path.join(OUT, "void_steel_sword.png"))


# ------------------------------------------------------------------ Void Steel pickaxe
PK = [(26, 14, 52), (56, 36, 98), (96, 68, 150), (146, 116, 206), (204, 178, 244)]
HEAD = [(4.5, 8.0, 1.2), (8.5, 5.0, 2.4), (14.0, 3.8, 3.0), (20.0, 4.8, 3.0), (25.0, 8.5, 2.6), (27.5, 14.0, 2.0), (28.0, 19.5, 1.0)]


def seg_dist(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy)))
    cx, cy = ax + vx * t, ay + vy * t
    return math.hypot(px - cx, py - cy), t


def pick_fn(s, d, x, y):
    px, py = x + 0.5, y + 0.5
    # can: tu goc duoi-trai len dau
    dist, t = seg_dist(px, py, 3.0, 29.0, 19.0, 6.5)
    if dist <= 1.9:
        side = (px - 3.0) * 16.0 + (py - 29.0) * 17.0  # khong dung
        k = 0.45 + 0.25 * math.sin((t * 6.0)) - 0.2 * (dist / 1.6)
        return ramp(PK, 0.18 + 0.28 * (0.5 + 0.5 * math.sin(t * 9.0)) + 0.18 * (1 - dist / 1.9))
    # dau cuoc: chuoi diem co do rong thay doi
    best = None
    for (ax, ay, aw), (bx, by, bw) in zip(HEAD, HEAD[1:]):
        dd, tt = seg_dist(px, py, ax, ay, bx, by)
        w = aw + (bw - aw) * tt
        if dd <= w and (best is None or dd / w < best[0]):
            best = (dd / w, tt, ax, ay, bx, by)
    if best:
        rel, tt, ax, ay, bx, by = best
        # phia ngoai (tren-phai) sang, phia trong toi
        nx, ny = (by - ay), -(bx - ax)
        ln = math.hypot(nx, ny) or 1
        side = ((px - (ax + (bx - ax) * tt)) * nx + (py - (ay + (by - ay) * tt)) * ny) / ln   # >0: ngoai
        base = 0.48 + 0.2 * side / 3.0 - 0.1 * rel
        if side > 1.0:
            base = 0.88
        elif side < -1.2:
            base = 0.18
        if hash2(x, y, 5) > 0.95:
            base += 0.15
        return ramp(PK, base)
    return None


def void_steel_pickaxe():
    im = render(pick_fn, (10, 5, 22))
    im.save(os.path.join(OUT, "void_steel_pickaxe.png"))


if __name__ == "__main__":
    rift_blade()
    void_steel_sword()
    void_steel_pickaxe()
    print("gen_tools32 xong")
