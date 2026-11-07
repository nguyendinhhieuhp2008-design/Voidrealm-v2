#!/usr/bin/env python3
"""Du lieu cho Void Realm: model/blockstate/lang/loot/recipe/tag cho khoi moi + chieu + worldgen + hang so Java."""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RES = os.path.join(ROOT, "src", "main", "resources")
JAVA = os.path.join(ROOT, "src", "main", "java", "com", "voidrealm", "mod", "world", "RealmConstants.java")
NS = "voidrealm"


def V(n):
    return NS + ":" + n


def jw(path, obj):
    full = os.path.join(RES, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
        fp.write("\n")


def merge(path, update, tag=False):
    full = os.path.join(RES, path)
    data = {}
    if os.path.exists(full):
        with open(full, encoding="utf-8") as fp:
            data = json.load(fp)
    if tag:
        vals = data.setdefault("values", [])
        for v in update:
            if v not in vals:
                vals.append(v)
        data.setdefault("replace", False)
    else:
        data.update(update)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
        fp.write("\n")


def write_constants(c):
    src = """package com.voidrealm.mod.world;

import net.minecraft.core.BlockPos;

/** Tu dong sinh boi tools/gen_realm.py - KHONG sua tay. */
public final class RealmConstants {
    public static final int GATE_FWD = %d;
    public static final int PILLAR_R = %d;
    public static final int PILLAR_TOP_DY = %d;
    public static final BlockPos NEXUS_ORIGIN = new BlockPos(%d, %d, %d);
    public static final int ARRIVE_X = %d;
    public static final int ARRIVE_Y = %d;
    public static final int ARRIVE_Z = %d;
    public static final int MARK_X = %d;
    public static final int MARK_Y = %d;
    public static final int MARK_Z = %d;

    private RealmConstants() {
    }
}
""" % (c["GATE_FWD"], c["PIL_R"], c["PILLAR_TOP_DY"], *c["ORIGIN"], *c["ARRIVE"], *c["MARK"])
    with open(JAVA, "w", encoding="utf-8") as fp:
        fp.write(src)


# ------------------------------------------------------------------ khoi: model + blockstate
def stairs_state(name):
    base = {"east": 0, "south": 90, "west": 180, "north": 270}
    var = {}
    for f, y in base.items():
        for half in ("bottom", "top"):
            for shape in ("straight", "inner_left", "inner_right", "outer_left", "outer_right"):
                model = {"straight": "", "inner_left": "_inner", "inner_right": "_inner",
                         "outer_left": "_outer", "outer_right": "_outer"}[shape]
                left = shape.endswith("left")
                if half == "bottom":
                    rot = (y - 90) % 360 if left else y
                    d = {"model": V("block/%s%s" % (name, model)), "y": rot, "uvlock": True}
                else:
                    rot = y if left else (y + 90) % 360
                    if shape == "straight":
                        rot = y
                    d = {"model": V("block/%s%s" % (name, model)), "x": 180, "y": rot, "uvlock": True}
                if d["y"] == 0:
                    d.pop("y")
                var["facing=%s,half=%s,shape=%s" % (f, half, shape)] = d
    return {"variants": var}


def blocks():
    tex = lambda n: V("block/" + n)
    # khoi tu nhien: xoay ngau nhien 4 huong de cac khoi canh nhau lien mach, khong lap hoa van
    for n in ("void_stone", "void_crystal_block"):
        jw("assets/voidrealm/blockstates/%s.json" % n, {"variants": {"": [
            {"model": V("block/" + n), "y": r} if r else {"model": V("block/" + n)} for r in (0, 90, 180, 270)]}})
    for n in ("void_tile", "void_chiseled", "void_crystal_block"):
        jw("assets/voidrealm/models/block/%s.json" % n, {"parent": "minecraft:block/cube_all", "textures": {"all": tex(n)}})
        jw("assets/voidrealm/models/item/%s.json" % n, {"parent": V("block/" + n)})
    for n in ("void_tile", "void_chiseled"):
        jw("assets/voidrealm/blockstates/%s.json" % n, {"variants": {"": {"model": V("block/" + n)}}})
    # tru
    jw("assets/voidrealm/models/block/void_pillar.json", {
        "parent": "minecraft:block/cube_column", "textures": {"end": tex("void_pillar_top"), "side": tex("void_pillar")}})
    jw("assets/voidrealm/models/block/void_pillar_horizontal.json", {
        "parent": "minecraft:block/cube_column_horizontal", "textures": {"end": tex("void_pillar_top"), "side": tex("void_pillar")}})
    jw("assets/voidrealm/blockstates/void_pillar.json", {"variants": {
        "axis=y": {"model": V("block/void_pillar")},
        "axis=z": {"model": V("block/void_pillar_horizontal"), "x": 90},
        "axis=x": {"model": V("block/void_pillar_horizontal"), "x": 90, "y": 90}}})
    jw("assets/voidrealm/models/item/void_pillar.json", {"parent": V("block/void_pillar")})
    # dat
    jw("assets/voidrealm/models/block/void_soil.json", {
        "parent": "minecraft:block/cube_bottom_top",
        "textures": {"top": tex("void_soil_top"), "side": tex("void_soil_side"), "bottom": tex("void_stone"),
                     "particle": tex("void_soil_side")}})
    jw("assets/voidrealm/blockstates/void_soil.json", {"variants": {"": {"model": V("block/void_soil")}}})
    jw("assets/voidrealm/models/item/void_soil.json", {"parent": V("block/void_soil")})
    # bac thang + phien
    t = {"bottom": tex("void_bricks"), "top": tex("void_bricks"), "side": tex("void_bricks")}
    for suffix, parent in (("", "stairs"), ("_inner", "inner_stairs"), ("_outer", "outer_stairs")):
        jw("assets/voidrealm/models/block/void_bricks_stairs%s.json" % suffix,
           {"parent": "minecraft:block/" + parent, "textures": t})
    jw("assets/voidrealm/blockstates/void_bricks_stairs.json", stairs_state("void_bricks_stairs"))
    jw("assets/voidrealm/models/item/void_bricks_stairs.json", {"parent": V("block/void_bricks_stairs")})
    jw("assets/voidrealm/models/block/void_bricks_slab.json", {"parent": "minecraft:block/slab", "textures": t})
    jw("assets/voidrealm/models/block/void_bricks_slab_top.json", {"parent": "minecraft:block/slab_top", "textures": t})
    jw("assets/voidrealm/blockstates/void_bricks_slab.json", {"variants": {
        "type=bottom": {"model": V("block/void_bricks_slab")},
        "type=top": {"model": V("block/void_bricks_slab_top")},
        "type=double": {"model": V("block/void_bricks")}}})
    jw("assets/voidrealm/models/item/void_bricks_slab.json", {"parent": V("block/void_bricks_slab")})
    # khung cong
    jw("assets/voidrealm/models/block/void_portal_frame.json", {"parent": "minecraft:block/cube_all", "textures": {"all": tex("void_portal_frame")}})
    jw("assets/voidrealm/models/block/void_portal_frame_lit.json", {"parent": "minecraft:block/cube_all", "textures": {"all": tex("void_portal_frame_lit")}})
    jw("assets/voidrealm/blockstates/void_portal_frame.json", {"variants": {
        "lit=false": {"model": V("block/void_portal_frame")}, "lit=true": {"model": V("block/void_portal_frame_lit")}}})
    jw("assets/voidrealm/models/item/void_portal_frame.json", {"parent": V("block/void_portal_frame")})
    # mat cong (tam mong)
    def plane(box, faces):
        el = {"from": box[0], "to": box[1], "shade": False, "faces": {}}
        for f in faces:
            el["faces"][f] = {"uv": [0, 0, 16, 16], "texture": "#t"}
        return el
    jw("assets/voidrealm/models/block/void_portal_x.json", {
        "render_type": "minecraft:translucent", "textures": {"t": tex("void_portal"), "particle": tex("void_portal")},
        "elements": [plane([[0, 0, 7], [16, 16, 9]], ["north", "south"])]})
    jw("assets/voidrealm/models/block/void_portal_z.json", {
        "render_type": "minecraft:translucent", "textures": {"t": tex("void_portal"), "particle": tex("void_portal")},
        "elements": [plane([[7, 0, 0], [9, 16, 16]], ["east", "west"])]})
    jw("assets/voidrealm/blockstates/void_portal.json", {"variants": {
        "axis=x": {"model": V("block/void_portal_x")}, "axis=z": {"model": V("block/void_portal_z")}}})
    # ban te
    def altar(inner):
        f = lambda t, rot=0: {"uv": [0, 0, 16, 16], "texture": t}
        S, T = "#side", "#top"
        els = [
            {"from": [0, 0, 0], "to": [16, 4, 16], "faces": {d: {"uv": [0, 0, 16, 4] if d not in ("up", "down") else [0, 0, 16, 16], "texture": S if d != "up" else T}
                                                            for d in ("north", "south", "east", "west", "up", "down")}},
            {"from": [0, 4, 0], "to": [16, 12, 2], "faces": {d: {"texture": S if d != "up" else T} for d in ("north", "south", "east", "west", "up")}},
            {"from": [0, 4, 14], "to": [16, 12, 16], "faces": {d: {"texture": S if d != "up" else T} for d in ("north", "south", "east", "west", "up")}},
            {"from": [0, 4, 2], "to": [2, 12, 14], "faces": {d: {"texture": S if d != "up" else T} for d in ("north", "south", "east", "west", "up")}},
            {"from": [14, 4, 2], "to": [16, 12, 14], "faces": {d: {"texture": S if d != "up" else T} for d in ("north", "south", "east", "west", "up")}},
            {"from": [2, 4, 2], "to": [14, 5, 14], "faces": {"up": {"uv": [2, 2, 14, 14], "texture": "#inner"}}},
        ]
        return {"textures": {"side": tex("void_altar_side"), "top": tex("void_altar_top"),
                             "inner": tex("void_altar_inner_on" if inner else "void_altar_inner"),
                             "particle": tex("void_altar_side")}, "elements": els}
    jw("assets/voidrealm/models/block/void_altar.json", altar(False))
    jw("assets/voidrealm/models/block/void_altar_on.json", altar(True))
    var = {}
    for f in ("north", "south", "east", "west"):
        for s in range(8):
            var["facing=%s,stage=%d" % (f, s)] = {"model": V("block/void_altar_on" if s else "block/void_altar")}
    jw("assets/voidrealm/blockstates/void_altar.json", {"variants": var})
    jw("assets/voidrealm/models/item/void_altar.json", {"parent": V("block/void_altar")})


NAMES = {
    "void_tile": ("Gạch Lát Hư Không", "Void Tile"),
    "void_pillar": ("Cột Hư Không", "Void Pillar"),
    "void_chiseled": ("Đá Khắc Hư Không", "Chiseled Void Stone"),
    "void_soil": ("Đất Hư Không", "Void Soil"),
    "void_crystal_block": ("Khối Tinh Thể Hư Không", "Void Crystal Block"),
    "void_bricks_stairs": ("Bậc Gạch Hư Không", "Void Brick Stairs"),
    "void_bricks_slab": ("Phiến Gạch Hư Không", "Void Brick Slab"),
    "void_portal_frame": ("Khung Cổng Hư Không", "Void Portal Frame"),
    "void_portal": ("Cổng Hư Không", "Void Portal"),
    "void_altar": ("Bàn Tế Hư Không", "Void Altar"),
}


def lang():
    vi = {"block.voidrealm." + k: v[0] for k, v in NAMES.items()}
    en = {"block.voidrealm." + k: v[1] for k, v in NAMES.items()}
    vi.update({
        "message.voidrealm.altar_hint": "Bàn tế đang chờ một vật phẩm vô giá... Hãy ném Trứng Rồng Ender vào đây.",
        "message.voidrealm.altar_busy": "Nghi lễ đang diễn ra. Hãy lùi lại và chứng kiến.",
        "biome.voidrealm.void_expanse": "Hư Không Mênh Mông",
        "biome.voidrealm.crystal_gardens": "Vườn Tinh Thể",
        "biome.voidrealm.starlit_abyss": "Vực Sao",
        "advancements.voidrealm.dummy": "",
    })
    en.update({
        "message.voidrealm.altar_hint": "The altar awaits a priceless offering... Throw a Dragon Egg onto it.",
        "message.voidrealm.altar_busy": "The ritual is underway. Step back and watch.",
        "biome.voidrealm.void_expanse": "Void Expanse",
        "biome.voidrealm.crystal_gardens": "Crystal Gardens",
        "biome.voidrealm.starlit_abyss": "Starlit Abyss",
        "advancements.voidrealm.dummy": "",
    })
    for d in (vi, en):
        d.pop("advancements.voidrealm.dummy")
    merge("assets/voidrealm/lang/vi_vn.json", vi)
    merge("assets/voidrealm/lang/en_us.json", en)


def loot_and_recipes():
    def drop(name, extra=None):
        pool = {"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                "entries": [{"type": "minecraft:item", "name": V(name)}]}
        if extra:
            pool["entries"][0]["functions"] = extra
        jw("data/voidrealm/loot_table/blocks/%s.json" % name, {
            "type": "minecraft:block", "random_sequence": "voidrealm:blocks/" + name, "pools": [pool]})
    for n in ("void_tile", "void_pillar", "void_chiseled", "void_soil", "void_crystal_block", "void_bricks_stairs",
              "void_portal_frame", "void_altar"):
        drop(n)
    drop("void_bricks_slab", [{"function": "minecraft:set_count", "count": 2.0, "add": False, "conditions": [
        {"condition": "minecraft:block_state_property", "block": V("void_bricks_slab"), "properties": {"type": "double"}}]},
        {"function": "minecraft:explosion_decay"}])

    def shaped(name, pattern, key, result, count=1):
        jw("data/voidrealm/recipe/%s.json" % name, {
            "type": "minecraft:crafting_shaped", "category": "building", "pattern": pattern,
            "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": result, "count": count}})
    B, SL, SH, ING = V("void_bricks"), V("void_bricks_slab"), V("void_shard"), V("void_steel_ingot")
    shaped("void_tile", ["BB", "BB"], {"B": B}, V("void_tile"), 4)
    shaped("void_bricks_stairs", ["B  ", "BB ", "BBB"], {"B": B}, V("void_bricks_stairs"), 4)
    shaped("void_bricks_slab", ["BBB"], {"B": B}, V("void_bricks_slab"), 6)
    shaped("void_pillar", ["B", "B"], {"B": B}, V("void_pillar"), 2)
    shaped("void_chiseled", ["S", "S"], {"S": SL}, V("void_chiseled"), 1)
    shaped("void_crystal_block", ["SS", "SS"], {"S": SH}, V("void_crystal_block"), 1)
    shaped("void_portal_frame", ["ICI", "C C", "ICI"], {"I": ING, "C": V("void_chiseled")}, V("void_portal_frame"), 4)
    jw("data/voidrealm/recipe/void_soil.json", {
        "type": "minecraft:crafting_shapeless", "category": "building",
        "ingredients": [{"item": V("void_stone")}, {"item": "minecraft:dirt"}], "result": {"id": V("void_soil"), "count": 2}})


def tags():
    pick = ["void_tile", "void_pillar", "void_chiseled", "void_crystal_block", "void_bricks_stairs", "void_bricks_slab",
            "void_portal_frame", "void_altar"]
    merge("data/minecraft/tags/block/mineable/pickaxe.json", [V(n) for n in pick], True)
    merge("data/minecraft/tags/block/mineable/shovel.json", [V("void_soil")], True)
    merge("data/minecraft/tags/block/stairs.json", [V("void_bricks_stairs")], True)
    merge("data/minecraft/tags/block/slabs.json", [V("void_bricks_slab")], True)
    merge("data/minecraft/tags/item/stairs.json", [V("void_bricks_stairs")], True)
    merge("data/minecraft/tags/item/slabs.json", [V("void_bricks_slab")], True)
    merge("data/minecraft/tags/block/needs_iron_tool.json", [V("void_portal_frame"), V("void_altar")], True)


def chests():
    def item(name, w, lo, hi):
        e = {"type": "minecraft:item", "name": name, "weight": w}
        if hi > 1:
            e["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": float(lo), "max": float(hi)}}]
        return e
    for name, rolls, ents in (
        ("void_sanctum", (4, 7), [item(V("void_shard"), 22, 4, 9), item(V("void_steel_ingot"), 14, 2, 5), item(V("rift_core"), 8, 1, 2),
                                  item("minecraft:ender_pearl", 14, 2, 5), item("minecraft:diamond", 8, 1, 3),
                                  item(V("void_fruit"), 10, 2, 4), item(V("wisp_core"), 5, 1, 1), item("minecraft:golden_apple", 4, 1, 1),
                                  item("minecraft:amethyst_shard", 14, 6, 14)]),
        ("void_island", (3, 5), [item(V("void_shard"), 24, 3, 8), item(V("void_fruit"), 12, 1, 3), item("minecraft:amethyst_shard", 16, 4, 12),
                                 item("minecraft:ender_pearl", 10, 1, 3), item(V("rift_core"), 5, 1, 1), item(V("void_steel_ingot"), 10, 1, 3),
                                 item("minecraft:chorus_fruit", 10, 2, 5), item(V("phase_silk"), 8, 1, 3)])):
        jw("data/voidrealm/loot_table/chests/%s.json" % name, {
            "type": "minecraft:chest", "pools": [{"rolls": {"type": "minecraft:uniform", "min": float(rolls[0]), "max": float(rolls[1])},
                                                  "bonus_rolls": 0.0, "entries": ents}]})


# ------------------------------------------------------------------ chieu + worldgen
def biome(name, sky, fog, water, particle, ambient, spawners_monster, spawners_creature, grass):
    eff = {"sky_color": sky, "fog_color": fog, "water_color": water, "water_fog_color": water,
           "grass_color": grass, "foliage_color": grass,
           "particle": {"probability": 0.02, "options": {"type": particle}},
           "ambient_sound": ambient,
           "mood_sound": {"sound": "minecraft:ambient.crimson_forest.mood", "tick_delay": 6000, "block_search_extent": 8, "offset": 2.0},
           "music": {"sound": "minecraft:music.end", "min_delay": 6000, "max_delay": 24000, "replace_current_music": False}}
    sp = {k: [] for k in ("monster", "creature", "ambient", "axolotls", "underground_water_creature",
                          "water_creature", "water_ambient", "misc")}
    sp["monster"] = [{"type": V(e), "weight": w, "minCount": lo, "maxCount": hi} for (e, w, lo, hi) in spawners_monster]
    sp["creature"] = [{"type": V(e), "weight": w, "minCount": lo, "maxCount": hi} for (e, w, lo, hi) in spawners_creature]
    jw("data/voidrealm/worldgen/biome/%s.json" % name, {
        "temperature": 0.5, "downfall": 0.5, "has_precipitation": False, "effects": eff,
        "carvers": {}, "features": [[] for _ in range(11)], "spawners": sp, "spawn_costs": {}})


def worldgen():
    jw("data/voidrealm/dimension_type/void_realm.json", {
        "ultrawarm": False, "natural": False, "coordinate_scale": 1.0, "has_skylight": False, "has_ceiling": False,
        "ambient_light": 0.12, "fixed_time": 6000, "piglin_safe": False, "bed_works": False, "respawn_anchor_works": False,
        "has_raids": False, "logical_height": 256, "min_y": 0, "height": 256, "infiniburn": "#minecraft:infiniburn_end",
        "effects": "minecraft:the_end", "monster_spawn_light_level": 15, "monster_spawn_block_light_limit": 0})
    jw("data/voidrealm/dimension/void_realm.json", {
        "type": V("void_realm"),
        "generator": {"type": "minecraft:noise", "settings": V("void_realm"),
                      "biome_source": {"type": "minecraft:checkerboard", "scale": 5,
                                       "biomes": [V("void_expanse"), V("crystal_gardens"), V("starlit_abyss")]}}})
    zero = {"type": "minecraft:constant", "argument": 0.0}
    router = {k: zero for k in ("barrier", "fluid_level_floodedness", "fluid_level_spread", "lava", "temperature", "vegetation",
                                "continents", "erosion", "depth", "ridges", "initial_density_without_jaggedness", "final_density",
                                "vein_toggle", "vein_ridged", "vein_gap")}
    jw("data/voidrealm/worldgen/noise_settings/void_realm.json", {
        "sea_level": -64, "disable_mob_generation": False, "aquifers_enabled": False, "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": {"Name": "minecraft:air"}, "default_fluid": {"Name": "minecraft:air"},
        "noise": {"min_y": 0, "height": 256, "size_horizontal": 2, "size_vertical": 1},
        "noise_router": router, "spawn_target": [],
        "surface_rule": {"type": "minecraft:block", "result_state": {"Name": "minecraft:air"}}})
    biome("void_expanse", 0x1a0a33, 0x2a1250, 0x6a3fd0, "minecraft:reverse_portal", "minecraft:ambient.basalt_deltas.loop",
          [("void_walker", 10, 1, 2), ("rift_archer", 6, 1, 2), ("phase_stalker", 5, 1, 1)], [("void_stalker_bird", 8, 1, 2)], 0x9a7bff)
    biome("crystal_gardens", 0x0b2a3a, 0x113d52, 0x2fbfd0, "minecraft:end_rod", "minecraft:ambient.warped_forest.loop",
          [("phase_stalker", 8, 1, 2), ("rift_archer", 5, 1, 1)], [("void_boar", 6, 2, 3), ("void_stalker_bird", 6, 1, 2)], 0x3fe0d0)
    biome("starlit_abyss", 0x05061c, 0x0a0f33, 0x3050c0, "minecraft:portal", "minecraft:ambient.soul_sand_valley.loop",
          [("void_walker", 8, 1, 2), ("rift_brute", 2, 1, 1)], [("void_stalker_bird", 8, 1, 3)], 0x7aa0ff)
    jw("data/voidrealm/tags/worldgen/biome/has_structure/void_islands.json", {
        "replace": False, "values": [V("void_expanse"), V("crystal_gardens"), V("starlit_abyss")]})
    isl = [("void_island_a", 3), ("void_island_b", 2), ("void_island_c", 3), ("void_island_d", 2)]
    jw("data/voidrealm/worldgen/template_pool/void_islands.json", {"fallback": "minecraft:empty", "elements": [
        {"weight": w, "element": {"element_type": "minecraft:single_pool_element", "location": V(n),
                                  "processors": "minecraft:empty", "projection": "rigid"}} for n, w in isl]})
    jw("data/voidrealm/worldgen/structure/void_islands.json", {
        "type": "minecraft:jigsaw", "biomes": "#voidrealm:has_structure/void_islands", "step": "surface_structures",
        "terrain_adaptation": "none", "spawn_overrides": {},
        "start_pool": V("void_islands"), "size": 1,
        "start_height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": 12}, "max_inclusive": {"absolute": 120}},
        "max_distance_from_center": 80, "use_expansion_hack": False})
    jw("data/voidrealm/worldgen/structure_set/void_islands.json", {
        "structures": [{"structure": V("void_islands"), "weight": 1}],
        "placement": {"type": "minecraft:random_spread", "spacing": 5, "separation": 2, "salt": 1840301}})
    # den te o Overworld
    jw("data/voidrealm/worldgen/template_pool/void_sanctum.json", {"fallback": "minecraft:empty", "elements": [{
        "weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": V("void_sanctum"),
                                 "processors": "minecraft:empty", "projection": "rigid"}}]})
    jw("data/voidrealm/worldgen/structure/void_sanctum.json", {
        "type": "minecraft:jigsaw", "biomes": "#voidrealm:has_structure/void_sanctum", "step": "surface_structures",
        "terrain_adaptation": "beard_thin", "spawn_overrides": {},
        "start_pool": V("void_sanctum"), "size": 1, "start_height": {"absolute": -5},
        "project_start_to_heightmap": "WORLD_SURFACE_WG", "max_distance_from_center": 80, "use_expansion_hack": False})
    jw("data/voidrealm/worldgen/structure_set/void_sanctum.json", {
        "structures": [{"structure": V("void_sanctum"), "weight": 1}],
        "placement": {"type": "minecraft:random_spread", "spacing": 40, "separation": 14, "salt": 1840309}})
    with open(os.path.join(RES, "data/voidrealm/tags/worldgen/biome/has_structure/void_obelisk.json"), encoding="utf-8") as fp:
        ob = json.load(fp)
    jw("data/voidrealm/tags/worldgen/biome/has_structure/void_sanctum.json", ob)


def write_all(consts):
    write_constants(consts)
    blocks()
    lang()
    loot_and_recipes()
    tags()
    chests()
    worldgen()
