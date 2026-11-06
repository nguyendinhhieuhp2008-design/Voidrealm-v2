package com.voidrealm.mod.registry;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.entity.PhaseStalker;
import com.voidrealm.mod.entity.BlackHole;
import com.voidrealm.mod.entity.RiftArcher;
import com.voidrealm.mod.entity.VoidStalkerBird;
import com.voidrealm.mod.entity.VoidWisp;
import com.voidrealm.mod.entity.RiftBrute;
import com.voidrealm.mod.entity.VoidBoar;
import com.voidrealm.mod.entity.VoidSovereign;
import com.voidrealm.mod.entity.VoidWalker;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(Registries.ENTITY_TYPE, VoidRealm.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<VoidWalker>> VOID_WALKER = ENTITIES.register("void_walker",
            () -> EntityType.Builder.of(VoidWalker::new, MobCategory.MONSTER)
                    .sized(0.6F, 1.95F)
                    .clientTrackingRange(8)
                    .build("void_walker"));

    public static final DeferredHolder<EntityType<?>, EntityType<RiftArcher>> RIFT_ARCHER = ENTITIES.register("rift_archer",
            () -> EntityType.Builder.of(RiftArcher::new, MobCategory.MONSTER)
                    .sized(0.6F, 1.99F)
                    .clientTrackingRange(8)
                    .build("rift_archer"));

    public static final DeferredHolder<EntityType<?>, EntityType<PhaseStalker>> PHASE_STALKER = ENTITIES.register("phase_stalker",
            () -> EntityType.Builder.of(PhaseStalker::new, MobCategory.MONSTER)
                    .sized(0.6F, 2.1F)
                    .clientTrackingRange(8)
                    .build("phase_stalker"));

    public static final DeferredHolder<EntityType<?>, EntityType<VoidBoar>> VOID_BOAR = ENTITIES.register("void_boar",
            () -> EntityType.Builder.of(VoidBoar::new, MobCategory.MONSTER)
                    .sized(1.0F, 1.1F)
                    .clientTrackingRange(8)
                    .build("void_boar"));

    public static final DeferredHolder<EntityType<?>, EntityType<RiftBrute>> RIFT_BRUTE = ENTITIES.register("rift_brute",
            () -> EntityType.Builder.of(RiftBrute::new, MobCategory.MONSTER)
                    .sized(0.9F, 2.7F)
                    .clientTrackingRange(10)
                    .build("rift_brute"));

    public static final DeferredHolder<EntityType<?>, EntityType<VoidSovereign>> VOID_SOVEREIGN = ENTITIES.register("void_sovereign",
            () -> EntityType.Builder.of(VoidSovereign::new, MobCategory.MONSTER)
                    .sized(1.2F, 3.6F)
                    .fireImmune()
                    .clientTrackingRange(12)
                    .build("void_sovereign"));

    public static final DeferredHolder<EntityType<?>, EntityType<BlackHole>> BLACK_HOLE = ENTITIES.register("black_hole",
            () -> EntityType.Builder.<BlackHole>of(BlackHole::new, MobCategory.MISC)
                    .sized(0.5F, 0.5F)
                    .noSave()
                    .fireImmune()
                    .clientTrackingRange(10)
                    .updateInterval(10)
                    .build("black_hole"));

    public static final DeferredHolder<EntityType<?>, EntityType<VoidWisp>> VOID_WISP = ENTITIES.register("void_wisp",
            () -> EntityType.Builder.of(VoidWisp::new, MobCategory.CREATURE)
                    .sized(0.5F, 0.6F)
                    .fireImmune()
                    .clientTrackingRange(10)
                    .build("void_wisp"));

    public static final DeferredHolder<EntityType<?>, EntityType<VoidStalkerBird>> VOID_STALKER_BIRD = ENTITIES.register("void_stalker_bird",
            () -> EntityType.Builder.of(VoidStalkerBird::new, MobCategory.CREATURE)
                    .sized(1.1F, 1.3F)
                    .clientTrackingRange(10)
                    .build("void_stalker_bird"));

    private ModEntities() {
    }
}
