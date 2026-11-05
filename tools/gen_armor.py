#!/usr/bin/env python3
"""Texture giap v3 (mac tren nguoi, 64x32) + icon 16x16 cho 8 mon giap.
Chay SAU gen_art.py / gen_textures.py:  python3 tools/gen_armor.py
Bo cuc UV theo vanilla: dau (0,0), than (16,16), tay phai (40,16), chan phai (0,16); trai la phan chieu.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402
from gen_art import hash2, vnoise, ramp  # noqa: E402

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "voidrealm", "textures")
ARM = os.path.join(RES, "models", "armor")
ITM = os.path.join(RES, "item")

# ---- bang mau
VS = [(14, 8, 34), (34, 22, 78), (66, 46, 130), (110, 84, 196), (166, 140, 248)]   # thep hu khong
VS_DARK = [(8, 5, 20), (20, 12, 48), (40, 26, 90), (70, 50, 140)]
GOLD = [(90, 56, 14), (170, 116, 28), (236, 184, 64), (255, 236, 150)]
CYAN = [(16, 90, 110), (40, 180, 200), (120, 240, 245), (225, 255, 255)]
PINK = [(110, 20, 110), (200, 60, 200), (250, 130, 250), (255, 220, 255)]
CL = [(24, 10, 52), (58, 24, 104), (104, 48, 160), (160, 86, 210)]                 # vai hu anh
CL_DARK = [(14, 6, 32), (36, 14, 72), (66, 28, 112), (100, 50, 150)]


class Tex:
    def __init__(self, seed):
        self.img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
        self.seed = seed

    def px(self, x, y, c):
        if 0 <= x < 64 and 0 <= y < 32:
            self.img.putpixel((x, y), (c[0], c[1], c[2], 255))

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def fill(self, x, y, w, h, cols, base=0.5, grain=0.16, bevel=True, scale=2.4, vertical=0.0):
        for j in range(h):
            for i in range(w):
                n = vnoise(x + i, y + j, scale, self.seed) - 0.5
                n += (hash2(x + i, y + j, self.seed + 3) - 0.5) * 0.35
                t = base + n * grain * 2
                if vertical:
                    t += (vnoise(x + i, 0, 1.2, self.seed + 9) - 0.5) * vertical
                if bevel:
                    if j == 0 or i == 0:
                        t += 0.13
                    if j == h - 1 or i == w - 1:
                        t -= 0.17
                self.px(x + i, y + j, ramp(cols, max(0.0, min(1.0, t))))

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.px(x + i, y + j, c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def art(self, x, y, rows, pal):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in pal:
                    self.px(x + i, y + j, pal[ch])

    def mirror_limbs(self):
        """Tay/chan trai = phan chieu cua phai (vanilla 64x32 tu lam, nhung ta ghi ro cho chac)."""
        pass

    def save(self, name):
        self.img.save(os.path.join(ARM, name + ".png"))


def c(cols, i):
    return cols[i]


def void_steel():
    # ------------------------------------------------ layer 1: mu, ao giap, tay, giay
    t = Tex(31)
    # ===== MU: head (0,0) 8x8x8
    for (x, y, w, h) in ((8, 0, 8, 8), (16, 0, 8, 8), (0, 8, 8, 8), (8, 8, 8, 8), (16, 8, 8, 8), (24, 8, 8, 8)):
        t.fill(x, y, w, h, VS, 0.5)
    # dinh dau: sống giữa + hoa van
    t.vline(11, 0, 8, c(VS, 3))
    t.vline(12, 0, 8, c(VS, 4))
    t.hline(8, 3, 8, c(VS, 1))
    t.hline(8, 4, 8, c(VS, 1))
    # vanh tran vang
    for fx in (0, 8, 16, 24):
        t.hline(fx, 8, 8, c(GOLD, 2))
        t.hline(fx, 9, 8, c(GOLD, 1))
    # mat truoc: ke ho nhin phat sang
    t.rect(10, 11, 4, 2, c(VS_DARK, 0))
    t.hline(9, 12, 6, c(VS_DARK, 0))
    t.hline(10, 12, 4, c(CYAN, 2))
    t.px(9, 12, c(CYAN, 1))
    t.px(14, 12, c(CYAN, 1))
    t.hline(11, 11, 2, c(CYAN, 3))
    # ma + ham: tam cheo
    t.rect(8, 13, 2, 3, c(VS, 2))
    t.rect(14, 13, 2, 3, c(VS, 2))
    t.hline(8, 15, 8, c(VS_DARK, 1))
    t.px(12, 14, c(CYAN, 2))
    t.px(12, 15, c(GOLD, 2))
    # ngọc trán
    t.px(11, 9, c(CYAN, 3))
    t.px(12, 9, c(CYAN, 3))
    t.px(11, 10, c(CYAN, 1))
    t.px(12, 10, c(CYAN, 1))
    # canh mu (hai ben): rune doc
    for sx in (0, 16):
        t.vline(sx + 3, 10, 4, c(CYAN, 1))
        t.vline(sx + 4, 11, 2, c(CYAN, 2))
        t.hline(sx, 14, 8, c(VS_DARK, 1))
    # sau gay: tam cheo
    for j in range(10, 16):
        for i in range(24, 32):
            if (i + j) % 4 == 0:
                t.px(i, j, c(VS, 1))
    t.hline(24, 15, 8, c(VS_DARK, 1))
    t.vline(27, 9, 7, c(CYAN, 1))
    t.vline(28, 9, 7, c(CYAN, 1))

    # ===== THAN: body (16,16) 8x12x4 -> front(20,20,8,12) back(32,20,8,12) sides (16,20),(28,20)
    t.fill(20, 16, 8, 4, VS, 0.6)        # tren (vai)
    t.fill(28, 16, 8, 4, VS_DARK, 0.5)   # duoi
    t.fill(20, 20, 8, 12, VS, 0.5)
    t.fill(32, 20, 8, 12, VS, 0.45)
    t.fill(16, 20, 4, 12, VS, 0.42)
    t.fill(28, 20, 4, 12, VS, 0.42)
    # nguc: hai tam giap + gem trung tam hinh thoi
    t.vline(23, 20, 8, c(VS_DARK, 0))
    t.vline(24, 20, 8, c(VS_DARK, 0))
    t.hline(20, 23, 8, c(VS_DARK, 0))
    t.hline(20, 27, 8, c(VS_DARK, 0))
    t.art(21, 21, [
        "..tt.tt.", ".tT.tT..", ".t......", "........"],
        {"t": c(VS, 4), "T": c(VS, 3)})
    t.art(22, 22, [
        "..GG..", ".GCCG.", "GCwwCG", "GCwwCG", ".GCCG.", "..GG.."],
        {"G": c(GOLD, 2), "C": c(CYAN, 1), "w": c(CYAN, 3)})
    # det luoi nhung duong sang
    t.px(20, 22, c(CYAN, 1))
    t.px(27, 22, c(CYAN, 1))
    t.px(20, 25, c(CYAN, 1))
    t.px(27, 25, c(CYAN, 1))
    # that lung vang + khoa
    t.hline(20, 28, 8, c(GOLD, 2))
    t.hline(20, 29, 8, c(GOLD, 1))
    t.rect(23, 28, 2, 2, c(CYAN, 2))
    t.px(23, 28, c(CYAN, 3))
    # vat ao duoi
    for i in range(20, 28):
        t.px(i, 31, c(VS_DARK, 0) if i % 2 else c(VS, 1))
    # lung: gai song + rune doc
    t.vline(35, 20, 12, c(VS_DARK, 0))
    t.vline(36, 20, 12, c(VS_DARK, 0))
    for j in range(21, 30, 3):
        t.hline(33, j, 6, c(VS_DARK, 1))
        t.px(35, j, c(CYAN, 2))
        t.px(36, j, c(CYAN, 2))
    t.hline(32, 28, 8, c(GOLD, 2))
    t.hline(32, 29, 8, c(GOLD, 1))
    # canh hong
    for sx in (16, 28):
        t.hline(sx, 28, 4, c(GOLD, 1))
        t.vline(sx + 1, 21, 6, c(VS_DARK, 1))

    # ===== TAY: arm (40,16) 4x12x4  top(44,16) bottom(48,16) r(40,20) f(44,20) l(48,20) b(52,20)
    t.fill(44, 16, 4, 4, VS, 0.65)
    t.fill(48, 16, 4, 4, VS_DARK, 0.4)
    for (x, y) in ((40, 20), (44, 20), (48, 20), (52, 20)):
        t.fill(x, y, 4, 12, VS, 0.5)
        # vai: vanh vang + gai
        t.hline(x, 20, 4, c(VS, 4))
        t.hline(x, 21, 4, c(VS, 3))
        t.hline(x, 22, 4, c(GOLD, 2))
        t.hline(x, 23, 4, c(GOLD, 0))
        # khuy tay
        t.hline(x, 26, 4, c(VS_DARK, 0))
        t.px(x + 1, 27, c(CYAN, 2))
        t.px(x + 2, 27, c(CYAN, 2))
        # bao tay
        t.hline(x, 29, 4, c(GOLD, 1))
        t.hline(x, 30, 4, c(VS_DARK, 1))
        t.hline(x, 31, 4, c(VS_DARK, 0))
    # gai vai (mat truoc/sau/ngoai)
    for x in (44, 52, 40):
        t.px(x + 1, 20, c(VS, 4))
        t.px(x + 2, 20, c(VS, 4))
        t.px(x + 1, 21, c(CYAN, 2))

    # ===== CHAN (giay): leg (0,16) 4x12x4  top(4,16) bottom(8,16) r(0,20) f(4,20) l(8,20) b(12,20)
    t.fill(4, 16, 4, 4, VS_DARK, 0.5)
    t.fill(8, 16, 4, 4, VS_DARK, 0.3)
    for (x, y) in ((0, 20), (4, 20), (8, 20), (12, 20)):
        # chi phan giay: 6 hang duoi (y=26..31)
        t.fill(x, 26, 4, 6, VS, 0.5)
        t.hline(x, 26, 4, c(GOLD, 2))
        t.hline(x, 27, 4, c(GOLD, 0))
        t.hline(x, 29, 4, c(VS_DARK, 0))
        t.px(x + 1, 28, c(CYAN, 2))
        t.px(x + 2, 28, c(CYAN, 2))
        t.hline(x, 31, 4, c(VS_DARK, 0))
    t.save("void_steel_layer_1")

    # ------------------------------------------------ layer 2: quan
    t = Tex(37)
    t.fill(20, 16, 8, 4, VS_DARK, 0.5)
    t.fill(28, 16, 8, 4, VS_DARK, 0.3)
    for (x, y, w, h) in ((16, 20, 4, 12), (20, 20, 8, 12), (28, 20, 4, 12), (32, 20, 8, 12)):
        t.fill(x, y, w, h, VS, 0.48)
        t.hline(x, 20, w, c(GOLD, 2))
        t.hline(x, 21, w, c(GOLD, 0))
        # tam ho tong
        t.hline(x, 25, w, c(VS_DARK, 0))
        t.hline(x, 29, w, c(VS_DARK, 0))
    # than truoc: khoa that lung + tam chan
    t.rect(23, 20, 2, 2, c(CYAN, 2))
    t.px(23, 20, c(CYAN, 3))
    t.vline(23, 22, 10, c(VS_DARK, 0))
    t.vline(24, 22, 10, c(VS_DARK, 0))
    t.art(20, 23, ["..t..t..", ".tT..Tt.", "........"], {"t": c(VS, 4), "T": c(VS, 3)})
    # sau: ke hai ben
    t.vline(35, 22, 10, c(VS_DARK, 0))
    t.vline(36, 22, 10, c(VS_DARK, 0))
    t.hline(32, 22, 8, c(CYAN, 1))
    # chan: top/bottom + 4 mat
    t.fill(4, 16, 4, 4, VS_DARK, 0.5)
    t.fill(8, 16, 4, 4, VS_DARK, 0.3)
    for (x, y) in ((0, 20), (4, 20), (8, 20), (12, 20)):
        t.fill(x, 20, 4, 12, VS, 0.5)
        t.hline(x, 20, 4, c(GOLD, 2))
        t.hline(x, 21, 4, c(GOLD, 0))
        # tam ho
        t.rect(x, 22, 4, 3, c(VS, 3))
        t.hline(x, 22, 4, c(VS, 4))
        # goi: ngoc cyan o mat truoc
        t.hline(x, 26, 4, c(VS_DARK, 0))
        t.hline(x, 30, 4, c(VS_DARK, 0))
    t.rect(5, 26, 2, 2, c(CYAN, 2))
    t.px(5, 26, c(CYAN, 3))
    t.px(6, 27, c(CYAN, 1))
    t.px(5, 27, c(CYAN, 1))
    t.px(6, 26, c(CYAN, 2))
    t.save("void_steel_layer_2")


def phase_cloth():
    t = Tex(53)
    # ===== MU TRUM
    for (x, y, w, h) in ((8, 0, 8, 8), (16, 0, 8, 8), (0, 8, 8, 8), (8, 8, 8, 8), (16, 8, 8, 8), (24, 8, 8, 8)):
        t.fill(x, y, w, h, CL, 0.46, grain=0.2, vertical=0.25)
    # dinh mu: nep nhan
    for j in range(0, 8):
        t.px(11, j, c(CL, 3))
        t.px(12, j, c(CL, 3))
    t.hline(8, 1, 8, c(CL_DARK, 1))
    # mat truoc: bong toi + hai mat sang
    t.rect(9, 10, 6, 4, c(CL_DARK, 0))
    t.hline(10, 9, 4, c(CL_DARK, 1))
    t.px(10, 11, c(PINK, 2))
    t.px(11, 11, c(PINK, 3))
    t.px(13, 11, c(PINK, 3))
    t.px(14, 11, c(PINK, 2))
    t.px(9, 11, c(PINK, 0))
    t.px(15, 11, c(PINK, 0))
    # vien vang quanh mat
    t.hline(8, 9, 1, c(GOLD, 2))
    t.vline(8, 9, 7, c(GOLD, 2))
    t.vline(15, 9, 7, c(GOLD, 2))
    t.hline(8, 8, 8, c(GOLD, 1))
    # vien vang duoi mu + mat truoc sang vang
    for fx in (0, 16, 24):
        t.hline(fx, 8, 8, c(GOLD, 1))
        t.hline(fx, 15, 8, c(CL_DARK, 0))
    t.hline(8, 15, 8, c(CL_DARK, 0))
    # sao hong tren dinh
    t.px(11, 3, c(PINK, 3))
    t.px(12, 4, c(PINK, 2))
    t.px(10, 4, c(PINK, 1))
    # sau: nep + sao
    for j in range(9, 15):
        t.px(27, j, c(CL_DARK, 0))
    t.px(26, 11, c(PINK, 2))
    t.px(29, 12, c(PINK, 2))

    # ===== AO CHOANG (than + tay)
    t.fill(20, 16, 8, 4, CL, 0.55, vertical=0.2)
    t.fill(28, 16, 8, 4, CL_DARK, 0.45)
    for (x, y, w, h) in ((16, 20, 4, 12), (20, 20, 8, 12), (28, 20, 4, 12), (32, 20, 8, 12)):
        t.fill(x, y, w, h, CL, 0.46, grain=0.2, vertical=0.3, bevel=False)
        # nep vai doc
        for i in range(0, w, 2):
            t.vline(x + i, y + 4, h - 4, c(CL_DARK, 1))
        # dai long vang
    # co ao + vien truoc
    t.hline(20, 20, 8, c(GOLD, 2))
    t.hline(20, 21, 8, c(GOLD, 0))
    t.vline(23, 22, 9, c(GOLD, 1))
    t.vline(24, 22, 9, c(GOLD, 2))
    # dai that lung tim + khuc tron
    t.hline(20, 27, 8, c(CL_DARK, 0))
    t.hline(20, 28, 8, c(PINK, 1))
    t.hline(20, 29, 8, c(CL_DARK, 0))
    t.px(23, 28, c(PINK, 3))
    t.px(24, 28, c(PINK, 3))
    # nguc: sao tam giac nhan
    t.art(21, 22, ["...pp...", "..pPPp..", "...pp..."], {"p": c(PINK, 1), "P": c(PINK, 3)})
    # lam hoa tiet o vat ao
    for i in range(20, 28):
        if i % 2 == 0:
            t.px(i, 31, c(PINK, 0))
        else:
            t.px(i, 30, c(CL_DARK, 0))
    # lung: ngoi sao lon
    t.art(33, 22, ["...pp...", "..pPPp..", ".pPPPPp.", "..pPPp..", "...pp..."],
          {"p": c(PINK, 1), "P": c(PINK, 3)})
    t.hline(32, 28, 8, c(PINK, 1))
    for i in range(32, 40):
        if i % 2 == 0:
            t.px(i, 31, c(PINK, 0))
    # tay: vien vang cuoi + gach nen
    t.fill(44, 16, 4, 4, CL, 0.55)
    t.fill(48, 16, 4, 4, CL_DARK, 0.4)
    for (x, y) in ((40, 20), (44, 20), (48, 20), (52, 20)):
        t.fill(x, y, 4, 12, CL, 0.46, grain=0.2, vertical=0.3, bevel=False)
        t.vline(x + 1, 24, 7, c(CL_DARK, 1))
        t.vline(x + 3, 24, 7, c(CL_DARK, 1))
        t.hline(x, 20, 4, c(GOLD, 1))
        t.hline(x, 29, 4, c(GOLD, 2))
        t.hline(x, 30, 4, c(GOLD, 0))
        t.px(x + 1, 26, c(PINK, 2))
        t.px(x + 2, 26, c(PINK, 1))
        # tua rua cuoi tay
        for i in range(4):
            if i % 2 == 0:
                t.px(x + i, 31, c(PINK, 1))
    # giay (chan): ong ngan + khuy
    t.fill(4, 16, 4, 4, CL_DARK, 0.5)
    t.fill(8, 16, 4, 4, CL_DARK, 0.3)
    for (x, y) in ((0, 20), (4, 20), (8, 20), (12, 20)):
        t.fill(x, 26, 4, 6, CL, 0.46, grain=0.2, vertical=0.25, bevel=False)
        t.hline(x, 26, 4, c(GOLD, 2))
        t.hline(x, 27, 4, c(GOLD, 0))
        t.px(x + 1, 29, c(PINK, 2))
        t.px(x + 2, 29, c(PINK, 1))
        t.hline(x, 31, 4, c(CL_DARK, 0))
    t.save("phase_cloth_layer_1")

    # ------------------ layer 2: quan
    t = Tex(59)
    t.fill(20, 16, 8, 4, CL_DARK, 0.5)
    t.fill(28, 16, 8, 4, CL_DARK, 0.3)
    t.fill(4, 16, 4, 4, CL_DARK, 0.5)
    t.fill(8, 16, 4, 4, CL_DARK, 0.3)
    for (x, y, w, h) in ((16, 20, 4, 12), (20, 20, 8, 12), (28, 20, 4, 12), (32, 20, 8, 12),
                         (0, 20, 4, 12), (4, 20, 4, 12), (8, 20, 4, 12), (12, 20, 4, 12)):
        t.fill(x, y, w, h, CL, 0.46, grain=0.2, vertical=0.3, bevel=False)
        t.hline(x, 20, w, c(GOLD, 2))
        t.hline(x, 21, w, c(GOLD, 0))
        for i in range(1, w, 2):
            t.vline(x + i, 23, h - 3, c(CL_DARK, 1))
        t.hline(x, 31, w, c(CL_DARK, 0))
    # day cuoi: tua ruoi hong
    for (x, w) in ((0, 16), (16, 24)):
        for i in range(x, x + w):
            if i % 2 == 0:
                t.px(i, 30, c(PINK, 1))
    t.rect(23, 20, 2, 2, c(PINK, 2))
    t.px(23, 20, c(PINK, 3))
    t.px(24, 26, c(PINK, 2))
    t.px(5, 25, c(PINK, 3))
    t.px(6, 26, c(PINK, 2))
    t.save("phase_cloth_layer_2")


# ------------------------------------------------------------------ ICON 16x16
def icon(name, rows, pal):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                col = pal[ch]
                im.putpixel((i, j), (col[0], col[1], col[2], 255))
    im.save(os.path.join(ITM, name + ".png"))


def icons():
    p = {
        "o": (10, 6, 22), "d": VS[1], "m": VS[2], "l": VS[3], "h": VS[4],
        "g": GOLD[2], "G": GOLD[1], "y": GOLD[3], "c": CYAN[1], "C": CYAN[2], "w": CYAN[3], "k": VS[0],
    }
    icon("void_steel_helmet", [
        "................",
        "......oooo......",
        "....oohhhhoo....",
        "...ohhllllhho...",
        "..ohlmmccmmlho..",
        "..ohlmmCCmmlho..",
        ".ogGgggyyggGggo.",
        ".odddddddddddo..",
        ".odmdoookoodmdo.",
        ".odmdocCCcodmdo.",
        ".odmdooooookmdo.",
        ".odmddddddddmdo.",
        ".okdmo....omdko.",
        "..ookk....kkoo..",
        "................",
        "................"], p)
    icon("void_steel_chestplate", [
        "................",
        ".oooo......oooo.",
        "ohhlloo..oollhho",
        "ohlmlloooollmlho",
        "ogGgmmmmmmmmgGgo",
        "ohdddmlhhlmdddho",
        ".ohdmmlcCClmmdho",
        ".odddmlCwwClmddo",
        ".oddmmlcCClmmddo",
        ".okddmmlccclmddo",
        "..oggGggyyggGggo",
        "..okdmmmCCmmdko.",
        "..okddmmmmmmdko.",
        "...okdddddddko..",
        "....oookkkkoo...",
        "................"], p)
    icon("void_steel_leggings", [
        "................",
        "..oooooooooooo..",
        "..ogGgggyyggGgo.",
        "..ohdmmcCCmmdho.",
        "..ohdmmmkmmmdho.",
        "..odmmmmokmmmdo.",
        "..odmlmmokmlmdo.",
        "..odmllmokmllmo.",
        "..odmCCmokmCCmo.",
        "..odmcCmokmcCmo.",
        "..odmmmmokmmmmo.",
        "..odmmdmokmdmmo.",
        "..okddmmokmmddo.",
        "..okkdkkokkdkko.",
        "...ookk...kkoo..",
        "................"], p)
    icon("void_steel_boots", [
        "................",
        "................",
        "................",
        "..oooo....oooo..",
        ".ogGggo..oggGgo.",
        ".ohdmmo..ommdho.",
        ".ohdmmo..ommdho.",
        ".odmmmo..ommmdo.",
        ".odmcCo..oCcmdo.",
        ".odmmmo..ommmdo.",
        "oodmmmooooommmdo",
        "ohmmlmmoommlmmho",
        "ohhllmmmmmmllhho",
        "okddddddddddddko",
        "okkcCkkkkkkCckko",
        ".oooooo..oooooo."], p)
    q = {
        "o": (22, 8, 40), "d": CL[1], "m": CL[2], "l": CL[3], "h": (210, 140, 240),
        "g": GOLD[2], "G": GOLD[1], "p": PINK[2], "P": PINK[3], "k": CL_DARK[0], "s": PINK[1],
    }
    icon("phase_cloth_hood", [
        "................",
        "......oooo......",
        "....oollllloo...",
        "...ollmmmmmllo..",
        "..olmmmddmmmlo..",
        "..olmmdkkdmmlo..",
        ".olmmdkkkkdmmlo.",
        ".olmdkkpPkkdmlo.",
        ".olmdkkkkkkdmlo.",
        ".ogmdkkkkkkdmgo.",
        ".olGgdkkkkdgGlo.",
        ".omlmGgggggmlmo.",
        ".odmmlGGGGlmmdo.",
        "..odmmlmmlmmdo..",
        "...ooddsddsoo...",
        "................"], q)
    icon("phase_cloth_tunic", [
        "................",
        ".ooo........ooo.",
        "ollmoo....oomllo",
        "olmmmlooooolmmmo",
        "ogGgmmlggllmgGgo",
        "olmdmmlgGlmmdmlo",
        "olmdmlmgGmlmdmlo",
        "olmddlmpPmlddmlo",
        ".odddlmPPmlddmo.",
        ".odddlmpPmlddmo.",
        ".oddsslgGlssddo.",
        ".oddmlsppslmddo.",
        ".odmmlmgGmlmmdo.",
        ".odmdlmgGmldmdo.",
        ".osdsdsGgdsdsdo.",
        "..o.s.s..s.s.o.."], q)
    icon("phase_cloth_leggings", [
        "................",
        "..oooooooooooo..",
        "..ogGgggPPggGgo.",
        "..olmmmmppmmmlo.",
        "..olmmmmkkmmmlo.",
        "..odmmmdokdmmmo.",
        "..odmlmdokdmlmo.",
        "..odmlmdokdmlmo.",
        "..odmmmdokdmmmo.",
        "..odmpmdokdmpmo.",
        "..odmPmdokdmPmo.",
        "..odmmmdokdmmmo.",
        "..osdmmdokdmmso.",
        "..os.sd.ok.ds.o.",
        "...o.s.....s.o..",
        "................"], q)
    icon("phase_cloth_boots", [
        "................",
        "................",
        "................",
        "..oooo....oooo..",
        ".ogGggo..oggGgo.",
        ".olmmlo..olmmlo.",
        ".odmmdo..odmmdo.",
        ".odmpdo..odpmdo.",
        ".odmmdo..odmmdo.",
        ".odmmdooooodmmdo",
        "olmmmmdooomlmmlo",
        "ollmmmmmmmmmmllo",
        "oddddddddddddddo",
        "ookpPkkkkkkPpkoo",
        ".ooooo....ooooo.",
        "................"], q)


if __name__ == "__main__":
    os.makedirs(ARM, exist_ok=True)
    void_steel()
    phase_cloth()
    icons()
    print("Xong giap v3")
