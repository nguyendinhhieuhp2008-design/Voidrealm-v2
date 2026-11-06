package com.voidrealm.mod.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** Mat Nhin Thuc Tai: cam tren tay de thay quang xuyen dia hinh va quai (ke ca tang hinh). Logic o ModGameEvents + XrayClient. */
public class EyeOfTheVoidItem extends Item {
    public EyeOfTheVoidItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.eye_of_the_void").withStyle(ChatFormatting.DARK_AQUA));
    }
}
