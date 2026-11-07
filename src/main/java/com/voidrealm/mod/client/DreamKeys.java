package com.voidrealm.mod.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.net.DreamActionPayload;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import org.lwjgl.glfw.GLFW;

/** Phim C (tang toc) va K (xuc tu) cua bo giap Mong Tinh. Doi phim trong Controls > Void Realm. */
public class DreamKeys {
    public static final KeyMapping BOOST = new KeyMapping("key.voidrealm.boost", InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_C, "key.categories.voidrealm");
    public static final KeyMapping TENTACLE = new KeyMapping("key.voidrealm.tentacle", InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_K, "key.categories.voidrealm");

    @EventBusSubscriber(modid = VoidRealm.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static class ModBus {
        @SubscribeEvent
        public static void registerKeys(RegisterKeyMappingsEvent event) {
            event.register(BOOST);
            event.register(TENTACLE);
        }
    }

    @EventBusSubscriber(modid = VoidRealm.MODID, value = Dist.CLIENT)
    public static class GameBus {
        @SubscribeEvent
        public static void onTick(ClientTickEvent.Post event) {
            Minecraft mc = Minecraft.getInstance();
            if (mc.player == null) {
                return;
            }
            while (BOOST.consumeClick()) {
                PacketDistributor.sendToServer(new DreamActionPayload(0));
            }
            while (TENTACLE.consumeClick()) {
                PacketDistributor.sendToServer(new DreamActionPayload(1));
            }
        }
    }

    private DreamKeys() {
    }
}
