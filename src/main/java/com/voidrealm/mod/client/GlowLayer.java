package com.voidrealm.mod.client;

import com.voidrealm.mod.VoidRealm;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Entity;

/** Lop phat sang (mat, rune, vet nut) - dung RenderType.eyes cua vanilla, rat nhe. Texture: textures/entity/NAME_glow.png */
public class GlowLayer<T extends Entity, M extends EntityModel<T>> extends EyesLayer<T, M> {
    private final RenderType glowType;

    public GlowLayer(RenderLayerParent<T, M> parent, String name) {
        super(parent);
        this.glowType = RenderType.eyes(
                ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/" + name + "_glow.png"));
    }

    @Override
    public RenderType renderType() {
        return this.glowType;
    }
}
