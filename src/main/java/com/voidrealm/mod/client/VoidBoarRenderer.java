package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.VoidBoar;
import net.minecraft.client.model.PigModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

/** Renderer Lon Rung Hu Khong: dung model lon cua vanilla + texture rieng 64x32. */
public class VoidBoarRenderer extends MobRenderer<VoidBoar, PigModel<VoidBoar>> {
    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/void_boar.png");

    public VoidBoarRenderer(EntityRendererProvider.Context context) {
        super(context, new PigModel<>(context.bakeLayer(ModelLayers.PIG)), 0.7F);
        this.addLayer(new GlowLayer<VoidBoar, PigModel<VoidBoar>>(this, "void_boar"));
    }

    @Override
    public ResourceLocation getTextureLocation(VoidBoar entity) {
        return TEXTURE;
    }

    @Override
    protected void scale(VoidBoar entity, PoseStack poseStack, float partialTickTime) {
        poseStack.scale(1.15F, 1.15F, 1.15F);
    }
}
