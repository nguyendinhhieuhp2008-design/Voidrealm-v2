package com.voidrealm.mod.registry;

import com.voidrealm.mod.VoidRealm;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModArmorMaterials {
    public static final DeferredRegister<ArmorMaterial> ARMOR_MATERIALS =
            DeferredRegister.create(Registries.ARMOR_MATERIAL, VoidRealm.MODID);

    /** Giap Thep Hu Khong: nang, bao ve cao. Texture: textures/models/armor/void_steel_layer_*.png */
    public static final DeferredHolder<ArmorMaterial, ArmorMaterial> VOID_STEEL = ARMOR_MATERIALS.register("void_steel",
            () -> new ArmorMaterial(
                    defense(4, 9, 7, 4, 11),
                    18,
                    SoundEvents.ARMOR_EQUIP_NETHERITE,
                    () -> Ingredient.of(ModItems.VOID_STEEL_INGOT.get()),
                    List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "void_steel"))),
                    3.5F,
                    0.05F));

    /** Giap Hu Anh: nhe, tang toc do. Texture: textures/models/armor/phase_cloth_layer_*.png */
    public static final DeferredHolder<ArmorMaterial, ArmorMaterial> PHASE_CLOTH = ARMOR_MATERIALS.register("phase_cloth",
            () -> new ArmorMaterial(
                    defense(2, 6, 5, 2, 7),
                    16,
                    SoundEvents.ARMOR_EQUIP_LEATHER,
                    () -> Ingredient.of(ModItems.PHASE_SILK.get()),
                    List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "phase_cloth"))),
                    1.0F,
                    0.0F));

    private static Map<ArmorItem.Type, Integer> defense(int helmet, int chestplate, int leggings, int boots, int body) {
        Map<ArmorItem.Type, Integer> map = new EnumMap<>(ArmorItem.Type.class);
        map.put(ArmorItem.Type.HELMET, helmet);
        map.put(ArmorItem.Type.CHESTPLATE, chestplate);
        map.put(ArmorItem.Type.LEGGINGS, leggings);
        map.put(ArmorItem.Type.BOOTS, boots);
        map.put(ArmorItem.Type.BODY, body);
        return map;
    }

    private ModArmorMaterials() {
    }
}
