package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.voidrealm.mod.VoidRealm;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Mob;

/**
 * Renderer dung chung cho quai hinh nguoi: dung model zombie cua vanilla (nhe, khong can model rieng)
 * (ModelExtras them sung/ao choang/canh) va texture 64x64 rieng cho tung quai.
 */
public class VoidHumanoidRenderer<T extends Mob> extends HumanoidMobRenderer<T, HumanoidModel<T>> {
    private final ResourceLocation texture;
    private final float scale;

    public VoidHumanoidRenderer(EntityRendererProvider.Context context, ModelLayerLocation layer, String textureName, float scale, float shadowRadius) {
        super(context, new HumanoidModel<T>(context.bakeLayer(layer)), shadowRadius);
        this.texture = ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/" + textureName + ".png");
        this.scale = scale;
        this.addLayer(new GlowLayer<T, HumanoidModel<T>>(this, textureName));
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return this.texture;
    }

    @Override
    protected void scale(T entity, PoseStack poseStack, float partialTickTime) {
        poseStack.scale(this.scale, this.scale, this.scale);
    }
}
