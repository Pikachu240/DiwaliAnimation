import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

def create_diwali_animation():
    width = 480
    height = 854  # 9:16 vertical Reel / Story format
    fps = 20
    num_frames = 60  # 3 seconds loop
    frames = []

    # Pre-generate stars
    random.seed(42)
    stars = [(random.randint(0, width), random.randint(0, int(height * 0.7)), random.uniform(0.8, 2.5), random.uniform(0, math.pi * 2)) for _ in range(80)]

    # Fireworks definitions
    fireworks = [
        {"start_frame": 0, "x": 140, "y": 200, "color": (255, 90, 90), "count": 40, "speed": 5.5},
        {"start_frame": 15, "x": 340, "y": 170, "color": (255, 215, 0), "count": 50, "speed": 6.5},
        {"start_frame": 30, "x": 190, "y": 280, "color": (80, 230, 255), "count": 40, "speed": 5.0},
        {"start_frame": 42, "x": 310, "y": 230, "color": (255, 120, 230), "count": 45, "speed": 6.0},
    ]

    for fw in fireworks:
        particles = []
        for _ in range(fw["count"]):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(1.0, fw["speed"])
            decay = random.uniform(0.92, 0.96)
            particles.append({"angle": angle, "spd": spd, "decay": decay})
        fw["particles"] = particles

    try:
        font_large = ImageFont.truetype("arial.ttf", 34)
        font_sub = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 15)
    except:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_small = ImageFont.load_default()

    for f in range(num_frames):
        t = f / num_frames
        
        # Deep night sky canvas
        img = Image.new("RGBA", (width, height), (10, 8, 28, 255))
        draw = ImageDraw.Draw(img)

        # Diya position
        diya_x = width // 2
        diya_y = int(height * 0.72)
        
        # Flame flicker factor
        flicker = 1.0 + 0.15 * math.sin(f * 0.8) + 0.08 * math.cos(f * 1.5)
        flame_h = 42 * flicker
        flame_w = 18 * (1.0 + 0.1 * math.sin(f * 1.2))

        # Ambient glow aura around diya
        glow_radius = int(130 * flicker)
        for r in range(glow_radius, 0, -15):
            alpha = int(45 * (1 - r / glow_radius))
            draw.ellipse(
                [diya_x - r, diya_y - r - 20, diya_x + r, diya_y + r - 20],
                fill=(255, 160, 20, alpha)
            )

        # Twinkling stars
        for sx, sy, size, phase in stars:
            twinkle = (math.sin(f * 0.2 + phase) + 1) / 2
            star_alpha = int(80 + 175 * twinkle)
            sz = size * (0.8 + 0.4 * twinkle)
            draw.ellipse([sx - sz, sy - sz, sx + sz, sy + sz], fill=(255, 255, 220, star_alpha))

        # Render Fireworks
        for fw in fireworks:
            age = f - fw["start_frame"]
            if age < 0:
                age += num_frames
            if 0 <= age < 24:
                cr, cg, cb = fw["color"]
                for p in fw["particles"]:
                    dist = (p["spd"] * age) * (1 - (age / 32))
                    px = fw["x"] + math.cos(p["angle"]) * dist * 3.8
                    py = fw["y"] + math.sin(p["angle"]) * dist * 3.8 + (age * 0.7)
                    alpha = max(0, int(255 * (1 - age / 24)))
                    rad = max(1, 2.5 * (1 - age / 26))
                    draw.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(cr, cg, cb, alpha))
                    if age < 10:
                        draw.ellipse([px - rad*1.8, py - rad*1.8, px + rad*1.8, py + rad*1.8], fill=(255, 255, 200, alpha // 2))

        # Floating golden sparkles rising from Diya
        for i in range(16):
            sp_phase = (f + i * 4) % num_frames
            sp_y = diya_y - 35 - (sp_phase * 6)
            sp_x = diya_x + math.sin(sp_phase * 0.3 + i) * (18 + i * 2.5)
            sp_alpha = max(0, int(220 * (1 - sp_phase / num_frames)))
            sp_sz = 1.5 + 0.8 * math.sin(i + f * 0.3)
            draw.ellipse([sp_x - sp_sz, sp_y - sp_sz, sp_x + sp_sz, sp_y + sp_sz], fill=(255, 225, 100, sp_alpha))

        # Decorative Rangoli arcs below Diya
        draw.ellipse([diya_x - 100, diya_y + 30, diya_x + 100, diya_y + 65], outline=(255, 215, 0, 150), width=2)
        draw.ellipse([diya_x - 80, diya_y + 35, diya_x + 80, diya_y + 60], outline=(255, 105, 180, 130), width=2)

        # Diya base (Terracotta clay lamp)
        draw.ellipse([diya_x - 65, diya_y, diya_x + 65, diya_y + 40], fill=(185, 90, 30, 255))
        draw.ellipse([diya_x - 60, diya_y + 3, diya_x + 60, diya_y + 32], fill=(215, 120, 45, 255))
        draw.arc([diya_x - 60, diya_y + 2, diya_x + 60, diya_y + 35], start=0, end=180, fill=(255, 215, 0, 255), width=3)
        draw.ellipse([diya_x - 48, diya_y + 6, diya_x + 48, diya_y + 22], fill=(130, 60, 20, 255))

        # Wick
        draw.line([diya_x, diya_y + 10, diya_x, diya_y - 4], fill=(40, 20, 10, 255), width=3)

        # Flame layers
        flame_top = diya_y - flame_h - 4
        # Outer
        draw.polygon([
            (diya_x, flame_top),
            (diya_x + flame_w, diya_y),
            (diya_x, diya_y + 5),
            (diya_x - flame_w, diya_y)
        ], fill=(255, 100, 10, 230))
        # Middle
        draw.polygon([
            (diya_x, flame_top + 7),
            (diya_x + flame_w * 0.65, diya_y - 2),
            (diya_x, diya_y + 2),
            (diya_x - flame_w * 0.65, diya_y - 2)
        ], fill=(255, 200, 30, 240))
        # Inner
        draw.polygon([
            (diya_x, flame_top + 15),
            (diya_x + flame_w * 0.35, diya_y - 4),
            (diya_x, diya_y + 1),
            (diya_x - flame_w * 0.35, diya_y - 4)
        ], fill=(255, 255, 220, 255))

        # Typography / Greeting
        shimmer = int(210 + 45 * math.sin(f * 0.15))
        draw.text((width // 2, 85), "HAPPY DIWALI", anchor="mm", font=font_large, fill=(255, shimmer, 50, 255))
        draw.text((width // 2, 125), "✨  SHUBH DEEPAWALI  ✨", anchor="mm", font=font_sub, fill=(255, 230, 160, 240))
        
        # Bottom greeting
        draw.text((width // 2, int(height * 0.86)), "May your life be bright & joyful", anchor="mm", font=font_small, fill=(240, 240, 240, 220))
        draw.text((width // 2, int(height * 0.90)), "✨ Saal Mubarak ✨", anchor="mm", font=font_sub, fill=(255, 215, 100, 240))

        # Convert to RGB
        bg_rgb = Image.new("RGB", (width, height), (8, 6, 20))
        bg_rgb.paste(img, (0, 0), img)
        frames.append(bg_rgb)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(out_dir, "diwali_greeting_reel.gif")
    
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,  # 50ms per frame = 20 fps
        loop=0,
        optimize=True
    )
    print("Animation successfully created at:", output_path)

if __name__ == "__main__":
    create_diwali_animation()
