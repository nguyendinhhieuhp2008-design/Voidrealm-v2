package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.VoidStalkerBird;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

/** Renderer Void Stalker Bird (texture 64x64 sinh tu tools/gen_magitech.py). */
public class VoidStalkerBirdRenderer extends MobRenderer<VoidStalkerBird, VoidStalkerBirdModel> {
    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/void_stalker_bird.png");

    public VoidStalkerBirdRenderer(EntityRendererProvider.Context context) {
        super(context, new VoidStalkerBirdModel(context.bakeLayer(ModModelLayers.VOID_STALKER_BIRD)), 0.6F);
    }

    @Override
    public ResourceLocation getTextureLocation(VoidStalkerBird entity) {
        return TEXTURE;
    }

    @Override
    protected void scale(VoidStalkerBird entity, PoseStack poseStack, float partialTickTime) {
        poseStack.scale(1.15F, 1.15F, 1.15F);
    }
}
