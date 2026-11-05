package com.voidrealm.mod;

import com.voidrealm.mod.registry.ModArmorMaterials;
import com.voidrealm.mod.registry.ModBlocks;
import com.voidrealm.mod.registry.ModCreativeTabs;
import com.voidrealm.mod.registry.ModEntities;
import com.voidrealm.mod.registry.ModItems;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;

/**
 * Void Realm - mang vu khi, giap, vat pham, quai vat va cong trinh tu mot khong gian khac.
 */
@Mod(VoidRealm.MODID)
public class VoidRealm {
    public static final String MODID = "voidrealm";

    public VoidRealm(IEventBus modEventBus, ModContainer modContainer) {
        ModBlocks.BLOCKS.register(modEventBus);
        ModArmorMaterials.ARMOR_MATERIALS.register(modEventBus);
        ModItems.ITEMS.register(modEventBus);
        ModEntities.ENTITIES.register(modEventBus);
        ModCreativeTabs.CREATIVE_TABS.register(modEventBus);

        modContainer.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }
}
