package com.voidrealm.mod.item;

import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Mui Khoan Mong Tinh.
 * - Shift + chuot phai: bat/tat che do dao 3x3.
 * - Giu chuot phai (khong shift): tich luc ~1.5 giay roi nha ra tia nang luong pha huy khoi 3x3 xa 20 block.
 */
public class DreamDrillItem extends PickaxeItem {
    private static final int CHARGE_TICKS = 30;
    private static final int BEAM_LENGTH = 20;
    private static final DustParticleOptions BLUE = new DustParticleOptions(new Vector3f(0.2F, 0.55F, 1.0F), 1.6F);
    private static boolean breaking = false;

    public DreamDrillItem(Tier tier, Properties properties) {
        super(tier, properties);
    }

    public static boolean is3x3(ItemStack stack) {
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag().getBoolean("drill3x3");
    }

    private static void toggle(ItemStack stack, Player player) {
        boolean now = !is3x3(stack);
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putBoolean("drill3x3", now));
        player.displayClientMessage(Component.translatable(now ? "message.voidrealm.drill_on" : "message.voidrealm.drill_off"), true);
        player.level().playSound(null, player.blockPosition(), SoundEvents.UI_BUTTON_CLICK.value(), SoundSource.PLAYERS, 0.8F, now ? 1.6F : 0.8F);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Player player = context.getPlayer();
        if (player != null && player.isShiftKeyDown()) {
            if (!context.getLevel().isClientSide) {
                toggle(context.getItemInHand(), player);
            }
            return InteractionResult.sidedSuccess(context.getLevel().isClientSide);
        }
        return InteractionResult.PASS;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.isShiftKeyDown()) {
            if (!level.isClientSide) {
                toggle(stack, player);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.fail(stack);
        }
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(stack);
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BOW;
    }

    @Override
    public int getUseDuration(ItemStack stack, LivingEntity entity) {
        return 72000;
    }

    @Override
    public void onUseTick(Level level, LivingEntity entity, ItemStack stack, int remaining) {
        if (level.isClientSide || !(level instanceof ServerLevel sl)) {
            return;
        }
        int charge = getUseDuration(stack, entity) - remaining;
        Vec3 look = entity.getLookAngle();
        Vec3 tip = entity.getEyePosition().add(look.scale(1.2D)).add(0.0D, -0.3D, 0.0D);
        double r = 1.2D * Math.max(0.1D, 1.0D - Math.min(charge, CHARGE_TICKS) / (double) CHARGE_TICKS);
        for (int k = 0; k < 3; k++) {
            double a = charge * 0.5D + k * 2.094D;
            Vec3 u = look.cross(new Vec3(0.0D, 1.0D, 0.0D));
            if (u.lengthSqr() < 1.0E-4D) {
                u = new Vec3(1.0D, 0.0D, 0.0D);
            }
            u = u.normalize();
            Vec3 w = look.cross(u).normalize();
            Vec3 p = tip.add(u.scale(Math.cos(a) * r)).add(w.scale(Math.sin(a) * r));
            sl.sendParticles(BLUE, p.x, p.y, p.z, 1, 0.0D, 0.0D, 0.0D, 0.0D);
        }
        if (charge == CHARGE_TICKS) {
            sl.playSound(null, entity.blockPosition(), SoundEvents.BEACON_POWER_SELECT, SoundSource.PLAYERS, 1.2F, 1.5F);
            sl.sendParticles(ParticleTypes.END_ROD, tip.x, tip.y, tip.z, 12, 0.3D, 0.3D, 0.3D, 0.05D);
        }
    }

    @Override
    public void releaseUsing(ItemStack stack, Level level, LivingEntity entity, int timeLeft) {
        if (level.isClientSide || !(entity instanceof ServerPlayer player) || !(level instanceof ServerLevel sl)) {
            return;
        }
        int charge = getUseDuration(stack, entity) - timeLeft;
        if (charge < CHARGE_TICKS) {
            return;
        }
        fireBeam(sl, player, stack);
        player.getCooldowns().addCooldown(this, 100);
    }

    private void fireBeam(ServerLevel level, ServerPlayer player, ItemStack stack) {
        Vec3 eye = player.getEyePosition();
        Vec3 look = player.getLookAngle();
        Vec3 u = look.cross(new Vec3(0.0D, 1.0D, 0.0D));
        if (u.lengthSqr() < 1.0E-4D) {
            u = new Vec3(1.0D, 0.0D, 0.0D);
        }
        u = u.normalize();
        Vec3 w = look.cross(u).normalize();
        Set<BlockPos> done = new HashSet<>();
        int broken = 0;
        for (int i = 1; i <= BEAM_LENGTH; i++) {
            Vec3 center = eye.add(look.scale(i));
            level.sendParticles(BLUE, center.x, center.y, center.z, 6, 0.5D, 0.5D, 0.5D, 0.0D);
            level.sendParticles(ParticleTypes.END_ROD, center.x, center.y, center.z, 1, 0.3D, 0.3D, 0.3D, 0.01D);
            for (int a = -1; a <= 1; a++) {
                for (int b = -1; b <= 1; b++) {
                    BlockPos pos = BlockPos.containing(center.add(u.scale(a)).add(w.scale(b)));
                    if (!done.add(pos)) {
                        continue;
                    }
                    BlockState state = level.getBlockState(pos);
                    if (state.isAir() || state.getDestroySpeed(level, pos) < 0.0F || !state.getFluidState().isEmpty()) {
                        continue;
                    }
                    if (level.destroyBlock(pos, true, player)) {
                        broken++;
                    }
                }
            }
        }
        stack.hurtAndBreak(Math.min(60, 4 + broken / 3), player, EquipmentSlot.MAINHAND);
        level.playSound(null, player.blockPosition(), SoundEvents.WARDEN_SONIC_BOOM, SoundSource.PLAYERS, 1.0F, 1.4F);
        level.playSound(null, player.blockPosition(), SoundEvents.GENERIC_EXPLODE.value(), SoundSource.PLAYERS, 0.6F, 1.6F);
    }

    @Override
    public boolean onBlockStartBreak(ItemStack stack, BlockPos pos, Player player) {
        Level level = player.level();
        if (level.isClientSide || breaking || !is3x3(stack) || !(player instanceof ServerPlayer sp)) {
            return false;
        }
        BlockHitResult hit = getPlayerPOVHitResult(level, player, ClipContext.Fluid.NONE);
        Direction face = hit.getType() == HitResult.Type.BLOCK ? hit.getDirection() : player.getDirection();
        float centerHardness = level.getBlockState(pos).getDestroySpeed(level, pos);
        breaking = true;
        try {
            for (int a = -1; a <= 1; a++) {
                for (int b = -1; b <= 1; b++) {
                    if (a == 0 && b == 0) {
                        continue;
                    }
                    BlockPos np = switch (face.getAxis()) {
                        case X -> pos.offset(0, a, b);
                        case Y -> pos.offset(a, 0, b);
                        default -> pos.offset(a, b, 0);
                    };
                    BlockState state = level.getBlockState(np);
                    float hardness = state.getDestroySpeed(level, np);
                    if (state.isAir() || hardness < 0.0F || hardness > Math.max(centerHardness + 2.0F, 6.0F)) {
                        continue;
                    }
                    if (stack.isCorrectToolForDrops(state) || stack.getDestroySpeed(state) > 1.0F) {
                        sp.gameMode.destroyBlock(np);
                    }
                }
            }
        } finally {
            breaking = false;
        }
        return false;
    }
}
