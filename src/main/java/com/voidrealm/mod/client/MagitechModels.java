package com.voidrealm.mod.client;

import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.model.geom.PartPose;

/** Tu dong sinh boi tools/gen_magitech.py - KHONG sua tay. */
public final class MagitechModels {
    public static LayerDefinition wisp() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition core = root.addOrReplaceChild("core", CubeListBuilder.create().texOffs(0, 0).addBox(-3F, -3F, -3F, 6F, 6F, 6F), PartPose.offset(0F, 20F, 0F));
        PartDefinition shell = core.addOrReplaceChild("shell", CubeListBuilder.create().texOffs(24, 0).addBox(-4F, -4F, -4F, 8F, 8F, 8F), PartPose.offset(0F, 0F, 0F));
        PartDefinition orbit = root.addOrReplaceChild("orbit", CubeListBuilder.create().texOffs(56, 0).addBox(0F, 0F, 0F, 1F, 1F, 1F), PartPose.offset(0F, 20F, 0F));
        PartDefinition o1 = orbit.addOrReplaceChild("o1", CubeListBuilder.create().texOffs(0, 16).addBox(-1F, -1F, -1F, 2F, 2F, 2F), PartPose.offset(7F, 0F, 0F));
        PartDefinition o2 = orbit.addOrReplaceChild("o2", CubeListBuilder.create().texOffs(8, 16).addBox(-1F, -1F, -1F, 2F, 2F, 2F), PartPose.offset(-7F, 0F, 0F));
        PartDefinition o3 = orbit.addOrReplaceChild("o3", CubeListBuilder.create().texOffs(16, 16).addBox(-1F, -1F, -1F, 2F, 2F, 2F), PartPose.offset(0F, -3F, 7F));
        PartDefinition o4 = orbit.addOrReplaceChild("o4", CubeListBuilder.create().texOffs(24, 16).addBox(-1F, -1F, -1F, 2F, 2F, 2F), PartPose.offset(0F, 3F, -7F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create().texOffs(32, 16).addBox(-1F, -1F, 0F, 2F, 2F, 4F), PartPose.offsetAndRotation(0F, 21F, 3F, 0.5F, 0F, 0F));
        return LayerDefinition.create(mesh, 64, 64);
    }

    public static LayerDefinition bird() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-3F, -3F, -5F, 6F, 6F, 10F), PartPose.offset(0F, 16F, 0F));
        PartDefinition chest = body.addOrReplaceChild("chest", CubeListBuilder.create().texOffs(32, 0).addBox(-2.5F, -1.5F, -7.5F, 5F, 4F, 3F), PartPose.offset(0F, 0F, 0F));
        PartDefinition head = body.addOrReplaceChild("head", CubeListBuilder.create().texOffs(48, 0).addBox(-2F, -2F, -3F, 4F, 4F, 4F), PartPose.offset(0F, -3.5F, -5.5F));
        PartDefinition beak_up = head.addOrReplaceChild("beak_up", CubeListBuilder.create().texOffs(0, 16).addBox(-1F, -0.6F, -6F, 2F, 1F, 3F), PartPose.offset(0F, 0F, 0F));
        PartDefinition beak_low = head.addOrReplaceChild("beak_low", CubeListBuilder.create().texOffs(10, 16).addBox(-1F, 0.4F, -5F, 2F, 1F, 2F), PartPose.offset(0F, 0F, 0F));
        PartDefinition crest = head.addOrReplaceChild("crest", CubeListBuilder.create().texOffs(18, 16).addBox(-0.5F, -4.6F, -1F, 1F, 3F, 4F), PartPose.offsetAndRotation(0F, 0F, 0F, 0.25F, 0F, 0F));
        PartDefinition wing_r = body.addOrReplaceChild("wing_r", CubeListBuilder.create().texOffs(28, 16).addBox(0F, -0.5F, -3F, 10F, 1F, 6F), PartPose.offset(3F, -1.5F, -1F));
        PartDefinition tip_r = wing_r.addOrReplaceChild("tip_r", CubeListBuilder.create().texOffs(0, 23).addBox(0F, -0.4F, -2.5F, 8F, 1F, 5F), PartPose.offset(10F, 0F, 0F));
        PartDefinition wing_l = body.addOrReplaceChild("wing_l", CubeListBuilder.create().texOffs(26, 23).addBox(-10F, -0.5F, -3F, 10F, 1F, 6F), PartPose.offset(-3F, -1.5F, -1F));
        PartDefinition tip_l = wing_l.addOrReplaceChild("tip_l", CubeListBuilder.create().texOffs(0, 30).addBox(-8F, -0.4F, -2.5F, 8F, 1F, 5F), PartPose.offset(-10F, 0F, 0F));
        PartDefinition tail_c = body.addOrReplaceChild("tail_c", CubeListBuilder.create().texOffs(26, 30).addBox(-1.5F, -0.5F, 0F, 3F, 1F, 9F), PartPose.offsetAndRotation(0F, 0.5F, 5F, 0.12F, 0F, 0F));
        PartDefinition tail_l = body.addOrReplaceChild("tail_l", CubeListBuilder.create().texOffs(0, 40).addBox(-1.5F, -0.5F, 0F, 3F, 1F, 8F), PartPose.offsetAndRotation(0F, 0.5F, 5F, 0.12F, -0.35F, 0F));
        PartDefinition tail_r = body.addOrReplaceChild("tail_r", CubeListBuilder.create().texOffs(22, 40).addBox(-1.5F, -0.5F, 0F, 3F, 1F, 8F), PartPose.offsetAndRotation(0F, 0.5F, 5F, 0.12F, 0.35F, 0F));
        PartDefinition leg_r = body.addOrReplaceChild("leg_r", CubeListBuilder.create().texOffs(44, 40).addBox(-0.5F, 0F, -0.5F, 1F, 4F, 1F), PartPose.offset(1.8F, 3F, 1F));
        PartDefinition foot_r = leg_r.addOrReplaceChild("foot_r", CubeListBuilder.create().texOffs(48, 40).addBox(-1.5F, 0F, -2F, 3F, 1F, 3F), PartPose.offset(0F, 4F, 0F));
        PartDefinition leg_l = body.addOrReplaceChild("leg_l", CubeListBuilder.create().texOffs(60, 40).addBox(-0.5F, 0F, -0.5F, 1F, 4F, 1F), PartPose.offset(-1.8F, 3F, 1F));
        PartDefinition foot_l = leg_l.addOrReplaceChild("foot_l", CubeListBuilder.create().texOffs(0, 49).addBox(-1.5F, 0F, -2F, 3F, 1F, 3F), PartPose.offset(0F, 4F, 0F));
        return LayerDefinition.create(mesh, 64, 64);
    }

    private MagitechModels() {
    }
}
