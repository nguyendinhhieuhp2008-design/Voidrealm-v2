package com.voidrealm.mod.registry;

import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.common.SimpleTier;

public class ModTiers {
    /** Thep Hu Khong: nhinh hon netherite mot chut ve sat thuong va do ben. */
    public static final Tier VOID_STEEL = new SimpleTier(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            2400,
            9.0F,
            4.5F,
            18,
            () -> Ingredient.of(ModItems.VOID_STEEL_INGOT.get()));

    /** Mong Tinh (Dream Crystal): ben, sat thuong cao. */
    public static final Tier DREAM = new SimpleTier(
            BlockTags.INCORRECT_FOR_NETHERITE_TOOL,
            2800,
            9.5F,
            4.5F,
            22,
            () -> Ingredient.of(ModItems.DREAM_CRYSTAL.get()));

    private ModTiers() {
    }
}
