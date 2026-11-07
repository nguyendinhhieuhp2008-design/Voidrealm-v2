#!/usr/bin/env python3
"""Cong trinh moi + chieu Void Realm.  Chay SAU gen_data.py:  python3 tools/gen_realm.py
Sinh: void_sanctum (le te 8 cot + den tho + cong 5x5), void_nexus (dao trung tam Void Realm), 4 dao troi,
va lam lai 3 cong trinh cu (obelisk / ruins / citadel) cho dep hon. Dong thoi sinh du lieu worldgen (chieu, biome...).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_structures import T, B, Sh, I, mklist, chest, spawner, AIR  # noqa: E402
from gen_art import hash2, vnoise  # noqa: E402

BR, STN = "voidrealm:void_bricks", "voidrealm:void_stone"
TILE, CHI, SOIL, CRY = "voidrealm:void_tile", "voidrealm:void_chiseled", "voidrealm:void_soil", "voidrealm:void_crystal_block"
STAIR, SLAB = "voidrealm:void_bricks_stairs", "voidrealm:void_bricks_slab"
FRAME, PORTAL, ALTAR, LANT = "voidrealm:void_portal_frame", "voidrealm:void_portal", "voidrealm:void_altar", "voidrealm:rift_lantern"
PIL, STEEL, ORE = "voidrealm:void_pillar", "voidrealm:void_steel_block", "voidrealm:void_crystal_ore"
DREAM = "voidrealm:dream_crystal_ore"
GOLD, AME, GLASS, ROD = "minecraft:gold_block", "minecraft:amethyst_block", "minecraft:purple_stained_glass", "minecraft:end_rod"
CHAIN, CRYOBS = "minecraft:chain", "minecraft:crying_obsidian"


# ------------------------------------------------------------------ tro giup xay
def stair(t, x, y, z, facing, half="bottom", shape="straight", block=STAIR):
    t.set(x, y, z, block, {"facing": facing, "half": half, "shape": shape, "waterlogged": "false"})


def slab(t, x, y, z, typ="bottom", block=SLAB):
    t.set(x, y, z, block, {"type": typ, "waterlogged": "false"})


def pillar(t, x, y0, y1, z, block=PIL):
    for y in range(y0, y1 + 1):
        t.set(x, y, z, block, {"axis": "y"})


def chain(t, x, y0, y1, z):
    for y in range(y0, y1 + 1):
        t.set(x, y, z, CHAIN, {"axis": "y", "waterlogged": "false"})


def soft(t, x, y, z, name, props=None):
    """Dat neu con trong khung."""
    if 0 <= x < t.size[0] and 0 <= y < t.size[1] and 0 <= z < t.size[2]:
        t.set(x, y, z, name, props)


def circle_cells(cx, cz, r):
    ri = int(math.ceil(r))
    for dx in range(-ri, ri + 1):
        for dz in range(-ri, ri + 1):
            d = math.hypot(dx, dz)
            if d <= r:
                yield cx + dx, cz + dz, d, math.atan2(dz, dx)


def facing_toward(dx, dz):
    if abs(dx) > abs(dz):
        return "west" if dx > 0 else "east"
    return "north" if dz > 0 else "south"


# ------------------------------------------------------------------ cong 5x5 (dung chung)
def gate(t, cx, cz, A, active, rise=0):
    """Cong huong +z, tam (cx, cz), hang day cua mat cong o y = A. Khung 7x7 (void_portal_frame), vien ngoai + trụ.
    active=True: mat cong da co san (cho cong tra ve trong Void Realm)."""
    props = {"lit": "true" if active else "false"}
    for dx in range(-3, 4):
        for dy in range(-1, 6):
            if abs(dx) == 3 or dy in (-1, 5):
                t.set(cx + dx, A + dy, cz, FRAME, props)
    # vien ngoai day 3 lop (z-1, z, z+1)
    for dz in (-1, 0, 1):
        for dx in range(-4, 5):
            for dy in range(-1, 7):
                outer = abs(dx) == 4 or dy == 6
                if outer and not (dz == 0 and False):
                    t.set(cx + dx, A + dy, cz + dz, BR)
        # lop trong giua (z-1, z+1) bao khung
        for dx in range(-3, 4):
            for dy in range(-1, 6):
                if (abs(dx) == 3 or dy in (-1, 5)) and dz != 0:
                    t.set(cx + dx, A + dy, cz + dz, CHI if (dx + dy) % 2 == 0 else BR)
    # rune vang tren vien
    for dx in (-4, 4):
        for dy in (0, 2, 4):
            t.set(cx + dx, A + dy, cz - 1, GOLD)
            t.set(cx + dx, A + dy, cz + 1, GOLD)
    # lintel
    for dx in range(-6, 7):
        t.set(cx + dx, A + 7, cz, CHI if abs(dx) % 2 == 0 else BR)
        for dz in (-1, 1):
            t.set(cx + dx, A + 7, cz + dz, BR)
    for dx in range(-5, 6):
        t.set(cx + dx, A + 8, cz, SLAB, {"type": "bottom", "waterlogged": "false"})
    # tru hai ben
    for sx in (-6, 6):
        pillar(t, cx + sx, A - 1, A + 9, cz)
        t.set(cx + sx, A + 10, cz, CRY)
        t.set(cx + sx, A + 11, cz, ROD, {"facing": "up"})
        t.set(cx + sx - (1 if sx < 0 else -1), A + 3, cz, LANT)
    # tinh the tren dinh
    t.set(cx, A + 9, cz, CRY)
    t.set(cx, A + 10, cz, CRY)
    t.set(cx, A + 11, cz, ROD, {"facing": "up"})
    for dx in (-2, 2):
        t.set(cx + dx, A + 9, cz, AME)
    if active:
        for dx in range(-2, 3):
            for dy in range(0, 5):
                t.set(cx + dx, A + dy, cz, PORTAL, {"axis": "x"})


# ------------------------------------------------------------------ 1. DEN TE (void_sanctum)
SC = 25            # tam
FL = 5             # lop san (mat dat)
Y0 = FL + 4        # san den tho
A_Y = Y0 + 1       # o ban te
GATE_FWD = 15
PIL_R = 21
PIL_TOP = 41       # y dinh cot (tuyet doi trong template)
PILLAR_TOP_DY = PIL_TOP - A_Y


def plaza(t):
    for x, z, d, ang in circle_cells(SC, SC, 24.5):
        for y in range(0, FL):
            t.set(x, y, z, STN)
        a = math.degrees(ang) % 45
        spoke = (min(a, 45 - a) < 3.2) and 11 <= d <= 21
        if d > 23.4:
            b = BR
        elif 20.0 <= d < 20.9 and int(d * 3 + ang * 12) % 3 == 0:
            b = CHI
        elif 14.0 <= d < 15.0:
            b = GOLD
        elif 17.5 <= d < 18.5:
            b = BR
        elif spoke:
            b = BR
        elif 21.5 <= d < 22.5:
            b = GOLD
        else:
            b = TILE
        t.set(x, FL, z, b)


def big_pillar(t, cx, cz):
    # bac + bệ
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            edge = max(abs(x - cx), abs(z - cz))
            if edge == 4:
                f = facing_toward(cx - x, cz - z)
                if abs(x - cx) == 4 and abs(z - cz) == 4:
                    continue
                stair(t, x, FL + 1, z, f)
            elif edge == 3:
                t.set(x, FL + 1, z, BR)
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            for y in (FL + 1, FL + 2):
                t.set(x, y, z, BR)
            t.set(x, FL + 3, z, CHI if (abs(x - cx) == 3 or abs(z - cz) == 3) else BR)
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            pillar(t, x, FL + 4, PIL_TOP - 8, z)
    for yb in (FL + 9, FL + 19):                      # vong chiseled nhô ra
        for x in range(cx - 2, cx + 3):
            for z in range(cz - 2, cz + 3):
                if max(abs(x - cx), abs(z - cz)) == 2:
                    t.set(x, yb, z, CHI)
                    t.set(x, yb + 1, z, BR) if (abs(x - cx) == 2 and abs(z - cz) == 2) else None
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            t.set(x, PIL_TOP - 7, z, BR)
            if max(abs(x - cx), abs(z - cz)) == 3:
                t.set(x, PIL_TOP - 6, z, GOLD if (abs(x - cx) + abs(z - cz)) % 2 == 0 else BR)
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            t.set(x, PIL_TOP - 6, z, CHI) if max(abs(x - cx), abs(z - cz)) < 3 else None
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            t.set(x, PIL_TOP - 5, z, CRY)
    pillar(t, cx, PIL_TOP - 4, PIL_TOP - 1, cz, CRY)
    t.set(cx, PIL_TOP, cz, ROD, {"facing": "up"})
    for (dx, dz) in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        t.set(cx + dx, PIL_TOP - 5, cz + dz, AME)
        t.set(cx + dx, PIL_TOP - 4, cz + dz, ROD, {"facing": "up"})


def temple(t):
    c = SC
    # 4 bac nen
    for k, half in enumerate((14, 12, 10, 8)):
        y = FL + 1 + k
        for x in range(c - half, c + half + 1):
            for z in range(c - half, c + half + 1):
                t.set(x, y, z, BR)
                for yy in range(FL + 1, y):
                    t.set(x, yy, z, BR)
        # san mat tren cung la tile
    for x in range(c - 8, c + 9):
        for z in range(c - 8, c + 9):
            t.set(x, Y0, z, TILE)
    # cau thang bac phia bac (north, z nho) va hai ben
    for k, half in enumerate((14, 12, 10, 8)):
        y = FL + 1 + k
        edge = c - half - 1
        for x in range(c - 4, c + 5):
            stair(t, x, y, edge, "south")
        for z in range(c - 2, c + 3):
            stair(t, c - half - 1, y, z, "east")
            stair(t, c + half + 1, y, z, "west")
        # lop duoi cua cau thang can nen ho tro
        for x in range(c - 4, c + 5):
            for yy in range(FL + 1, y):
                t.set(x, yy, edge, BR)
    # hoa van san den tho
    for x in range(c - 8, c + 9):
        for z in range(c - 8, c + 9):
            dd = math.hypot(x - c, z - c)
            if 2.2 <= dd < 3.2 or 6.2 <= dd < 6.9:
                t.set(x, Y0, z, CHI if int(dd * 3 + x + z) % 2 == 0 else GOLD)
    # day cot
    for k in range(-7, 8, 2):
        for (x, z) in ((c + k, c - 7), (c + k, c + 7), (c - 7, c + k), (c + 7, c + k)):
            if abs(x - c) <= 1 and abs(z - c) in (7,):
                continue
            pillar(t, x, Y0 + 1, Y0 + 8, z)
            t.set(x, Y0 + 9, z, CHI)
            soft(t, x, Y0 + 1, z, BR) if False else None
    # cella: tuong |d| = 5
    for x in range(c - 5, c + 6):
        for z in range(c - 5, c + 6):
            if max(abs(x - c), abs(z - c)) == 5:
                for y in range(Y0 + 1, Y0 + 9):
                    t.set(x, y, z, BR)
    for y in range(Y0 + 1, Y0 + 5):                 # cua bac va nam
        for dx in (-1, 0, 1):
            t.set(c + dx, y, c - 5, AIR)
            t.set(c + dx, y, c + 5, AIR)
    for dx in (-1, 0, 1):
        t.set(c + dx, Y0 + 5, c - 5, CHI)
        t.set(c + dx, Y0 + 5, c + 5, CHI)
    for k in (-3, 3):                                # cua so kinh mau
        for y in range(Y0 + 4, Y0 + 7):
            for (x, z) in ((c + k, c - 5), (c + k, c + 5), (c - 5, c + k), (c + 5, c + k)):
                t.set(x, y, z, GLASS)
    for x in range(c - 5, c + 6):                    # tran
        for z in range(c - 5, c + 6):
            t.set(x, Y0 + 9, z, BR)
    # xa ngang (entablature)
    for x in range(c - 8, c + 9):
        for z in range(c - 8, c + 9):
            if max(abs(x - c), abs(z - c)) in (7, 8):
                t.set(x, Y0 + 9, z, BR if max(abs(x - c), abs(z - c)) == 8 else CHI)
                t.set(x, Y0 + 10, z, BR)
    # mai thap tang
    for k in range(0, 7):
        w = 8 - k
        y = Y0 + 11 + k
        for x in range(c - w, c + w + 1):
            for z in range(c - w, c + w + 1):
                e = max(abs(x - c), abs(z - c))
                if e == w:
                    if abs(x - c) == w and abs(z - c) == w:
                        t.set(x, y, z, BR)
                    else:
                        stair(t, x, y, z, facing_toward(x - c if abs(x - c) == w else 0, z - c if abs(z - c) == w else 0))
                else:
                    t.set(x, y, z, BR if k < 6 else CHI)
    top = Y0 + 17
    pillar(t, c, top + 1, top + 4, c, CRY)
    t.set(c, top + 5, c, ROD, {"facing": "up"})
    for (dx, dz) in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        t.set(c + dx, Y0 + 11 + 5, c + dz, GOLD)
    # noi that
    for (dx, dz) in ((3, 3), (-3, 3), (3, -3), (-3, -3)):
        t.set(c + dx, Y0 + 1, c + dz, BR)
        t.set(c + dx, Y0 + 2, c + dz, LANT)
        chain(t, c + dx, Y0 + 7, Y0 + 8, c + dz)
        t.set(c + dx, Y0 + 6, c + dz, LANT)
    t.set(c, Y0 + 8, c, CHAIN, {"axis": "y", "waterlogged": "false"})
    t.set(c, Y0 + 7, c, LANT)
    for z in (c - 4, c + 4):
        for x in (c - 4, c + 4):
            t.set(x, Y0 + 1, z, AME)
    t.set(c, A_Y, c, ALTAR, {"facing": "south", "stage": "0"})
    chest(t, c - 4, Y0 + 1, c, "east", "void_sanctum")


def dais(t):
    c = SC
    gz = c + GATE_FWD
    for x in range(c - 8, c + 9):
        for z in range(c + 7, gz + 7):
            for y in range(FL + 1, Y0):
                t.set(x, y, z, BR)
            t.set(x, Y0, z, TILE)
    for x in range(c - 8, c + 9):
        for z in range(gz - 7, gz + 7):
            d = abs(x - c)
            if d in (7, 8) or z in (gz + 6,):
                t.set(x, Y0, z, BR)
    # hoa van tren dais
    for x in range(c - 2, c + 3):
        for z in range(gz - 6, gz - 1):
            t.set(x, Y0, z, CHI if (x + z) % 2 == 0 else GOLD)
    # bac 2 ben dais
    for side in (-1, 1):
        for k in range(4):
            x = c + side * (9 + k)
            for z in (gz - 1, gz, gz + 1):
                for yy in range(FL + 1, Y0 - 3 + (3 - k) + 0):
                    pass
                for yy in range(FL + 1, Y0 - (3 - k)):
                    t.set(x, yy, z, BR)
                stair(t, x, Y0 - (3 - k), z, "west" if side > 0 else "east")
    for z in range(gz + 7, gz + 8):
        pass
    gate(t, c, gz, A_Y, False)
    # den hai ben cong
    for sx in (-7, 7):
        t.set(c + sx, Y0 + 1, gz - 3, LANT)


def sanctum():
    t = T(51, 47, 51)
    plaza(t)
    temple(t)
    dais(t)
    for k in range(8):
        ang = math.radians(22.5 + 45 * k)
        big_pillar(t, SC + int(round(PIL_R * math.sin(ang))), SC + int(round(PIL_R * math.cos(ang))))
    # cot den quanh vong
    for k in range(8):
        ang = math.radians(45 * k)
        x, z = SC + int(round(23 * math.sin(ang))), SC + int(round(23 * math.cos(ang)))
        if (x, FL + 1, z) in t.blocks:
            continue
        for y in range(FL + 1, FL + 4):
            t.set(x, y, z, PIL, {"axis": "y"})
        t.set(x, FL + 4, z, LANT)
    t.save("void_sanctum")
    return PILLAR_TOP_DY



# ------------------------------------------------------------------ dao troi dung chung
def spire(t, x, y, z, h, wide=1):
    """Ngon tinh the nhon: than rong o goc, thu hep dan."""
    for k in range(h):
        r = wide if k < h * 0.45 else 0
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + (1 if r == 0 else 0):
                    soft(t, x + dx, y + k, z + dz, CRY)
    soft(t, x, y + h, z, ROD, {"facing": "up"})


def cluster(t, x, y, z):
    soft(t, x, y, z, "minecraft:amethyst_cluster", {"facing": "up", "waterlogged": "false"})


def crystal_tree(t, x, y, z, rnd, h=None):
    h = h or rnd.randint(6, 9)
    pillar(t, x, y, y + h, z)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                d = math.sqrt(dx * dx + dy * dy * 1.4 + dz * dz)
                if d <= 3.1 and (dx or dz or dy < 0 or dy > 2) and not (dx == 0 and dz == 0 and dy <= 0):
                    r = rnd.random()
                    if r < 0.12:
                        continue
                    soft(t, x + dx, y + h + dy + 1, z + dz, CRY if r < 0.45 else (AME if r < 0.8 else GLASS))
    for dx, dz in ((2, 0), (-2, 1), (0, -2), (1, 2)):
        if rnd.random() < 0.8:
            chain(t, x + dx, y + h - 3, y + h - 3, z + dz) if False else None
            for yy in range(y + h - 3, y + h - 1):
                soft(t, x + dx, yy, z + dz, CHAIN, {"axis": "y", "waterlogged": "false"})
            soft(t, x + dx, y + h - 4, z + dz, LANT)


def island_base(t, cx, cz, top_y, R, depth, seed, with_soil=True, ore_chance=0.02, dream_chance=0.5):
    rnd = random.Random(seed)
    surface = {}
    for x, z, d, ang in circle_cells(cx, cz, int(R * 1.3)):
        w = R * (0.82 + 0.34 * vnoise(x, z, 7.0, seed))
        if d > w:
            continue
        u = d / w
        dep = int(depth * (1 - u * u) ** 0.85 * (0.7 + 0.6 * vnoise(x, z, 4.0, seed + 5))) + 1
        surf = top_y + (1 if (u < 0.6 and vnoise(x, z, 5.0, seed + 9) > 0.7) else 0)
        surface[(x, z)] = surf
        for y in range(max(0, top_y - dep), surf + 1):
            if y == surf and with_soil:
                b = SOIL
            elif y >= surf - 2 and with_soil and u < 0.95:
                b = SOIL if y == surf - 1 else STN
            else:
                b = ORE if rnd.random() < ore_chance else STN
            t.set(x, y, z, b)
    # mo Dream Crystal (hiem): cum 3-5 khoi o phan duoi / sườn dao
    cells = list(surface.keys())
    if rnd.random() < dream_chance:
        for _ in range(40):
            x, z = rnd.choice(cells)
            col = [y for (xx, y, zz) in t.blocks if xx == x and zz == z]
            if len(col) < 6:
                continue
            y0 = min(col) + rnd.randint(0, 2)
            if (x, y0, z) not in t.blocks:
                continue
            vein = {(x, y0, z)}
            want = rnd.randint(3, 5)
            for _ in range(60):
                if len(vein) >= want:
                    break
                bx, by, bz = rnd.choice(sorted(vein))
                dx, dy, dz = rnd.choice(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
                q = (bx + dx, by + dy, bz + dz)
                if q in t.blocks and t.blocks[q][0] in (STN,):
                    vein.add(q)
            if len(vein) >= 3:
                for q in vein:
                    t.set(q[0], q[1], q[2], DREAM)
                break
    # nhu thach

    for _ in range(int(R * 1.2)):
        x, z = rnd.choice(cells)
        y = top_y
        while (x, y - 1, z) in t.blocks:
            y -= 1
        ln = rnd.randint(3, 8)
        for k in range(ln):
            r = 1 if k < ln * 0.35 else 0
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if abs(dx) + abs(dz) <= r:
                        soft(t, x + dx, y - 1 - k, z + dz, STN)
        if rnd.random() < 0.5:
            soft(t, x, y - 1 - ln, z, "minecraft:amethyst_cluster", {"facing": "down", "waterlogged": "false"})
    return surface, rnd


def decorate_surface(t, surface, rnd, density=0.02, spires=3, avoid=lambda x, z: False):
    cells = [c for c in surface if not avoid(*c)]
    for _ in range(spires):
        x, z = rnd.choice(cells)
        spire(t, x, surface[(x, z)] + 1, z, rnd.randint(7, 14), 1)
    for (x, z) in cells:
        if rnd.random() < density and (x, surface[(x, z)] + 1, z) not in t.blocks:
            cluster(t, x, surface[(x, z)] + 1, z)


# ------------------------------------------------------------------ TRUNG TAM HU KHONG (nexus)
NEX_SIZE = (49, 46, 49)
NEX_TOP = 22
NEX_C = 24
NEX_GATE_Z = 14
NEX_A = NEX_TOP + 1


def nexus():
    t = T(*NEX_SIZE)
    surface, rnd = island_base(t, NEX_C, NEX_C, NEX_TOP, 22, 20, 700, True, 0.03, 0.0)
    c = NEX_C
    for k in [k for k in t.blocks if k[1] > NEX_TOP and math.hypot(k[0] - c, k[2] - c) < 15.5]:
        del t.blocks[k]
    # quang truong tile
    for x, z, d, ang in circle_cells(c, c, 13.5):
        if (x, NEX_TOP, z) not in t.blocks:
            continue
        if d > 12.5:
            b = BR
        elif 11.0 <= d < 12.0:
            b = GOLD
        elif 7.5 <= d < 8.5 and int(d * 3 + ang * 12) % 2 == 0:
            b = CHI
        elif 3.0 <= d < 4.0:
            b = BR
        else:
            a = math.degrees(ang) % 45
            b = BR if (min(a, 45 - a) < 3 and 4 <= d <= 11) else TILE
        t.set(x, NEX_TOP, z, b)
    t.set(c, NEX_TOP, c, CHI)
    gate(t, c, NEX_GATE_Z, NEX_A, True)
    # duong den tu cong ra
    for k, z in enumerate(range(NEX_GATE_Z + 4, NEX_GATE_Z + 14, 3)):
        for sx in (-3, 3):
            t.set(c + sx, NEX_TOP + 1, z, BR)
            t.set(c + sx, NEX_TOP + 2, z, LANT)
    # 2 dai phun Thac Nguoc
    for sx in (-10, 10):
        bx, bz = c + sx, c + 5
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                m = max(abs(dx), abs(dz))
                if m == 2:
                    t.set(bx + dx, NEX_TOP + 1, bz + dz, BR)
                elif m <= 1:
                    t.set(bx + dx, NEX_TOP, bz + dz, CHI if (dx == 0 and dz == 0) else GOLD)
        t.set(bx, NEX_TOP + 1, bz, "voidrealm:void_flux", {"age": "0"})
    # 4 tru tinh the
    for (dx, dz) in ((-14, -4), (14, -4), (-12, 12), (12, 12)):
        for x in range(c + dx - 1, c + dx + 2):
            for z in range(c + dz - 1, c + dz + 2):
                t.set(x, NEX_TOP + 1, z, BR)
        spire(t, c + dx, NEX_TOP + 2, c + dz, 11, 1)
    # cay tinh the o rim
    for (dx, dz) in ((-17, 6), (17, 6), (0, 18), (-6, -17), (7, -17)):
        x, z = c + dx, c + dz
        if (x, NEX_TOP, z) in t.blocks:
            crystal_tree(t, x, NEX_TOP + 1, z, rnd)
    decorate_surface(t, surface, rnd, 0.025, 0, avoid=lambda x, z: math.hypot(x - c, z - c) < 14)
    chest(t, c + 6, NEX_TOP + 1, c - 6, "south", "void_island")
    t.save("void_nexus")
    return t


# ------------------------------------------------------------------ 3 cong trinh cu, lam lai
def ring_facing(x, z, c):
    dx, dz = c - x, c - z
    if abs(dx) > abs(dz):
        return "east" if dx > 0 else "west"
    return "south" if dz > 0 else "north"


def ladder_col(t, x, y0, y1, z, facing):
    for y in range(y0, y1 + 1):
        t.set(x, y, z, "minecraft:ladder", {"facing": facing, "waterlogged": "false"})


def obelisk():
    """Thap Bia 15x36x15, FL=2. Cua o phia +z."""
    t = T(15, 36, 15)
    FL, c = 2, 7
    t.fill(0, 0, 0, 14, FL - 1, 14, STN)
    for x in range(15):
        for z in range(15):
            edge = x in (0, 14) or z in (0, 14)
            if edge:
                t.set(x, FL, z, STN)
                stair(t, x, FL, z, ring_facing(x, z, c)) if (x not in (0, 14) or z not in (0, 14)) else None
            else:
                m = max(abs(x - c), abs(z - c))
                t.set(x, FL, z, CHI if m in (3, 4) and (x + z) % 2 == 0 else (BR if m == 5 else TILE))
    # 2 tang than thap (9x9)
    for base, top in ((FL + 1, FL + 10), (FL + 12, FL + 21)):
        t.fill(3, base, 3, 11, top, 11, AIR)
        for x in range(3, 12):
            for z in range(3, 12):
                if x in (3, 11) or z in (3, 11):
                    for y in range(base, top + 1):
                        t.set(x, y, z, BR)
        for cx in (3, 11):
            for cz in (3, 11):
                pillar(t, cx, base, top, cz)
        for y in range(base + 3, top - 1):                       # cua so kinh dung
            for p in (5, 9):
                for (x, z) in ((3, p), (11, p), (p, 3), (p, 11)):
                    if not (z == 11 and base == FL + 1 and y < FL + 5):
                        t.set(x, y, z, GLASS)
        for y in (base, top):                                    # dai chi
            for x in range(3, 12):
                for z in range(3, 12):
                    if x in (3, 11) or z in (3, 11):
                        t.set(x, y, z, CHI if (x + z) % 2 == 0 else GOLD)
    for x in range(3, 12):                                       # san cac tang
        for z in range(3, 12):
            t.set(x, FL + 11, z, TILE)
            t.set(x, FL + 22, z, TILE)
    t.fill(6, FL + 1, 11, 8, FL + 4, 11, AIR)                    # cua
    for dx in (-2, 2):
        t.set(c + dx, FL + 4, 12, LANT)
        pillar(t, c + dx, FL + 1, FL + 3, 12)
    for k in range(3):                                           # bac cap
        for x in range(6, 9):
            stair(t, x, FL, 12 + k // 2 + (1 if k == 2 else 0), "north") if False else None
    # thang
    ladder_col(t, 4, FL + 1, FL + 10, 7, "east")
    t.set(4, FL + 11, 7, AIR)
    ladder_col(t, 4, FL + 11, FL + 22, 7, "east")
    t.set(4, FL + 22, 7, AIR)
    ladder_col(t, 4, FL + 22, FL + 23, 7, "east")
    # noi that
    for (x, z) in ((5, 5), (9, 5), (5, 9), (9, 9)):
        t.set(x, FL + 1, z, BR)
        t.set(x, FL + 2, z, LANT)
    t.set(c, FL + 1, c, CHI)
    t.set(c, FL + 2, c, CRY)
    chest(t, 9, FL + 1, 7, "west", "void_obelisk")
    spawner(t, c, FL + 12, c, "rift_archer")
    for (x, z) in ((5, 5), (9, 9), (5, 9), (9, 5)):
        t.set(x, FL + 12, z, LANT)
    # san thuong + lan can
    for x in range(3, 12):
        for z in range(3, 12):
            if x in (3, 11) or z in (3, 11):
                t.set(x, FL + 23, z, BR)
                if (x + z) % 2 == 0:
                    t.set(x, FL + 24, z, STN)
    t.set(4, FL + 23, 7, AIR)
    t.set(4, FL + 23, 7, "minecraft:ladder", {"facing": "east", "waterlogged": "false"})
    t.fill(6, FL + 23, 6, 8, FL + 23, 8, STN)
    t.fill(7, FL + 24, 7, 7, FL + 29, 7, STEEL)
    t.set(7, FL + 30, 7, ROD, {"facing": "up"})
    t.set(7, FL + 31, 7, LANT)
    for (x, z) in ((6, 7), (8, 7), (7, 6), (7, 8)):
        t.set(x, FL + 25, z, CRY)
    chest(t, 10, FL + 23, 7, "west", "void_obelisk")
    for (x, z) in ((4, 4), (10, 4), (4, 10), (10, 10)):
        t.set(x, FL + 23, z, LANT)
    # tru hinh quanh chan
    for (x, z) in ((1, 1), (13, 1), (1, 13), (13, 13)):
        pillar(t, x, FL + 1, FL + 5, z)
        t.set(x, FL + 6, z, LANT)
    t.save("void_obelisk")
    return t


def ruins():
    """Phe Tich 19x12x19, FL=1."""
    rnd = random.Random(1840202)
    t = T(19, 12, 19)
    FL, c = 1, 9
    for x, z, d, ang in circle_cells(c, c, 9.4):
        for y in range(0, FL):
            t.set(x, y, z, STN)
        r = rnd.random()
        if d > 8.2:
            b = BR if r > 0.3 else STN
        elif d < 2.6:
            b = CHI
        elif 5.6 <= d < 6.4:
            b = GOLD if int(ang * 8 / math.pi) % 2 == 0 else TILE
        else:
            b = TILE if r > 0.18 else ("minecraft:cracked_deepslate_bricks" if r > 0.06 else BR)
        if r < 0.05 and d > 3:
            continue
        t.set(x, FL, z, b)
    for k in range(8):                                           # cot gay
        ang = math.radians(45 * k + 22.5)
        x, z = c + int(round(7 * math.sin(ang))), c + int(round(7 * math.cos(ang)))
        h = rnd.choice([2, 3, 4, 6, 7, 8])
        for y in range(FL + 1, FL + 1 + h):
            t.set(x, y, z, PIL, {"axis": "y"})
        if h < 6:
            stair(t, x, FL + 1 + h, z, ring_facing(x, z, c), "bottom")
        else:
            t.set(x, FL + 1 + h, z, LANT)
        for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):      # manh vo
            if rnd.random() < 0.35:
                soft(t, x + dx * 2, FL + 1, z + dz * 2, BR)
    for z in (c - 3, c + 3):                                     # vom do nat
        for y in range(FL + 1, FL + 5):
            pillar(t, c - 3, y, y, z) if y < FL + 5 else None
    t.set(c - 3, FL + 5, c - 3, BR)
    for x in range(c - 3, c):
        t.set(x, FL + 5, c - 3, STN)
    # dai tho giua
    t.fill(c - 1, FL + 1, c - 1, c + 1, FL + 1, c + 1, STN)
    t.set(c, FL + 2, c, CHI)
    t.set(c, FL + 3, c, "minecraft:crying_obsidian")
    chest(t, c + 1, FL + 2, c - 1, "south", "rift_ruins")
    spawner(t, c - 1, FL + 2, c + 1, "void_walker")
    for (x, z) in ((c - 4, c), (c + 4, c)):
        cluster(t, x, FL + 1, z)
    for _ in range(14):
        a = rnd.random() * 6.28
        d = 3 + rnd.random() * 5
        x, z = c + int(d * math.cos(a)), c + int(d * math.sin(a))
        if (x, FL + 1, z) not in t.blocks and (x, FL, z) in t.blocks:
            t.set(x, FL + 1, z, rnd.choice([BR, STN, CRYOBS, "minecraft:cobweb"]))
    t.entity("voidrealm:void_walker", c + 3.5, FL + 1.0, c + 3.5)
    t.save("rift_ruins")
    return t


def citadel():
    """Phao Dai 39x40x39, FL=5. Cong chinh o phia +z, ngai vang o phia -z."""
    t = T(39, 40, 39)
    FL, c = 5, 19
    t.fill(0, 0, 0, 38, FL - 1, 38, STN)
    for x in range(39):
        for z in range(39):
            if x in (0, 38) or z in (0, 38):
                t.set(x, FL, z, STN)
                if not (x in (0, 38) and z in (0, 38)):
                    stair(t, x, FL, z, ring_facing(x, z, c))
            else:
                m = max(abs(x - c), abs(z - c))
                t.set(x, FL, z, GOLD if m == 15 else (BR if m in (14, 16, 17) else TILE if (x + z) % 7 else CHI))
    # tuong ngoai 31x31 (4..34), cao 9, nhip nham
    for x in range(4, 35):
        for z in range(4, 35):
            if x in (4, 34) or z in (4, 34):
                for y in range(FL + 1, FL + 9):
                    t.set(x, y, z, BR)
                if (x + z) % 2 == 0:
                    t.set(x, FL + 9, z, STN)
    for x in range(4, 35):
        for z in (4, 34):
            t.set(x, FL + 8, z, CHI if x % 4 == 0 else BR)
    t.fill(16, FL + 1, 34, 22, FL + 7, 34, AIR)                  # cong
    for sx in (15, 23):
        pillar(t, sx, FL + 1, FL + 9, 34)
    for x in range(15, 24):
        t.set(x, FL + 8, 34, CHI if x % 2 else GOLD)
    for x in (16, 22):
        t.set(x, FL + 6, 33, LANT)
    # 4 thap goc 7x7, cao 22
    for (cx, cz) in ((4, 4), (34, 4), (4, 34), (34, 34)):
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                if max(abs(dx), abs(dz)) == 3:
                    for y in range(FL + 1, FL + 21):
                        t.set(cx + dx, y, cz + dz, BR)
                elif max(abs(dx), abs(dz)) <= 2:
                    t.set(cx + dx, FL + 12, cz + dz, TILE)
                    t.set(cx + dx, FL + 21, cz + dz, TILE)
        for y in range(FL + 1, FL + 21):
            for (ex, ez) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
                t.set(cx + ex, y, cz + ez, PIL, {"axis": "y"})
        for y in (FL + 6, FL + 7, FL + 15, FL + 16):
            for p in (-1, 1):
                for (x, z) in ((cx - 3, cz + p), (cx + 3, cz + p), (cx + p, cz - 3), (cx + p, cz + 3)):
                    t.set(x, y, z, GLASS)
        spire(t, cx, FL + 22, cz, 11, 1)
        t.set(cx, FL + 14, cz, LANT)
        t.set(cx, FL + 5 + 2, cz, LANT)
    # tru + den san trong
    for (x, z) in ((11, 30), (27, 30), (11, 24), (27, 24)):
        pillar(t, x, FL + 1, FL + 4, z)
        t.set(x, FL + 5, z, LANT)
    # chinh dien: 15x15 (12..26), cao 22, chua ngai vang
    K0, K1 = 12, 26
    for x in range(K0, K1 + 1):
        for z in range(K0, K1 + 1):
            wall = x in (K0, K1) or z in (K0, K1)
            for y in range(FL + 1, FL + 23):
                if wall:
                    t.set(x, y, z, BR)
            t.set(x, FL + 22, z, TILE)
    t.fill(K0 + 1, FL + 1, K0 + 1, K1 - 1, FL + 21, K1 - 1, AIR)
    for x in range(K0 + 1, K1):
        for z in range(K0 + 1, K1):
            t.set(x, FL + 22, z, TILE)
    for (x, z) in ((K0, K0), (K1, K0), (K0, K1), (K1, K1)):
        pillar(t, x, FL + 1, FL + 22, z)
    for y in range(FL + 1, FL + 22, 7):                          # dai tuong
        for x in range(K0, K1 + 1):
            for z in range(K0, K1 + 1):
                if x in (K0, K1) or z in (K0, K1):
                    t.set(x, y + 6 if y + 6 <= FL + 21 else y, z, CHI if (x + z) % 2 else GOLD)
    for y in (FL + 4, FL + 5, FL + 6, FL + 11, FL + 12, FL + 13, FL + 17, FL + 18):
        for p in (15, 17, 19, 21, 23):
            for (x, z) in ((K0, p), (K1, p), (p, K0)):
                t.set(x, y, z, GLASS)
    t.fill(17, FL + 1, K1, 21, FL + 5, K1, AIR)                  # cua dien
    for x in (16, 22):
        pillar(t, x, FL + 1, FL + 6, K1)
    for x in range(16, 23):
        t.set(x, FL + 6, K1, CHI)
    # 4 tru trong dai sanh + den chum
    for (x, z) in ((15, 16), (23, 16), (15, 22), (23, 22)):
        pillar(t, x, FL + 1, FL + 15, z)
        t.set(x, FL + 16, z, CHI)
        t.set(x, FL + 5, z - 1, LANT)
        t.set(x, FL + 5, z + 1, LANT)
    # ban tho + ngai vang (z = 13..16)
    t.fill(14, FL + 1, 13, 24, FL + 1, 16, STN)
    t.fill(15, FL + 2, 13, 23, FL + 2, 15, BR)
    t.fill(17, FL + 3, 13, 21, FL + 3, 14, STEEL)
    t.fill(18, FL + 4, 13, 20, FL + 5, 13, CHI)
    t.set(19, FL + 6, 13, GOLD)
    for x in (17, 21):
        pillar(t, x, FL + 4, FL + 8, 13)
        t.set(x, FL + 9, 13, LANT)
    for x in range(14, 25):
        stair(t, x, FL + 1, 17, "north") if x not in (19,) else stair(t, x, FL + 1, 17, "north")
    chest(t, 15, FL + 3, 13, "south", "void_citadel")
    chest(t, 23, FL + 3, 13, "south", "void_citadel")
    # tho nguyet quang: tuong sau co tinh the
    for x in (14, 24):
        spire(t, x, FL + 2, 18, 5, 1) if False else None
    # mai nhon + thap trung tam
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            m = max(abs(dx), abs(dz))
            if m <= 4:
                t.set(c + dx, FL + 23, c + dz, BR if m == 4 else TILE)
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            t.set(c + dx, FL + 24, c + dz, BR if max(abs(dx), abs(dz)) == 2 else CHI)
    spire(t, c, FL + 25, c, 8, 2)
    t.set(c, FL + 33, c, LANT)
    # ranh gioi san: den hai ben loi di
    for z in range(K1 + 2, 33, 3):
        for sx in (-2, 2):
            t.set(c + sx, FL + 1, z, BR)
            t.set(c + sx, FL + 2, z, LANT)
    t.entity("voidrealm:void_sovereign", 19.5, FL + 3.0, 15.5)
    t.entity("voidrealm:rift_brute", 16.5, FL + 1.0, 20.5)
    t.entity("voidrealm:rift_brute", 22.5, FL + 1.0, 20.5)
    t.entity("voidrealm:void_walker", 19.5, FL + 1.0, 23.5)
    t.save("void_citadel")
    return t


# ------------------------------------------------------------------ 4 dao troi
def island_a():
    top, R = 20, 15
    t = T(2 * R + 5, top + 26, 2 * R + 5)
    c = R + 2
    surface, rnd = island_base(t, c, c, top, R, 17, 801)
    decorate_surface(t, surface, rnd, 0.05, 6)
    for _ in range(3):
        x, z = rnd.choice(list(surface))
        crystal_tree(t, x, surface[(x, z)] + 1, z, rnd)
    t.save("void_island_a")
    return t


def island_b():
    top, R = 18, 13
    t = T(2 * R + 5, top + 24, 2 * R + 5)
    c = R + 2
    surface, rnd = island_base(t, c, c, top, R, 15, 802)
    # den tho nho: cong vom + 4 cot + ban lo
    for x in range(c - 4, c + 5):
        for z in range(c - 4, c + 5):
            if math.hypot(x - c, z - c) <= 4.6:
                t.set(x, top, z, TILE if (x + z) % 2 else BR)
    for (dx, dz) in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
        h = rnd.randint(4, 7)
        pillar(t, c + dx, top + 1, top + h, c + dz)
        t.set(c + dx, top + h + 1, c + dz, CHI)
    for dx in range(-3, 4):
        t.set(c + dx, top + 6, c - 3, BR) if (c + dx, top + 6, c - 3) not in t.blocks else None
    for dx in (-1, 0, 1):
        t.set(c + dx, top + 1, c, SLAB, {"type": "bottom", "waterlogged": "false"}) if dx else None
    t.set(c, top + 1, c, CHI)
    t.set(c, top + 2, c, LANT)
    spire(t, c, top + 3, c, 6, 0) if False else None
    chest(t, c, top + 1, c + 3, "north", "void_island")
    spawner(t, c - 3, top + 1, c, "phase_stalker")
    decorate_surface(t, surface, rnd, 0.04, 3, avoid=lambda x, z: math.hypot(x - c, z - c) < 6)
    t.save("void_island_b")
    return t


def island_c():
    top, R = 18, 17
    t = T(2 * R + 5, top + 30, 2 * R + 5)
    c = R + 2
    surface, rnd = island_base(t, c, c, top, R, 14, 803)
    # ho phun thac nguoc
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            m = max(abs(dx), abs(dz))
            if m == 2:
                t.set(c + dx, top + 1, c + dz, BR)
            else:
                t.set(c + dx, top, c + dz, GOLD if (dx or dz) else CHI)
    t.set(c, top + 1, c, "voidrealm:void_flux", {"age": "0"})
    for (dx, dz) in ((7, 3), (-8, 1), (3, -8), (-4, 8), (9, -6), (-9, -7)):
        x, z = c + dx, c + dz
        if (x, surface.get((x, z), top), z) in t.blocks:
            crystal_tree(t, x, surface[(x, z)] + 1, z, rnd)
    t.entity("voidrealm:void_stalker_bird", c + 4.5, top + 1.0, c + 4.5)
    decorate_surface(t, surface, rnd, 0.035, 2, avoid=lambda x, z: math.hypot(x - c, z - c) < 4)
    t.save("void_island_c")
    return t


def island_d():
    top, R = 26, 10
    t = T(2 * R + 5, top + 34, 2 * R + 5)
    c = R + 2
    surface, rnd = island_base(t, c, c, top, R, 24, 804, True, 0.05)
    # thap nhon: than da + dai vang + ngon tinh the
    for y in range(top + 1, top + 16):
        w = 2 if y < top + 9 else 1
        for dx in range(-w, w + 1):
            for dz in range(-w, w + 1):
                if abs(dx) + abs(dz) <= w + (1 if w == 1 else 0):
                    t.set(c + dx, y, c + dz, PIL if (dx == 0 and dz == 0) or w == 1 else BR, {"axis": "y"} if (dx == 0 and dz == 0) or w == 1 else None)
    for y in (top + 4, top + 9, top + 13):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if max(abs(dx), abs(dz)) == 2 and abs(dx) + abs(dz) <= 3:
                    t.set(c + dx, y, c + dz, GOLD if y == top + 9 else CHI)
    spire(t, c, top + 16, c, 14, 1)
    t.set(c, top + 1, c + 3, LANT)
    t.entity("voidrealm:void_stalker_bird", c + 3.5, top + 1.0, c - 3.5)
    decorate_surface(t, surface, rnd, 0.06, 2, avoid=lambda x, z: math.hypot(x - c, z - c) < 4)
    t.save("void_island_d")
    return t


# ------------------------------------------------------------------ xem truoc (chi de kiem tra bang mat)
PREVIEW_COL = {
    BR: (90, 70, 150), STN: (50, 36, 90), TILE: (70, 60, 130), CHI: (60, 220, 230), SOIL: (50, 160, 150), CRY: (200, 130, 255),
    STAIR: (110, 90, 170), SLAB: (110, 90, 170), FRAME: (230, 190, 60), PORTAL: (120, 200, 255), ALTAR: (255, 255, 255),
    LANT: (255, 160, 255), PIL: (120, 100, 190), STEEL: (130, 120, 200), ORE: (160, 90, 230), GOLD: (250, 210, 70), AME: (170, 100, 220),
    GLASS: (200, 120, 240), ROD: (255, 255, 255), CHAIN: (120, 120, 140), CRYOBS: (50, 10, 90), "minecraft:chest": (200, 130, 50),
    "voidrealm:void_flux": (140, 220, 255), "minecraft:spawner": (30, 30, 60),
}


def preview(t, name, outdir):
    from PIL import Image
    sx, sy, sz = t.size
    top = Image.new("RGB", (sx, sz), (20, 20, 30))
    front = Image.new("RGB", (sx, sy), (20, 20, 30))
    for (x, y, z), (nm, props, nbt) in t.blocks.items():
        if nm == AIR:
            continue
        col = PREVIEW_COL.get(nm, (255, 0, 0))
        top.putpixel((x, z), tuple(int(c * (0.45 + 0.55 * y / max(1, sy))) for c in col)) if True else None
    # lay khoi cao nhat o moi cot
    best = {}
    for (x, y, z), (nm, props, nbt) in t.blocks.items():
        if nm != AIR and ((x, z) not in best or y > best[(x, z)][0]):
            best[(x, z)] = (y, nm)
    for (x, z), (y, nm) in best.items():
        col = PREVIEW_COL.get(nm, (255, 0, 0))
        top.putpixel((x, z), tuple(int(c * (0.4 + 0.6 * y / max(1, sy))) for c in col))
    nearest = {}
    for (x, y, z), (nm, props, nbt) in t.blocks.items():
        if nm != AIR and ((x, y) not in nearest or z < nearest[(x, y)][0]):
            nearest[(x, y)] = (z, nm)
    for (x, y), (z, nm) in nearest.items():
        col = PREVIEW_COL.get(nm, (255, 0, 0))
        front.putpixel((x, sy - 1 - y), tuple(int(c * (0.5 + 0.5 * (1 - z / max(1, sz)))) for c in col))
    W = Image.new("RGB", (sx * 6 + sz * 6 + 30, max(sz, sy) * 6 + 10), (40, 40, 50))
    W.paste(top.resize((sx * 6, sz * 6), Image.NEAREST), (5, 5))
    W.paste(front.resize((sx * 6, sy * 6), Image.NEAREST), (sx * 6 + 20, 5))
    W.save(os.path.join(outdir, "prev_" + name + ".png"))


if __name__ == "__main__":
    sanctum()
    nexus()
    for f in (island_a, island_b, island_c, island_d):
        f()
    obelisk()
    ruins()
    citadel()
    import gen_realm_data as D
    D.write_all({"GATE_FWD": GATE_FWD, "PIL_R": PIL_R, "PILLAR_TOP_DY": PILLAR_TOP_DY,
                 "ORIGIN": (-24, 60, -24), "ARRIVE": (NEX_C, NEX_A, NEX_GATE_Z + 5), "MARK": (NEX_C, NEX_A, NEX_GATE_Z)})
    print("gen_realm xong")
