import math
import os

os.makedirs('website/assets/ui', exist_ok=True)

def generate_pixel_cloud_svg(filename, width, height, lobes, grid=6, fill_to_bottom=True):
    cols = width // grid
    rows = height // grid
    
    # 0 = empty, 1 = occupied
    occupied = [[0]*cols for _ in range(rows)]
    
    # Render organic circular/puffy lobes
    for (cx, cy, r, aspect) in lobes:
        cg_x = cx / grid
        cg_y = cy / grid
        rg = r / grid
        
        min_r = max(0, int(cg_y - rg))
        max_r = min(rows, int(cg_y + rg + 1))
        min_c = max(0, int(cg_x - rg * aspect))
        max_c = min(cols, int(cg_x + rg * aspect + 1))
        
        for row in range(min_r, max_r):
            for col in range(min_c, max_c):
                dx = (col - cg_x) / aspect
                dy = (row - cg_y)
                if dx*dx + dy*dy <= rg*rg:
                    occupied[row][col] = 1
                    
    # Fill downwards to bottom edge so the cloud anchors cleanly
    if fill_to_bottom:
        for c in range(cols):
            filling = False
            for r in range(rows):
                if occupied[r][c] == 1:
                    filling = True
                if filling:
                    occupied[r][c] = 1
                    
    # Determine pixel shading depth
    # We find distance from the top cloud surface
    depth = [[-1]*cols for _ in range(rows)]
    for c in range(cols):
        current_depth = -1
        for r in range(rows):
            if occupied[r][c] == 1:
                if current_depth == -1:
                    current_depth = 0
                else:
                    current_depth += 1
                depth[r][c] = current_depth
                
    # Also calculate distance from side edges for rounded puff shading
    for r in range(rows):
        for c in range(cols):
            if occupied[r][c] == 1:
                # check horizontal distance to edge
                left_dist = 0
                while c - left_dist >= 0 and occupied[r][c - left_dist] == 1:
                    left_dist += 1
                right_dist = 0
                while c + right_dist < cols and occupied[r][c + right_dist] == 1:
                    right_dist += 1
                min_edge = min(left_dist, right_dist)
                if min_edge <= 2 and depth[r][c] > min_edge:
                    depth[r][c] = min_edge

    # Color Palette: Warm Sunset Cloud Aesthetic (Golden hour Nalanda sky)
    # Tier 0: Sunlit Rim Highlight (Cream/White)
    # Tier 1: Bright Amber Gold
    # Tier 2: Warm Saffron
    # Tier 3: Dusky Terracotta Amber
    # Tier 4: Deep Dusk Umber
    # Tier 5: Seamless Background Tone (#090e15)
    colors = {
        0: '#fffbeb',  # Cream sunlit edge
        1: '#fef08a',  # Soft pale gold
        2: '#fbbf24',  # Radiant amber
        3: '#d97706',  # Warm saffron
        4: '#92400e',  # Terracotta dusk
        5: '#451a03',  # Deep sunset umber
        6: '#151e2b',  # Slate dusk
        7: '#090e15',  # Seamless background fill
    }
    
    def get_tier(d, r_norm):
        if d == 0:
            return 0
        elif d == 1:
            return 1
        elif d <= 3:
            return 2
        elif d <= 6:
            return 3
        elif d <= 10:
            return 4
        elif d <= 15:
            return 5
        elif d <= 22 or r_norm < 0.8:
            return 6
        else:
            return 7

    cell_color = [[None]*cols for _ in range(rows)]
    for r in range(rows):
        r_norm = r / rows
        for c in range(cols):
            if occupied[r][c] == 1:
                t = get_tier(depth[r][c], r_norm)
                cell_color[r][c] = colors[t]

    # Optimize output by merging adjacent horizontal cells of same color
    rects = []
    for r in range(rows):
        c = 0
        while c < cols:
            color = cell_color[r][c]
            if color is not None:
                start_c = c
                while c < cols and cell_color[r][c] == color:
                    c += 1
                length = c - start_c
                rects.append(f'<rect x="{start_c*grid}" y="{r*grid}" width="{length*grid}" height="{grid}" fill="{color}"/>')
            else:
                c += 1
                
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" preserveAspectRatio="none" style="shape-rendering: crispEdges;">
{''.join(rects)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Generated {filename} ({width}x{height}, {len(rects)} rects, {len(svg)} chars)')


# ═══════════════════════════════════════════════════════════════
# 1. Left Cloud Bank (cloud_bank_left.svg)
# Majestic billowing cumulus bank covering from left across center
# ═══════════════════════════════════════════════════════════════
lobes_left = [
    # (cx, cy, radius, aspect_ratio)
    (-60, 260, 200, 1.4),
    (80, 220, 170, 1.3),
    (240, 160, 160, 1.25),
    (140, 120, 110, 1.2),
    (380, 180, 150, 1.3),
    (320, 100, 100, 1.2),
    (520, 150, 130, 1.25),
    (460, 70, 90, 1.15),
    (660, 190, 140, 1.3),
    (600, 120, 100, 1.2),
    (800, 230, 150, 1.35),
    (740, 160, 95, 1.2),
    (940, 270, 140, 1.4),
    (870, 210, 80, 1.2),
    (1060, 310, 120, 1.5),
]
generate_pixel_cloud_svg('website/assets/ui/cloud_bank_left.svg', 1100, 360, lobes_left, grid=6, fill_to_bottom=True)


# ═══════════════════════════════════════════════════════════════
# 2. Right Cloud Bank (cloud_bank_right.svg)
# Matching billowing cumulus bank covering from right across center
# ═══════════════════════════════════════════════════════════════
lobes_right = [
    (1160, 260, 200, 1.4),
    (1020, 220, 170, 1.3),
    (860, 160, 160, 1.25),
    (960, 120, 110, 1.2),
    (720, 180, 150, 1.3),
    (780, 100, 100, 1.2),
    (580, 150, 130, 1.25),
    (640, 70, 90, 1.15),
    (440, 190, 140, 1.3),
    (500, 120, 100, 1.2),
    (300, 230, 150, 1.35),
    (360, 160, 95, 1.2),
    (160, 270, 140, 1.4),
    (230, 210, 80, 1.2),
    (40, 310, 120, 1.5),
]
generate_pixel_cloud_svg('website/assets/ui/cloud_bank_right.svg', 1100, 360, lobes_right, grid=6, fill_to_bottom=True)


# ═══════════════════════════════════════════════════════════════
# 3. Fluffy Floating Cloud Puffs (cloud_float_puffs.svg)
# Cute independent cumulus puffs that drift upward on scroll
# ═══════════════════════════════════════════════════════════════
lobes_float = [
    (140, 90, 55, 1.2),
    (190, 65, 48, 1.15),
    (245, 80, 52, 1.2),
    (170, 110, 65, 1.35),
    (220, 115, 60, 1.3),
    
    (460, 75, 45, 1.2),
    (505, 55, 40, 1.15),
    (550, 70, 42, 1.2),
    (490, 95, 55, 1.3),
    (530, 100, 50, 1.3)
]
generate_pixel_cloud_svg('website/assets/ui/cloud_float_puffs.svg', 700, 170, lobes_float, grid=5, fill_to_bottom=False)


# ═══════════════════════════════════════════════════════════════
# 4. Full Width Seamless Horizon Cloud Bank (cloud_horizon_full.svg)
# ═══════════════════════════════════════════════════════════════
lobes_full = [
    (-40, 180, 140, 1.3), (120, 130, 120, 1.2), (280, 100, 130, 1.25),
    (440, 130, 115, 1.2), (600, 90, 135, 1.2), (760, 125, 120, 1.2),
    (940, 80, 145, 1.25), (1120, 120, 120, 1.2), (1300, 90, 135, 1.2),
    (1470, 130, 120, 1.2), (1640, 95, 130, 1.25), (1800, 130, 120, 1.2),
    (1960, 170, 130, 1.3)
]
generate_pixel_cloud_svg('website/assets/ui/cloud_horizon_full.svg', 1920, 250, lobes_full, grid=6, fill_to_bottom=True)


# ═══════════════════════════════════════════════════════════════
# 5. Soft Golden Mist Sweep (cloud_mist_sweep_v2.svg)
# Softly dithered atmospheric cloud band for Section 2 -> 3
# ═══════════════════════════════════════════════════════════════
lobes_mist = [
    (150, 80, 180, 1.8), (450, 60, 200, 1.7), (800, 85, 210, 1.75),
    (1150, 60, 200, 1.7), (1500, 80, 210, 1.8), (1850, 65, 190, 1.75)
]
generate_pixel_cloud_svg('website/assets/ui/cloud_mist_sweep_v2.svg', 1920, 160, lobes_mist, grid=8, fill_to_bottom=False)
