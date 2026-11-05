package com.voidrealm.mod.registry;

import com.voidrealm.mod.VoidRealm;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, VoidRealm.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN = CREATIVE_TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.voidrealm"))
                    .icon(() -> new ItemStack(ModItems.VOID_STEEL_INGOT.get()))
                    .displayItems((parameters, output) ->
                            ModItems.ITEMS.getEntries().forEach(holder -> output.accept(holder.get())))
                    .build());

    private ModCreativeTabs() {
    }
}
