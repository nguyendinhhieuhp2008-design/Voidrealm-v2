package com.voidrealm.mod.client;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.VoidWisp;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;

/** Renderer Void Wisp: luon sang toi da (tu phat sang). */
public class VoidWispRenderer extends MobRenderer<VoidWisp, VoidWispModel> {
    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "textures/entity/void_wisp.png");

    public VoidWispRenderer(EntityRendererProvider.Context context) {
        super(context, new VoidWispModel(context.bakeLayer(ModModelLayers.VOID_WISP)), 0.2F);
    }

    @Override
    public ResourceLocation getTextureLocation(VoidWisp entity) {
        return TEXTURE;
    }

    @Override
    protected int getBlockLightLevel(VoidWisp entity, BlockPos pos) {
        return 15;
    }
}
