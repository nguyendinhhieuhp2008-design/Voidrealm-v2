package com.voidrealm.mod.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.registry.ModItems;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;
import net.neoforged.neoforge.common.Tags;

/**
 * Mat Nhin Thuc Tai (phia client): khi cam item, quet quang trong ban kinh {@link #RADIUS}
 * moi giay mot lan va ve khung mau xuyen tuong quanh cac khoi quang.
 */
@EventBusSubscriber(modid = VoidRealm.MODID, value = Dist.CLIENT)
public class XrayClient {
    private static final int RADIUS = 10;
    private static final List<Entry> ORES = new ArrayList<>();

    private record Entry(BlockPos pos, float r, float g, float b) {
    }

    private static boolean holdingEye(LocalPlayer player) {
        return player.getMainHandItem().is(ModItems.EYE_OF_THE_VOID.get())
                || player.getOffhandItem().is(ModItems.EYE_OF_THE_VOID.get());
    }

    @SubscribeEvent
    public static void onClientTick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        ClientLevel level = mc.level;
        if (player == null || level == null || !holdingEye(player)) {
            if (!ORES.isEmpty()) {
                ORES.clear();
            }
            return;
        }
        if (player.tickCount % 20 != 0) {
            return;
        }
        List<Entry> found = new ArrayList<>();
        BlockPos center = player.blockPosition();
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        for (int dx = -RADIUS; dx <= RADIUS; dx++) {
            for (int dy = -RADIUS; dy <= RADIUS; dy++) {
                for (int dz = -RADIUS; dz <= RADIUS; dz++) {
                    cursor.set(center.getX() + dx, center.getY() + dy, center.getZ() + dz);
                    BlockState state = level.getBlockState(cursor);
                    if (state.isAir() || !state.is(Tags.Blocks.ORES)) {
                        continue;
                    }
                    found.add(colorFor(cursor.immutable(), BuiltInRegistries.BLOCK.getKey(state.getBlock()).getPath()));
                    if (found.size() >= 400) {
                        break;
                    }
                }
            }
        }
        ORES.clear();
        ORES.addAll(found);
    }

    private static Entry colorFor(BlockPos pos, String id) {
        if (id.contains("diamond")) {
            return new Entry(pos, 0.3F, 1.0F, 1.0F);
        } else if (id.contains("emerald")) {
            return new Entry(pos, 0.2F, 1.0F, 0.3F);
        } else if (id.contains("gold")) {
            return new Entry(pos, 1.0F, 0.85F, 0.1F);
        } else if (id.contains("iron")) {
            return new Entry(pos, 0.95F, 0.7F, 0.55F);
        } else if (id.contains("copper")) {
            return new Entry(pos, 1.0F, 0.5F, 0.2F);
        } else if (id.contains("redstone")) {
            return new Entry(pos, 1.0F, 0.15F, 0.15F);
        } else if (id.contains("lapis")) {
            return new Entry(pos, 0.2F, 0.3F, 1.0F);
        } else if (id.contains("coal")) {
            return new Entry(pos, 0.6F, 0.6F, 0.6F);
        } else if (id.contains("debris") || id.contains("netherite")) {
            return new Entry(pos, 0.8F, 0.4F, 0.2F);
        } else if (id.contains("void")) {
            return new Entry(pos, 0.8F, 0.4F, 1.0F);
        }
        return new Entry(pos, 1.0F, 1.0F, 1.0F);
    }

    @SubscribeEvent
    public static void onRender(RenderLevelStageEvent event) {
        if (event.getStage() != RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS || ORES.isEmpty()) {
            return;
        }
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null || !holdingEye(mc.player)) {
            return;
        }
        PoseStack pose = event.getPoseStack();
        Vec3 cam = event.getCamera().getPosition();
        MultiBufferSource.BufferSource buffers = mc.renderBuffers().bufferSource();
        VertexConsumer consumer = buffers.getBuffer(XrayTypes.BOX);
        pose.pushPose();
        pose.translate(-cam.x, -cam.y, -cam.z);
        for (Entry e : ORES) {
            LevelRenderer.renderLineBox(pose, consumer, new AABB(e.pos()).inflate(0.003D), e.r(), e.g(), e.b(), 0.95F);
        }
        pose.popPose();
        buffers.endBatch(XrayTypes.BOX);
    }

    private XrayClient() {
    }
}
