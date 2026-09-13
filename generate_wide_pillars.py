import os

os.makedirs('website/assets/ui', exist_ok=True)

def generate_wide_pillar_svg(filename, is_left=True):
    # Width: 96px, Height: 1000px
    # Palette: Ancient Nalanda Sandstone & Gold
    # Highlights: #fff7ed, #fef08a, #fbbf24
    # Mid-tone: #f59e0b, #d97706, #b45309
    # Shadow/Terracotta: #78350f, #451a03
    # Dark core: #121822, #080c10
    
    W = 96
    elements = []
    
    # ── 1. Shaft (Main Vertical Body from Y=80 to Y=910) ──
    shaft_x = 18
    shaft_w = 60
    
    # Base fill of shaft
    elements.append(f'<rect x="{shaft_x}" y="80" width="{shaft_w}" height="830" fill="#0d141e"/>')
    
    # Multiple fluted vertical stone ribs (mirrored symmetrically)
    if is_left:
        ribs = [
            (18, 4, '#fbbf24', 0.9),  # Gold sunlit outer rib
            (24, 7, '#fef08a', 0.8),  # Pale gold inner rib
            (33, 9, '#f59e0b', 0.9),  # Warm amber rib
            (44, 11, '#d97706', 1.0), # Central primary sandstone rib
            (57, 9, '#b45309', 0.9),  # Terracotta shaded rib
            (68, 6, '#78350f', 0.9),  # Dark shadow rib
            (76, 2, '#451a03', 1.0)   # Deep edge rib
        ]
    else:
        ribs = [
            (18, 2, '#451a03', 1.0),  # Deep edge rib (inner)
            (22, 6, '#78350f', 0.9),  # Dark shadow rib
            (30, 9, '#b45309', 0.9),  # Terracotta shaded rib
            (41, 11, '#d97706', 1.0), # Central primary sandstone rib
            (54, 9, '#f59e0b', 0.9),  # Warm amber rib
            (65, 7, '#fef08a', 0.8),  # Pale gold inner rib
            (74, 4, '#fbbf24', 0.9)   # Gold sunlit outer rib
        ]
    for rx, rw, col, op in ribs:
        elements.append(f'<rect x="{rx}" y="80" width="{rw}" height="830" fill="{col}" opacity="{op}"/>')
        
    # Vertical stone contour lines
    elements.append(f'<line x1="{shaft_x}" y1="80" x2="{shaft_x}" y2="910" stroke="#f59e0b" stroke-width="2"/>')
    elements.append(f'<line x1="{shaft_x + shaft_w}" y1="80" x2="{shaft_x + shaft_w}" y2="910" stroke="#f59e0b" stroke-width="2"/>')
    elements.append(f'<line x1="{shaft_x + 6}" y1="80" x2="{shaft_x + 6}" y2="910" stroke="#78350f" stroke-width="1"/>')
    elements.append(f'<line x1="{shaft_x + shaft_w - 6}" y1="80" x2="{shaft_x + shaft_w - 6}" y2="910" stroke="#451a03" stroke-width="1"/>')

    # Decorative Ringed Bands (Carved Mouldings / Patta) along the shaft
    for y_pos in [190, 330, 470, 610, 750, 890]:
        # Outer stepped frame
        elements.append(f'<rect x="10" y="{y_pos-12}" width="76" height="24" fill="#141d28" stroke="#f59e0b" stroke-width="2"/>')
        elements.append(f'<rect x="6" y="{y_pos-7}" width="84" height="14" fill="#b45309" stroke="#d97706" stroke-width="1"/>')
        elements.append(f'<rect x="12" y="{y_pos-3}" width="72" height="6" fill="#fbbf24"/>')
        # Center carved rosette & diamond gem
        elements.append(f'<polygon points="48,{y_pos-9} 56,{y_pos} 48,{y_pos+9} 40,{y_pos}" fill="#fef08a" stroke="#78350f" stroke-width="1"/>')
        elements.append(f'<circle cx="28" cy="{y_pos}" r="3" fill="#fef08a"/>')
        elements.append(f'<circle cx="68" cy="{y_pos}" r="3" fill="#fef08a"/>')

    # ── 2. Stepped Capital (Top: Y=0 to Y=80) ──
    # The capital flares outward to support the Torana crossbeam
    if is_left:
        # Left pillar: Capital bracket reaches rightward towards the connecting beam
        elements.append('<polygon points="0,0 96,0 96,28 80,48 80,80 18,80 18,48 0,28" fill="#151e2b" stroke="#f59e0b" stroke-width="2.5"/>')
        # Stepped abacus mouldings
        elements.append('<rect x="4" y="4" width="88" height="8" fill="#fef08a"/>')
        elements.append('<rect x="8" y="14" width="82" height="10" fill="#d97706"/>')
        elements.append('<rect x="14" y="26" width="70" height="12" fill="#b45309"/>')
        elements.append('<rect x="20" y="40" width="56" height="14" fill="#1a2533" stroke="#d97706" stroke-width="1"/>')
        # Lotus Medallion in capital center
        elements.append('<circle cx="48" cy="60" r="12" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>')
        elements.append('<circle cx="48" cy="60" r="6" fill="#fef08a"/>')
        # Supporting corbel bracket locking rightwards with beam
        elements.append('<polygon points="80,18 96,8 96,38 80,48" fill="#fbbf24" stroke="#78350f" stroke-width="1"/>')
    else:
        # Right pillar: Capital bracket reaches leftward towards the connecting beam
        elements.append('<polygon points="0,0 96,0 96,28 78,48 78,80 16,80 16,48 0,28" fill="#151e2b" stroke="#f59e0b" stroke-width="2.5"/>')
        elements.append('<rect x="4" y="4" width="88" height="8" fill="#fef08a"/>')
        elements.append('<rect x="6" y="14" width="82" height="10" fill="#d97706"/>')
        elements.append('<rect x="12" y="26" width="70" height="12" fill="#b45309"/>')
        elements.append('<rect x="20" y="40" width="56" height="14" fill="#1a2533" stroke="#d97706" stroke-width="1"/>')
        elements.append('<circle cx="48" cy="60" r="12" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>')
        elements.append('<circle cx="48" cy="60" r="6" fill="#fef08a"/>')
        # Supporting corbel bracket locking leftwards with beam
        elements.append('<polygon points="16,18 0,8 0,38 16,48" fill="#fbbf24" stroke="#78350f" stroke-width="1"/>')

    # ── 3. Stepped Base Plinth (Bottom: Y=910 to Y=1000) ──
    # Wide stepped stone pedestal
    elements.append('<rect x="12" y="910" width="72" height="20" fill="#151e2b" stroke="#d97706" stroke-width="2"/>')
    elements.append('<rect x="18" y="915" width="60" height="10" fill="#d97706"/>')
    elements.append('<rect x="6" y="930" width="84" height="26" fill="#141d28" stroke="#f59e0b" stroke-width="2"/>')
    elements.append('<rect x="12" y="938" width="72" height="10" fill="#b45309"/>')
    elements.append('<rect x="0" y="956" width="96" height="44" fill="#090e15" stroke="#f59e0b" stroke-width="2"/>')
    elements.append('<rect x="6" y="964" width="84" height="14" fill="#d97706"/>')
    elements.append('<rect x="12" y="980" width="72" height="8" fill="#fbbf24"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 1000" width="100%" height="100%" preserveAspectRatio="none" style="shape-rendering: crispEdges;">
{''.join(elements)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Generated wide {filename} ({W}x1000)')

generate_wide_pillar_svg('website/assets/ui/pillar_left.svg', is_left=True)
generate_wide_pillar_svg('website/assets/ui/pillar_right.svg', is_left=False)
