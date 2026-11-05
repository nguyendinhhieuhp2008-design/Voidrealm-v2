#!/usr/bin/env python3
"""Sinh 3 cong trinh (.nbt) cho Void Realm: Thap Bia, Phe Tich, Thanh Tri Hu Khong.
Chay: python3 tools/gen_structures.py
Chi nhung o duoc dat ro rang moi nam trong file (cac o con lai giu nguyen dia hinh).
Lop 'san' (floor layer) la lop FL; cac lop duoi no la mong (xem STRUCTS trong gen_data.py: start_height = -FL).
"""
import gzip
import math
import os
import random
import struct

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "data", "voidrealm", "structure")
os.makedirs(OUT, exist_ok=True)
DATA_VERSION = 3955  # Minecraft 1.21.1


# ------------------------------------------------------------ NBT toi gian
def _s(v):
    b = v.encode("utf-8")
    return struct.pack(">H", len(b)) + b


class B(int): pass      # byte
class Sh(int): pass     # short
class I(int): pass      # int
class F(float): pass    # float
class D(float): pass    # double
class L(list): pass     # list; truyen (tag_id, [items])


def tag_id(v):
    if isinstance(v, B): return 1
    if isinstance(v, Sh): return 2
    if isinstance(v, I): return 3
    if isinstance(v, F): return 5
    if isinstance(v, D): return 6
    if isinstance(v, str): return 8
    if isinstance(v, L): return 9
    if isinstance(v, dict): return 10
    raise TypeError(type(v))


def payload(v):
    if isinstance(v, B): return struct.pack(">b", v)
    if isinstance(v, Sh): return struct.pack(">h", v)
    if isinstance(v, I): return struct.pack(">i", v)
    if isinstance(v, F): return struct.pack(">f", v)
    if isinstance(v, D): return struct.pack(">d", v)
    if isinstance(v, str): return _s(v)
    if isinstance(v, L):
        tid, items = v.tid, list(v)
        return struct.pack(">bi", tid, len(items)) + b"".join(payload(i) for i in items)
    if isinstance(v, dict):
        out = b""
        for k, val in v.items():
            out += struct.pack(">b", tag_id(val)) + _s(k) + payload(val)
        return out + b"\x00"
    raise TypeError(type(v))


def mklist(tid, items):
    l = L(items)
    l.tid = tid
    return l


def write_nbt(path, root):
    data = struct.pack(">b", 10) + _s("") + payload(root)
    with gzip.GzipFile(path, "wb", mtime=0) as f:
        f.write(data)


# ------------------------------------------------------------ khung xay dung
class T:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.blocks = {}
        self.entities = []

    def set(self, x, y, z, name, props=None, nbt=None):
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]):
            raise ValueError("ngoai khung: %s" % ((x, y, z),))
        self.blocks[(x, y, z)] = (name, tuple(sorted((props or {}).items())), nbt)

    def fill(self, x0, y0, z0, x1, y1, z1, name, props=None):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.set(x, y, z, name, props)

    def shell(self, x0, y0, z0, x1, y1, z1, name):
        """Chi dat vo ngoai (4 mat ben) cua hop, khong dat san/tran."""
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    if x in (x0, x1) or z in (z0, z1):
                        self.set(x, y, z, name)

    def entity(self, name, x, y, z, extra=None):
        nbt = {"id": name, "PersistenceRequired": B(1)}
        if extra:
            nbt.update(extra)
        self.entities.append(((x, y, z), nbt))

    def save(self, fname):
        palette, index = [], {}
        blocks = []
        for (x, y, z), (name, props, nbt) in sorted(self.blocks.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2])):
            key = (name, props)
            if key not in index:
                index[key] = len(palette)
                e = {"Name": name}
                if props:
                    e["Properties"] = {k: v for k, v in props}
                palette.append(e)
            b = {"pos": mklist(3, [I(x), I(y), I(z)]), "state": I(index[key])}
            if nbt:
                b["nbt"] = nbt
            blocks.append(b)
        ents = []
        for (x, y, z), nbt in self.entities:
            ents.append({"pos": mklist(6, [D(x), D(y), D(z)]),
                         "blockPos": mklist(3, [I(int(math.floor(x))), I(int(math.floor(y))), I(int(math.floor(z)))]),
                         "nbt": nbt})
        root = {"DataVersion": I(DATA_VERSION),
                "size": mklist(3, [I(v) for v in self.size]),
                "palette": mklist(10, palette), "blocks": mklist(10, blocks), "entities": mklist(10, ents)}
        write_nbt(os.path.join(OUT, fname + ".nbt"), root)
        print("%-14s kich thuoc=%s  so khoi=%d  thuc the=%d" % (fname, self.size, len(blocks), len(ents)))


AIR = "minecraft:air"
STONE, BRICK, STEEL, LANT = "voidrealm:void_stone", "voidrealm:void_bricks", "voidrealm:void_steel_block", "voidrealm:rift_lantern"
GLASS = "minecraft:purple_stained_glass"
CRY, OBS = "minecraft:crying_obsidian", "minecraft:obsidian"
CRACK = "minecraft:cracked_deepslate_bricks"


def chest(t, x, y, z, facing, table):
    t.set(x, y, z, "minecraft:chest", {"facing": facing, "type": "single", "waterlogged": "false"},
          {"id": "minecraft:chest", "LootTable": "voidrealm:chests/" + table})


def spawner(t, x, y, z, mob):
    t.set(x, y, z, "minecraft:spawner", None, {
        "id": "minecraft:mob_spawner",
        "SpawnData": {"entity": {"id": "voidrealm:" + mob}},
        "Delay": Sh(20), "MinSpawnDelay": Sh(400), "MaxSpawnDelay": Sh(1000),
        "SpawnCount": Sh(2), "MaxNearbyEntities": Sh(4), "RequiredPlayerRange": Sh(14), "SpawnRange": Sh(4)})


def ladder(t, x, y0, y1, z, facing):
    for y in range(y0, y1 + 1):
        t.set(x, y, z, "minecraft:ladder", {"facing": facing, "waterlogged": "false"})


# ------------------------------------------------------------ 1. Thap Bia (9 x 22 x 9), FL = 2
def obelisk():
    t = T(9, 22, 9)
    FL = 2
    t.fill(0, 0, 0, 8, FL - 1, 8, STONE)
    t.fill(0, FL, 0, 8, FL, 8, BRICK)
    for base, top in ((3, 8), (10, 14)):                      # hai tang
        t.fill(1, base, 1, 7, top, 7, AIR)
        t.shell(0, base, 0, 8, top, 8, BRICK)
    for y in range(3, 15):                                    # cot goc
        for cx in (0, 8):
            for cz in (0, 8):
                t.set(cx, y, cz, STONE)
    t.fill(0, 9, 0, 8, 9, 8, BRICK)                           # san tang 2
    t.fill(0, 15, 0, 8, 15, 8, BRICK)                         # san mai
    for y in (5, 6, 11, 12):                                  # cua so kinh (tranh cot thang o z=4)
        for z in (2, 6):
            t.set(0, y, z, GLASS)
            t.set(8, y, z, GLASS)
        for x in (2, 6):
            t.set(x, y, 0, GLASS)
            if y > 6:
                t.set(x, y, 8, GLASS)
    t.fill(3, 3, 8, 5, 5, 8, AIR)                             # cong vao (phia z=8)
    t.set(2, 5, 8, LANT)
    t.set(6, 5, 8, LANT)
    # thang leo o sat tuong x=0
    ladder(t, 1, 3, 8, 4, "east")
    t.set(1, 9, 4, "minecraft:ladder", {"facing": "east", "waterlogged": "false"})
    ladder(t, 1, 10, 15, 4, "east")
    for (x, z) in ((7, 1), (1, 7), (7, 7)):
        t.set(x, 3, z, LANT)
    chest(t, 7, 3, 4, "west", "void_obelisk")
    spawner(t, 4, 10, 4, "rift_archer")
    for (x, z) in ((7, 1), (1, 7), (7, 7), (1, 1)):
        t.set(x, 10, z, LANT)
    # mai + lan can + ngon thap bia
    for x in range(9):
        for z in range(9):
            if x in (0, 8) or z in (0, 8):
                t.set(x, 16, z, BRICK)
                if (x + z) % 2 == 0:
                    t.set(x, 17, z, STONE)
    t.fill(3, 16, 3, 5, 16, 5, STONE)
    t.fill(4, 17, 4, 4, 19, 4, BRICK)
    t.set(4, 20, 4, STEEL)
    t.set(4, 21, 4, LANT)
    chest(t, 6, 16, 4, "west", "void_obelisk")
    for (x, z) in ((1, 1), (7, 1), (1, 7), (7, 7)):
        t.set(x, 17, z, LANT)
    t.save("void_obelisk")


# ------------------------------------------------------------ 2. Phe Tich (15 x 9 x 15), FL = 1
def ruins():
    rnd = random.Random(1840202)
    t = T(15, 9, 15)
    c, R = 7, 7
    for x in range(15):
        for z in range(15):
            d = math.hypot(x - c, z - c)
            if d <= R + 0.3:
                t.set(x, 0, z, STONE)
                r = rnd.random()
                t.set(x, 1, z, BRICK if r < 0.45 else (STONE if r < 0.8 else CRACK))
                if d <= 3.2 and (x + z) % 2 == 0:
                    t.set(x, 1, z, OBS)
    for k in range(8):                                         # 8 tru da, gay do nhieu muc
        a = k * math.pi / 4
        px, pz = int(round(c + 6 * math.cos(a))), int(round(c + 6 * math.sin(a)))
        h = rnd.randint(2, 7)
        for y in range(2, 2 + h):
            t.set(px, y, pz, BRICK if y < 2 + h - 1 else (CRY if rnd.random() < 0.6 else CRACK))
        if k % 3 == 0:
            t.set(px, 2 + h, pz, LANT)
    for _ in range(14):                                        # da vun
        x, z = rnd.randint(1, 13), rnd.randint(1, 13)
        if 3.5 < math.hypot(x - c, z - c) < 6 and (x, 2, z) not in t.blocks:
            t.set(x, 2, z, rnd.choice([STONE, CRACK, BRICK]))
    t.fill(6, 2, 6, 8, 2, 8, STONE)                            # ban tho
    spawner(t, 7, 3, 7, "void_walker")
    for (x, z) in ((6, 6), (8, 6), (6, 8), (8, 8)):
        t.set(x, 3, z, LANT)
    chest(t, 10, 2, 7, "west", "rift_ruins")
    t.save("rift_ruins")


# ------------------------------------------------------------ 3. Thanh Tri (31 x 28 x 31), FL = 5
def citadel():
    t = T(31, 28, 31)
    FL, N = 5, 30
    t.fill(0, 0, 0, N, FL - 1, N, STONE)
    for x in range(N + 1):
        for z in range(N + 1):
            t.set(x, FL, z, BRICK if (x + z) % 2 == 0 else STONE)
    for x in range(14, 17):                                    # loi di tu cong den thap chinh
        for z in range(22, N + 1):
            t.set(x, FL, z, STEEL if x == 15 and z % 3 == 0 else OBS)
    # tuong thanh day 2 o, cao 9 (y=6..14) + rang cua
    for x in range(N + 1):
        for z in range(N + 1):
            edge = min(x, z, N - x, N - z)
            if edge <= 1:
                for y in range(FL + 1, FL + 10):
                    t.set(x, y, z, BRICK)
                if edge == 0 and (x + z) % 2 == 0:
                    t.set(x, FL + 10, z, STONE)
    t.fill(13, FL + 1, 29, 17, FL + 6, 30, AIR)                # cong thanh
    t.fill(12, FL + 1, 29, 12, FL + 7, 30, STONE)
    t.fill(18, FL + 1, 29, 18, FL + 7, 30, STONE)
    t.fill(12, FL + 7, 29, 18, FL + 7, 30, STONE)
    t.set(11, FL + 4, 28, LANT)
    t.set(19, FL + 4, 28, LANT)
    # 4 thap goc 7x7, cao 15
    towers = {(0, 0): "void_walker", (24, 0): None, (0, 24): None, (24, 24): "void_walker"}
    for (ox, oz), mob in towers.items():
        t.fill(ox + 1, FL + 1, oz + 1, ox + 5, FL + 14, oz + 5, AIR)
        t.shell(ox, FL + 1, oz, ox + 6, FL + 14, oz + 6, BRICK)
        t.fill(ox, FL + 15, oz, ox + 6, FL + 15, oz + 6, STONE)
        for x in range(ox, ox + 7):
            for z in range(oz, oz + 7):
                if (x in (ox, ox + 6) or z in (oz, oz + 6)) and (x + z) % 2 == 0:
                    t.set(x, FL + 16, z, STONE)
        for y in (FL + 4, FL + 5, FL + 9, FL + 10):            # kinh
            t.set(ox if ox == 0 else ox + 6, y, oz + 3, GLASS)
            t.set(ox + 3, y, oz if oz == 0 else oz + 6, GLASS)
        # cua thap huong vao san
        dx = ox + 6 if ox == 0 else ox
        t.fill(dx, FL + 1, oz + 3, dx, FL + 3, oz + 3, AIR)
        t.set(ox + 3, FL + 1 + 7, oz + 3, LANT)
        t.set(ox + 3, FL + 17, oz + 3, LANT)
        if mob:
            spawner(t, ox + 3, FL + 1, oz + 3, "phase_stalker")
        else:
            chest(t, ox + 3, FL + 1, oz + 3, "south", "void_citadel")
    # ===== thap chinh (keep) 15x15: x,z = 8..22
    t.fill(10, FL + 1, 10, 20, FL + 12, 20, AIR)
    t.shell(8, FL + 1, 8, 22, FL + 12, 22, BRICK)
    for x in range(8, 23):                                     # tuong day 2 o (lop trong)
        for z in range(8, 23):
            if min(x - 8, z - 8, 22 - x, 22 - z) == 1:
                for y in range(FL + 1, FL + 13):
                    t.set(x, y, z, BRICK)
    t.fill(8, FL + 13, 8, 22, FL + 14, 22, STONE)              # mai
    for x in range(8, 23):
        for z in range(8, 23):
            if (x in (8, 22) or z in (8, 22)) and (x + z) % 2 == 0:
                t.set(x, FL + 15, z, STONE)
    t.fill(14, FL + 1, 21, 16, FL + 4, 22, AIR)                # cua vao dien
    for y in (FL + 5, FL + 6, FL + 8, FL + 9):                 # cua so kinh
        for p in (9, 13, 17, 21):
            t.set(8, y, p, GLASS)
            t.set(22, y, p, GLASS)
            t.set(p, y, 8, GLASS)
    # tru trong dai sanh
    for (x, z) in ((12, 12), (18, 12), (12, 18), (18, 18)):
        t.fill(x, FL + 1, z, x, FL + 12, z, BRICK)
        t.set(x, FL + 4, z - 1, LANT)
        t.set(x, FL + 4, z + 1, LANT)
    # ban dieu va ngai (phia z=10)
    t.fill(11, FL + 1, 10, 19, FL + 1, 13, STONE)
    t.fill(12, FL + 2, 10, 18, FL + 2, 12, BRICK)
    t.fill(14, FL + 3, 10, 16, FL + 3, 10, STEEL)
    t.set(15, FL + 4, 10, LANT)
    chest(t, 13, FL + 3, 10, "south", "void_citadel")
    chest(t, 17, FL + 3, 10, "south", "void_citadel")
    # thap nhon tren mai
    t.fill(13, FL + 15, 13, 17, FL + 15, 17, STONE)
    t.fill(14, FL + 16, 14, 16, FL + 16, 16, BRICK)
    t.fill(15, FL + 17, 15, 15, FL + 20, 15, STEEL)
    t.set(15, FL + 21, 15, LANT)
    # den duong trong san
    for (x, z) in ((13, 25), (17, 25), (13, 28), (17, 28)):
        t.fill(x, FL + 1, z, x, FL + 3, z, BRICK)
        t.set(x, FL + 4, z, LANT)
    # sinh vat: chua te + ho phap + ke lang thang
    t.entity("voidrealm:void_sovereign", 15.5, FL + 3.0, 11.5)
    t.entity("voidrealm:rift_brute", 12.5, FL + 1.0, 16.5)
    t.entity("voidrealm:rift_brute", 18.5, FL + 1.0, 16.5)
    t.entity("voidrealm:void_walker", 15.5, FL + 1.0, 18.5)
    t.save("void_citadel")


if __name__ == "__main__":
    obelisk()
    ruins()
    citadel()
