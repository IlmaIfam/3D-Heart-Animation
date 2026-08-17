from vpython import *
import numpy as np
import random
import math

# ==========================================
# 3D GLOWING HEART
# ==========================================

scene = canvas(
    title="❤️ 3D Glowing Heart",
    width=1000,
    height=750,
    background=vector(0.005, 0.005, 0.015)
)

scene.camera.pos = vector(0, 0, 42)
scene.camera.axis = vector(0, 0, -42)

# Remove normal axes
scene.autoscale = False
scene.range = 18

# ==========================================
# HEART PARTICLES
# ==========================================

particles = []

# Heart mathematical surface
for i in range(100):

    u = 2 * np.pi * i / 100

    for j in range(50):

        v = np.pi * j / 49

        x = 16 * np.sin(v)**3 * np.cos(u)

        y = (
            13 * np.cos(v)
            - 5 * np.cos(2*v)
            - 2 * np.cos(3*v)
            - np.cos(4*v)
        )

        z = 8 * np.sin(v) * np.sin(u)

        # Scale
        p = vector(
            x * 0.65,
            y * 0.65,
            z * 0.65
        )

        # Small glowing particle
        particle = sphere(
            pos=p,
            radius=random.uniform(0.07, 0.13),
            color=vector(1, random.uniform(0.05, 0.3), 0.15),
            emissive=True
        )

        particles.append(particle)


# ==========================================
# FLOATING PARTICLES
# ==========================================

stars = []

for i in range(250):

    p = vector(
        random.uniform(-25, 25),
        random.uniform(-20, 20),
        random.uniform(-15, 15)
    )

    star = sphere(
        pos=p,
        radius=random.uniform(0.015, 0.05),
        color=vector(1, random.uniform(0.1, 0.4), 0.3),
        emissive=True
    )

    stars.append(star)


# ==========================================
# HEART GLOW
# ==========================================

glow = sphere(
    pos=vector(0, 0, 0),
    radius=7,
    color=vector(0.5, 0.01, 0.02),
    opacity=0.04,
    emissive=True
)


# ==========================================
# ANIMATION
# ==========================================

angle = 0
time = 0

# Save original positions
original_positions = [vector(p.pos.x, p.pos.y, p.pos.z)
                      for p in particles]


while True:

    rate(60)

    time += 0.05
    angle += 0.012

    # ======================================
    # HEART BEATING EFFECT
    # ======================================

    beat = 1 + 0.08 * math.sin(time * 4)

    # ======================================
    # ROTATION + BEAT
    # ======================================

    for particle, original in zip(particles, original_positions):

        # Scale for heartbeat
        x = original.x * beat
        y = original.y * beat
        z = original.z * beat

        # Rotate around Y axis
        new_x = x * math.cos(angle) - z * math.sin(angle)
        new_z = x * math.sin(angle) + z * math.cos(angle)

        particle.pos = vector(
            new_x,
            y,
            new_z
        )

    # ======================================
    # GLOW PULSE
    # ======================================

    glow.radius = 7 * beat

    # ======================================
    # FLOATING PARTICLE MOVEMENT
    # ======================================

    for star in stars:

        star.pos.y += 0.01

        if star.pos.y > 20:
            star.pos.y = -20