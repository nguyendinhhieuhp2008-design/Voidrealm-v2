package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.voidrealm.mod.entity.VoidStalkerBird;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.util.Mth;

/** Model Void Stalker Bird: than, dau, mo, mao, hai canh 2 doan va 3 long duoi. Canh vo manh khi bay. */
public class VoidStalkerBirdModel extends EntityModel<VoidStalkerBird> {
    private final ModelPart root;
    private final ModelPart body;
    private final ModelPart head;
    private final ModelPart wingR;
    private final ModelPart wingL;
    private final ModelPart tipR;
    private final ModelPart tipL;
    private final ModelPart tailL;
    private final ModelPart tailR;
    private final ModelPart tailC;
    private final ModelPart legR;
    private final ModelPart legL;

    public VoidStalkerBirdModel(ModelPart root) {
        this.root = root;
        this.body = root.getChild("body");
        this.head = this.body.getChild("head");
        this.wingR = this.body.getChild("wing_r");
        this.wingL = this.body.getChild("wing_l");
        this.tipR = this.wingR.getChild("tip_r");
        this.tipL = this.wingL.getChild("tip_l");
        this.tailL = this.body.getChild("tail_l");
        this.tailR = this.body.getChild("tail_r");
        this.tailC = this.body.getChild("tail_c");
        this.legR = this.body.getChild("leg_r");
        this.legL = this.body.getChild("leg_l");
    }

    @Override
    public void setupAnim(VoidStalkerBird entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        float flap = Mth.sin(ageInTicks * 0.45F);
        float amp = entity.isVehicle() ? 0.75F : 0.5F;
        this.wingR.zRot = flap * amp;
        this.wingL.zRot = -flap * amp;
        this.tipR.zRot = Mth.sin(ageInTicks * 0.45F - 0.9F) * amp * 0.9F;
        this.tipL.zRot = -Mth.sin(ageInTicks * 0.45F - 0.9F) * amp * 0.9F;
        this.body.y = 16.0F + Mth.sin(ageInTicks * 0.45F + 1.2F) * 0.7F;
        this.body.xRot = Mth.clamp(headPitch * 0.01F, -0.3F, 0.3F);
        this.head.xRot = headPitch * ((float) Math.PI / 180F) * 0.6F;
        this.head.yRot = netHeadYaw * ((float) Math.PI / 180F);
        float sway = Mth.sin(ageInTicks * 0.2F) * 0.08F;
        this.tailL.yRot = -0.35F + sway;
        this.tailR.yRot = 0.35F - sway;
        this.tailC.xRot = 0.12F + Mth.sin(ageInTicks * 0.3F) * 0.05F;
        this.legR.xRot = 0.7F;
        this.legL.xRot = 0.7F;
    }

    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer buffer, int packedLight, int packedOverlay, int color) {
        this.root.render(poseStack, buffer, packedLight, packedOverlay, color);
    }
}
