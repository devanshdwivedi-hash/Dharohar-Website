import os

os.makedirs('website/assets/ui', exist_ok=True)

def generate_corner_cloud(filename, width, height, origin='tl', grid=5):
    cols = width // grid
    rows = height // grid
    
    occupied = [[0]*cols for _ in range(rows)]
    
    if origin == 'tl':
        lobes = [
            (0, 0, 95), (25, 15, 85), (60, 0, 80),
            (0, 60, 80), (45, 55, 70), (90, 25, 60),
            (25, 90, 60), (70, 75, 50), (120, 45, 45),
            (55, 110, 40), (100, 85, 40), (140, 60, 35)
        ]
    elif origin == 'tr':
        lobes = [
            (width, 0, 95), (width-25, 15, 85), (width-60, 0, 80),
            (width, 60, 80), (width-45, 55, 70), (width-90, 25, 60),
            (width-25, 90, 60), (width-70, 75, 50), (width-120, 45, 45),
            (width-55, 110, 40), (width-100, 85, 40), (width-140, 60, 35)
        ]
    elif origin == 'bl':
        lobes = [
            (0, height, 95), (25, height-15, 85), (60, height, 80),
            (0, height-60, 80), (45, height-55, 70), (90, height-25, 60),
            (25, height-90, 60), (70, height-75, 50), (120, height-45, 45),
            (55, height-110, 40), (100, height-85, 40), (140, height-60, 35)
        ]
    elif origin == 'br':
        lobes = [
            (width, height, 95), (width-25, height-15, 85), (width-60, height, 80),
            (width, height-60, 80), (width-45, height-55, 70), (width-90, height-25, 60),
            (width-25, height-90, 60), (width-70, height-75, 50), (width-120, height-45, 45),
            (width-55, height-110, 40), (width-100, height-85, 40), (width-140, height-60, 35)
        ]

    for cx, cy, r in lobes:
        cg_x = cx / grid
        cg_y = cy / grid
        rg = r / grid
        
        min_r = max(0, int(cg_y - rg))
        max_r = min(rows, int(cg_y + rg + 1))
        min_c = max(0, int(cg_x - rg))
        max_c = min(cols, int(cg_x + rg + 1))
        
        for r_idx in range(min_r, max_r):
            for c_idx in range(min_c, max_c):
                dx = c_idx - cg_x
                dy = r_idx - cg_y
                if dx*dx + dy*dy <= rg*rg:
                    occupied[r_idx][c_idx] = 1

    shading = [[0]*cols for _ in range(rows)]
    for r_idx in range(rows):
        for c_idx in range(cols):
            if occupied[r_idx][c_idx] == 1:
                is_edge = False
                if origin == 'tl':
                    if (r_idx < rows-1 and occupied[r_idx+1][c_idx] == 0) or (c_idx < cols-1 and occupied[r_idx][c_idx+1] == 0):
                        is_edge = True
                elif origin == 'tr':
                    if (r_idx < rows-1 and occupied[r_idx+1][c_idx] == 0) or (c_idx > 0 and occupied[r_idx][c_idx-1] == 0):
                        is_edge = True
                elif origin == 'bl':
                    if (r_idx > 0 and occupied[r_idx-1][c_idx] == 0) or (c_idx < cols-1 and occupied[r_idx][c_idx+1] == 0):
                        is_edge = True
                elif origin == 'br':
                    if (r_idx > 0 and occupied[r_idx-1][c_idx] == 0) or (c_idx > 0 and occupied[r_idx][c_idx-1] == 0):
                        is_edge = True

                is_top_facing = (r_idx == 0) or (r_idx > 0 and occupied[r_idx-1][c_idx] == 0)

                if is_top_facing or (origin in ('bl', 'br') and is_edge):
                    shading[r_idx][c_idx] = 1 # White Highlight
                elif is_edge:
                    shading[r_idx][c_idx] = 3 # Golden Amber Shadow
                else:
                    shading[r_idx][c_idx] = 2 # Soft Cream Body

    colors = {
        1: '#ffffff',  # White highlight
        2: '#fffbeb',  # Soft cream body
        3: '#fbbf24',  # Golden amber
    }
    
    rects = []
    for r_idx in range(rows):
        c_idx = 0
        while c_idx < cols:
            val = shading[r_idx][c_idx]
            if val != 0:
                start_c = c_idx
                while c_idx < cols and shading[r_idx][c_idx] == val:
                    c_idx += 1
                length = c_idx - start_c
                rects.append(f'<rect x="{start_c*grid}" y="{r_idx*grid}" width="{length*grid}" height="{grid}" fill="{colors[val]}"/>')
            else:
                c_idx += 1
                
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="shape-rendering: crispEdges;">
{''.join(rects)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Generated {filename} ({width}x{height}, {len(rects)} rects)')

generate_corner_cloud('website/assets/ui/corner_cloud_tl.svg', 220, 180, origin='tl', grid=5)
generate_corner_cloud('website/assets/ui/corner_cloud_tr.svg', 220, 180, origin='tr', grid=5)
generate_corner_cloud('website/assets/ui/corner_cloud_bl.svg', 220, 180, origin='bl', grid=5)
generate_corner_cloud('website/assets/ui/corner_cloud_br.svg', 220, 180, origin='br', grid=5)
