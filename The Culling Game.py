from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random

# Window dimensions
WIDTH = 1000
HEIGHT = 800

# Camera transition configuration
CAMERA_START_X = 0.0
CAMERA_START_Y = -330.0
CAMERA_START_Z = 205.0
CAMERA_TARGET_START_X = 0.0
CAMERA_TARGET_START_Y = 0.0
CAMERA_TARGET_START_Z = 82.0

INTRO_CAMERA_X = 0.0
INTRO_CAMERA_Y = 0.0
INTRO_CAMERA_Z = 620.0
INTRO_TARGET_X = 0.0
INTRO_TARGET_Y = 0.0
INTRO_TARGET_Z = 0.0
INTRO_TRANSITION_FRAMES = 120

# Camera variables (start from intro position, then transition to start position)
camera_x = INTRO_CAMERA_X
camera_y = INTRO_CAMERA_Y
camera_z = INTRO_CAMERA_Z
camera_target_x = INTRO_TARGET_X
camera_target_y = INTRO_TARGET_Y
camera_target_z = INTRO_TARGET_Z
intro_active = True
intro_frame = 0

# Player and enemy state
player_pos = (-170.0, 0.0)
player_angle_deg = 270.0
player_walk_phase = 0.0

punch_phase = 0
punch_progress = 0.0
PUNCH_STEP = 0.05
punch_damage_applied = False
PUNCH_RANGE = 95.0
PUNCH_ANGLE_RANGE = 120.0
ENEMY_HIT_KNOCKBACK = 20.0

enemy_pos = (170.0, 0.0)
enemy_punch_phase = 0
enemy_punch_progress = 0.0
enemy_raise_progress = 0.0
ENEMY_PUNCH_STEP = 0.01
ENEMY_RAISE_STEP = 0.02
ENEMY_HAND_FORWARD_EXT = 14.0
ENEMY_HAND_Z_SCALE = 0.6

ENEMY_BULLET_SPEED = 6.0
ENEMY_BULLET_COOLDOWN_FRAMES = 200
ENEMY_HIT_SHOOT_DELAY_FRAMES = 4
ENEMY_BULLET_RADIUS = 4.0
ENEMY_BULLET_HIT_RADIUS = 26.0
enemy_bullets = []
enemy_bullet_cooldown = 0
combat_started = False
PLAYER_MOVE_STEP = 6.0
ENEMY_CHASE_SPEED = 0.6
ENEMY_CHASE_STOP_DISTANCE = 90.0
PLAYER_ENEMY_MIN_DISTANCE = 90.0

# Flying phase state (starts after enemy loses 3 lives/segments)
enemy_flying = False
ENEMY_FLY_HEIGHT = 140.0
ENEMY_ORBIT_RADIUS = 150.0
ENEMY_ORBIT_SPEED = 0.02
enemy_orbit_angle = 0.0

# Assassin phase (starts after enemy loses 6 lives/segments)
ENEMY_ASSASSIN_TRIGGER_HEALTH = 40.0
enemy_assassin_mode = False
enemy_visible = True
enemy_respawn_timer = 0
ENEMY_RESPAWN_FRAMES = 70
ENEMY_ASSASSIN_SPEED = 0.45
ENEMY_SWORD_RANGE = 26.0
ENEMY_SWORD_STAB_FRAMES = 18
ENEMY_ASSASSIN_BODY_STOP_DISTANCE = PLAYER_ENEMY_MIN_DISTANCE
enemy_descending = False
enemy_descend_frame = 0
ENEMY_DESCEND_FRAMES = 24
enemy_stab_timer = 0

# Enemy fireball attack (used in flying phase)
FIREBALL_RADIUS = 8.0
FIREBALL_COOLDOWN_FRAMES = 350
FIREBALL_GRAVITY = 0.18
FIREBALL_AIM_HEIGHT = 160.0
enemy_fireballs = []
enemy_fireball_cooldown = FIREBALL_COOLDOWN_FRAMES

# Floor damage marks from fireball impacts
scorch_marks = []
SCORCH_RADIUS = 38.0

# Player inferno beam attack (replaces punch/shield)
inferno_active = False
INFERNO_BEAM_LENGTH = 420.0
INFERNO_HIT_RADIUS = 34.0
inferno_hit_cooldown = 0
INFERNO_HIT_COOLDOWN_FRAMES = 10
INFERNO_BURST_FRAMES = 12
inferno_frames_left = 0

# Player gun (used in assassin phase)
PLAYER_BULLET_SPEED = 10.0
PLAYER_BULLET_RADIUS = 4.0
PLAYER_BULLET_COOLDOWN_FRAMES = 8
player_bullets = []
player_bullet_cooldown = 0

# Player wound visuals from assassin sword hits
wound_patches = []
WOUND_PATCH_MAX = 12
WOUND_PATCH_LIFE_FRAMES = 420

PLAYER_MAX_HEALTH = 100.0
ENEMY_MAX_HEALTH = 100.0
HEALTH_BAR_SEGMENTS = 9
player_health = PLAYER_MAX_HEALTH
enemy_health = ENEMY_MAX_HEALTH

# Shield state
shield_active = False
shield_hold_time = 0
ENEMY_SHIELD_WAIT_FRAMES = 200
enemy_wait_timer = 0
SHIELD_DISTANCE = 15.0
SHIELD_WIDTH = 35.0
SHIELD_HEIGHT = 60.0
SHIELD_Z_BOTTOM = 60.0
SHIELD_Z_TOP = 160.0

# Collision radius for movement clamping
ARENA_RADIUS = 290.0


def reset_game_state():
    """Resets gameplay and camera values."""
    global camera_x, camera_y, camera_z
    global camera_target_x, camera_target_y, camera_target_z
    global player_pos, player_angle_deg, player_walk_phase
    global punch_phase, punch_progress, punch_damage_applied
    global enemy_pos, enemy_punch_phase, enemy_punch_progress, enemy_raise_progress
    global enemy_bullets, enemy_bullet_cooldown, combat_started
    global player_health, enemy_health
    global shield_active, shield_hold_time, enemy_wait_timer
    global intro_active, intro_frame
    global enemy_flying, enemy_orbit_angle
    global enemy_assassin_mode, enemy_visible, enemy_respawn_timer
    global enemy_descending, enemy_descend_frame
    global enemy_stab_timer
    global enemy_fireballs, enemy_fireball_cooldown
    global scorch_marks
    global inferno_active, inferno_hit_cooldown, inferno_frames_left
    global player_bullets, player_bullet_cooldown
    global wound_patches

    camera_x = INTRO_CAMERA_X
    camera_y = INTRO_CAMERA_Y
    camera_z = INTRO_CAMERA_Z
    camera_target_x = INTRO_TARGET_X
    camera_target_y = INTRO_TARGET_Y
    camera_target_z = INTRO_TARGET_Z
    intro_active = True
    intro_frame = 0

    player_pos = (-170.0, 0.0)
    player_angle_deg = 270.0
    player_walk_phase = 0.0

    punch_phase = 0
    punch_progress = 0.0
    punch_damage_applied = False

    enemy_pos = (170.0, 0.0)
    enemy_punch_phase = 0
    enemy_punch_progress = 0.0
    enemy_raise_progress = 0.0

    enemy_bullets = []
    enemy_bullet_cooldown = 0
    enemy_fireballs = []
    enemy_fireball_cooldown = FIREBALL_COOLDOWN_FRAMES
    scorch_marks = []
    player_bullets = []
    player_bullet_cooldown = 0
    combat_started = False

    enemy_flying = False
    enemy_orbit_angle = 0.0
    enemy_assassin_mode = False
    enemy_visible = True
    enemy_respawn_timer = 0
    enemy_descending = False
    enemy_descend_frame = 0
    enemy_stab_timer = 0

    player_health = PLAYER_MAX_HEALTH
    enemy_health = ENEMY_MAX_HEALTH

    shield_active = False
    shield_hold_time = 0
    enemy_wait_timer = 0
    inferno_active = False
    inferno_hit_cooldown = 0
    inferno_frames_left = 0
    wound_patches = []

def draw_shrine():
    """Draw the expanded tile/bone arena foundation"""

    # Very large tile field at base. Tiles inside scorch zones turn black.
    glPushMatrix()
    glTranslatef(0, 0, 1)

    normal_tile_color = (0.55, 0.45, 0.30)
    damaged_tile_color = (0.03, 0.03, 0.03)

    tile_half = 5.0
    glBegin(GL_QUADS)
    for i in range(-50, 51):
        for j in range(-50, 51):
            dist = (i * i + j * j) ** 0.5
            if dist < 50 and (i + j) % 2 == 0:
                tile_x = i * 12.0
                tile_y = j * 12.0

                damaged = False
                for mark in scorch_marks:
                    dx = tile_x - mark["x"]
                    dy = tile_y - mark["y"]
                    if (dx * dx + dy * dy) <= (mark["r"] * mark["r"]):
                        damaged = True
                        break

                if damaged:
                    glColor3f(damaged_tile_color[0], damaged_tile_color[1], damaged_tile_color[2])
                else:
                    glColor3f(normal_tile_color[0], normal_tile_color[1], normal_tile_color[2])

                glVertex3f(tile_x - tile_half, tile_y - tile_half, 0)
                glVertex3f(tile_x + tile_half, tile_y - tile_half, 0)
                glVertex3f(tile_x + tile_half, tile_y + tile_half, 0)
                glVertex3f(tile_x - tile_half, tile_y + tile_half, 0)
    glEnd()
    glPopMatrix()

def draw_decorations():
    """Decorations removed to keep only arena and gameplay actors."""
    return


def draw_box(x1, x2, y1, y2, z1, z2, color):
    """Draws a colored 3D box using 6 quad faces."""
    r, g, b = color
    b1 = (x1, y1, z1)
    b2 = (x2, y1, z1)
    b3 = (x2, y2, z1)
    b4 = (x1, y2, z1)
    t1 = (x1, y1, z2)
    t2 = (x2, y1, z2)
    t3 = (x2, y2, z2)
    t4 = (x1, y2, z2)

    faces = [
        ((b4, b3, t3, t4), 1.08),
        ((b2, b1, t1, t2), 0.86),
        ((b1, b4, t4, t1), 0.78),
        ((b3, b2, t2, t3), 0.92),
        ((t1, t4, t3, t2), 1.16),
        ((b4, b1, b2, b3), 0.72),
    ]

    cx, cy, cz = camera_x, camera_y, camera_z
    ordered = []
    for verts, shade in faces:
        mx = (verts[0][0] + verts[1][0] + verts[2][0] + verts[3][0]) * 0.25
        my = (verts[0][1] + verts[1][1] + verts[2][1] + verts[3][1]) * 0.25
        mz = (verts[0][2] + verts[1][2] + verts[2][2] + verts[3][2]) * 0.25
        dist2 = ((cx - mx) * (cx - mx)) + ((cy - my) * (cy - my)) + ((cz - mz) * (cz - mz))
        ordered.append((dist2, verts, shade))

    ordered.sort(key=lambda item: item[0], reverse=True)

    glBegin(GL_QUADS)
    for _, verts, shade in ordered:
        glColor3f(min(1.0, r * shade), min(1.0, g * shade), min(1.0, b * shade))
        glVertex3f(*verts[0])
        glVertex3f(*verts[1])
        glVertex3f(*verts[2])
        glVertex3f(*verts[3])
    glEnd()


def draw_rotated_box(x1, x2, y1, y2, z1, z2, color, origin_x, origin_y, angle_rad):
    """Draws a box rotated on XY plane around an origin."""
    r, g, b = color
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    def world_point(local_x, local_y, z_val):
        wx = origin_x + (local_x * cos_a) - (local_y * sin_a)
        wy = origin_y + (local_x * sin_a) + (local_y * cos_a)
        return (wx, wy, z_val)

    b1 = world_point(x1, y1, z1)
    b2 = world_point(x2, y1, z1)
    b3 = world_point(x2, y2, z1)
    b4 = world_point(x1, y2, z1)
    t1 = world_point(x1, y1, z2)
    t2 = world_point(x2, y1, z2)
    t3 = world_point(x2, y2, z2)
    t4 = world_point(x1, y2, z2)

    faces = [
        ((b4, b3, t3, t4), 1.08),
        ((b2, b1, t1, t2), 0.86),
        ((b1, b4, t4, t1), 0.78),
        ((b3, b2, t2, t3), 0.92),
        ((t1, t4, t3, t2), 1.16),
        ((b4, b1, b2, b3), 0.72),
    ]

    cx, cy, cz = camera_x, camera_y, camera_z
    ordered = []
    for verts, shade in faces:
        mx = (verts[0][0] + verts[1][0] + verts[2][0] + verts[3][0]) * 0.25
        my = (verts[0][1] + verts[1][1] + verts[2][1] + verts[3][1]) * 0.25
        mz = (verts[0][2] + verts[1][2] + verts[2][2] + verts[3][2]) * 0.25
        dist2 = ((cx - mx) * (cx - mx)) + ((cy - my) * (cy - my)) + ((cz - mz) * (cz - mz))
        ordered.append((dist2, verts, shade))

    ordered.sort(key=lambda item: item[0], reverse=True)

    glBegin(GL_QUADS)
    for _, verts, shade in ordered:
        glColor3f(min(1.0, r * shade), min(1.0, g * shade), min(1.0, b * shade))
        glVertex3f(*verts[0])
        glVertex3f(*verts[1])
        glVertex3f(*verts[2])
        glVertex3f(*verts[3])
    glEnd()


def draw_player():
    """Draws the player character."""
    player_x, player_y = player_pos
    angle_rad = math.radians(player_angle_deg)
    leg_swing = 10.0 * math.sin(player_walk_phase)
    left_leg_shift = -leg_swing
    right_leg_shift = leg_swing

    def lerp(start, end, t):
        return start + ((end - start) * t)

    player_hand_forward_ext = 14.0
    player_hand_z_scale = 0.6

    def scale_hand_z(z1, z2):
        center = (z1 + z2) * 0.5
        half = (z2 - z1) * 0.5 * player_hand_z_scale
        return center - half, center + half

    left_hand_x1, left_hand_x2 = -30, -12
    left_hand_y1, left_hand_y2 = -8, 8
    left_hand_z1, left_hand_z2 = 80, 120

    right_hand_x1, right_hand_x2 = 12, 30
    right_hand_y1, right_hand_y2 = -8, 8
    right_hand_z1, right_hand_z2 = 80, 120

    hands_up = shield_active or inferno_active

    if not hands_up:
        if punch_phase == 1:
            right_hand_y1 = lerp(-8, 2, punch_progress)
            right_hand_y2 = lerp(8, 22, punch_progress)
            right_hand_z1 = lerp(80, 88, punch_progress)
            right_hand_z2 = lerp(120, 108, punch_progress)
        elif punch_phase == 2:
            right_hand_y1, right_hand_y2 = 2, 22
            right_hand_z1 = lerp(88, 100, punch_progress)
            right_hand_z2 = lerp(108, 120, punch_progress)
        elif punch_phase == 3:
            right_hand_y1, right_hand_y2 = 2, 22
            right_hand_z1 = lerp(100, 84, punch_progress)
            right_hand_z2 = lerp(120, 104, punch_progress)
        elif punch_phase == 4:
            right_hand_y1 = lerp(2, -8, punch_progress)
            right_hand_y2 = lerp(22, 8, punch_progress)
            right_hand_z1 = lerp(84, 80, punch_progress)
            right_hand_z2 = lerp(104, 120, punch_progress)

        left_hand_y2 += player_hand_forward_ext
        right_hand_y2 += player_hand_forward_ext

        left_hand_z1, left_hand_z2 = scale_hand_z(left_hand_z1, left_hand_z2)
        right_hand_z1, right_hand_z2 = scale_hand_z(right_hand_z1, right_hand_z2)
    else:
        left_hand_x1, left_hand_x2 = -26, -8
        right_hand_x1, right_hand_x2 = 8, 26
        left_hand_y1, left_hand_y2 = 6, 24
        right_hand_y1, right_hand_y2 = 6, 24
        left_hand_z1, left_hand_z2 = 110, 122
        right_hand_z1, right_hand_z2 = 110, 122

    def pbox(x1, x2, y1, y2, z1, z2, color):
        draw_rotated_box(x1, x2, y1, y2, z1, z2, color, player_x, player_y, angle_rad)

    body_color = (0.25, 0.25, 0.25)
    leg_color = (0.1, 0.0, 0.0)
    shoe_color = (0.85, 0.1, 0.1)
    skin_color = (1.0, 0.82, 0.67)
    eye_color = (0.0, 0.0, 0.0)
    hair_color = (0.82, 0.56, 0.68)

    pbox(-20, 20, -10, 10, 70, 130, body_color)

    # Wound patches from enemy sword cuts (persist for a while).
    for patch in wound_patches:
        pbox(patch["x1"], patch["x2"], patch["y1"], patch["y2"], patch["z1"], patch["z2"], (0.75, 0.0, 0.0))

    pbox(-18, -2, -8 + left_leg_shift, 8 + left_leg_shift, 20, 70, leg_color)
    pbox(2, 18, -8 + right_leg_shift, 8 + right_leg_shift, 20, 70, leg_color)
    pbox(left_hand_x1, left_hand_x2, left_hand_y1, left_hand_y2, left_hand_z1, left_hand_z2, body_color)
    pbox(right_hand_x1, right_hand_x2, right_hand_y1, right_hand_y2, right_hand_z1, right_hand_z2, body_color)

    # Fists at hand tips
    fist_half_w = 4.0
    fist_depth = 6.0
    fist_z_pad = 4.0
    left_fist_xc = (left_hand_x1 + left_hand_x2) * 0.5
    right_fist_xc = (right_hand_x1 + right_hand_x2) * 0.5
    pbox(
        left_fist_xc - fist_half_w, left_fist_xc + fist_half_w,
        left_hand_y2, left_hand_y2 + fist_depth,
        left_hand_z1 + fist_z_pad, left_hand_z2 - fist_z_pad,
        skin_color,
    )
    pbox(
        right_fist_xc - fist_half_w, right_fist_xc + fist_half_w,
        right_hand_y2, right_hand_y2 + fist_depth,
        right_hand_z1 + fist_z_pad, right_hand_z2 - fist_z_pad,
        skin_color,
    )

    if enemy_assassin_mode:
        # Player gun in assassin phase.
        pbox(12, 30, right_hand_y2 + 4, right_hand_y2 + 24, right_hand_z1 + 4, right_hand_z1 + 14, (0.3, 0.3, 0.3))

    pbox(-22, -4, -12 + left_leg_shift, 12 + left_leg_shift, 10, 20, shoe_color)
    pbox(4, 22, -12 + right_leg_shift, 12 + right_leg_shift, 10, 20, shoe_color)
    pbox(-13, 13, -10, 10, 128, 141, shoe_color)
    pbox(-18, 18, -12, 12, 140, 176, skin_color)
    pbox(-19, 19, -12, 12, 176, 184, hair_color)
    pbox(-8, -4, 12, 14, 158, 163, eye_color)
    pbox(4, 8, 12, 14, 158, 163, eye_color)


def draw_shield():
    """Draws a transparent shield in front of the player."""
    if (not shield_active) or enemy_flying:
        return

    player_x, player_y = player_pos
    player_angle_rad = math.radians(player_angle_deg)

    shield_x = player_x - math.sin(player_angle_rad) * SHIELD_DISTANCE
    shield_y = player_y + math.cos(player_angle_rad) * SHIELD_DISTANCE

    glColor3f(0.3, 0.7, 1.0)

    segments = 32
    shield_rotation = player_angle_rad + (math.pi / 2.0)

    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        angle = (math.pi * i) / segments - (math.pi / 2.0)
        local_x = SHIELD_WIDTH * math.cos(angle)
        local_y = SHIELD_HEIGHT * math.sin(angle)

        rotated_x = local_x * math.cos(shield_rotation) - local_y * math.sin(shield_rotation)
        rotated_y = local_x * math.sin(shield_rotation) + local_y * math.cos(shield_rotation)

        x = shield_x + rotated_x
        y = shield_y + rotated_y

        glVertex3f(x, y, SHIELD_Z_BOTTOM)
        glVertex3f(x, y, SHIELD_Z_TOP)
    glEnd()


def compute_enemy_right_hand_pose():
    """Computes enemy punch hand and muzzle position in local space."""
    right_hand_y1, right_hand_y2 = -8, 8
    right_hand_z1, right_hand_z2 = 80, 120
    right_hand_x1, right_hand_x2 = 12, 30

    def lerp(start, end, t):
        return start + ((end - start) * t)

    if enemy_punch_phase == 0:
        raise_y1, raise_y2 = 14, 34
        raise_z1, raise_z2 = 88, 122
        right_hand_y1 = lerp(right_hand_y1, raise_y1, enemy_raise_progress)
        right_hand_y2 = lerp(right_hand_y2, raise_y2, enemy_raise_progress)
        right_hand_z1 = lerp(right_hand_z1, raise_z1, enemy_raise_progress)
        right_hand_z2 = lerp(right_hand_z2, raise_z2, enemy_raise_progress)
    elif enemy_punch_phase == 1:
        right_hand_y1 = lerp(-8, 2, enemy_punch_progress)
        right_hand_y2 = lerp(8, 22, enemy_punch_progress)
        right_hand_z1 = lerp(80, 88, enemy_punch_progress)
        right_hand_z2 = lerp(120, 108, enemy_punch_progress)
    elif enemy_punch_phase == 2:
        right_hand_y1, right_hand_y2 = 2, 22
        right_hand_z1 = lerp(88, 100, enemy_punch_progress)
        right_hand_z2 = lerp(108, 120, enemy_punch_progress)
    elif enemy_punch_phase == 3:
        right_hand_y1, right_hand_y2 = 2, 22
        right_hand_z1 = lerp(100, 84, enemy_punch_progress)
        right_hand_z2 = lerp(120, 104, enemy_punch_progress)
    elif enemy_punch_phase == 4:
        right_hand_y1 = lerp(2, -8, enemy_punch_progress)
        right_hand_y2 = lerp(22, 8, enemy_punch_progress)
        right_hand_z1 = lerp(84, 80, enemy_punch_progress)
        right_hand_z2 = lerp(104, 120, enemy_punch_progress)

    right_hand_y2 += ENEMY_HAND_FORWARD_EXT

    center = (right_hand_z1 + right_hand_z2) * 0.5
    half = (right_hand_z2 - right_hand_z1) * 0.5 * ENEMY_HAND_Z_SCALE
    right_hand_z1 = center - half
    right_hand_z2 = center + half

    hand_z_span = right_hand_z2 - right_hand_z1
    muzzle_x1 = right_hand_x1 + 2
    muzzle_x2 = right_hand_x1 + 16
    muzzle_y1 = right_hand_y2 - 4.0
    muzzle_y2 = right_hand_y2 + 18.0
    muzzle_z1 = right_hand_z1 + hand_z_span * 0.25
    muzzle_z2 = right_hand_z1 + hand_z_span * 0.7

    return (
        right_hand_x1, right_hand_x2,
        right_hand_y1, right_hand_y2,
        right_hand_z1, right_hand_z2,
        muzzle_x1, muzzle_x2,
        muzzle_y1, muzzle_y2,
        muzzle_z1, muzzle_z2,
    )


def compute_enemy_muzzle_world():
    """Returns muzzle world position and bullet direction toward player."""
    enemy_x, enemy_y = enemy_pos
    player_x, player_y = player_pos
    enemy_angle_rad = math.atan2(-(player_x - enemy_x), (player_y - enemy_y))

    (
        _, _,
        _, _,
        _, _,
        muzzle_x1, muzzle_x2,
        muzzle_y1, muzzle_y2,
        muzzle_z1, muzzle_z2,
    ) = compute_enemy_right_hand_pose()

    local_x = (muzzle_x1 + muzzle_x2) * 0.5
    local_y = (muzzle_y1 + muzzle_y2) * 0.5
    local_z = (muzzle_z1 + muzzle_z2) * 0.5

    cos_a = math.cos(enemy_angle_rad)
    sin_a = math.sin(enemy_angle_rad)
    world_x = enemy_x + (local_x * cos_a) - (local_y * sin_a)
    world_y = enemy_y + (local_x * sin_a) + (local_y * cos_a)

    dir_x = player_x - enemy_x
    dir_y = player_y - enemy_y
    dir_len = math.sqrt((dir_x * dir_x) + (dir_y * dir_y))
    if dir_len > 0.0001:
        dir_x /= dir_len
        dir_y /= dir_len
    else:
        dir_x, dir_y = 0.0, 1.0

    return world_x, world_y, local_z, dir_x, dir_y


def draw_enemy():
    """Draws the enemy character."""
    if enemy_assassin_mode and not enemy_visible:
        return

    enemy_x, enemy_y = enemy_pos
    player_x, player_y = player_pos
    enemy_angle_rad = math.atan2(-(player_x - enemy_x), (player_y - enemy_y))

    if enemy_flying:
        enemy_z_offset = ENEMY_FLY_HEIGHT
    elif enemy_descending:
        t = min(1.0, enemy_descend_frame / float(ENEMY_DESCEND_FRAMES))
        enemy_z_offset = ENEMY_FLY_HEIGHT * (1.0 - t)
    else:
        enemy_z_offset = 0.0

    def ebox(x1, x2, y1, y2, z1, z2, color):
        draw_rotated_box(x1, x2, y1, y2, z1 + enemy_z_offset, z2 + enemy_z_offset, color, enemy_x, enemy_y, enemy_angle_rad)

    body_color = (0.05, 0.05, 0.05)
    pants_color = (0.1, 0.0, 0.0)
    shoe_color = (0.6, 0.6, 0.6)
    skin_color = (1.0, 0.82, 0.67)
    hand_color = body_color
    hair_color = (0.55, 0.2, 0.65)
    eye_color = (0.0, 0.0, 0.0)
    metal_color = (0.28, 0.28, 0.28)

    def scale_hand_z(z1, z2):
        center = (z1 + z2) * 0.5
        half = (z2 - z1) * 0.5 * ENEMY_HAND_Z_SCALE
        return center - half, center + half

    left_hand_y1, left_hand_y2 = -8, 8 + ENEMY_HAND_FORWARD_EXT
    left_hand_z1, left_hand_z2 = 80, 120
    left_hand_z1, left_hand_z2 = scale_hand_z(left_hand_z1, left_hand_z2)

    (
        right_hand_x1, right_hand_x2,
        right_hand_y1, right_hand_y2,
        right_hand_z1, right_hand_z2,
        muzzle_x1, muzzle_x2,
        muzzle_y1, muzzle_y2,
        muzzle_z1, muzzle_z2,
    ) = compute_enemy_right_hand_pose()

    ebox(-20, 20, -10, 10, 70, 130, body_color)
    ebox(-18, -2, -8, 8, 20, 70, pants_color)
    ebox(2, 18, -8, 8, 20, 70, pants_color)
    ebox(-38, -20, left_hand_y1, left_hand_y2, left_hand_z1, left_hand_z2, hand_color)
    ebox(right_hand_x1, right_hand_x2, right_hand_y1, right_hand_y2, right_hand_z1, right_hand_z2, hand_color)

    # Fists at hand tips
    fist_half_w = 4.0
    fist_depth = 6.0
    fist_z_pad = 4.0
    left_fist_xc = (-38 + -20) * 0.5
    right_fist_xc = (right_hand_x1 + right_hand_x2) * 0.5
    ebox(
        left_fist_xc - fist_half_w, left_fist_xc + fist_half_w,
        left_hand_y2, left_hand_y2 + fist_depth,
        left_hand_z1 + fist_z_pad, left_hand_z2 - fist_z_pad,
        skin_color,
    )
    ebox(
        right_fist_xc - fist_half_w, right_fist_xc + fist_half_w,
        right_hand_y2, right_hand_y2 + fist_depth,
        right_hand_z1 + fist_z_pad, right_hand_z2 - fist_z_pad,
        skin_color,
    )

    if (not enemy_flying) and (not enemy_assassin_mode) and (not enemy_descending):
        ebox(muzzle_x1, muzzle_x2, muzzle_y1, muzzle_y2, muzzle_z1, muzzle_z2, metal_color)

    if enemy_assassin_mode and not enemy_descending:
        # Silver sword in assassin mode.
        sword_x1 = right_hand_x1 + 4.0
        sword_x2 = right_hand_x1 + 10.0
        sword_y1 = right_hand_y2 - 2.0
        sword_y2 = right_hand_y2 + 34.0
        sword_z1 = right_hand_z1 + 5.0
        sword_z2 = right_hand_z1 + 14.0
        ebox(sword_x1, sword_x2, sword_y1, sword_y2, sword_z1, sword_z2, (0.75, 0.75, 0.8))
    ebox(-22, -4, -12, 12, 10, 20, shoe_color)
    ebox(4, 22, -12, 12, 10, 20, shoe_color)
    ebox(-13, 13, -10, 10, 128, 141, body_color)
    ebox(-18, 18, -12, 12, 140, 176, skin_color)
    ebox(-8, -4, 12, 14, 158, 163, eye_color)
    ebox(4, 8, 12, 14, 158, 163, eye_color)
    ebox(-19, 19, -12, 12, 176, 184, hair_color)


def draw_enemy_bullets():
    """Draws all enemy bullets."""
    if not enemy_bullets:
        return

    bullet_color = (0.2, 0.2, 0.2)
    radius = ENEMY_BULLET_RADIUS
    for bullet in enemy_bullets:
        x, y, z = bullet["pos"]
        draw_box(x - radius, x + radius, y - radius, y + radius, z - radius, z + radius, bullet_color)


def draw_player_bullets():
    """Draws player gun bullets in assassin phase."""
    if not player_bullets:
        return

    for bullet in player_bullets:
        x, y, z = bullet["pos"]
        r = PLAYER_BULLET_RADIUS
        draw_box(x - r, x + r, y - r, y + r, z - r, z + r, (1.0, 0.6, 0.15))


def draw_enemy_fireballs():
    """Draws enemy fireballs in flying phase."""
    if not enemy_fireballs:
        return

    for fireball in enemy_fireballs:
        x, y, z = fireball["pos"]
        r = FIREBALL_RADIUS
        draw_box(x - r, x + r, y - r, y + r, z - r, z + r, (1.0, 0.35, 0.0))


def draw_scorch_marks():
    """Draws dark damaged floor areas where fireballs landed."""
    if not scorch_marks:
        return

    for mark in scorch_marks:
        cx = mark["x"]
        cy = mark["y"]
        radius = mark["r"]
        draw_box(cx - radius, cx + radius, cy - radius, cy + radius, 1.1, 1.6, (0.03, 0.03, 0.03))


def compute_player_fist_world_positions_for_inferno():
    """Returns world positions for left/right fists while inferno pose is active."""
    player_x, player_y = player_pos
    angle_rad = math.radians(player_angle_deg)

    # Match raised-hands pose from draw_player inferno branch.
    left_x1, left_x2 = -26.0, -8.0
    right_x1, right_x2 = 8.0, 26.0
    left_y2 = 24.0
    right_y2 = 24.0
    left_z1, left_z2 = 110.0, 122.0
    right_z1, right_z2 = 110.0, 122.0

    left_local_x = (left_x1 + left_x2) * 0.5
    right_local_x = (right_x1 + right_x2) * 0.5
    left_local_y = left_y2 + 6.0
    right_local_y = right_y2 + 6.0
    left_local_z = (left_z1 + left_z2) * 0.5
    right_local_z = (right_z1 + right_z2) * 0.5

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    left_world_x = player_x + (left_local_x * cos_a) - (left_local_y * sin_a)
    left_world_y = player_y + (left_local_x * sin_a) + (left_local_y * cos_a)
    right_world_x = player_x + (right_local_x * cos_a) - (right_local_y * sin_a)
    right_world_y = player_y + (right_local_x * sin_a) + (right_local_y * cos_a)

    return (
        (left_world_x, left_world_y, left_local_z),
        (right_world_x, right_world_y, right_local_z),
        angle_rad,
    )


def respawn_enemy_around_player():
    """Places enemy at a random point around player within arena bounds."""
    px, py = player_pos
    for _ in range(20):
        a = random.uniform(0.0, 2.0 * math.pi)
        radius = random.uniform(210.0, 280.0)
        ex = px + (math.cos(a) * radius)
        ey = py + (math.sin(a) * radius)
        dist_center = math.sqrt((ex * ex) + (ey * ey))
        max_dist = ARENA_RADIUS - 12.0
        if dist_center <= max_dist:
            return (ex, ey)

    # Fallback clamp
    a = random.uniform(0.0, 2.0 * math.pi)
    max_dist = ARENA_RADIUS - 12.0
    return (math.cos(a) * max_dist, math.sin(a) * max_dist)


def spawn_player_bullet():
    """Spawns one player gun bullet from right hand in current facing direction."""
    (left_fist, right_fist, angle_rad) = compute_player_fist_world_positions_for_inferno()
    sx, sy, sz = right_fist
    dir_x = -math.sin(angle_rad)
    dir_y = math.cos(angle_rad)

    player_bullets.append({
        "pos": [sx, sy, sz],
        "vel": [dir_x * PLAYER_BULLET_SPEED, dir_y * PLAYER_BULLET_SPEED],
    })


def add_player_wound_patch_from_enemy():
    """Adds a small red wound patch on the side of player's torso facing the enemy."""
    px, py = player_pos
    ex, ey = enemy_pos
    angle_rad = math.radians(player_angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # Convert enemy direction to player's local space to place patch on hit side.
    vx = ex - px
    vy = ey - py
    local_x = (vx * cos_a) + (vy * sin_a)
    local_y = (-vx * sin_a) + (vy * cos_a)

    cx = max(-14.0, min(14.0, local_x * 0.2))
    cy = max(-8.0, min(8.0, local_y * 0.2))
    cz = random.uniform(88.0, 118.0)
    half = random.uniform(2.4, 3.8)

    wound_patches.append({
        "x1": cx - half,
        "x2": cx + half,
        "y1": cy - half,
        "y2": cy + half,
        "z1": cz - 1.3,
        "z2": cz + 1.3,
        "life": WOUND_PATCH_LIFE_FRAMES,
    })
    if len(wound_patches) > WOUND_PATCH_MAX:
        del wound_patches[0:len(wound_patches) - WOUND_PATCH_MAX]


def draw_inferno_beams():
    """Draws dual inferno beams from player's fists at a 45-degree upward angle."""
    if not inferno_active:
        return

    (left_fist, right_fist, angle_rad) = compute_player_fist_world_positions_for_inferno()
    fwd_x = -math.sin(angle_rad)
    fwd_y = math.cos(angle_rad)

    # 45-degree direction: equal forward and upward components.
    dir_x = fwd_x * 0.7071
    dir_y = fwd_y * 0.7071
    dir_z = 0.7071

    beam_color = (1.0, 0.45, 0.05)
    sx, sy, sz = right_fist
    ex = sx + (dir_x * INFERNO_BEAM_LENGTH)
    ey = sy + (dir_y * INFERNO_BEAM_LENGTH)
    ez = sz + (dir_z * INFERNO_BEAM_LENGTH)
    draw_thick_line_3d(sx, sy, sz, ex, ey, ez, 4.0, beam_color)


def draw_health_bars():
    """Draws player and enemy health bars as 9 segments at fixed top screen corners."""
    player_ratio = 0.0
    enemy_ratio = 0.0
    if PLAYER_MAX_HEALTH > 0:
        player_ratio = max(0.0, min(1.0, player_health / PLAYER_MAX_HEALTH))
    if ENEMY_MAX_HEALTH > 0:
        enemy_ratio = max(0.0, min(1.0, enemy_health / ENEMY_MAX_HEALTH))

    # Calculate filled segments.
    num_segments = HEALTH_BAR_SEGMENTS
    player_filled = int(player_ratio * num_segments)
    enemy_filled = int(enemy_ratio * num_segments)

    margin_x = 18.0
    margin_top = 18.0
    segment_width = 16.0
    segment_height = 14.0
    gap = 1.0
    frame = 3.0
    num_segments = HEALTH_BAR_SEGMENTS

    def draw_rect_2d(x, y, w, h, color):
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_QUADS)
        glVertex3f(x, y, 0)
        glVertex3f(x + w, y, 0)
        glVertex3f(x + w, y + h, 0)
        glVertex3f(x, y + h, 0)
        glEnd()

    def text_width(text, font):
        # Approximate width to avoid GLUT width helper not used in intro file.
        return len(text) * 10

    def draw_text_2d(x, y, text, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_18):
        glColor3f(color[0], color[1], color[2])
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ord(ch))

    # Calculate total bar width for 9 segments
    total_bar_width = (segment_width * num_segments) + (gap * (num_segments - 1))
    
    left_x = margin_x
    top_y = HEIGHT - margin_top
    right_x = WIDTH - margin_x - total_bar_width

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()



    # Draw player health segments (top-left)
    for i in range(num_segments):
        seg_x = left_x + (i * (segment_width + gap))
        if i < player_filled:
            # Filled segment - blue
            draw_rect_2d(seg_x, top_y - segment_height, segment_width, segment_height, (0.2, 0.45, 1.0))
        else:
            # Empty segment - dark
            draw_rect_2d(seg_x, top_y - segment_height, segment_width, segment_height, (0.1, 0.1, 0.1))
        # Draw segment border - light gray
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINE_LOOP)
        glVertex3f(seg_x, top_y - segment_height, 0)
        glVertex3f(seg_x + segment_width, top_y - segment_height, 0)
        glVertex3f(seg_x + segment_width, top_y, 0)
        glVertex3f(seg_x, top_y, 0)
        glEnd()

    # Draw enemy health segments (top-right)
    for i in range(num_segments):
        seg_x = right_x + (i * (segment_width + gap))
        if i < enemy_filled:
            # Filled segment - red
            draw_rect_2d(seg_x, top_y - segment_height, segment_width, segment_height, (1.0, 0.0, 0.0))
        else:
            # Empty segment - dark
            draw_rect_2d(seg_x, top_y - segment_height, segment_width, segment_height, (0.1, 0.1, 0.1))
        # Draw segment border - light gray
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINE_LOOP)
        glVertex3f(seg_x, top_y - segment_height, 0)
        glVertex3f(seg_x + segment_width, top_y - segment_height, 0)
        glVertex3f(seg_x + segment_width, top_y, 0)
        glVertex3f(seg_x, top_y, 0)
        glEnd()

    player_title = "Itadori Yuji"
    enemy_title = "Kenjaku"
    title_y = top_y - segment_height - 24.0

    player_title_x = left_x + ((total_bar_width - text_width(player_title, GLUT_BITMAP_HELVETICA_18)) * 0.5)
    enemy_title_x = right_x + ((total_bar_width - text_width(enemy_title, GLUT_BITMAP_HELVETICA_18)) * 0.5)

    draw_text_2d(player_title_x, title_y, player_title)
    draw_text_2d(enemy_title_x, title_y, enemy_title)

    # Top overlay text for game state
    status_y = top_y - segment_height - 52.0
    if player_health <= 0.0:
        defeat_text = "Defeated! Press R to restart."
        defeat_w = text_width(defeat_text, GLUT_BITMAP_HELVETICA_18)
        draw_text_2d((WIDTH - defeat_w) * 0.5, status_y, defeat_text, color=(1.0, 0.45, 0.45))
    elif enemy_health <= 0.0:
        winner_text = "Winner! Press R to restart."
        winner_w = text_width(winner_text, GLUT_BITMAP_HELVETICA_18)
        draw_text_2d((WIDTH - winner_w) * 0.5, status_y, winner_text, color=(0.45, 1.0, 0.45))
    elif not combat_started:
        start_text = "Press SPACE to Start"
        start_text_width = text_width(start_text, GLUT_BITMAP_HELVETICA_18)
        start_x = (WIDTH - start_text_width) * 0.5
        draw_text_2d(start_x, status_y, start_text, color=(1.0, 1.0, 0.0))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_thick_line_3d(x1, y1, z1, x2, y2, z2, width, color):
    """Draws a screen-plane thick line as a small quad strip replacement."""
    dx = x2 - x1
    dy = y2 - y1
    line_len = math.sqrt((dx * dx) + (dy * dy))
    if line_len <= 0.0001:
        return

    nx = -dy / line_len
    ny = dx / line_len
    half_w = width * 0.5

    ox = nx * half_w
    oy = ny * half_w

    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex3f(x1 - ox, y1 - oy, z1)
    glVertex3f(x1 + ox, y1 + oy, z1)
    glVertex3f(x2 + ox, y2 + oy, z2)
    glVertex3f(x2 - ox, y2 - oy, z2)
    glEnd()


def setupCamera():
    """Configures camera projection and view."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, WIDTH / float(HEIGHT), 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

    gluLookAt(
        camera_x, camera_y, camera_z,
        camera_target_x, camera_target_y, camera_target_z,
        0, 0, 1
    )

def specialKeyListener(key, x, y):
    """
    Handles arrow keys: left/right rotate view, up/down zoom.
    """
    global camera_x, camera_y, camera_z
    global camera_target_x, camera_target_y, camera_target_z
    global intro_active

    if intro_active:
        return

    zoom_step = 25.0
    turn_step = math.radians(4.0)

    dir_x = camera_target_x - camera_x
    dir_y = camera_target_y - camera_y
    dir_z = camera_target_z - camera_z
    dir_len = math.sqrt((dir_x * dir_x) + (dir_y * dir_y) + (dir_z * dir_z))
    if dir_len > 0.0001:
        dir_x /= dir_len
        dir_y /= dir_len
        dir_z /= dir_len
    
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        orbit_x = camera_x - camera_target_x
        orbit_y = camera_y - camera_target_y
        orbit_len = math.sqrt((orbit_x * orbit_x) + (orbit_y * orbit_y))

        if orbit_len > 0.0001:
            angle = turn_step if key == GLUT_KEY_LEFT else -turn_step
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            new_orbit_x = (orbit_x * cos_a) - (orbit_y * sin_a)
            new_orbit_y = (orbit_x * sin_a) + (orbit_y * cos_a)
            camera_x = camera_target_x + new_orbit_x
            camera_y = camera_target_y + new_orbit_y
    elif key == GLUT_KEY_UP and dir_len > 0.0001:
        camera_x += dir_x * zoom_step
        camera_y += dir_y * zoom_step
        camera_z += dir_z * zoom_step
    elif key == GLUT_KEY_DOWN and dir_len > 0.0001:
        camera_x -= dir_x * zoom_step
        camera_y -= dir_y * zoom_step
        camera_z -= dir_z * zoom_step

def keyboardListener(key, x, y):
    """
    Handles camera and player movement controls
    """
    global camera_x, camera_y, camera_z
    global camera_target_x, camera_target_y, camera_target_z
    global player_pos, player_angle_deg, player_walk_phase, combat_started
    global player_health, enemy_health
    global intro_active, enemy_assassin_mode

    cam_x, cam_y, cam_z = camera_x, camera_y, camera_z
    target_x, target_y, target_z = camera_target_x, camera_target_y, camera_target_z
    player_x, player_y = player_pos
    player_angle = player_angle_deg
    walk_phase = player_walk_phase

    player_move_step = PLAYER_MOVE_STEP
    player_angle_rad = math.radians(player_angle)
    forward_x = -math.sin(player_angle_rad)
    forward_y = math.cos(player_angle_rad)
    right_x = math.cos(player_angle_rad)
    right_y = math.sin(player_angle_rad)

    if key in (b'r', b'R'):
        reset_game_state()
        return

    if intro_active:
        return

    if key == b' ' and player_health > 0.0 and enemy_health > 0.0:
        combat_started = True

    if key in (b'l', b'L'):
        cam_z = max(70, cam_z - 10)
    elif key in (b'k', b'K'):
        cam_z = min(700, cam_z + 10)
    elif key in (b'o', b'O'):
        cam_x += 12
        target_x += 12
    elif key in (b'p', b'P'):
        cam_x -= 12
        target_x -= 12
    elif key in (b'u', b'U', b'i', b'I'):
        camera_move_step = 20
        dir_x = target_x - cam_x
        dir_y = target_y - cam_y
        dir_len = math.sqrt((dir_x * dir_x) + (dir_y * dir_y))
        if dir_len > 0.0001:
            cam_forward_x = dir_x / dir_len
            cam_forward_y = dir_y / dir_len
            if key in (b'u', b'U'):
                cam_x += cam_forward_x * camera_move_step
                cam_y += cam_forward_y * camera_move_step
                target_x += cam_forward_x * camera_move_step
                target_y += cam_forward_y * camera_move_step
            else:
                cam_x -= cam_forward_x * camera_move_step
                cam_y -= cam_forward_y * camera_move_step
                target_x -= cam_forward_x * camera_move_step
                target_y -= cam_forward_y * camera_move_step
    elif key in (b'h', b'H', b'j', b'J'):
        dir_x = target_x - cam_x
        dir_y = target_y - cam_y
        dir_len = math.sqrt((dir_x * dir_x) + (dir_y * dir_y))
        if dir_len > 0.0001:
            turn_step = math.radians(4)
            turn_angle = turn_step if key in (b'h', b'H') else -turn_step
            cos_a = math.cos(turn_angle)
            sin_a = math.sin(turn_angle)
            new_dir_x = (dir_x * cos_a) - (dir_y * sin_a)
            new_dir_y = (dir_x * sin_a) + (dir_y * cos_a)
            target_x = cam_x + new_dir_x
            target_y = cam_y + new_dir_y
    elif key in (b'q', b'Q'):
        if combat_started:
            player_angle += 6
    elif key in (b'e', b'E'):
        if combat_started:
            player_angle -= 6
    elif key in (b'w', b'W'):
        if combat_started:
            player_x -= right_x * player_move_step
            player_y -= right_y * player_move_step
            walk_phase += 0.7
    elif key in (b's', b'S'):
        if combat_started:
            player_x += right_x * player_move_step
            player_y += right_y * player_move_step
            walk_phase += 0.7
    elif key in (b'd', b'D'):
        if combat_started:
            player_x += forward_x * player_move_step
            player_y += forward_y * player_move_step
            walk_phase += 0.7
    elif key in (b'a', b'A'):
        if combat_started:
            player_x -= forward_x * player_move_step
            player_y -= forward_y * player_move_step
            walk_phase += 0.7
    elif key == b'\033':  # ESC
        sys.exit()

    player_dist = math.sqrt((player_x * player_x) + (player_y * player_y))
    player_max_dist = ARENA_RADIUS - 10
    if player_dist > player_max_dist and player_dist > 0.0001:
        scale = player_max_dist / player_dist
        player_x *= scale
        player_y *= scale

    # Prevent player from overlapping enemy body.
    ex, ey = enemy_pos
    to_player_x = player_x - ex
    to_player_y = player_y - ey
    pe_dist = math.sqrt((to_player_x * to_player_x) + (to_player_y * to_player_y))
    if pe_dist < PLAYER_ENEMY_MIN_DISTANCE:
        if pe_dist > 0.0001:
            scale = PLAYER_ENEMY_MIN_DISTANCE / pe_dist
            player_x = ex + (to_player_x * scale)
            player_y = ey + (to_player_y * scale)
        else:
            player_x = ex
            player_y = ey - PLAYER_ENEMY_MIN_DISTANCE

    camera_x, camera_y, camera_z = cam_x, cam_y, cam_z
    camera_target_x, camera_target_y, camera_target_z = target_x, target_y, target_z
    player_pos = (player_x, player_y)
    player_angle_deg = player_angle % 360.0
    player_walk_phase = walk_phase % (2 * math.pi)


def mouseListener(button, state, x, y):
    """Mouse controls: RMB shield hold in all phases; LMB attack per phase."""
    global punch_phase, punch_progress, punch_damage_applied
    global shield_active, shield_hold_time, enemy_wait_timer, combat_started
    global player_angle_deg, enemy_health, enemy_pos, enemy_bullet_cooldown
    global inferno_active, enemy_flying, inferno_frames_left
    global enemy_bullets, enemy_assassin_mode, enemy_descending
    global player_bullets, player_bullet_cooldown

    if not combat_started:
        return

    # Shield is always on right mouse button.
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # No shield during flying mode.
        if enemy_flying and (not enemy_assassin_mode):
            return
        shield_active = True
        inferno_active = False
        inferno_frames_left = 0
        shield_hold_time = 0
        punch_phase = 0
        punch_progress = 0.0
        punch_damage_applied = False
        return

    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        if shield_active:
            shield_active = False
            enemy_wait_timer = ENEMY_SHIELD_WAIT_FRAMES
        return

    if enemy_assassin_mode:
        # In assassin mode, left click shoots; right click stays shield.
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and player_bullet_cooldown <= 0:
            spawn_player_bullet()
            player_bullet_cooldown = PLAYER_BULLET_COOLDOWN_FRAMES
        return
    
    if not enemy_flying:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and punch_phase == 0 and not shield_active:
            punch_phase = 1
            punch_progress = 0.0
            punch_damage_applied = False

            # Punch damage only applies at close range.
            px, py = player_pos
            ex, ey = enemy_pos
            dist = math.sqrt(((px - ex) * (px - ex)) + ((py - ey) * (py - ey)))
            if dist <= PUNCH_RANGE:
                enemy_health = max(0.0, enemy_health - (ENEMY_MAX_HEALTH * 0.10))

                # Enemy steps back when punched.
                if dist > 0.0001:
                    away_x = (ex - px) / dist
                    away_y = (ey - py) / dist
                else:
                    away_x, away_y = 1.0, 0.0

                new_ex = ex + (away_x * ENEMY_HIT_KNOCKBACK)
                new_ey = ey + (away_y * ENEMY_HIT_KNOCKBACK)

                # Keep enemy inside arena bounds.
                enemy_dist_from_center = math.sqrt((new_ex * new_ex) + (new_ey * new_ey))
                enemy_max_dist = ARENA_RADIUS - 10.0
                if enemy_dist_from_center > enemy_max_dist and enemy_dist_from_center > 0.0001:
                    scale = enemy_max_dist / enemy_dist_from_center
                    new_ex *= scale
                    new_ey *= scale

                enemy_pos = (new_ex, new_ey)

                # Very short pause, then enemy starts shooting again.
                enemy_bullet_cooldown = ENEMY_HIT_SHOOT_DELAY_FRAMES

    else:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            inferno_active = True
            inferno_frames_left = INFERNO_BURST_FRAMES
            shield_active = False
            shield_hold_time = 0
            punch_phase = 0
            punch_progress = 0.0
            punch_damage_applied = False

def idle():
    """
    Idle function that triggers screen redraw
    """
    global punch_phase, punch_progress, punch_damage_applied
    global enemy_raise_progress, enemy_punch_phase, enemy_punch_progress
    global enemy_bullet_cooldown, enemy_bullets, combat_started
    global player_health, enemy_health, enemy_pos
    global shield_active, shield_hold_time
    global camera_x, camera_y, camera_z
    global camera_target_x, camera_target_y, camera_target_z
    global intro_active, intro_frame
    global enemy_flying, enemy_orbit_angle
    global enemy_assassin_mode, enemy_visible, enemy_respawn_timer
    global enemy_descending, enemy_descend_frame
    global enemy_stab_timer
    global enemy_fireballs, enemy_fireball_cooldown, scorch_marks
    global inferno_active, inferno_hit_cooldown, inferno_frames_left
    global player_bullets, player_bullet_cooldown
    global wound_patches

    if intro_active:
        intro_frame += 1
        t = min(1.0, intro_frame / float(INTRO_TRANSITION_FRAMES))
        smooth_t = (t * t) * (3.0 - (2.0 * t))

        camera_x = INTRO_CAMERA_X + ((CAMERA_START_X - INTRO_CAMERA_X) * smooth_t)
        camera_y = INTRO_CAMERA_Y + ((CAMERA_START_Y - INTRO_CAMERA_Y) * smooth_t)
        camera_z = INTRO_CAMERA_Z + ((CAMERA_START_Z - INTRO_CAMERA_Z) * smooth_t)

        camera_target_x = INTRO_TARGET_X + ((CAMERA_TARGET_START_X - INTRO_TARGET_X) * smooth_t)
        camera_target_y = INTRO_TARGET_Y + ((CAMERA_TARGET_START_Y - INTRO_TARGET_Y) * smooth_t)
        camera_target_z = INTRO_TARGET_Z + ((CAMERA_TARGET_START_Z - INTRO_TARGET_Z) * smooth_t)

        if t >= 1.0:
            intro_active = False
            camera_x = CAMERA_START_X
            camera_y = CAMERA_START_Y
            camera_z = CAMERA_START_Z
            camera_target_x = CAMERA_TARGET_START_X
            camera_target_y = CAMERA_TARGET_START_Y
            camera_target_z = CAMERA_TARGET_START_Z

        glutPostRedisplay()
        return

    player_ratio = 0.0
    enemy_ratio = 0.0
    if PLAYER_MAX_HEALTH > 0.0:
        player_ratio = max(0.0, min(1.0, player_health / PLAYER_MAX_HEALTH))
    if ENEMY_MAX_HEALTH > 0.0:
        enemy_ratio = max(0.0, min(1.0, enemy_health / ENEMY_MAX_HEALTH))

    player_segments = int(player_ratio * HEALTH_BAR_SEGMENTS)
    enemy_segments = int(enemy_ratio * HEALTH_BAR_SEGMENTS)

    if player_health <= 0.0 or enemy_health <= 0.0 or player_segments <= 0 or enemy_segments <= 0:
        if player_segments <= 0:
            player_health = 0.0
        if enemy_segments <= 0:
            enemy_health = 0.0
        combat_started = False
        shield_active = False
        inferno_active = False
        inferno_frames_left = 0
        enemy_bullets = []
        enemy_fireballs = []
        player_bullets = []
        glutPostRedisplay()
        return

    # Flying phase begins after enemy loses 3 lives (3 x 10% health).
    if (not enemy_flying) and (not enemy_assassin_mode) and (not enemy_descending) and enemy_health <= (ENEMY_MAX_HEALTH * 0.70):
        enemy_flying = True
        enemy_bullets = []
        enemy_bullet_cooldown = ENEMY_BULLET_COOLDOWN_FRAMES
        enemy_fireball_cooldown = FIREBALL_COOLDOWN_FRAMES
        shield_active = False
        inferno_active = False
        inferno_frames_left = 0
        punch_phase = 0
        punch_progress = 0.0
        punch_damage_applied = False

    # Assassin phase starts once enemy loses 3 lives during flight (health reaches 40%).
    if enemy_flying and (not enemy_assassin_mode) and (not enemy_descending) and enemy_health <= ENEMY_ASSASSIN_TRIGGER_HEALTH:
        enemy_health = ENEMY_ASSASSIN_TRIGGER_HEALTH
        enemy_descending = True
        enemy_descend_frame = 0
        shield_active = False
        inferno_active = False
        inferno_frames_left = 0
        enemy_fireballs = []

    if enemy_descending:
        enemy_descend_frame += 1
        if enemy_descend_frame >= ENEMY_DESCEND_FRAMES:
            enemy_descending = False
            enemy_flying = False
            enemy_assassin_mode = True
            enemy_visible = False
            enemy_respawn_timer = ENEMY_RESPAWN_FRAMES
            enemy_bullets = []
            enemy_fireballs = []
            inferno_active = False
            inferno_frames_left = 0
            enemy_stab_timer = 0

    if combat_started and (not enemy_flying) and (not enemy_assassin_mode) and (not enemy_descending):
        px, py = player_pos
        ex, ey = enemy_pos
        dx = px - ex
        dy = py - ey
        dist = math.sqrt((dx * dx) + (dy * dy))

        if dist > ENEMY_CHASE_STOP_DISTANCE and dist > 0.0001:
            step = min(ENEMY_CHASE_SPEED, dist - ENEMY_CHASE_STOP_DISTANCE)
            ex += (dx / dist) * step
            ey += (dy / dist) * step
            enemy_pos = (ex, ey)
        elif dist < ENEMY_CHASE_STOP_DISTANCE and dist > 0.0001:
            step = min(ENEMY_CHASE_SPEED, ENEMY_CHASE_STOP_DISTANCE - dist)
            ex -= (dx / dist) * step
            ey -= (dy / dist) * step
            enemy_pos = (ex, ey)

    if combat_started and enemy_flying and (not enemy_descending):
        px, py = player_pos
        enemy_orbit_angle += ENEMY_ORBIT_SPEED
        enemy_pos = (
            px + (math.cos(enemy_orbit_angle) * ENEMY_ORBIT_RADIUS),
            py + (math.sin(enemy_orbit_angle) * ENEMY_ORBIT_RADIUS),
        )

    if combat_started and enemy_assassin_mode:
        if player_bullet_cooldown > 0:
            player_bullet_cooldown -= 1

        if not enemy_visible:
            enemy_respawn_timer -= 1
            if enemy_respawn_timer <= 0:
                enemy_pos = respawn_enemy_around_player()
                enemy_visible = True
        else:
            px, py = player_pos
            ex, ey = enemy_pos
            dx = px - ex
            dy = py - ey
            dist = math.sqrt((dx * dx) + (dy * dy))

            if enemy_stab_timer > 0:
                enemy_stab_timer -= 1
                if enemy_stab_timer <= 0:
                    enemy_visible = False
                    enemy_respawn_timer = ENEMY_RESPAWN_FRAMES
            else:
                if dist > 0.0001:
                    step = min(ENEMY_ASSASSIN_SPEED, max(0.0, dist - ENEMY_ASSASSIN_BODY_STOP_DISTANCE))
                    ex += (dx / dist) * step
                    ey += (dy / dist) * step
                    enemy_pos = (ex, ey)

                    # Recompute distance after move so stab starts exactly at stop point.
                    dx = px - ex
                    dy = py - ey
                    dist = math.sqrt((dx * dx) + (dy * dy))

                # Sword cut starts at body stop point; body stays outside player.
                if dist <= ENEMY_ASSASSIN_BODY_STOP_DISTANCE:
                    if not shield_active:
                        player_health = max(0.0, player_health - (PLAYER_MAX_HEALTH * 0.10))
                        add_player_wound_patch_from_enemy()
                        enemy_stab_timer = ENEMY_SWORD_STAB_FRAMES
                    else:
                        enemy_visible = False
                        enemy_respawn_timer = ENEMY_RESPAWN_FRAMES

    if enemy_punch_phase == 0 and enemy_raise_progress < 1.0 and not shield_active:
        enemy_raise_progress = min(1.0, enemy_raise_progress + ENEMY_RAISE_STEP)

    if combat_started and (not enemy_flying) and (not enemy_assassin_mode) and (not enemy_descending):
        if enemy_bullet_cooldown > 0:
            enemy_bullet_cooldown -= 1
        else:
            muzzle_x, muzzle_y, muzzle_z, dir_x, dir_y = compute_enemy_muzzle_world()
            enemy_bullets.append({
                "pos": [muzzle_x, muzzle_y, muzzle_z],
                "vel": [dir_x * ENEMY_BULLET_SPEED, dir_y * ENEMY_BULLET_SPEED],
            })
            enemy_bullet_cooldown = ENEMY_BULLET_COOLDOWN_FRAMES

    if combat_started and enemy_flying and (not enemy_descending):
        if enemy_fireball_cooldown > 0:
            enemy_fireball_cooldown -= 1
        else:
            ex, ey = enemy_pos
            px, py = player_pos
            sx, sy, sz = ex, ey, FIREBALL_AIM_HEIGHT + ENEMY_FLY_HEIGHT
            dx = px - sx
            dy = py - sy
            dist_xy = math.sqrt((dx * dx) + (dy * dy))
            if dist_xy > 0.0001:
                dir_x = dx / dist_xy
                dir_y = dy / dist_xy
            else:
                dir_x, dir_y = 0.0, 1.0

            speed_xy = 2.8
            enemy_fireballs.append({
                "pos": [sx, sy, sz],
                "vel": [dir_x * speed_xy, dir_y * speed_xy, -2.3],
                "landed": False,
            })
            enemy_fireball_cooldown = FIREBALL_COOLDOWN_FRAMES

    if enemy_fireballs:
        updated_fireballs = []
        px, py = player_pos
        for fireball in enemy_fireballs:
            if fireball["landed"]:
                continue

            fireball["pos"][0] += fireball["vel"][0]
            fireball["pos"][1] += fireball["vel"][1]
            fireball["pos"][2] += fireball["vel"][2]
            fireball["vel"][2] -= FIREBALL_GRAVITY

            fx, fy, fz = fireball["pos"]
            if fz <= 1.0:
                fireball["landed"] = True
                scorch_marks.append({"x": fx, "y": fy, "r": SCORCH_RADIUS})
                if len(scorch_marks) > 40:
                    scorch_marks = scorch_marks[-40:]

                hit_dx = fx - px
                hit_dy = fy - py
                if ((hit_dx * hit_dx) + (hit_dy * hit_dy)) <= ((SCORCH_RADIUS + 8.0) * (SCORCH_RADIUS + 8.0)):
                    player_health = max(0.0, player_health - (PLAYER_MAX_HEALTH * 0.10))
                continue

            updated_fireballs.append(fireball)

        enemy_fireballs = updated_fireballs

    # Inferno beam hit logic (LMB click burst). Beam damages enemy in flying mode.
    if inferno_active:
        if inferno_frames_left > 0:
            inferno_frames_left -= 1
        if inferno_frames_left <= 0:
            inferno_active = False

    if inferno_hit_cooldown > 0:
        inferno_hit_cooldown -= 1

    if inferno_active and combat_started and enemy_flying and (not enemy_descending) and inferno_hit_cooldown == 0:
        (left_fist, right_fist, angle_rad) = compute_player_fist_world_positions_for_inferno()
        fwd_x = -math.sin(angle_rad)
        fwd_y = math.cos(angle_rad)
        dir_x = fwd_x * 0.7071
        dir_y = fwd_y * 0.7071
        dir_z = 0.7071

        ex, ey = enemy_pos
        ez = 100.0 + ENEMY_FLY_HEIGHT
        hit = False
        sx, sy, sz = right_fist
        vx = ex - sx
        vy = ey - sy
        vz = ez - sz
        t = (vx * dir_x) + (vy * dir_y) + (vz * dir_z)
        if t < 0.0:
            t = 0.0
        elif t > INFERNO_BEAM_LENGTH:
            t = INFERNO_BEAM_LENGTH

        cx = sx + (dir_x * t)
        cy = sy + (dir_y * t)
        cz = sz + (dir_z * t)
        ddx = ex - cx
        ddy = ey - cy
        ddz = ez - cz
        if ((ddx * ddx) + (ddy * ddy) + (ddz * ddz)) <= (INFERNO_HIT_RADIUS * INFERNO_HIT_RADIUS):
            hit = True

        if hit:
            # In flight mode enemy can lose at most 3 lives here, then transitions to assassin.
            enemy_health = max(ENEMY_ASSASSIN_TRIGGER_HEALTH, enemy_health - (ENEMY_MAX_HEALTH * 0.10))
            inferno_hit_cooldown = INFERNO_HIT_COOLDOWN_FRAMES

    # Immediate transition check after inferno damage application.
    if enemy_flying and (not enemy_assassin_mode) and (not enemy_descending) and enemy_health <= ENEMY_ASSASSIN_TRIGGER_HEALTH:
        enemy_health = ENEMY_ASSASSIN_TRIGGER_HEALTH
        enemy_descending = True
        enemy_descend_frame = 0
        shield_active = False
        inferno_active = False
        inferno_frames_left = 0
        enemy_fireballs = []

    if player_bullets:
        updated_player_bullets = []
        arena_limit_sq = (ARENA_RADIUS + 120.0) * (ARENA_RADIUS + 120.0)
        for bullet in player_bullets:
            bullet["pos"][0] += bullet["vel"][0]
            bullet["pos"][1] += bullet["vel"][1]
            bx, by, bz = bullet["pos"]

            if enemy_assassin_mode and enemy_visible:
                ex, ey = enemy_pos
                hit_dx = bx - ex
                hit_dy = by - ey
                if ((hit_dx * hit_dx) + (hit_dy * hit_dy)) <= ((PLAYER_BULLET_RADIUS + 14.0) * (PLAYER_BULLET_RADIUS + 14.0)):
                    enemy_health = max(0.0, enemy_health - (ENEMY_MAX_HEALTH * 0.10))
                    enemy_visible = False
                    enemy_respawn_timer = ENEMY_RESPAWN_FRAMES
                    enemy_stab_timer = 0
                    continue

            if (bx * bx + by * by) <= arena_limit_sq:
                updated_player_bullets.append(bullet)
        player_bullets = updated_player_bullets

    if enemy_bullets:
        updated_bullets = []
        px, py = player_pos
        hit_radius_sq = ENEMY_BULLET_HIT_RADIUS * ENEMY_BULLET_HIT_RADIUS
        arena_limit_sq = (ARENA_RADIUS + 120.0) * (ARENA_RADIUS + 120.0)
        
        # Shield parameters
        shield_params = None
        if shield_active:
            player_angle_rad = math.radians(player_angle_deg)
            fwd_x = -math.sin(player_angle_rad)
            fwd_y = math.cos(player_angle_rad)
            shield_x = px + (fwd_x * SHIELD_DISTANCE)
            shield_y = py + (fwd_y * SHIELD_DISTANCE)
            shield_radius_sq = (SHIELD_WIDTH + ENEMY_BULLET_RADIUS + 8.0) ** 2
            shield_params = {
                'x': shield_x, 'y': shield_y,
                'radius_sq': shield_radius_sq,
                'fwd_x': fwd_x, 'fwd_y': fwd_y,
                'z_bottom': SHIELD_Z_BOTTOM, 'z_top': SHIELD_Z_TOP
            }

        for bullet in enemy_bullets:
            prev_bx = bullet["pos"][0]
            prev_by = bullet["pos"][1]
            bullet["pos"][0] += bullet["vel"][0]
            bullet["pos"][1] += bullet["vel"][1]
            bx, by, bz = bullet["pos"]
            dx = bx - px
            dy = by - py

            # Check if shield blocks the bullet
            bullet_blocked = False
            if shield_params is not None:
                seg_dx = bx - prev_bx
                seg_dy = by - prev_by
                seg_len_sq = (seg_dx * seg_dx) + (seg_dy * seg_dy)

                if seg_len_sq > 0.0001:
                    t = (((shield_params['x'] - prev_bx) * seg_dx) + ((shield_params['y'] - prev_by) * seg_dy)) / seg_len_sq
                    if t < 0.0:
                        t = 0.0
                    elif t > 1.0:
                        t = 1.0
                else:
                    t = 0.0

                closest_x = prev_bx + (seg_dx * t)
                closest_y = prev_by + (seg_dy * t)
                sx = closest_x - shield_params['x']
                sy = closest_y - shield_params['y']
                z_ok = (shield_params['z_bottom'] - ENEMY_BULLET_RADIUS) <= bz <= (shield_params['z_top'] + ENEMY_BULLET_RADIUS)
                if ((sx * sx + sy * sy) <= shield_params['radius_sq']) and z_ok:
                    bullet_blocked = True

            if bullet_blocked:
                # Bullet blocked by shield - vanish at shield coordinates
                continue

            # Check if bullet hits player
            if (dx * dx + dy * dy) <= hit_radius_sq:
                player_health = max(0.0, player_health - (PLAYER_MAX_HEALTH * 0.10))
                continue

            # Check if bullet is out of bounds
            if (bx * bx + by * by) > arena_limit_sq:
                continue

            # Bullet persists
            updated_bullets.append(bullet)

        enemy_bullets = updated_bullets

    if wound_patches:
        updated_wounds = []
        for patch in wound_patches:
            patch["life"] -= 1
            if patch["life"] > 0:
                updated_wounds.append(patch)
        wound_patches = updated_wounds

    if punch_phase != 0 and not shield_active and not enemy_flying:
        punch_progress += PUNCH_STEP

        if punch_progress >= 1.0:
            punch_progress = 0.0
            punch_phase += 1
            if punch_phase > 4:
                punch_phase = 0

    glutPostRedisplay()

def showScreen():
    """
    Display function to render the game scene
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WIDTH, HEIGHT)
    
    setupCamera()
    
    # Unified maroon environment - floor and walls in one pass.
    bg_min = -1300
    bg_max = 1300
    bg_bottom = -100
    bg_top = 1300
    back_wall_y = 980

    glBegin(GL_QUADS)
    glColor3f(0.2, 0.0, 0.0)

    # Floor (extended base)
    glVertex3f(bg_min, bg_min, bg_bottom)
    glVertex3f(bg_max, bg_min, bg_bottom)
    glVertex3f(bg_max, bg_max, bg_bottom)
    glVertex3f(bg_min, bg_max, bg_bottom)

    # Back wall (kept closer so it renders as maroon instead of appearing black)
    glVertex3f(bg_min, back_wall_y, bg_bottom)
    glVertex3f(bg_max, back_wall_y, bg_bottom)
    glVertex3f(bg_max, back_wall_y, bg_top)
    glVertex3f(bg_min, back_wall_y, bg_top)

    # -Y wall
    glVertex3f(bg_max, bg_min, bg_bottom)
    glVertex3f(bg_min, bg_min, bg_bottom)
    glVertex3f(bg_min, bg_min, bg_top)
    glVertex3f(bg_max, bg_min, bg_top)

    # +X wall (correct CCW)
    glVertex3f(bg_max, bg_min, bg_bottom)
    glVertex3f(bg_max, bg_max, bg_bottom)
    glVertex3f(bg_max, bg_max, bg_top)
    glVertex3f(bg_max, bg_min, bg_top)

    # -X wall
    glVertex3f(bg_min, bg_min, bg_bottom)
    glVertex3f(bg_min, bg_max, bg_bottom)
    glVertex3f(bg_min, bg_max, bg_top)
    glVertex3f(bg_min, bg_min, bg_top)

    # Top panel
    glVertex3f(bg_min, bg_min, bg_top)
    glVertex3f(bg_max, bg_min, bg_top)
    glVertex3f(bg_max, bg_max, bg_top)
    glVertex3f(bg_min, bg_max, bg_top)
    glEnd()

    draw_scorch_marks()
    
    # Draw shrine
    draw_shrine()
    draw_enemy()
    draw_enemy_bullets()
    draw_player_bullets()
    draw_enemy_fireballs()
    draw_player()
    draw_inferno_beams()
    draw_shield()
    draw_health_bars()
    
    glutSwapBuffers()

def main():
    """Main function"""
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"The Culling Game")
    glEnable(GL_COLOR_MATERIAL)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(120, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
