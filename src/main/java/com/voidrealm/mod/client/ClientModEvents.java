package com.voidrealm.mod.client;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.registry.ModEntities;
import com.voidrealm.mod.entity.VoidSovereign;
import com.voidrealm.mod.entity.RiftBrute;
import com.voidrealm.mod.entity.PhaseStalker;
import com.voidrealm.mod.entity.VoidWalker;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Dang ky renderer phia client. */
@EventBusSubscriber(modid = VoidRealm.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientModEvents {

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(ModModelLayers.VOID_WALKER, ModelExtras::voidWalker);
        event.registerLayerDefinition(ModModelLayers.PHASE_STALKER, ModelExtras::phaseStalker);
        event.registerLayerDefinition(ModModelLayers.RIFT_BRUTE, ModelExtras::riftBrute);
        event.registerLayerDefinition(ModModelLayers.VOID_SOVEREIGN, ModelExtras::voidSovereign);
        event.registerLayerDefinition(ModModelLayers.RIFT_ARCHER, ModelExtras::riftArcher);
        event.registerLayerDefinition(ModModelLayers.VOID_BOAR, ModelExtras::voidBoar);
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(ModEntities.VOID_WALKER.get(),
                context -> new VoidHumanoidRenderer<VoidWalker>(context, ModModelLayers.VOID_WALKER, "void_walker", 1.0F, 0.5F));
        event.registerEntityRenderer(ModEntities.PHASE_STALKER.get(),
                context -> new VoidHumanoidRenderer<PhaseStalker>(context, ModModelLayers.PHASE_STALKER, "phase_stalker", 1.05F, 0.5F));
        event.registerEntityRenderer(ModEntities.RIFT_BRUTE.get(),
                context -> new VoidHumanoidRenderer<RiftBrute>(context, ModModelLayers.RIFT_BRUTE, "rift_brute", 1.4F, 0.9F));
        event.registerEntityRenderer(ModEntities.VOID_SOVEREIGN.get(),
                context -> new VoidHumanoidRenderer<VoidSovereign>(context, ModModelLayers.VOID_SOVEREIGN, "void_sovereign", 1.9F, 1.4F));
        event.registerEntityRenderer(ModEntities.RIFT_ARCHER.get(), RiftArcherRenderer::new);
        event.registerEntityRenderer(ModEntities.VOID_BOAR.get(), VoidBoarRenderer::new);
    }

    private ClientModEvents() {
    }
}
