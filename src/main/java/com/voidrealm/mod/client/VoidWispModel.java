package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.voidrealm.mod.entity.VoidWisp;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/** Model Void Wisp: loi phat sang, vo thung lo, 4 manh pha le xoay quanh. */
public class VoidWispModel extends EntityModel<VoidWisp> {
    private final ModelPart root;
    private final ModelPart core;
    private final ModelPart orbit;
    private final ModelPart tail;

    public VoidWispModel(ModelPart root) {
        this.root = root;
        this.core = root.getChild("core");
        this.orbit = root.getChild("orbit");
        this.tail = root.getChild("tail");
    }

    @Override
    public void setupAnim(VoidWisp entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        this.root.y = Mth.sin(ageInTicks * 0.12F) * 1.4F;
        this.core.yRot = ageInTicks * 0.06F;
        this.core.xRot = Mth.sin(ageInTicks * 0.05F) * 0.25F;
        this.orbit.yRot = ageInTicks * 0.16F;
        this.orbit.xRot = Mth.sin(ageInTicks * 0.09F) * 0.35F;
        this.tail.xRot = 0.5F + Mth.sin(ageInTicks * 0.2F) * 0.15F;
        this.root.yRot = netHeadYaw * ((float) Math.PI / 180F);
    }

    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay, int color) {
        this.root.render(poseStack, buffer, packedLight, packedOverlay, color);
    }
}
