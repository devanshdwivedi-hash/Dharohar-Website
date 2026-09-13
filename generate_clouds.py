import math
import os

os.makedirs('website/assets/ui', exist_ok=True)

def build_cloud_svg(filename, width, height, lobes, grid=8, opacity=1.0, is_banner=True):
    cols = width // grid
    rows = height // grid
    
    occupied = [[0]*cols for _ in range(rows)]
    
    for (cx, cy, rx, ry) in lobes:
        cx_g = int(cx / grid)
        cy_g = int(cy / grid)
        rx_g = int(rx / grid)
        ry_g = int(ry / grid)
        
        for r in range(rows):
            for c in range(cols):
                dx = (c - cx_g) / max(1, rx_g)
                dy = (r - cy_g) / max(1, ry_g)
                if dx*dx + dy*dy <= 1.0:
                    occupied[r][c] = 1
                    
    if is_banner:
        for c in range(cols):
            filling = False
            for r in range(rows):
                if occupied[r][c] == 1:
                    filling = True
                if filling:
                    occupied[r][c] = 1
                    
    cell_type = [[0]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if occupied[r][c] == 1:
                is_top = (r == 0) or (occupied[r-1][c] == 0) or (c > 0 and occupied[r][c-1] == 0) or (c < cols-1 and occupied[r][c+1] == 0)
                if is_top:
                    cell_type[r][c] = 1 # rim gold
                else:
                    is_near_top = (r > 0 and cell_type[r-1][c] == 1) or (c > 0 and cell_type[r][c-1] == 1) or (c < cols-1 and cell_type[r][c+1] == 1)
                    if is_near_top:
                        cell_type[r][c] = 2 # amber
                    elif r < rows * 0.65:
                        cell_type[r][c] = 3 # midnight slate
                    else:
                        cell_type[r][c] = 4 # deep parchment base
                        
    colors = {
        1: '#fbbf24', # Gold highlight
        2: '#d97706', # Warm Amber
        3: '#141d27', # Deep Midnight Slate
        4: '#080c10', # Base Parchment Dark
    }
    
    rects = []
    for r in range(rows):
        c = 0
        while c < cols:
            t = cell_type[r][c]
            if t != 0:
                start_c = c
                while c < cols and cell_type[r][c] == t:
                    c += 1
                length = c - start_c
                rects.append(f'<rect x="{start_c*grid}" y="{r*grid}" width="{length*grid}" height="{grid}" fill="{colors[t]}"/>')
            else:
                c += 1
                
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" preserveAspectRatio="none" style="shape-rendering: crispEdges;">
{''.join(rects)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Generated {filename}, size: {len(svg)} chars')

# 1. Full bottom banner for Section 1 bottom edge
lobes_banner = [
    (0, 160, 200, 120), (180, 120, 220, 130), (380, 90, 260, 140),
    (600, 140, 200, 120), (780, 100, 240, 130), (1020, 80, 280, 150),
    (1250, 130, 220, 130), (1450, 90, 250, 140), (1700, 120, 220, 130),
    (1920, 150, 240, 140)
]
build_cloud_svg('website/assets/ui/cloud_banner_dense.svg', 1920, 260, lobes_banner, grid=8, is_banner=True)

# 2. Foreground Left Cloud (parts to left on scroll)
lobes_left = [
    (0, 280, 320, 200), (160, 220, 280, 180), (320, 290, 260, 170),
    (100, 360, 350, 190), (0, 420, 400, 200)
]
build_cloud_svg('website/assets/ui/cloud_fg_left.svg', 800, 450, lobes_left, grid=10, is_banner=True)

# 3. Foreground Right Cloud (parts to right on scroll)
lobes_right = [
    (800, 280, 320, 200), (640, 220, 280, 180), (480, 290, 260, 170),
    (700, 360, 350, 190), (800, 420, 400, 200)
]
build_cloud_svg('website/assets/ui/cloud_fg_right.svg', 800, 450, lobes_right, grid=10, is_banner=True)

# 4. Midground Floating Cloud
lobes_mid = [
    (180, 120, 180, 80), (340, 90, 220, 90), (500, 110, 190, 85),
    (300, 160, 260, 90)
]
build_cloud_svg('website/assets/ui/cloud_mid_float.svg', 700, 240, lobes_mid, grid=8, is_banner=False)

# 5. Section 2 to Section 3 mist sweep
lobes_mist = [
    (100, 140, 300, 80), (400, 110, 350, 90), (750, 150, 320, 85),
    (1100, 120, 380, 90), (1450, 140, 320, 85), (1800, 110, 340, 90)
]
build_cloud_svg('website/assets/ui/cloud_mist_sweep.svg', 1920, 260, lobes_mist, grid=12, is_banner=False)
