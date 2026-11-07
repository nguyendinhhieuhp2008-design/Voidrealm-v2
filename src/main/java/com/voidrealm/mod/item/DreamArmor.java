package com.voidrealm.mod.item;

import com.voidrealm.mod.registry.ModArmorMaterials;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ArmorItem;

public final class DreamArmor {
    public static boolean hasFullSet(LivingEntity entity) {
        for (EquipmentSlot slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            if (!(entity.getItemBySlot(slot).getItem() instanceof ArmorItem armor)
                    || armor.getMaterial().value() != ModArmorMaterials.DREAM.get()) {
                return false;
            }
        }
        return true;
    }

    private DreamArmor() {
    }
}
