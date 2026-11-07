package com.voidrealm.mod.item;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.CrossbowItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** No Mong Tinh: nap rat nhanh (chi can giu ~0.3 giay). Sat thuong/xuyen them xu ly o DreamEvents. */
public class DreamCrossbowItem extends CrossbowItem {
    private static final int HEAD_START = 19;

    public DreamCrossbowItem(Properties properties) {
        super(properties);
    }

    @Override
    public void releaseUsing(ItemStack stack, Level level, LivingEntity entity, int timeLeft) {
        super.releaseUsing(stack, level, entity, timeLeft - HEAD_START);
    }
}
