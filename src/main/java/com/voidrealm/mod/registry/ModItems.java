package com.voidrealm.mod.registry;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.item.EyeOfTheVoidItem;
import com.voidrealm.mod.item.GravityStaffItem;
import com.voidrealm.mod.item.RiftBladeItem;
import com.voidrealm.mod.item.VoidPiercerItem;
import com.voidrealm.mod.item.VoidReaperItem;
import com.voidrealm.mod.item.VoidTetherItem;
import com.voidrealm.mod.item.WarpRodItem;
import com.voidrealm.mod.item.WispCoreItem;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.level.block.Block;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(VoidRealm.MODID);

    private static final ResourceLocation BASE_ATTACK_DAMAGE_ID = ResourceLocation.withDefaultNamespace("base_attack_damage");
    private static final ResourceLocation BASE_ATTACK_SPEED_ID = ResourceLocation.withDefaultNamespace("base_attack_speed");
    private static final ResourceLocation PIERCER_REACH_ID = ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "voidpiercer_reach");

    // ---------------------------------------------------------------- Vat lieu
    public static final DeferredHolder<Item, Item> VOID_SHARD = ITEMS.register("void_shard",
            () -> new Item(new Item.Properties().fireResistant()));

    public static final DeferredHolder<Item, Item> VOID_STEEL_INGOT = ITEMS.register("void_steel_ingot",
            () -> new Item(new Item.Properties().fireResistant()));

    public static final DeferredHolder<Item, Item> PHASE_SILK = ITEMS.register("phase_silk",
            () -> new Item(new Item.Properties()));

    public static final DeferredHolder<Item, Item> RIFT_CORE = ITEMS.register("rift_core",
            () -> new Item(new Item.Properties().fireResistant().rarity(Rarity.EPIC)));

    public static final DeferredHolder<Item, Item> VOID_APPLE = ITEMS.register("void_apple",
            () -> new Item(new Item.Properties()
                    .rarity(Rarity.RARE)
                    .food(new FoodProperties.Builder()
                            .nutrition(8)
                            .saturationModifier(1.2F)
                            .alwaysEdible()
                            .effect(() -> new MobEffectInstance(MobEffects.REGENERATION, 160, 1), 1.0F)
                            .effect(() -> new MobEffectInstance(MobEffects.ABSORPTION, 1200, 1), 1.0F)
                            .build())));

    // ---------------------------------------------------------------- Cong cu Thep Hu Khong
    public static final DeferredHolder<Item, Item> VOID_STEEL_SWORD = ITEMS.register("void_steel_sword",
            () -> new SwordItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant()
                    .attributes(SwordItem.createAttributes(ModTiers.VOID_STEEL, 3, -2.4F))));

    public static final DeferredHolder<Item, Item> VOID_STEEL_PICKAXE = ITEMS.register("void_steel_pickaxe",
            () -> new PickaxeItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant()
                    .attributes(PickaxeItem.createAttributes(ModTiers.VOID_STEEL, 1.0F, -2.8F))));

    public static final DeferredHolder<Item, Item> VOID_STEEL_AXE = ITEMS.register("void_steel_axe",
            () -> new AxeItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant()
                    .attributes(AxeItem.createAttributes(ModTiers.VOID_STEEL, 5.0F, -3.0F))));

    public static final DeferredHolder<Item, Item> VOID_STEEL_SHOVEL = ITEMS.register("void_steel_shovel",
            () -> new ShovelItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant()
                    .attributes(ShovelItem.createAttributes(ModTiers.VOID_STEEL, 1.5F, -3.0F))));

    public static final DeferredHolder<Item, Item> VOID_STEEL_HOE = ITEMS.register("void_steel_hoe",
            () -> new HoeItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant()
                    .attributes(HoeItem.createAttributes(ModTiers.VOID_STEEL, -4.0F, 0.0F))));

    // ---------------------------------------------------------------- Vu khi dac biet
    public static final DeferredHolder<Item, Item> RIFT_BLADE = ITEMS.register("rift_blade",
            () -> new RiftBladeItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant().rarity(Rarity.EPIC)
                    .attributes(weaponAttributes(ModTiers.VOID_STEEL, 3.0F, -2.2F, 0.0D))));

    public static final DeferredHolder<Item, Item> VOID_REAPER = ITEMS.register("void_reaper",
            () -> new VoidReaperItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant().rarity(Rarity.EPIC)
                    .attributes(weaponAttributes(ModTiers.VOID_STEEL, 6.0F, -3.0F, 0.0D))));

    public static final DeferredHolder<Item, Item> VOIDPIERCER = ITEMS.register("voidpiercer",
            () -> new VoidPiercerItem(ModTiers.VOID_STEEL, new Item.Properties().fireResistant().rarity(Rarity.RARE)
                    .attributes(weaponAttributes(ModTiers.VOID_STEEL, 4.0F, -2.8F, 2.0D))));

    public static final DeferredHolder<Item, Item> GRAVITY_STAFF = ITEMS.register("gravity_staff",
            () -> new GravityStaffItem(new Item.Properties().stacksTo(1).durability(600).rarity(Rarity.RARE)));

    // ---------------------------------------------------------------- Phep thuat & Magitech
    public static final DeferredHolder<Item, Item> WARP_ROD = ITEMS.register("warp_rod",
            () -> new WarpRodItem(new Item.Properties().stacksTo(1).durability(300).rarity(Rarity.EPIC)));

    public static final DeferredHolder<Item, Item> EYE_OF_THE_VOID = ITEMS.register("eye_of_the_void",
            () -> new EyeOfTheVoidItem(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).fireResistant()));

    public static final DeferredHolder<Item, Item> VOID_TETHER = ITEMS.register("void_tether",
            () -> new VoidTetherItem(new Item.Properties().stacksTo(1).durability(250).rarity(Rarity.RARE)));

    public static final DeferredHolder<Item, Item> WISP_CORE = ITEMS.register("wisp_core",
            () -> new WispCoreItem(new Item.Properties().stacksTo(1).rarity(Rarity.RARE).fireResistant()));

    public static final DeferredHolder<Item, Item> VOID_FRUIT = ITEMS.register("void_fruit",
            () -> new Item(new Item.Properties()
                    .rarity(Rarity.UNCOMMON)
                    .food(new FoodProperties.Builder()
                            .nutrition(6)
                            .saturationModifier(0.9F)
                            .alwaysEdible()
                            .effect(() -> new MobEffectInstance(MobEffects.LEVITATION, 60, 0), 1.0F)
                            .effect(() -> new MobEffectInstance(MobEffects.SLOW_FALLING, 240, 0), 1.0F)
                            .build())));

    // ---------------------------------------------------------------- Giap Thep Hu Khong
    public static final DeferredHolder<Item, Item> VOID_STEEL_HELMET =
            armor("void_steel_helmet", ModArmorMaterials.VOID_STEEL, ArmorItem.Type.HELMET, 40, true);
    public static final DeferredHolder<Item, Item> VOID_STEEL_CHESTPLATE =
            armor("void_steel_chestplate", ModArmorMaterials.VOID_STEEL, ArmorItem.Type.CHESTPLATE, 40, true);
    public static final DeferredHolder<Item, Item> VOID_STEEL_LEGGINGS =
            armor("void_steel_leggings", ModArmorMaterials.VOID_STEEL, ArmorItem.Type.LEGGINGS, 40, true);
    public static final DeferredHolder<Item, Item> VOID_STEEL_BOOTS =
            armor("void_steel_boots", ModArmorMaterials.VOID_STEEL, ArmorItem.Type.BOOTS, 40, true);

    // ---------------------------------------------------------------- Giap Hu Anh
    public static final DeferredHolder<Item, Item> PHASE_CLOTH_HOOD =
            armor("phase_cloth_hood", ModArmorMaterials.PHASE_CLOTH, ArmorItem.Type.HELMET, 22, false);
    public static final DeferredHolder<Item, Item> PHASE_CLOTH_TUNIC =
            armor("phase_cloth_tunic", ModArmorMaterials.PHASE_CLOTH, ArmorItem.Type.CHESTPLATE, 22, false);
    public static final DeferredHolder<Item, Item> PHASE_CLOTH_LEGGINGS =
            armor("phase_cloth_leggings", ModArmorMaterials.PHASE_CLOTH, ArmorItem.Type.LEGGINGS, 22, false);
    public static final DeferredHolder<Item, Item> PHASE_CLOTH_BOOTS =
            armor("phase_cloth_boots", ModArmorMaterials.PHASE_CLOTH, ArmorItem.Type.BOOTS, 22, false);

    // ---------------------------------------------------------------- Khoi (item)
    public static final DeferredHolder<Item, Item> VOID_CRYSTAL_ORE_ITEM = blockItem("void_crystal_ore", ModBlocks.VOID_CRYSTAL_ORE);
    public static final DeferredHolder<Item, Item> DEEPSLATE_VOID_CRYSTAL_ORE_ITEM = blockItem("deepslate_void_crystal_ore", ModBlocks.DEEPSLATE_VOID_CRYSTAL_ORE);
    public static final DeferredHolder<Item, Item> VOID_STEEL_BLOCK_ITEM = blockItem("void_steel_block", ModBlocks.VOID_STEEL_BLOCK);
    public static final DeferredHolder<Item, Item> VOID_STONE_ITEM = blockItem("void_stone", ModBlocks.VOID_STONE);
    public static final DeferredHolder<Item, Item> VOID_BRICKS_ITEM = blockItem("void_bricks", ModBlocks.VOID_BRICKS);
    public static final DeferredHolder<Item, Item> RIFT_LANTERN_ITEM = blockItem("rift_lantern", ModBlocks.RIFT_LANTERN);
    public static final DeferredHolder<Item, Item> VOID_TILE_ITEM = blockItem("void_tile", ModBlocks.VOID_TILE);
    public static final DeferredHolder<Item, Item> VOID_PILLAR_ITEM = blockItem("void_pillar", ModBlocks.VOID_PILLAR);
    public static final DeferredHolder<Item, Item> VOID_CHISELED_ITEM = blockItem("void_chiseled", ModBlocks.VOID_CHISELED);
    public static final DeferredHolder<Item, Item> VOID_SOIL_ITEM = blockItem("void_soil", ModBlocks.VOID_SOIL);
    public static final DeferredHolder<Item, Item> VOID_CRYSTAL_BLOCK_ITEM = blockItem("void_crystal_block", ModBlocks.VOID_CRYSTAL_BLOCK);
    public static final DeferredHolder<Item, Item> VOID_BRICKS_STAIRS_ITEM = blockItem("void_bricks_stairs", ModBlocks.VOID_BRICKS_STAIRS);
    public static final DeferredHolder<Item, Item> VOID_BRICKS_SLAB_ITEM = blockItem("void_bricks_slab", ModBlocks.VOID_BRICKS_SLAB);
    public static final DeferredHolder<Item, Item> VOID_PORTAL_FRAME_ITEM = blockItem("void_portal_frame", ModBlocks.VOID_PORTAL_FRAME);
    public static final DeferredHolder<Item, Item> VOID_ALTAR_ITEM = blockItem("void_altar", ModBlocks.VOID_ALTAR);
    public static final DeferredHolder<Item, Item> VOID_GATEWAY_ITEM = ITEMS.register("void_gateway",
            () -> new BlockItem(ModBlocks.VOID_GATEWAY.get(), new Item.Properties().rarity(Rarity.RARE)));
    public static final DeferredHolder<Item, Item> VOID_FLUX_ITEM = ITEMS.register("void_flux",
            () -> new BlockItem(ModBlocks.VOID_FLUX.get(), new Item.Properties().stacksTo(16).rarity(Rarity.UNCOMMON)));

    // ---------------------------------------------------------------- Trung sinh quai
    public static final DeferredHolder<Item, Item> VOID_WALKER_SPAWN_EGG = ITEMS.register("void_walker_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.VOID_WALKER, 0x1B1033, 0xA070FF, new Item.Properties()));
    public static final DeferredHolder<Item, Item> RIFT_ARCHER_SPAWN_EGG = ITEMS.register("rift_archer_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.RIFT_ARCHER, 0x2A2438, 0x7FE0FF, new Item.Properties()));
    public static final DeferredHolder<Item, Item> PHASE_STALKER_SPAWN_EGG = ITEMS.register("phase_stalker_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.PHASE_STALKER, 0x14081F, 0xFF5CE1, new Item.Properties()));
    public static final DeferredHolder<Item, Item> VOID_BOAR_SPAWN_EGG = ITEMS.register("void_boar_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.VOID_BOAR, 0x2B1E3F, 0xD8B6FF, new Item.Properties()));
    public static final DeferredHolder<Item, Item> RIFT_BRUTE_SPAWN_EGG = ITEMS.register("rift_brute_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.RIFT_BRUTE, 0x3A2A55, 0xFF8A3D, new Item.Properties()));
    public static final DeferredHolder<Item, Item> VOID_SOVEREIGN_SPAWN_EGG = ITEMS.register("void_sovereign_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.VOID_SOVEREIGN, 0x0B0614, 0xE040FF, new Item.Properties().rarity(Rarity.EPIC)));

    public static final DeferredHolder<Item, Item> VOID_WISP_SPAWN_EGG = ITEMS.register("void_wisp_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.VOID_WISP, 0x1A3A5A, 0x9FFFFF, new Item.Properties()));
    public static final DeferredHolder<Item, Item> VOID_STALKER_BIRD_SPAWN_EGG = ITEMS.register("void_stalker_bird_spawn_egg",
            () -> new DeferredSpawnEggItem(ModEntities.VOID_STALKER_BIRD, 0x2A1450, 0x40E8FF, new Item.Properties()));

    // ---------------------------------------------------------------- Tro giup
    private static DeferredHolder<Item, Item> blockItem(String name, DeferredHolder<Block, Block> block) {
        return ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
    }

    private static DeferredHolder<Item, Item> armor(String name, DeferredHolder<ArmorMaterial, ArmorMaterial> material,
                                                    ArmorItem.Type type, int durabilityMultiplier, boolean fireproof) {
        return ITEMS.register(name, () -> {
            Item.Properties properties = new Item.Properties().durability(type.getDurability(durabilityMultiplier));
            if (fireproof) {
                properties.fireResistant();
            }
            return new ArmorItem(material, type, properties);
        });
    }

    private static ItemAttributeModifiers weaponAttributes(Tier tier, float damage, float speed, double reach) {
        ItemAttributeModifiers.Builder builder = ItemAttributeModifiers.builder()
                .add(Attributes.ATTACK_DAMAGE,
                        new AttributeModifier(BASE_ATTACK_DAMAGE_ID, damage + tier.getAttackDamageBonus(), AttributeModifier.Operation.ADD_VALUE),
                        EquipmentSlotGroup.MAINHAND)
                .add(Attributes.ATTACK_SPEED,
                        new AttributeModifier(BASE_ATTACK_SPEED_ID, speed, AttributeModifier.Operation.ADD_VALUE),
                        EquipmentSlotGroup.MAINHAND);
        if (reach > 0.0D) {
            builder.add(Attributes.ENTITY_INTERACTION_RANGE,
                    new AttributeModifier(PIERCER_REACH_ID, reach, AttributeModifier.Operation.ADD_VALUE),
                    EquipmentSlotGroup.MAINHAND);
        }
        return builder.build();
    }

    private ModItems() {
    }
}
