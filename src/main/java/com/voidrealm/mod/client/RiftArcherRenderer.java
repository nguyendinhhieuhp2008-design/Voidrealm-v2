package com.voidrealm.mod.client;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.RiftArcher;
import net.minecraft.client.model.SkeletonModel;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

/** Renderer Cung Thu Di Gioi: dung model xuong cua vanilla + texture rieng 64x32. */
public class RiftArcherRenderer extends HumanoidMobRenderer<RiftArcher, SkeletonModel<RiftArcher>> {
    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/rift_archer.png");

    public RiftArcherRenderer(EntityRendererProvider.Context context) {
        super(context, new SkeletonModel<>(context.bakeLayer(ModModelLayers.RIFT_ARCHER)), 0.5F);
        this.addLayer(new GlowLayer<RiftArcher, SkeletonModel<RiftArcher>>(this, "rift_archer"));
    }

    @Override
    public ResourceLocation getTextureLocation(RiftArcher entity) {
        return TEXTURE;
    }
}
