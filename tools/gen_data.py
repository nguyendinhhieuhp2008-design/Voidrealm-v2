#!/usr/bin/env python3
"""Sinh assets (model, blockstate, lang) va data (recipe, loot, tag, worldgen) cho Void Realm.
Chay: python3 tools/gen_data.py   (dinh dang cho Minecraft 1.21.1: thu muc so it)
"""
import json
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources")
NS = "voidrealm"


def w(path, obj):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def it(n):
    return {"item": n}


V = lambda n: NS + ":" + n

# ---------------------------------------------------------------- danh sach
BLOCKS = ["void_crystal_ore", "deepslate_void_crystal_ore", "void_steel_block", "void_stone", "void_bricks", "rift_lantern"]
GENERATED = ["void_shard", "void_steel_ingot", "phase_silk", "rift_core", "void_apple",
             "void_steel_helmet", "void_steel_chestplate", "void_steel_leggings", "void_steel_boots",
             "phase_cloth_hood", "phase_cloth_tunic", "phase_cloth_leggings", "phase_cloth_boots"]
HANDHELD = ["void_steel_sword", "void_steel_pickaxe", "void_steel_axe", "void_steel_shovel", "void_steel_hoe",
            "rift_blade", "void_reaper", "voidpiercer", "gravity_staff"]
MOBS = ["void_walker", "rift_archer", "phase_stalker", "void_boar", "rift_brute", "void_sovereign"]

# ---------------------------------------------------------------- models
MODELED = {"void_shard", "void_steel_ingot", "phase_silk", "rift_core", "void_apple", "void_steel_sword", "void_steel_pickaxe",
           "void_steel_axe", "void_steel_shovel", "void_steel_hoe", "rift_blade", "void_reaper", "voidpiercer", "gravity_staff"}
BLOCK_MODELED = {"void_crystal_ore", "deepslate_void_crystal_ore", "rift_lantern"}
GENERATED = [n for n in GENERATED if n not in MODELED]
HANDHELD = [n for n in HANDHELD if n not in MODELED]
for n in GENERATED:
    w(f"assets/{NS}/models/item/{n}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": V("item/" + n)}})
for n in HANDHELD:
    w(f"assets/{NS}/models/item/{n}.json", {"parent": "minecraft:item/handheld", "textures": {"layer0": V("item/" + n)}})
for n in MOBS:
    w(f"assets/{NS}/models/item/{n}_spawn_egg.json", {"parent": "minecraft:item/template_spawn_egg"})
for n in BLOCKS:
    if n in BLOCK_MODELED:
        w(f"assets/{NS}/models/item/{n}.json", {"parent": V("block/" + n)})
        w(f"assets/{NS}/blockstates/{n}.json", {"variants": {"": {"model": V("block/" + n)}}})
        continue
    w(f"assets/{NS}/models/block/{n}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": V("block/" + n)}})
    w(f"assets/{NS}/models/item/{n}.json", {"parent": V("block/" + n)})
    w(f"assets/{NS}/blockstates/{n}.json", {"variants": {"": {"model": V("block/" + n)}}})

# ---------------------------------------------------------------- lang
VI = {
    "itemGroup.voidrealm": "Void Realm - Cõi Hư Không",
    "item.voidrealm.void_shard": "Mảnh Hư Không",
    "item.voidrealm.void_steel_ingot": "Thỏi Thép Hư Không",
    "item.voidrealm.phase_silk": "Tơ Hư Ảnh",
    "item.voidrealm.rift_core": "Lõi Khe Nứt",
    "item.voidrealm.void_apple": "Táo Hư Không",
    "item.voidrealm.void_steel_sword": "Kiếm Thép Hư Không",
    "item.voidrealm.void_steel_pickaxe": "Cuốc Chim Thép Hư Không",
    "item.voidrealm.void_steel_axe": "Rìu Thép Hư Không",
    "item.voidrealm.void_steel_shovel": "Xẻng Thép Hư Không",
    "item.voidrealm.void_steel_hoe": "Cuốc Thép Hư Không",
    "item.voidrealm.rift_blade": "Kiếm Xé Không Gian",
    "item.voidrealm.void_reaper": "Lưỡi Hái Hư Vô",
    "item.voidrealm.voidpiercer": "Giáo Xuyên Hư Không",
    "item.voidrealm.gravity_staff": "Trượng Trọng Lực",
    "item.voidrealm.void_steel_helmet": "Mũ Thép Hư Không",
    "item.voidrealm.void_steel_chestplate": "Áo Giáp Thép Hư Không",
    "item.voidrealm.void_steel_leggings": "Quần Thép Hư Không",
    "item.voidrealm.void_steel_boots": "Giày Thép Hư Không",
    "item.voidrealm.phase_cloth_hood": "Mũ Trùm Hư Ảnh",
    "item.voidrealm.phase_cloth_tunic": "Áo Choàng Hư Ảnh",
    "item.voidrealm.phase_cloth_leggings": "Quần Hư Ảnh",
    "item.voidrealm.phase_cloth_boots": "Giày Hư Ảnh",
    "block.voidrealm.void_crystal_ore": "Quặng Tinh Thể Hư Không",
    "block.voidrealm.deepslate_void_crystal_ore": "Quặng Tinh Thể Hư Không Phiến Thạch",
    "block.voidrealm.void_steel_block": "Khối Thép Hư Không",
    "block.voidrealm.void_stone": "Đá Hư Không",
    "block.voidrealm.void_bricks": "Gạch Hư Không",
    "block.voidrealm.rift_lantern": "Đèn Khe Nứt",
    "entity.voidrealm.void_walker": "Kẻ Lang Thang Hư Không",
    "entity.voidrealm.rift_archer": "Cung Thủ Dị Giới",
    "entity.voidrealm.phase_stalker": "Kẻ Rình Rập Hư Ảnh",
    "entity.voidrealm.void_boar": "Lợn Rừng Hư Không",
    "entity.voidrealm.rift_brute": "Hộ Pháp Dị Giới",
    "entity.voidrealm.void_sovereign": "Chúa Tể Hư Không",
    "item.voidrealm.void_walker_spawn_egg": "Trứng Kẻ Lang Thang Hư Không",
    "item.voidrealm.rift_archer_spawn_egg": "Trứng Cung Thủ Dị Giới",
    "item.voidrealm.phase_stalker_spawn_egg": "Trứng Kẻ Rình Rập Hư Ảnh",
    "item.voidrealm.void_boar_spawn_egg": "Trứng Lợn Rừng Hư Không",
    "item.voidrealm.rift_brute_spawn_egg": "Trứng Hộ Pháp Dị Giới",
    "item.voidrealm.void_sovereign_spawn_egg": "Trứng Chúa Tể Hư Không",
    "tooltip.voidrealm.rift_blade": "Chuột phải: lao nhanh về phía trước (dịch chuyển ngắn).",
    "tooltip.voidrealm.void_reaper": "Đánh trúng gây Héo Mòn và hút một ít máu.",
    "tooltip.voidrealm.gravity_staff": "Chuột phải: kéo mọi sinh vật xung quanh về phía bạn và làm chậm chúng.",
}
EN = {
    "itemGroup.voidrealm": "Void Realm",
    "item.voidrealm.void_shard": "Void Shard",
    "item.voidrealm.void_steel_ingot": "Void Steel Ingot",
    "item.voidrealm.phase_silk": "Phase Silk",
    "item.voidrealm.rift_core": "Rift Core",
    "item.voidrealm.void_apple": "Void Apple",
    "item.voidrealm.void_steel_sword": "Void Steel Sword",
    "item.voidrealm.void_steel_pickaxe": "Void Steel Pickaxe",
    "item.voidrealm.void_steel_axe": "Void Steel Axe",
    "item.voidrealm.void_steel_shovel": "Void Steel Shovel",
    "item.voidrealm.void_steel_hoe": "Void Steel Hoe",
    "item.voidrealm.rift_blade": "Rift Blade",
    "item.voidrealm.void_reaper": "Void Reaper",
    "item.voidrealm.voidpiercer": "Voidpiercer",
    "item.voidrealm.gravity_staff": "Gravity Staff",
    "item.voidrealm.void_steel_helmet": "Void Steel Helmet",
    "item.voidrealm.void_steel_chestplate": "Void Steel Chestplate",
    "item.voidrealm.void_steel_leggings": "Void Steel Leggings",
    "item.voidrealm.void_steel_boots": "Void Steel Boots",
    "item.voidrealm.phase_cloth_hood": "Phase Cloth Hood",
    "item.voidrealm.phase_cloth_tunic": "Phase Cloth Tunic",
    "item.voidrealm.phase_cloth_leggings": "Phase Cloth Leggings",
    "item.voidrealm.phase_cloth_boots": "Phase Cloth Boots",
    "block.voidrealm.void_crystal_ore": "Void Crystal Ore",
    "block.voidrealm.deepslate_void_crystal_ore": "Deepslate Void Crystal Ore",
    "block.voidrealm.void_steel_block": "Block of Void Steel",
    "block.voidrealm.void_stone": "Void Stone",
    "block.voidrealm.void_bricks": "Void Bricks",
    "block.voidrealm.rift_lantern": "Rift Lantern",
    "entity.voidrealm.void_walker": "Void Walker",
    "entity.voidrealm.rift_archer": "Rift Archer",
    "entity.voidrealm.phase_stalker": "Phase Stalker",
    "entity.voidrealm.void_boar": "Void Boar",
    "entity.voidrealm.rift_brute": "Rift Brute",
    "entity.voidrealm.void_sovereign": "Void Sovereign",
    "item.voidrealm.void_walker_spawn_egg": "Void Walker Spawn Egg",
    "item.voidrealm.rift_archer_spawn_egg": "Rift Archer Spawn Egg",
    "item.voidrealm.phase_stalker_spawn_egg": "Phase Stalker Spawn Egg",
    "item.voidrealm.void_boar_spawn_egg": "Void Boar Spawn Egg",
    "item.voidrealm.rift_brute_spawn_egg": "Rift Brute Spawn Egg",
    "item.voidrealm.void_sovereign_spawn_egg": "Void Sovereign Spawn Egg",
    "tooltip.voidrealm.rift_blade": "Right click: dash a short distance forward.",
    "tooltip.voidrealm.void_reaper": "Hits inflict Wither and heal the wielder a little.",
    "tooltip.voidrealm.gravity_staff": "Right click: pull every creature nearby toward you and slow them.",
}
w(f"assets/{NS}/lang/vi_vn.json", VI)
w(f"assets/{NS}/lang/en_us.json", EN)

# ---------------------------------------------------------------- recipes
def shaped(name, pattern, key, result, count=1, cat="equipment"):
    w(f"data/{NS}/recipe/{name}.json", {
        "type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
        "key": {k: it(v) for k, v in key.items()}, "result": {"id": result, "count": count}})


def shapeless(name, ings, result, count=1, cat="misc"):
    w(f"data/{NS}/recipe/{name}.json", {
        "type": "minecraft:crafting_shapeless", "category": cat,
        "ingredients": [it(i) for i in ings], "result": {"id": result, "count": count}})


ING, STK, SH, CORE, SILK = V("void_steel_ingot"), "minecraft:stick", V("void_shard"), V("rift_core"), V("phase_silk")
shapeless("void_steel_ingot", [SH, SH, "minecraft:iron_ingot"], ING)
shapeless("void_steel_ingot_from_block", [V("void_steel_block")], ING, 9)
shaped("void_steel_block", ["III", "III", "III"], {"I": ING}, V("void_steel_block"), cat="building")
shapeless("void_stone", [SH] + ["minecraft:stone"] * 4, V("void_stone"), 4, "building")
shaped("void_bricks", ["SS", "SS"], {"S": V("void_stone")}, V("void_bricks"), 4, "building")
w(f"data/{NS}/recipe/void_bricks_from_stonecutting.json", {
    "type": "minecraft:stonecutting", "ingredient": it(V("void_stone")), "result": {"id": V("void_bricks"), "count": 1}})
shaped("rift_lantern", [" S ", "SGS", " S "], {"S": SH, "G": "minecraft:glowstone"}, V("rift_lantern"), cat="building")
shaped("void_apple", [" S ", "SAS", " S "], {"S": SH, "A": "minecraft:apple"}, V("void_apple"), cat="misc")
shaped("void_steel_sword", ["I", "I", "S"], {"I": ING, "S": STK}, V("void_steel_sword"))
shaped("void_steel_pickaxe", ["III", " S ", " S "], {"I": ING, "S": STK}, V("void_steel_pickaxe"))
shaped("void_steel_axe", ["II", "IS", " S"], {"I": ING, "S": STK}, V("void_steel_axe"))
shaped("void_steel_shovel", ["I", "S", "S"], {"I": ING, "S": STK}, V("void_steel_shovel"))
shaped("void_steel_hoe", ["II", " S", " S"], {"I": ING, "S": STK}, V("void_steel_hoe"))
shaped("rift_blade", ["R", "I", "S"], {"R": CORE, "I": ING, "S": STK}, V("rift_blade"))
shaped("void_reaper", ["II ", " SR", " S "], {"I": ING, "S": STK, "R": CORE}, V("void_reaper"))
shaped("voidpiercer", ["  I", " S ", "R  "], {"I": ING, "S": STK, "R": CORE}, V("voidpiercer"))
shaped("gravity_staff", ["  R", " S ", "S  "], {"R": CORE, "S": STK}, V("gravity_staff"))
for prefix, mat, parts in (("void_steel", ING, ("helmet", "chestplate", "leggings", "boots")),
                           ("phase_cloth", SILK, ("hood", "tunic", "leggings", "boots"))):
    pats = [["MMM", "M M"], ["M M", "MMM", "MMM"], ["MMM", "M M", "M M"], ["M M", "M M"]]
    for part, pat in zip(parts, pats):
        shaped(f"{prefix}_{part}", pat, {"M": mat}, V(f"{prefix}_{part}"))

# ---------------------------------------------------------------- loot
def block_loot(name, entries):
    w(f"data/{NS}/loot_table/blocks/{name}.json", {
        "type": "minecraft:block", "random_sequence": f"{NS}:blocks/{name}",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "entries": entries}]})


silk = [{"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
    {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]
for ore in ("void_crystal_ore", "deepslate_void_crystal_ore"):
    block_loot(ore, [{"type": "minecraft:alternatives", "children": [
        {"type": "minecraft:item", "name": V(ore), "conditions": silk},
        {"type": "minecraft:item", "name": SH, "functions": [
            {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1.0, "max": 3.0}},
            {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
            {"function": "minecraft:explosion_decay"}]}]}])
for b in ("void_steel_block", "void_stone", "void_bricks", "rift_lantern"):
    w(f"data/{NS}/loot_table/blocks/{b}.json", {
        "type": "minecraft:block", "random_sequence": f"{NS}:blocks/{b}",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                   "entries": [{"type": "minecraft:item", "name": V(b)}]}]})


def drop(item, lo, hi, looting=0, chance=None):
    e = {"type": "minecraft:item", "name": item, "functions": [
        {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": float(lo), "max": float(hi)}}]}
    if looting:
        e["functions"].append({"function": "minecraft:looting_enchant", "count": {"type": "minecraft:uniform", "min": 0.0, "max": float(looting)}})
    pool = {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [e]}
    if chance is not None:
        pool["conditions"] = [{"condition": "minecraft:random_chance", "chance": chance}]
    return pool


def entity_loot(name, pools):
    w(f"data/{NS}/loot_table/entities/{name}.json", {"type": "minecraft:entity", "pools": pools})


entity_loot("void_walker", [drop(SH, 0, 2, 1), drop(V("void_apple"), 1, 1, 0, 0.03)])
entity_loot("rift_archer", [drop("minecraft:arrow", 0, 2, 1), drop("minecraft:bone", 0, 1, 1), drop(SH, 0, 1, 1, 0.5)])
entity_loot("phase_stalker", [drop(SILK, 1, 2, 1), drop("minecraft:ender_pearl", 0, 1, 1, 0.25)])
entity_loot("void_boar", [drop("minecraft:porkchop", 1, 3, 1), drop(SH, 0, 1, 1, 0.3)])
entity_loot("rift_brute", [drop(SH, 1, 3, 1), drop("minecraft:iron_ingot", 0, 2, 1), drop(ING, 0, 1, 1, 0.4), drop(CORE, 1, 1, 0, 0.08)])
entity_loot("void_sovereign", [drop(CORE, 2, 3), drop(ING, 4, 8), drop(V("void_apple"), 1, 2), drop(SH, 6, 12)])


def chest(name, rolls, entries, bonus=None):
    pools = [{"rolls": {"type": "minecraft:uniform", "min": float(rolls[0]), "max": float(rolls[1])}, "bonus_rolls": 0.0,
              "entries": [{"type": "minecraft:item", "name": n, "weight": wt,
                           "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": float(lo), "max": float(hi)}}]}
                          for (n, wt, lo, hi) in entries]}]
    if bonus:
        pools.append(bonus)
    w(f"data/{NS}/loot_table/chests/{name}.json", {"type": "minecraft:chest", "pools": pools})


chest("void_obelisk", (2, 4), [(SH, 20, 2, 5), ("minecraft:iron_ingot", 15, 1, 3), ("minecraft:arrow", 10, 4, 12),
      (SILK, 8, 1, 3), (V("void_apple"), 4, 1, 1), ("minecraft:ender_pearl", 5, 1, 2), ("minecraft:diamond", 3, 1, 1),
      (ING, 3, 1, 1), ("minecraft:golden_apple", 2, 1, 1)])
chest("rift_ruins", (3, 5), [(SH, 20, 3, 6), ("minecraft:iron_ingot", 12, 2, 4), (SILK, 10, 2, 4),
      (V("void_apple"), 6, 1, 2), ("minecraft:diamond", 5, 1, 2), (ING, 6, 1, 2), ("minecraft:ender_pearl", 6, 1, 3),
      ("minecraft:golden_apple", 3, 1, 1)],
      bonus={"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:random_chance", "chance": 0.35}],
             "entries": [{"type": "minecraft:item", "name": CORE}]})
chest("void_citadel", (4, 6), [(ING, 20, 2, 5), (SH, 20, 4, 8), (V("void_apple"), 10, 1, 3), ("minecraft:diamond", 10, 1, 3),
      (SILK, 10, 3, 6), ("minecraft:ender_pearl", 8, 2, 4), ("minecraft:enchanted_golden_apple", 2, 1, 1),
      ("minecraft:netherite_scrap", 4, 1, 2)],
      bonus={"rolls": 1.0, "bonus_rolls": 0.0, "entries": [{"type": "minecraft:item", "name": CORE}]})

# ---------------------------------------------------------------- tags
def tag(path, values):
    w(f"data/{path}.json", {"replace": False, "values": values})


tag("minecraft/tags/block/mineable/pickaxe", [V(b) for b in BLOCKS])
tag("minecraft/tags/block/needs_iron_tool", [V("void_crystal_ore"), V("deepslate_void_crystal_ore"), V("void_steel_block")])
tag("minecraft/tags/item/swords", [V("void_steel_sword"), V("rift_blade"), V("void_reaper"), V("voidpiercer")])
tag("minecraft/tags/item/pickaxes", [V("void_steel_pickaxe")])
tag("minecraft/tags/item/axes", [V("void_steel_axe")])
tag("minecraft/tags/item/shovels", [V("void_steel_shovel")])
tag("minecraft/tags/item/hoes", [V("void_steel_hoe")])
tag("minecraft/tags/item/head_armor", [V("void_steel_helmet"), V("phase_cloth_hood")])
tag("minecraft/tags/item/chest_armor", [V("void_steel_chestplate"), V("phase_cloth_tunic")])
tag("minecraft/tags/item/leg_armor", [V("void_steel_leggings"), V("phase_cloth_leggings")])
tag("minecraft/tags/item/foot_armor", [V("void_steel_boots"), V("phase_cloth_boots")])

# biome tags cho cong trinh va quai
tag(f"{NS}/tags/worldgen/biome/has_structure/void_obelisk",
    ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:savanna", "minecraft:desert",
     "minecraft:snowy_plains", "#minecraft:is_forest", "#minecraft:is_taiga"])
tag(f"{NS}/tags/worldgen/biome/has_structure/rift_ruins",
    ["#minecraft:is_forest", "#minecraft:is_taiga", "#minecraft:is_hill", "#minecraft:is_jungle", "minecraft:swamp", "minecraft:plains"])
tag(f"{NS}/tags/worldgen/biome/has_structure/void_citadel",
    ["minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:savanna", "minecraft:desert", "minecraft:snowy_plains"])
tag(f"{NS}/tags/worldgen/biome/boar_habitat", ["#minecraft:is_forest", "#minecraft:is_taiga", "minecraft:plains"])

# ---------------------------------------------------------------- worldgen: quang
w(f"data/{NS}/worldgen/configured_feature/void_crystal_ore.json", {
    "type": "minecraft:ore",
    "config": {"discard_chance_on_air_exposure": 0.0, "size": 6, "targets": [
        {"state": {"Name": V("void_crystal_ore")}, "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}},
        {"state": {"Name": V("deepslate_void_crystal_ore")}, "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"}}]}})
w(f"data/{NS}/worldgen/placed_feature/void_crystal_ore.json", {
    "feature": V("void_crystal_ore"),
    "placement": [{"type": "minecraft:count", "count": 3}, {"type": "minecraft:in_square"},
                  {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                   "min_inclusive": {"absolute": -64}, "max_inclusive": {"absolute": 32}}},
                  {"type": "minecraft:biome"}]})
w(f"data/{NS}/neoforge/biome_modifier/add_void_crystal_ore.json", {
    "type": "neoforge:add_features", "biomes": "#minecraft:is_overworld",
    "features": V("void_crystal_ore"), "step": "underground_ores"})


def spawns(name, biomes, entries):
    w(f"data/{NS}/neoforge/biome_modifier/{name}.json", {
        "type": "neoforge:add_spawns", "biomes": biomes,
        "spawners": [{"type": V(e), "weight": wt, "minCount": lo, "maxCount": hi} for (e, wt, lo, hi) in entries]})


spawns("spawn_overworld", "#minecraft:is_overworld",
       [("void_walker", 6, 1, 2), ("rift_archer", 4, 1, 2), ("phase_stalker", 2, 1, 1)])
spawns("spawn_boar", f"#{NS}:boar_habitat", [("void_boar", 8, 2, 3)])

# ---------------------------------------------------------------- worldgen: cong trinh
STRUCTS = {
    # ten: (spacing, separation, salt, floor_layers, spawns)
    "void_obelisk": (22, 8, 1840201, 2, [("rift_archer", 1, 1, 2), ("phase_stalker", 1, 1, 1)]),
    "rift_ruins": (18, 6, 1840202, 1, [("void_walker", 1, 1, 3), ("rift_archer", 1, 1, 2)]),
    "void_citadel": (48, 16, 1840203, 5, [("rift_brute", 2, 1, 2), ("void_walker", 1, 1, 3), ("phase_stalker", 1, 1, 2)]),
}
for name, (spacing, sep, salt, fl, sp) in STRUCTS.items():
    w(f"data/{NS}/worldgen/template_pool/{name}.json", {"fallback": "minecraft:empty", "elements": [{
        "weight": 1, "element": {"element_type": "minecraft:single_pool_element", "location": V(name),
                                 "processors": "minecraft:empty", "projection": "rigid"}}]})
    w(f"data/{NS}/worldgen/structure/{name}.json", {
        "type": "minecraft:jigsaw", "biomes": f"#{NS}:has_structure/{name}", "step": "surface_structures",
        "terrain_adaptation": "beard_thin",
        "spawn_overrides": {"monster": {"bounding_box": "full", "spawns": [
            {"type": V(e), "weight": wt, "minCount": lo, "maxCount": hi} for (e, wt, lo, hi) in sp]}},
        "start_pool": V(name), "size": 1, "start_height": {"absolute": -fl},
        "project_start_to_heightmap": "WORLD_SURFACE_WG", "max_distance_from_center": 80, "use_expansion_hack": False})
    w(f"data/{NS}/worldgen/structure_set/{name}.json", {
        "structures": [{"structure": V(name), "weight": 1}],
        "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": sep, "salt": salt}})

print("gen_data: xong")
