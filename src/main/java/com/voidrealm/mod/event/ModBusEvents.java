package com.voidrealm.mod.event;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.PhaseStalker;
import com.voidrealm.mod.entity.RiftArcher;
import com.voidrealm.mod.entity.RiftBrute;
import com.voidrealm.mod.entity.VoidBoar;
import com.voidrealm.mod.entity.VoidSovereign;
import com.voidrealm.mod.entity.VoidWalker;
import com.voidrealm.mod.registry.ModEntities;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.event.entity.RegisterSpawnPlacementsEvent;

/** Su kien o mod bus: thuoc tinh quai va dieu kien xuat hien. */
@EventBusSubscriber(modid = VoidRealm.MODID, bus = EventBusSubscriber.Bus.MOD)
public class ModBusEvents {

    @SubscribeEvent
    public static void onAttributes(EntityAttributeCreationEvent event) {
        event.put(ModEntities.VOID_WALKER.get(), VoidWalker.createAttributes().build());
        event.put(ModEntities.RIFT_ARCHER.get(), RiftArcher.createAttributes().build());
        event.put(ModEntities.PHASE_STALKER.get(), PhaseStalker.createAttributes().build());
        event.put(ModEntities.VOID_BOAR.get(), VoidBoar.createAttributes().build());
        event.put(ModEntities.RIFT_BRUTE.get(), RiftBrute.createAttributes().build());
        event.put(ModEntities.VOID_SOVEREIGN.get(), VoidSovereign.createAttributes().build());
    }

    @SubscribeEvent
    public static void onSpawnPlacements(RegisterSpawnPlacementsEvent event) {
        event.register(ModEntities.VOID_WALKER.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.OR);
        event.register(ModEntities.RIFT_ARCHER.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.OR);
        event.register(ModEntities.PHASE_STALKER.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.OR);
        event.register(ModEntities.VOID_BOAR.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.OR);
        event.register(ModEntities.RIFT_BRUTE.get(), SpawnPlacementTypes.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules,
                RegisterSpawnPlacementsEvent.Operation.OR);
    }

    private ModBusEvents() {
    }
}
