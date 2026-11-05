package com.voidrealm.mod.client;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.QuadrupedModel;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * DO TOOLS/gen_art.py SINH RA - khong sua tay. Model 3D rieng cua quai: giu khung vanilla (nhe)
 * va gan them sung, mu, ao choang, canh, duoi, nanh... vao cac bo phan co san.
 */
public final class ModelExtras {
    private static float r(float degrees) {
        return (float) Math.toRadians(degrees);
    }

    public static LayerDefinition voidWalker() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.getChild("head").addOrReplaceChild("hood_peak", CubeListBuilder.create().texOffs(0, 32).addBox(-2.0F, -1.5F, -0.5F, 4.0F, 3.0F, 5.0F), PartPose.offsetAndRotation(0.0F, -8.2F, 2.0F, r(-25.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("cloak", CubeListBuilder.create().texOffs(18, 32).addBox(-5.0F, 0.0F, 0.0F, 10.0F, 14.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 0.5F, 2.3F, r(4.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("cloak_hem", CubeListBuilder.create().texOffs(40, 32).addBox(-5.0F, 0.0F, 0.0F, 10.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 14.3F, 2.6F, r(8.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("shard", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -1.5F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(8.5F, -3.0F, 0.0F, r(0.0F), r(0.0F), r(15.0F)));
        root.getChild("body").addOrReplaceChild("shard_l", CubeListBuilder.create().texOffs(56, 16).mirror().addBox(-0.5F, -1.5F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-8.5F, -3.0F, 0.0F, r(0.0F), r(0.0F), r(-15.0F)));
        return LayerDefinition.create(mesh, 64, 64);
    }

    public static LayerDefinition phaseStalker() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.getChild("head").addOrReplaceChild("crest_a", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -4.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -8.0F, -1.0F, r(-20.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("crest_b", CubeListBuilder.create().texOffs(60, 16).addBox(-0.5F, -5.0F, -0.5F, 1.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -8.0F, 1.0F, r(-35.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("crest_c", CubeListBuilder.create().texOffs(56, 21).addBox(-0.5F, -5.0F, -0.5F, 1.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -8.0F, 3.0F, r(-50.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("spine_0", CubeListBuilder.create().texOffs(60, 22).addBox(-0.5F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 1.0F, 2.2F, r(35.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("spine_1", CubeListBuilder.create().texOffs(60, 22).addBox(-0.5F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 4.5F, 2.2F, r(40.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("spine_2", CubeListBuilder.create().texOffs(60, 22).addBox(-0.5F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 8.0F, 2.2F, r(50.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("tail_a", CubeListBuilder.create().texOffs(0, 32).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 2.0F, 7.0F), PartPose.offsetAndRotation(0.0F, 10.5F, 2.0F, r(25.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("tail_b", CubeListBuilder.create().texOffs(18, 32).addBox(-0.5F, 0.0F, 0.0F, 1.0F, 1.0F, 5.0F), PartPose.offsetAndRotation(0.0F, 12.5F, 8.0F, r(40.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("claw_0", CubeListBuilder.create().texOffs(56, 27).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(-2.5F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("claw_0_l", CubeListBuilder.create().texOffs(56, 27).mirror().addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(2.5F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("claw_1", CubeListBuilder.create().texOffs(56, 27).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(-1.0F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("claw_1_l", CubeListBuilder.create().texOffs(56, 27).mirror().addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(1.0F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("claw_2", CubeListBuilder.create().texOffs(56, 27).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(0.5F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("claw_2_l", CubeListBuilder.create().texOffs(56, 27).mirror().addBox(-0.5F, 0.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(-0.5F, 12.0F, 0.0F, r(-10.0F), r(0.0F), r(0.0F)));
        return LayerDefinition.create(mesh, 64, 64);
    }

    public static LayerDefinition riftBrute() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.getChild("head").addOrReplaceChild("horn_base", CubeListBuilder.create().texOffs(56, 16).addBox(-1.0F, -4.0F, -1.0F, 2.0F, 4.0F, 2.0F), PartPose.offsetAndRotation(4.3F, -7.5F, 0.0F, r(0.0F), r(0.0F), r(-28.0F)));
        root.getChild("head").addOrReplaceChild("horn_base_l", CubeListBuilder.create().texOffs(56, 16).mirror().addBox(-1.0F, -4.0F, -1.0F, 2.0F, 4.0F, 2.0F), PartPose.offsetAndRotation(-4.3F, -7.5F, 0.0F, r(0.0F), r(0.0F), r(28.0F)));
        root.getChild("head").addOrReplaceChild("horn_tip", CubeListBuilder.create().texOffs(56, 22).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(6.4F, -11.0F, 0.0F, r(0.0F), r(0.0F), r(-50.0F)));
        root.getChild("head").addOrReplaceChild("horn_tip_l", CubeListBuilder.create().texOffs(56, 22).mirror().addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-6.4F, -11.0F, 0.0F, r(0.0F), r(0.0F), r(50.0F)));
        root.getChild("right_arm").addOrReplaceChild("pauldron", CubeListBuilder.create().texOffs(0, 32).addBox(-3.0F, -1.0F, -3.0F, 6.0F, 2.0F, 6.0F), PartPose.offsetAndRotation(-1.0F, -1.5F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("pauldron_l", CubeListBuilder.create().texOffs(0, 32).mirror().addBox(-3.0F, -1.0F, -3.0F, 6.0F, 2.0F, 6.0F), PartPose.offsetAndRotation(1.0F, -1.5F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("p_spike", CubeListBuilder.create().texOffs(60, 22).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-1.0F, -3.0F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("p_spike_l", CubeListBuilder.create().texOffs(60, 22).mirror().addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(1.0F, -3.0F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("fist", CubeListBuilder.create().texOffs(24, 32).addBox(-2.5F, 0.0F, -2.5F, 5.0F, 3.0F, 5.0F), PartPose.offsetAndRotation(-1.0F, 10.0F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("left_arm").addOrReplaceChild("fist_l", CubeListBuilder.create().texOffs(24, 32).mirror().addBox(-2.5F, 0.0F, -2.5F, 5.0F, 3.0F, 5.0F), PartPose.offsetAndRotation(1.0F, 10.0F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("back_plate", CubeListBuilder.create().texOffs(44, 32).addBox(-3.5F, 0.0F, 0.0F, 7.0F, 8.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 0.5F, 2.2F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("b_spike_0", CubeListBuilder.create().texOffs(56, 26).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 3.0F), PartPose.offsetAndRotation(-2.5F, 3.0F, 3.2F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("b_spike_1", CubeListBuilder.create().texOffs(56, 26).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 3.0F), PartPose.offsetAndRotation(0.0F, 6.0F, 3.2F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("b_spike_2", CubeListBuilder.create().texOffs(56, 26).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 3.0F), PartPose.offsetAndRotation(2.5F, 3.0F, 3.2F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("skirt", CubeListBuilder.create().texOffs(0, 40).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 2.0F, 4.0F), PartPose.offsetAndRotation(0.0F, 10.5F, 0.0F, r(0.0F), r(0.0F), r(0.0F)));
        return LayerDefinition.create(mesh, 64, 64);
    }

    public static LayerDefinition voidSovereign() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.getChild("head").addOrReplaceChild("cspike_0", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -8.2F, -3.6F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("cspike_1", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(3.4F, -8.2F, -3.4F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("cspike_2", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-3.4F, -8.2F, -3.4F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("cspike_3", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -8.2F, 3.6F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("cspike_4", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(3.4F, -8.2F, 3.4F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("cspike_5", CubeListBuilder.create().texOffs(56, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-3.4F, -8.2F, 3.4F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("horn_1", CubeListBuilder.create().texOffs(56, 20).addBox(-1.0F, -5.0F, -1.0F, 2.0F, 5.0F, 2.0F), PartPose.offsetAndRotation(3.2F, -8.0F, 0.0F, r(0.0F), r(0.0F), r(-20.0F)));
        root.getChild("head").addOrReplaceChild("horn_1_l", CubeListBuilder.create().texOffs(56, 20).mirror().addBox(-1.0F, -5.0F, -1.0F, 2.0F, 5.0F, 2.0F), PartPose.offsetAndRotation(-3.2F, -8.0F, 0.0F, r(0.0F), r(0.0F), r(20.0F)));
        root.getChild("head").addOrReplaceChild("horn_2", CubeListBuilder.create().texOffs(56, 27).addBox(-1.0F, -4.0F, -1.0F, 2.0F, 4.0F, 2.0F), PartPose.offsetAndRotation(5.4F, -12.6F, 0.0F, r(0.0F), r(0.0F), r(-45.0F)));
        root.getChild("head").addOrReplaceChild("horn_2_l", CubeListBuilder.create().texOffs(56, 27).mirror().addBox(-1.0F, -4.0F, -1.0F, 2.0F, 4.0F, 2.0F), PartPose.offsetAndRotation(-5.4F, -12.6F, 0.0F, r(0.0F), r(0.0F), r(45.0F)));
        root.getChild("head").addOrReplaceChild("horn_3", CubeListBuilder.create().texOffs(60, 16).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(8.6F, -15.2F, 0.0F, r(0.0F), r(0.0F), r(-75.0F)));
        root.getChild("head").addOrReplaceChild("horn_3_l", CubeListBuilder.create().texOffs(60, 16).mirror().addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-8.6F, -15.2F, 0.0F, r(0.0F), r(0.0F), r(75.0F)));
        root.getChild("body").addOrReplaceChild("cape", CubeListBuilder.create().texOffs(0, 32).addBox(-5.0F, 0.0F, 0.0F, 10.0F, 14.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 0.5F, 2.4F, r(5.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("cape_low", CubeListBuilder.create().texOffs(22, 32).addBox(-5.0F, 0.0F, 0.0F, 10.0F, 8.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 14.2F, 3.6F, r(10.0F), r(0.0F), r(0.0F)));
        root.getChild("right_arm").addOrReplaceChild("sh_spike", CubeListBuilder.create().texOffs(44, 32).addBox(-0.5F, -4.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(-1.0F, -2.0F, 0.0F, r(0.0F), r(0.0F), r(20.0F)));
        root.getChild("left_arm").addOrReplaceChild("sh_spike_l", CubeListBuilder.create().texOffs(44, 32).mirror().addBox(-0.5F, -4.0F, -0.5F, 1.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(1.0F, -2.0F, 0.0F, r(0.0F), r(0.0F), r(-20.0F)));
        root.getChild("body").addOrReplaceChild("blade_a", CubeListBuilder.create().texOffs(48, 32).addBox(-0.5F, -10.0F, -1.0F, 1.0F, 10.0F, 2.0F), PartPose.offsetAndRotation(3.5F, 3.0F, 3.5F, r(0.0F), r(0.0F), r(-25.0F)));
        root.getChild("body").addOrReplaceChild("blade_a_l", CubeListBuilder.create().texOffs(48, 32).mirror().addBox(-0.5F, -10.0F, -1.0F, 1.0F, 10.0F, 2.0F), PartPose.offsetAndRotation(-3.5F, 3.0F, 3.5F, r(0.0F), r(0.0F), r(25.0F)));
        root.getChild("body").addOrReplaceChild("blade_b", CubeListBuilder.create().texOffs(54, 33).addBox(-0.5F, -8.0F, -1.0F, 1.0F, 8.0F, 2.0F), PartPose.offsetAndRotation(3.5F, 5.0F, 3.2F, r(0.0F), r(0.0F), r(-55.0F)));
        root.getChild("body").addOrReplaceChild("blade_b_l", CubeListBuilder.create().texOffs(54, 33).mirror().addBox(-0.5F, -8.0F, -1.0F, 1.0F, 8.0F, 2.0F), PartPose.offsetAndRotation(-3.5F, 5.0F, 3.2F, r(0.0F), r(0.0F), r(55.0F)));
        root.getChild("body").addOrReplaceChild("core_gem", CubeListBuilder.create().texOffs(22, 41).addBox(-2.0F, 0.0F, -0.5F, 4.0F, 4.0F, 1.0F), PartPose.offsetAndRotation(0.0F, 3.0F, -2.3F, r(0.0F), r(0.0F), r(0.0F)));
        return LayerDefinition.create(mesh, 64, 64);
    }

    public static LayerDefinition riftArcher() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(-5.0F, 2.0F, 0.0F));
        root.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(40, 16).mirror().addBox(-1.0F, -2.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(5.0F, 2.0F, 0.0F));
        root.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(-2.0F, 12.0F, 0.0F));
        root.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(0, 16).mirror().addBox(-1.0F, 0.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(2.0F, 12.0F, 0.0F));
        root.getChild("head").addOrReplaceChild("hood_tip", CubeListBuilder.create().texOffs(48, 16).addBox(-2.0F, -1.5F, -0.5F, 4.0F, 3.0F, 4.0F), PartPose.offsetAndRotation(0.0F, -8.3F, 1.5F, r(-20.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("quiver", CubeListBuilder.create().texOffs(8, 16).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 6.0F, 2.0F), PartPose.offsetAndRotation(2.5F, 1.0F, 2.8F, r(0.0F), r(0.0F), r(10.0F)));
        root.getChild("body").addOrReplaceChild("arrow_0", CubeListBuilder.create().texOffs(48, 23).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(1.5F, 1.2F, 3.0F, r(0.0F), r(0.0F), r(10.0F)));
        root.getChild("body").addOrReplaceChild("arrow_1", CubeListBuilder.create().texOffs(48, 23).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(3.5F, 1.2F, 3.0F, r(0.0F), r(0.0F), r(10.0F)));
        root.getChild("body").addOrReplaceChild("scarf_tail", CubeListBuilder.create().texOffs(52, 23).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 6.0F, 1.0F), PartPose.offsetAndRotation(3.0F, 0.5F, 3.2F, r(8.0F), r(0.0F), r(0.0F)));
        return LayerDefinition.create(mesh, 64, 32);
    }

    public static LayerDefinition voidBoar() {
        MeshDefinition mesh = QuadrupedModel.createBodyMesh(6, CubeDeformation.NONE);
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -4.0F, -8.0F, 8.0F, 8.0F, 8.0F)
                .texOffs(16, 16).addBox(-2.0F, 0.0F, -9.0F, 4.0F, 3.0F, 1.0F), PartPose.offset(0.0F, 12.0F, -6.0F));
        root.getChild("head").addOrReplaceChild("tusk_a", CubeListBuilder.create().texOffs(32, 0).addBox(-0.5F, -0.5F, -1.5F, 1.0F, 1.0F, 3.0F), PartPose.offsetAndRotation(3.0F, 2.5F, -9.5F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("tusk_a_l", CubeListBuilder.create().texOffs(32, 0).mirror().addBox(-0.5F, -0.5F, -1.5F, 1.0F, 1.0F, 3.0F), PartPose.offsetAndRotation(-3.0F, 2.5F, -9.5F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("tusk_b", CubeListBuilder.create().texOffs(40, 0).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(3.0F, 2.2F, -11.0F, r(-15.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("tusk_b_l", CubeListBuilder.create().texOffs(40, 0).mirror().addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F), PartPose.offsetAndRotation(-3.0F, 2.2F, -11.0F, r(-15.0F), r(0.0F), r(0.0F)));
        root.getChild("head").addOrReplaceChild("crest", CubeListBuilder.create().texOffs(44, 0).addBox(-1.0F, -2.0F, -2.0F, 2.0F, 2.0F, 4.0F), PartPose.offsetAndRotation(0.0F, -3.8F, -4.0F, r(0.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("crystal_0", CubeListBuilder.create().texOffs(16, 20).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 4.0F), PartPose.offsetAndRotation(0.0F, -6.0F, 1.0F, r(-10.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("crystal_1", CubeListBuilder.create().texOffs(0, 26).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 3.0F), PartPose.offsetAndRotation(0.0F, -1.0F, 1.0F, r(10.0F), r(0.0F), r(0.0F)));
        root.getChild("body").addOrReplaceChild("crystal_2", CubeListBuilder.create().texOffs(10, 26).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 4.0F), PartPose.offsetAndRotation(0.0F, 4.0F, 1.0F, r(-10.0F), r(0.0F), r(0.0F)));
        return LayerDefinition.create(mesh, 64, 32);
    }

    private ModelExtras() {
    }
}
