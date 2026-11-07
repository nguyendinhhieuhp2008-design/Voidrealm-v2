package com.voidrealm.mod.net;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.event.DreamAbilities;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

@EventBusSubscriber(modid = VoidRealm.MODID, bus = EventBusSubscriber.Bus.MOD)
public class NetEvents {
    @SubscribeEvent
    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar("1");
        registrar.playToServer(DreamActionPayload.TYPE, DreamActionPayload.CODEC, (payload, context) ->
                context.enqueueWork(() -> {
                    if (context.player() instanceof ServerPlayer player) {
                        if (payload.action() == 0) {
                            DreamAbilities.boost(player);
                        } else if (payload.action() == 1) {
                            DreamAbilities.tentacles(player);
                        }
                    }
                }));
    }

    private NetEvents() {
    }
}
