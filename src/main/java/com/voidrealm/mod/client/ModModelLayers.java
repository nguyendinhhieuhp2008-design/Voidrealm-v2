package com.voidrealm.mod.client;

import com.voidrealm.mod.VoidRealm;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.resources.ResourceLocation;

/** Vi tri cac lop model 3D rieng cua quai (xem ModelExtras). */
public final class ModModelLayers {
    public static final ModelLayerLocation VOID_WALKER = layer("void_walker");
    public static final ModelLayerLocation PHASE_STALKER = layer("phase_stalker");
    public static final ModelLayerLocation RIFT_BRUTE = layer("rift_brute");
    public static final ModelLayerLocation VOID_SOVEREIGN = layer("void_sovereign");
    public static final ModelLayerLocation RIFT_ARCHER = layer("rift_archer");
    public static final ModelLayerLocation VOID_BOAR = layer("void_boar");

    private static ModelLayerLocation layer(String name) {
        return new ModelLayerLocation(ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, name), "main");
    }

    private ModModelLayers() {
    }
}
