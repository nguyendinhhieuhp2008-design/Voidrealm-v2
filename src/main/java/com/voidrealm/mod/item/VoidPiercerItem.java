package com.voidrealm.mod.item;

import com.voidrealm.mod.effect.Fx;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.phys.Vec3;

/** Giao Xuyen Hu Khong: tam voi xa hon, danh trung de lai tia sang noi tu nguoi cam den muc tieu. */
public class VoidPiercerItem extends SwordItem {
    public VoidPiercerItem(Tier tier, Item.Properties properties) {
        super(tier, properties);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        if (target.level() instanceof ServerLevel level) {
            Vec3 from = attacker.getEyePosition().add(0.0D, -0.3D, 0.0D);
            Vec3 to = new Vec3(target.getX(), target.getY() + target.getBbHeight() * 0.5D, target.getZ());
            Fx.line(level, from, to, ParticleTypes.ELECTRIC_SPARK, 0.35D);
            Fx.burst(level, to.x, to.y, to.z, ParticleTypes.END_ROD, 8, 0.3D, 0.1D);
        }
        return super.hurtEnemy(stack, target, attacker);
    }
}
