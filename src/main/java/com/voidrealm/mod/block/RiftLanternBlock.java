package com.voidrealm.mod.block;

import com.voidrealm.mod.Config;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** Den Khe Nut: toa hat xoay quanh (chi hien thi o phia client). */
public class RiftLanternBlock extends Block {
    public RiftLanternBlock(Properties properties) {
        super(properties);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (Config.roll(random, 5)) {
            level.addParticle(ParticleTypes.REVERSE_PORTAL,
                    pos.getX() + 0.5D + (random.nextDouble() - 0.5D) * 1.4D,
                    pos.getY() + 0.5D + (random.nextDouble() - 0.5D) * 1.4D,
                    pos.getZ() + 0.5D + (random.nextDouble() - 0.5D) * 1.4D,
                    0.0D, 0.02D, 0.0D);
        }
        if (Config.roll(random, 14)) {
            level.addParticle(ParticleTypes.END_ROD,
                    pos.getX() + random.nextDouble(), pos.getY() + 1.0D, pos.getZ() + random.nextDouble(),
                    0.0D, 0.04D, 0.0D);
        }
    }
}
