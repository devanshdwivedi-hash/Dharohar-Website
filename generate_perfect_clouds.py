import math
import os

os.makedirs('website/assets/ui', exist_ok=True)

def create_pixel_cloud(filename, width, height, domes, grid=6, fade_bottom=True):
    cols = width // grid
    rows = height // grid
    
    # 0 = transparent, 1 = cloud body
    cloud = [[0]*cols for _ in range(rows)]
    dome_ids = [[-1]*cols for _ in range(rows)]
    
    # Place puffy circular domes
    for d_idx, (cx, cy, r, aspect) in enumerate(domes):
        cg_x = cx / grid
        cg_y = cy / grid
        rg = r / grid
        
        min_r = max(0, int(cg_y - rg))
        max_r = min(rows, int(cg_y + rg + 1))
        min_c = max(0, int(cg_x - rg * aspect))
        max_c = min(cols, int(cg_x + rg * aspect + 1))
        
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                dx = (c - cg_x) / aspect
                dy = (r - cg_y)
                if dx*dx + dy*dy <= rg*rg:
                    cloud[r][c] = 1
                    dome_ids[r][c] = d_idx
                    
    # Fill downwards to bottom edge so the cloud has a solid base
    if fade_bottom:
        for c in range(cols):
            filling = False
            for r in range(rows):
                if cloud[r][c] == 1:
                    filling = True
                if filling:
                    cloud[r][c] = 1
                    
    # Now assign clean, professional pixel art shading:
    # 0 = empty
    # 1 = Highlight (Top sunlit edge of domes: Pure White)
    # 2 = Main Cloud Body (Soft Cream Ivory)
    # 3 = Underside Puff Shadow (Warm Golden Amber)
    # 4 = Deep Base Slate (#090e15)
    
    shading = [[0]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if cloud[r][c] == 1:
                # Check if it's the top edge
                is_top = (r == 0) or (cloud[r-1][c] == 0) or (c > 0 and cloud[r][c-1] == 0) or (c < cols-1 and cloud[r][c+1] == 0)
                is_second_top = (r > 0 and shading[r-1][c] == 1) or (c > 0 and shading[r][c-1] == 1)
                
                # Bottom third of the cloud container
                is_base = (r >= rows - 5) if fade_bottom else False
                is_lower = (r >= rows - 12) if fade_bottom else False
                
                if is_top:
                    shading[r][c] = 1 # White rim
                elif is_second_top and r < rows * 0.4:
                    shading[r][c] = 1 # Extra crisp highlight
                elif is_base:
                    shading[r][c] = 4 # Deep base matching section 2
                elif is_lower:
                    shading[r][c] = 3 # Soft golden amber shadow
                else:
                    # Check if near a bottom curve of any dome
                    shading[r][c] = 2 # Soft cream ivory body

    # Pixel Art Palette
    colors = {
        1: '#ffffff',  # Pure Sunlit White Highlight
        2: '#fffbeb',  # Soft Warm Cream Cloud Body
        3: '#fbbf24',  # Golden Amber Puff Shadow
        4: '#090e15',  # Seamless Background Fill
    }
    
    # Merge horizontal adjacent pixels of same color to optimize SVG
    rects = []
    for r in range(rows):
        c = 0
        while c < cols:
            val = shading[r][c]
            if val != 0:
                start_c = c
                while c < cols and shading[r][c] == val:
                    c += 1
                length = c - start_c
                rects.append(f'<rect x="{start_c*grid}" y="{r*grid}" width="{length*grid}" height="{grid}" fill="{colors[val]}"/>')
            else:
                c += 1
                
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="shape-rendering: crispEdges;">
{''.join(rects)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Created {filename}: {width}x{height}, {len(rects)} rects')

# 1. Left Cloud Bank (Curtain that slides left)
# Wide natural cumulus bank with varied organic puff heights
domes_left = [
    (0, 160, 110, 1.3),
    (80, 120, 95, 1.2),
    (180, 80, 90, 1.25),
    (120, 50, 60, 1.15),
    (270, 95, 85, 1.2),
    (360, 60, 75, 1.2),
    (450, 100, 80, 1.25),
    (530, 80, 70, 1.2),
    (620, 115, 85, 1.25),
    (700, 140, 90, 1.3),
    (780, 165, 80, 1.35),
]
create_pixel_cloud('website/assets/ui/pixel_clouds_left.svg', 800, 200, domes_left, grid=5, fade_bottom=True)

# 2. Right Cloud Bank (Curtain that slides right)
domes_right = [
    (800, 160, 110, 1.3),
    (720, 120, 95, 1.2),
    (620, 80, 90, 1.25),
    (680, 50, 60, 1.15),
    (530, 95, 85, 1.2),
    (440, 60, 75, 1.2),
    (350, 100, 80, 1.25),
    (270, 80, 70, 1.2),
    (180, 115, 85, 1.25),
    (100, 140, 90, 1.3),
    (20, 165, 80, 1.35),
]
create_pixel_cloud('website/assets/ui/pixel_clouds_right.svg', 800, 200, domes_right, grid=5, fade_bottom=True)

# 3. Fluffy Floating Center Cloud
domes_center = [
    (70, 65, 45, 1.2),
    (110, 45, 40, 1.15),
    (160, 55, 42, 1.2),
    (200, 70, 38, 1.2),
    (130, 80, 50, 1.3)
]
create_pixel_cloud('website/assets/ui/pixel_clouds_center.svg', 280, 110, domes_center, grid=4, fade_bottom=False)

# 4. Soft Baseline Cloud Horizon
domes_base = [
    (0, 90, 80, 1.3), (120, 70, 75, 1.2), (240, 55, 70, 1.2),
    (360, 75, 75, 1.2), (480, 50, 80, 1.25), (600, 70, 70, 1.2),
    (720, 55, 75, 1.2), (840, 75, 70, 1.2), (960, 45, 85, 1.25),
    (1080, 70, 75, 1.2), (1200, 50, 80, 1.2), (1320, 75, 70, 1.2),
    (1440, 55, 75, 1.2), (1560, 70, 75, 1.2), (1680, 50, 80, 1.25),
    (1800, 75, 75, 1.2), (1920, 85, 80, 1.3)
]
create_pixel_cloud('website/assets/ui/pixel_clouds_base.svg', 1920, 140, domes_base, grid=6, fade_bottom=True)
